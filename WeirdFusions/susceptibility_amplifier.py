#!/usr/bin/env python3
"""
WeirdFusions / Susceptibility Amplifier
---------------------------------------

A deliberately narrow-band, safety-bounded speaker -> room -> microphone
feedback instrument.

The point is NOT to amplify an unknown external signal directly.
The program creates a known macroscopic oscillator whose required gain and
trajectory can become sensitive to small changes in the physical acoustic plant.

Three arms:
  OPEN  : probe tone -> speaker -> world -> mic
  FIXED : probe + fixed narrow-band regenerative feedback
  EDGE  : probe + feedback; a slow controller changes feedback gain to hold
          a target microphone mode amplitude.

The feedback path is intentionally narrow-band. Each microphone block is
lock-in-demodulated at one selected frequency; the complex coefficient is
re-synthesised at that frequency with a controlled phase correction.

Safety:
  * starts muted
  * conservative MAX OUTPUT default
  * hard block limiter
  * automatic mute on unexpectedly large microphone RMS
  * callback watchdog / underflow counters where PyAudio reports them
  * no broadband raw mic->speaker path

This is an experiment, not a measurement instrument until calibrated.

Dependencies:
    pip install numpy matplotlib pyaudio

Run:
    python susceptibility_amplifier.py
    python susceptibility_amplifier.py --list-devices
    python susceptibility_amplifier.py --selftest
"""

from __future__ import annotations

import argparse
import csv
import math
import os
import queue
import threading
import time
from collections import deque
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional

import numpy as np

try:
    import pyaudio
except Exception:
    pyaudio = None

# GUI imports are delayed for --selftest / --list-devices.


TAU = 2.0 * math.pi
EPS = 1e-12


@dataclass
class Config:
    sample_rate: int = 44100
    block_size: int = 1024
    frequency_hz: float = 700.0

    # Conservative defaults. Physical loudness ALSO depends on interface/speaker knobs.
    probe_amp: float = 0.004
    max_output: float = 0.030
    panic_mic_rms: float = 0.20

    fixed_gain: float = 0.50
    edge_gain: float = 0.50
    max_feedback_gain: float = 8.0

    # Applied to the regenerated microphone phasor.
    phase_deg: float = 0.0

    # EDGE controller.
    target_mode_amp: float = 0.010
    edge_kp: float = 0.16
    edge_ki: float = 0.035
    controller_slew: float = 0.08  # max fractional gain move per analysis block

    # Optional slow AGC only on the probe would confound the experiment, so absent.
    mode: str = "OPEN"  # OPEN / FIXED / EDGE

    # Analysis.
    history_seconds: float = 2.5
    log_period_s: float = 0.25


@dataclass
class Stats:
    t: float = 0.0
    mic_rms: float = 0.0
    mic_peak: float = 0.0
    mode_amp: float = 0.0
    mode_phase_deg: float = 0.0
    output_rms: float = 0.0
    output_peak: float = 0.0
    feedback_gain: float = 0.0
    phase_deg: float = 0.0
    peak_freq_hz: float = float("nan")
    q_estimate: float = float("nan")
    orbit_distance: float = float("nan")
    clip_count: int = 0
    xrun_count: int = 0
    muted: bool = True
    mode: str = "OPEN"


class EdgeController:
    """Slow multiplicative PI controller on feedback gain."""

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.integral = 0.0
        self.gain = cfg.edge_gain

    def reset(self, gain: Optional[float] = None) -> None:
        self.integral = 0.0
        self.gain = self.cfg.edge_gain if gain is None else float(gain)

    def update(self, measured_amp: float, dt: float) -> float:
        target = max(self.cfg.target_mode_amp, 1e-7)
        measured = max(float(measured_amp), 1e-7)

        # Log error gives symmetric multiplicative behaviour.
        err = math.log(target / measured)
        self.integral = float(np.clip(self.integral + err * dt, -8.0, 8.0))
        raw = self.cfg.edge_kp * err + self.cfg.edge_ki * self.integral

        # Do not let one bad block launch the loop.
        raw = float(np.clip(raw, -self.cfg.controller_slew, self.cfg.controller_slew))
        self.gain *= math.exp(raw)
        self.gain = float(np.clip(self.gain, 0.0, self.cfg.max_feedback_gain))
        return self.gain


class OrbitBaseline:
    """
    Baseline on a compact delay-embedding signature.

    Signature:
      mean(x0,x1,x2)                 3
      upper covariance triangle      6
      radius mean/std/q90            3
    """

    def __init__(self):
        self.samples: list[np.ndarray] = []
        self.mean: Optional[np.ndarray] = None
        self.std: Optional[np.ndarray] = None
        self.collect_until = 0.0

    @staticmethod
    def signature(x: np.ndarray, delay: int) -> np.ndarray:
        x = np.asarray(x, dtype=np.float64)
        delay = max(1, int(delay))
        if x.size <= 2 * delay + 16:
            return np.zeros(12, dtype=np.float64)

        a = x[2 * delay :]
        b = x[delay : -delay]
        c = x[: -2 * delay]
        E = np.column_stack((a, b, c))

        mu = E.mean(axis=0)
        C = np.cov(E, rowvar=False)
        tri = C[np.triu_indices(3)]
        R = np.linalg.norm(E - mu, axis=1)
        radial = np.array([R.mean(), R.std(), np.quantile(R, 0.90)])
        return np.concatenate((mu, tri, radial))

    def begin(self, seconds: float) -> None:
        self.samples = []
        self.mean = None
        self.std = None
        self.collect_until = time.monotonic() + float(seconds)

    @property
    def collecting(self) -> bool:
        return time.monotonic() < self.collect_until

    @property
    def ready(self) -> bool:
        return self.mean is not None and self.std is not None

    def observe(self, sig: np.ndarray) -> None:
        if self.collecting:
            self.samples.append(np.asarray(sig, dtype=np.float64).copy())
        elif self.collect_until > 0 and self.mean is None and len(self.samples) >= 4:
            X = np.vstack(self.samples)
            self.mean = X.mean(axis=0)
            # Robust floor prevents "perfectly constant" channels from exploding.
            raw_std = X.std(axis=0, ddof=1)
            scale = max(float(np.median(np.abs(X))) * 1e-3, 1e-7)
            self.std = np.maximum(raw_std, scale)
            self.collect_until = 0.0

    def distance(self, sig: np.ndarray) -> float:
        if not self.ready:
            return float("nan")
        z = (np.asarray(sig) - self.mean) / self.std
        return float(np.sqrt(np.mean(z * z)))


class CSVLogger:
    FIELDS = [
        "time_iso", "elapsed_s", "trial_id", "arm", "label_hidden",
        "freq_hz", "mic_rms", "mic_peak", "mode_amp", "mode_phase_deg",
        "output_rms", "output_peak", "feedback_gain", "phase_correction_deg",
        "peak_freq_hz", "q_estimate", "orbit_distance",
        "clip_count", "xrun_count", "muted",
    ]

    def __init__(self):
        self.fp = None
        self.writer = None
        self.path: Optional[Path] = None

    def start(self, path: str | os.PathLike) -> None:
        self.stop()
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.fp = self.path.open("w", newline="", encoding="utf-8")
        self.writer = csv.DictWriter(self.fp, fieldnames=self.FIELDS)
        self.writer.writeheader()
        self.fp.flush()

    def write(self, stats: Stats, trial_id: str, label_hidden: str, elapsed: float) -> None:
        if self.writer is None:
            return
        row = {
            "time_iso": datetime.now().isoformat(timespec="milliseconds"),
            "elapsed_s": f"{elapsed:.6f}",
            "trial_id": trial_id,
            "arm": stats.mode,
            "label_hidden": label_hidden,
            "freq_hz": f"{stats.peak_freq_hz if math.isfinite(stats.peak_freq_hz) else 0:.6f}",
            "mic_rms": f"{stats.mic_rms:.9g}",
            "mic_peak": f"{stats.mic_peak:.9g}",
            "mode_amp": f"{stats.mode_amp:.9g}",
            "mode_phase_deg": f"{stats.mode_phase_deg:.6f}",
            "output_rms": f"{stats.output_rms:.9g}",
            "output_peak": f"{stats.output_peak:.9g}",
            "feedback_gain": f"{stats.feedback_gain:.9g}",
            "phase_correction_deg": f"{stats.phase_deg:.6f}",
            "peak_freq_hz": f"{stats.peak_freq_hz:.6f}" if math.isfinite(stats.peak_freq_hz) else "",
            "q_estimate": f"{stats.q_estimate:.6f}" if math.isfinite(stats.q_estimate) else "",
            "orbit_distance": f"{stats.orbit_distance:.6f}" if math.isfinite(stats.orbit_distance) else "",
            "clip_count": stats.clip_count,
            "xrun_count": stats.xrun_count,
            "muted": int(stats.muted),
        }
        self.writer.writerow(row)
        self.fp.flush()

    def stop(self) -> None:
        if self.fp is not None:
            self.fp.close()
        self.fp = None
        self.writer = None


class SusceptibilityDSP:
    """
    Thread-safe DSP core. PyAudio callback calls process().
    GUI can update cfg fields under lock.
    """

    def __init__(self, cfg: Config):
        self.cfg = cfg
        self.lock = threading.RLock()
        self.controller = EdgeController(cfg)
        self.baseline = OrbitBaseline()

        self.phase = 0.0
        self.muted = True
        self.clip_count = 0
        self.xrun_count = 0
        self.start_time = time.monotonic()

        n_hist = int(cfg.sample_rate * cfg.history_seconds)
        self.history = deque(maxlen=max(n_hist, cfg.block_size * 4))
        self.last_input = np.zeros(cfg.block_size, np.float32)
        self.last_output = np.zeros(cfg.block_size, np.float32)
        self.stats = Stats()

        self._last_log_t = 0.0
        self.log_queue: "queue.SimpleQueue[Stats]" = queue.SimpleQueue()

    def reset(self) -> None:
        with self.lock:
            self.phase = 0.0
            self.controller.reset(self.cfg.edge_gain)
            self.baseline = OrbitBaseline()
            self.history.clear()
            self.clip_count = 0
            self.xrun_count = 0
            self.start_time = time.monotonic()

    def set_muted(self, flag: bool) -> None:
        with self.lock:
            self.muted = bool(flag)

    def panic(self) -> None:
        with self.lock:
            self.muted = True

    def mark_xrun(self) -> None:
        with self.lock:
            self.xrun_count += 1

    def _analysis_frequency(self) -> float:
        return float(np.clip(self.cfg.frequency_hz, 20.0, self.cfg.sample_rate * 0.45))

    def process(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=np.float32).reshape(-1)
        N = x.size
        if N == 0:
            return x

        with self.lock:
            cfg = self.cfg
            f = self._analysis_frequency()
            sr = cfg.sample_rate
            dt = N / sr

            # Remove block DC; a DC offset should never regenerate through the speaker.
            xd = x.astype(np.float64) - float(np.mean(x))

            # One continuous reference phase for lock-in + synthesis.
            w = TAU * f / sr
            theta = self.phase + w * np.arange(N)
            ej = np.exp(-1j * theta)
            c = (2.0 / N) * np.dot(xd, ej)
            mode_amp = float(abs(c))
            mode_phase = math.degrees(math.atan2(c.imag, c.real))

            mic_rms = float(np.sqrt(np.mean(xd * xd)))
            mic_peak = float(np.max(np.abs(xd))) if N else 0.0

            if mic_rms > cfg.panic_mic_rms:
                # Unexpectedly large microphone level: fail closed.
                self.muted = True

            if cfg.mode == "EDGE":
                gain = self.controller.update(mode_amp, dt)
            elif cfg.mode == "FIXED":
                gain = float(np.clip(cfg.fixed_gain, 0.0, cfg.max_feedback_gain))
                self.controller.gain = gain
            else:
                gain = 0.0

            # Seed/probe is always deterministic and tiny.
            probe = cfg.probe_amp * np.sin(theta)

            # Narrow-band regenerative path.
            phase_corr = math.radians(cfg.phase_deg)
            fb_complex = gain * c * np.exp(1j * phase_corr)
            feedback = np.real(fb_complex * np.exp(1j * theta))

            y = probe + feedback

            # Hard safety bound: scale whole block rather than waveform clipping.
            requested_peak = float(np.max(np.abs(y))) if N else 0.0
            if requested_peak > cfg.max_output > 0:
                self.clip_count += int(np.sum(np.abs(y) > cfg.max_output))
                y *= cfg.max_output / max(requested_peak, EPS)

            if self.muted:
                y[:] = 0.0

            out_rms = float(np.sqrt(np.mean(y * y)))
            out_peak = float(np.max(np.abs(y))) if N else 0.0

            self.phase = float((self.phase + w * N) % TAU)
            self.last_input = x.copy()
            self.last_output = y.astype(np.float32).copy()
            self.history.extend(x.tolist())

            # Delay ~= quarter cycle gives an informative phase portrait for a sinusoid.
            delay = max(1, int(sr / max(f, 1.0) / 4.0))
            sig = self.baseline.signature(np.asarray(self.history, dtype=np.float64), delay)
            self.baseline.observe(sig)
            orbit_distance = self.baseline.distance(sig)

            peak_f, q_est = spectral_metrics(
                np.asarray(self.history, dtype=np.float64), sr, f
            )

            now = time.monotonic()
            self.stats = Stats(
                t=now - self.start_time,
                mic_rms=mic_rms,
                mic_peak=mic_peak,
                mode_amp=mode_amp,
                mode_phase_deg=mode_phase,
                output_rms=out_rms,
                output_peak=out_peak,
                feedback_gain=gain,
                phase_deg=cfg.phase_deg,
                peak_freq_hz=peak_f,
                q_estimate=q_est,
                orbit_distance=orbit_distance,
                clip_count=self.clip_count,
                xrun_count=self.xrun_count,
                muted=self.muted,
                mode=cfg.mode,
            )

            if now - self._last_log_t >= cfg.log_period_s:
                self.log_queue.put(self.stats)
                self._last_log_t = now

            return y.astype(np.float32)

    def snapshot(self):
        with self.lock:
            return (
                Stats(**asdict(self.stats)),
                self.last_input.copy(),
                self.last_output.copy(),
                np.asarray(self.history, dtype=np.float32).copy(),
            )


def spectral_metrics(x: np.ndarray, sr: int, expected_f: float) -> tuple[float, float]:
    """Peak frequency and crude -3 dB Q estimate around the selected mode."""
    x = np.asarray(x, dtype=np.float64)
    if x.size < 256:
        return float("nan"), float("nan")

    # Limit work and keep frequency resolution stable.
    max_n = min(x.size, 32768)
    x = x[-max_n:]
    x = x - x.mean()
    win = np.hanning(x.size)
    X = np.abs(np.fft.rfft(x * win))
    F = np.fft.rfftfreq(x.size, 1.0 / sr)

    lo = max(20.0, expected_f * 0.65)
    hi = min(sr * 0.48, expected_f * 1.35)
    mask = (F >= lo) & (F <= hi)
    if not np.any(mask):
        return float("nan"), float("nan")

    idxs = np.flatnonzero(mask)
    k = idxs[np.argmax(X[mask])]
    peak = float(F[k])
    a = float(X[k])
    if a <= EPS:
        return peak, float("nan")

    half = a / math.sqrt(2.0)
    kl = k
    while kl > 1 and X[kl] >= half:
        kl -= 1
    kr = k
    while kr < X.size - 1 and X[kr] >= half:
        kr += 1

    bw = float(F[kr] - F[kl]) if kr > kl else 0.0
    q = peak / bw if bw > 0 else float("nan")
    return peak, q


class AudioEngine:
    def __init__(self, dsp: SusceptibilityDSP):
        if pyaudio is None:
            raise RuntimeError("PyAudio is not installed. Run: pip install pyaudio")
        self.dsp = dsp
        self.pa = pyaudio.PyAudio()
        self.stream = None

    def devices(self):
        ins, outs = [], []
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            label = f"{i}: {info.get('name', 'device')}"
            if info.get("maxInputChannels", 0) > 0:
                ins.append((label, i))
            if info.get("maxOutputChannels", 0) > 0:
                outs.append((label, i))
        return ins, outs

    def start(self, input_index: int, output_index: int) -> None:
        self.stop()
        cfg = self.dsp.cfg

        def callback(in_data, frame_count, time_info, status_flags):
            if status_flags:
                self.dsp.mark_xrun()
            try:
                x = np.frombuffer(in_data, dtype=np.float32).copy()
                if x.size != frame_count:
                    x = np.resize(x, frame_count).astype(np.float32)
                y = self.dsp.process(x)
                return (y.tobytes(), pyaudio.paContinue)
            except Exception:
                self.dsp.panic()
                z = np.zeros(frame_count, dtype=np.float32)
                return (z.tobytes(), pyaudio.paContinue)

        self.stream = self.pa.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=cfg.sample_rate,
            input=True,
            output=True,
            input_device_index=int(input_index),
            output_device_index=int(output_index),
            frames_per_buffer=cfg.block_size,
            stream_callback=callback,
            start=False,
        )
        self.stream.start_stream()

    def stop(self) -> None:
        if self.stream is not None:
            try:
                self.stream.stop_stream()
            except Exception:
                pass
            try:
                self.stream.close()
            except Exception:
                pass
            self.stream = None

    def close(self) -> None:
        self.stop()
        self.pa.terminate()


def selftest() -> int:
    print("Susceptibility Amplifier self-test")
    ok_all = True

    # T1: lock-in amplitude and phase are recovered.
    cfg = Config(sample_rate=44100, block_size=2048, frequency_hz=731.0)
    dsp = SusceptibilityDSP(cfg)
    dsp.set_muted(False)
    t = np.arange(cfg.block_size) / cfg.sample_rate
    x = 0.02 * np.sin(TAU * cfg.frequency_hz * t + 0.37)
    _ = dsp.process(x.astype(np.float32))
    s, *_ = dsp.snapshot()
    e_amp = abs(s.mode_amp - 0.02)
    ok = e_amp < 0.0015
    print(f"[T1] lock-in amplitude {s.mode_amp:.5f}, error {e_amp:.5f}: {'PASS' if ok else 'FAIL'}")
    ok_all &= ok

    # T2: output safety bound survives absurd gain.
    with dsp.lock:
        dsp.cfg.mode = "FIXED"
        dsp.cfg.fixed_gain = 1000.0
        dsp.cfg.max_feedback_gain = 1000.0
        dsp.cfg.max_output = 0.025
    y = dsp.process(x.astype(np.float32))
    ok = float(np.max(np.abs(y))) <= 0.0250001
    print(f"[T2] hard output bound peak={np.max(np.abs(y)):.5f}: {'PASS' if ok else 'FAIL'}")
    ok_all &= ok

    # T3: edge controller raises gain when measured amplitude is too small.
    ctl = EdgeController(cfg)
    ctl.reset(0.5)
    g0 = ctl.gain
    for _ in range(20):
        ctl.update(cfg.target_mode_amp * 0.25, cfg.block_size / cfg.sample_rate)
    ok = ctl.gain > g0
    print(f"[T3] weak plant -> gain rises {g0:.3f} -> {ctl.gain:.3f}: {'PASS' if ok else 'FAIL'}")
    ok_all &= ok

    # T4: edge controller lowers gain when measured amplitude is too large.
    ctl.reset(0.5)
    g0 = ctl.gain
    for _ in range(20):
        ctl.update(cfg.target_mode_amp * 4.0, cfg.block_size / cfg.sample_rate)
    ok = ctl.gain < g0
    print(f"[T4] strong plant -> gain falls {g0:.3f} -> {ctl.gain:.3f}: {'PASS' if ok else 'FAIL'}")
    ok_all &= ok

    # T5: orbit baseline notices a structural waveform change.
    base = OrbitBaseline()
    base.begin(0.001)
    # Force collection without sleeping by extending manually.
    base.collect_until = time.monotonic() + 10
    delay = 13
    rng = np.random.default_rng(4)
    for k in range(20):
        tt = np.arange(4096)
        xx = 0.02 * np.sin(2*np.pi*tt/52.0 + 0.02*rng.normal())
        xx += 0.0003 * rng.normal(size=tt.size)
        base.samples.append(base.signature(xx, delay))
    X = np.vstack(base.samples)
    base.mean = X.mean(axis=0)
    base.std = np.maximum(X.std(axis=0, ddof=1), 1e-7)
    base.collect_until = 0
    normal = base.signature(0.02*np.sin(2*np.pi*np.arange(4096)/52.0), delay)
    changed = base.signature(
        0.02*np.sin(2*np.pi*np.arange(4096)/52.0)
        + 0.008*np.sin(2*np.pi*np.arange(4096)/31.0), delay
    )
    d0, d1 = base.distance(normal), base.distance(changed)
    ok = d1 > d0 * 2.0
    print(f"[T5] orbit change distance baseline={d0:.2f}, changed={d1:.2f}: {'PASS' if ok else 'FAIL'}")
    ok_all &= ok

    print("SELFTEST", "PASS" if ok_all else "FAIL")
    return 0 if ok_all else 1


def list_devices() -> int:
    if pyaudio is None:
        print("PyAudio is not installed.")
        return 1
    pa = pyaudio.PyAudio()
    try:
        for i in range(pa.get_device_count()):
            d = pa.get_device_info_by_index(i)
            print(
                f"{i:2d}  in={int(d.get('maxInputChannels',0)):2d} "
                f"out={int(d.get('maxOutputChannels',0)):2d} "
                f"rate={int(d.get('defaultSampleRate',0)):6d}  {d.get('name','')}"
            )
    finally:
        pa.terminate()
    return 0


def run_gui() -> int:
    if pyaudio is None:
        raise RuntimeError("PyAudio is not installed. Run: pip install pyaudio")

    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    import matplotlib
    matplotlib.use("TkAgg")
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    cfg = Config()
    dsp = SusceptibilityDSP(cfg)
    audio = AudioEngine(dsp)
    logger = CSVLogger()

    root = tk.Tk()
    root.title("WeirdFusions — Susceptibility Amplifier")
    root.geometry("1500x900")
    root.minsize(1150, 720)

    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    left = ttk.Frame(root, padding=10)
    left.grid(row=0, column=0, sticky="ns")
    plot_frame = ttk.Frame(root, padding=(0, 10, 10, 10))
    plot_frame.grid(row=0, column=1, sticky="nsew")
    plot_frame.rowconfigure(0, weight=1)
    plot_frame.columnconfigure(0, weight=1)

    # ---------------- devices ----------------
    ins, outs = audio.devices()
    in_map = {label: idx for label, idx in ins}
    out_map = {label: idx for label, idx in outs}

    dev = ttk.LabelFrame(left, text="AUDIO DEVICES", padding=8)
    dev.pack(fill="x", pady=(0, 8))

    in_var = tk.StringVar(value=ins[0][0] if ins else "")
    out_var = tk.StringVar(value=outs[0][0] if outs else "")

    ttk.Label(dev, text="Input").pack(anchor="w")
    in_box = ttk.Combobox(dev, textvariable=in_var, values=list(in_map), state="readonly", width=42)
    in_box.pack(fill="x", pady=(0, 5))
    ttk.Label(dev, text="Output").pack(anchor="w")
    out_box = ttk.Combobox(dev, textvariable=out_var, values=list(out_map), state="readonly", width=42)
    out_box.pack(fill="x")

    # ---------------- arm + safety ----------------
    arm = ttk.LabelFrame(left, text="ARM / SAFETY", padding=8)
    arm.pack(fill="x", pady=(0, 8))
    mode_var = tk.StringVar(value=cfg.mode)
    mode_row = ttk.Frame(arm)
    mode_row.pack(fill="x")
    for m in ("OPEN", "FIXED", "EDGE"):
        ttk.Radiobutton(mode_row, text=m, value=m, variable=mode_var).pack(side="left", expand=True)

    state_var = tk.StringVar(value="MUTED — start audio, then unmute")
    state_label = ttk.Label(arm, textvariable=state_var)
    state_label.pack(fill="x", pady=6)

    btn_row = ttk.Frame(arm)
    btn_row.pack(fill="x")
    start_btn = ttk.Button(btn_row, text="START AUDIO")
    start_btn.pack(side="left", expand=True, fill="x", padx=(0, 3))
    mute_btn = ttk.Button(btn_row, text="UNMUTE")
    mute_btn.pack(side="left", expand=True, fill="x", padx=3)
    panic_btn = ttk.Button(btn_row, text="EMERGENCY MUTE")
    panic_btn.pack(side="left", expand=True, fill="x", padx=(3, 0))

    ttk.Label(
        arm,
        text="Start with interface/speaker monitor low.\n"
             "Software MAX OUTPUT is not an SPL guarantee.",
        foreground="#8a3b00",
        justify="left",
    ).pack(anchor="w", pady=(6, 0))

    # ---------------- parameters ----------------
    params = ttk.LabelFrame(left, text="LOOP", padding=8)
    params.pack(fill="x", pady=(0, 8))

    controls = {}

    def scale_row(parent, label, lo, hi, value, resolution=0.01):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label, width=18).pack(side="left")
        var = tk.DoubleVar(value=value)
        scl = tk.Scale(
            row, from_=lo, to=hi, resolution=resolution, orient="horizontal",
            variable=var, showvalue=False, length=190
        )
        scl.pack(side="left", fill="x", expand=True)
        val = ttk.Label(row, width=10)
        val.pack(side="right")
        controls[label] = (var, val)
        return var

    freq_v = scale_row(params, "MODE FREQ Hz", 40, 5000, cfg.frequency_hz, 1)
    probe_v = scale_row(params, "PROBE AMP", 0.0, 0.03, cfg.probe_amp, 0.0005)
    fixed_v = scale_row(params, "FIXED GAIN", 0.0, 8.0, cfg.fixed_gain, 0.01)
    target_v = scale_row(params, "TARGET MODE AMP", 0.001, 0.08, cfg.target_mode_amp, 0.0005)
    phase_v = scale_row(params, "PHASE DEG", -180, 180, cfg.phase_deg, 1)
    maxout_v = scale_row(params, "MAX OUTPUT", 0.005, 0.12, cfg.max_output, 0.001)

    # ---------------- experiment ----------------
    exp = ttk.LabelFrame(left, text="EXPERIMENT", padding=8)
    exp.pack(fill="x", pady=(0, 8))

    ttk.Label(exp, text="Trial ID").grid(row=0, column=0, sticky="w")
    trial_var = tk.StringVar(value="baseline")
    ttk.Entry(exp, textvariable=trial_var, width=18).grid(row=0, column=1, sticky="ew", padx=5)

    ttk.Label(exp, text="Hidden label").grid(row=1, column=0, sticky="w")
    label_var = tk.StringVar(value="")
    ttk.Entry(exp, textvariable=label_var, width=18).grid(row=1, column=1, sticky="ew", padx=5)
    exp.columnconfigure(1, weight=1)

    baseline_btn = ttk.Button(exp, text="CAPTURE BASELINE 5 s")
    baseline_btn.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(6, 3))
    log_btn = ttk.Button(exp, text="START CSV LOG")
    log_btn.grid(row=3, column=0, columnspan=2, sticky="ew", pady=3)

    # ---------------- metrics ----------------
    met = ttk.LabelFrame(left, text="LIVE READOUT", padding=8)
    met.pack(fill="both", expand=True)

    metrics = {}
    for name in (
        "mic RMS", "mode amp", "feedback gain", "mode phase", "peak freq",
        "Q estimate", "orbit distance", "output peak", "clip count", "xrun count"
    ):
        row = ttk.Frame(met)
        row.pack(fill="x")
        ttk.Label(row, text=name).pack(side="left")
        v = ttk.Label(row, text="—")
        v.pack(side="right")
        metrics[name] = v

    # ---------------- plots ----------------
    fig = Figure(figsize=(10, 7), dpi=100)
    ax_wave = fig.add_subplot(221)
    ax_spec = fig.add_subplot(222)
    ax_orbit = fig.add_subplot(223, projection="3d")
    ax_ctrl = fig.add_subplot(224)
    fig.tight_layout(pad=2.0)

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    ctrl_t = deque(maxlen=600)
    ctrl_g = deque(maxlen=600)
    ctrl_d = deque(maxlen=600)

    running = {"audio": False, "logging": False}
    gui_start = time.monotonic()

    def sync_cfg():
        with dsp.lock:
            cfg.mode = mode_var.get()
            cfg.frequency_hz = float(freq_v.get())
            cfg.probe_amp = float(probe_v.get())
            cfg.fixed_gain = float(fixed_v.get())
            cfg.target_mode_amp = float(target_v.get())
            cfg.phase_deg = float(phase_v.get())
            cfg.max_output = float(maxout_v.get())

        controls["MODE FREQ Hz"][1].config(text=f"{cfg.frequency_hz:.0f}")
        controls["PROBE AMP"][1].config(text=f"{cfg.probe_amp:.4f}")
        controls["FIXED GAIN"][1].config(text=f"{cfg.fixed_gain:.2f}")
        controls["TARGET MODE AMP"][1].config(text=f"{cfg.target_mode_amp:.4f}")
        controls["PHASE DEG"][1].config(text=f"{cfg.phase_deg:+.0f}")
        controls["MAX OUTPUT"][1].config(text=f"{cfg.max_output:.3f}")

    def do_start():
        try:
            if not in_var.get() or not out_var.get():
                raise RuntimeError("Select both an input and output device.")
            dsp.set_muted(True)
            audio.start(in_map[in_var.get()], out_map[out_var.get()])
            running["audio"] = True
            start_btn.config(text="RESTART AUDIO")
            mute_btn.config(text="UNMUTE")
            state_var.set("MUTED — audio running")
        except Exception as e:
            messagebox.showerror("Audio start failed", str(e))

    def do_mute_toggle():
        with dsp.lock:
            new_state = not dsp.muted
            dsp.muted = new_state
        mute_btn.config(text="UNMUTE" if new_state else "MUTE")
        state_var.set("MUTED" if new_state else f"LIVE — {cfg.mode}")

    def do_panic():
        dsp.panic()
        mute_btn.config(text="UNMUTE")
        state_var.set("EMERGENCY MUTED")

    def do_baseline():
        dsp.baseline.begin(5.0)
        state_var.set("CAPTURING 5 s BASELINE")

    def do_log():
        if not running["logging"]:
            default = f"susceptibility_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            path = filedialog.asksaveasfilename(
                title="Save experiment log",
                initialfile=default,
                defaultextension=".csv",
                filetypes=[("CSV", "*.csv")],
            )
            if not path:
                return
            logger.start(path)
            running["logging"] = True
            log_btn.config(text="STOP CSV LOG")
        else:
            logger.stop()
            running["logging"] = False
            log_btn.config(text="START CSV LOG")

    start_btn.config(command=do_start)
    mute_btn.config(command=do_mute_toggle)
    panic_btn.config(command=do_panic)
    baseline_btn.config(command=do_baseline)
    log_btn.config(command=do_log)

    def update_gui():
        sync_cfg()
        s, x, y, hist = dsp.snapshot()

        if dsp.baseline.collecting:
            state_var.set("CAPTURING BASELINE…")
        elif dsp.baseline.ready and s.muted:
            state_var.set("MUTED — baseline ready")
        elif not s.muted:
            state_var.set(f"LIVE — {s.mode}")

        metrics["mic RMS"].config(text=f"{s.mic_rms:.6f}")
        metrics["mode amp"].config(text=f"{s.mode_amp:.6f}")
        metrics["feedback gain"].config(text=f"{s.feedback_gain:.4f}")
        metrics["mode phase"].config(text=f"{s.mode_phase_deg:+.1f}°")
        metrics["peak freq"].config(text=f"{s.peak_freq_hz:.2f} Hz" if math.isfinite(s.peak_freq_hz) else "—")
        metrics["Q estimate"].config(text=f"{s.q_estimate:.1f}" if math.isfinite(s.q_estimate) else "—")
        metrics["orbit distance"].config(text=f"{s.orbit_distance:.2f}" if math.isfinite(s.orbit_distance) else "—")
        metrics["output peak"].config(text=f"{s.output_peak:.5f}")
        metrics["clip count"].config(text=str(s.clip_count))
        metrics["xrun count"].config(text=str(s.xrun_count))

        # Drain stats queue and log / history.
        while True:
            try:
                qstats = dsp.log_queue.get_nowait()
            except Exception:
                break
            ctrl_t.append(qstats.t)
            ctrl_g.append(qstats.feedback_gain)
            ctrl_d.append(qstats.orbit_distance)
            if running["logging"]:
                logger.write(qstats, trial_var.get(), label_var.get(), qstats.t)

        # Plots.
        ax_wave.clear()
        if x.size:
            ms = np.arange(x.size) * 1000.0 / cfg.sample_rate
            ax_wave.plot(ms, x, linewidth=0.8, label="mic")
            ax_wave.plot(ms, y, linewidth=0.8, alpha=0.75, label="out")
        ax_wave.set_title("latest block")
        ax_wave.set_xlabel("ms")
        ax_wave.legend(loc="upper right", fontsize=8)
        ax_wave.grid(alpha=0.2)

        ax_spec.clear()
        if hist.size >= 256:
            z = hist[-min(hist.size, 16384):].astype(np.float64)
            z -= z.mean()
            W = np.hanning(z.size)
            X = np.abs(np.fft.rfft(z * W))
            F = np.fft.rfftfreq(z.size, 1.0 / cfg.sample_rate)
            mask = (F >= max(1.0, cfg.frequency_hz * 0.35)) & (F <= cfg.frequency_hz * 1.8)
            if np.any(mask):
                ax_spec.plot(F[mask], 20*np.log10(X[mask] + 1e-12), linewidth=0.9)
                ax_spec.axvline(cfg.frequency_hz, linestyle="--", linewidth=0.8)
        ax_spec.set_title("spectrum around selected mode")
        ax_spec.set_xlabel("Hz")
        ax_spec.set_ylabel("dB rel.")
        ax_spec.grid(alpha=0.2)

        ax_orbit.clear()
        if hist.size >= 256:
            delay = max(1, int(cfg.sample_rate / max(cfg.frequency_hz, 1.0) / 4.0))
            h = hist[-min(hist.size, 5000):]
            if h.size > 2 * delay + 10:
                a = h[2*delay:]
                b = h[delay:-delay]
                c = h[:-2*delay]
                stride = max(1, a.size // 1200)
                ax_orbit.plot(a[::stride], b[::stride], c[::stride], linewidth=0.55)
        ax_orbit.set_title("delay orbit")
        ax_orbit.set_xlabel("x(t)")
        ax_orbit.set_ylabel("x(t-τ)")
        ax_orbit.set_zlabel("x(t-2τ)")

        ax_ctrl.clear()
        if ctrl_t:
            tt = np.asarray(ctrl_t)
            gg = np.asarray(ctrl_g)
            ax_ctrl.plot(tt, gg, label="feedback gain")
            finite_d = np.asarray([v if math.isfinite(v) else np.nan for v in ctrl_d])
            if np.any(np.isfinite(finite_d)):
                ax2 = ax_ctrl.twinx()
                ax2.plot(tt, finite_d, alpha=0.55, label="orbit Δ")
                ax2.set_ylabel("orbit Δ")
        ax_ctrl.set_title("controller / susceptibility readout")
        ax_ctrl.set_xlabel("s")
        ax_ctrl.set_ylabel("gain")
        ax_ctrl.grid(alpha=0.2)

        fig.tight_layout(pad=1.5)
        canvas.draw_idle()

        root.after(150, update_gui)

    def on_close():
        dsp.panic()
        logger.stop()
        audio.close()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.bind("<Escape>", lambda e: do_panic())
    sync_cfg()
    root.after(150, update_gui)
    root.mainloop()
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true", help="run DSP/controller tests without audio")
    ap.add_argument("--list-devices", action="store_true", help="print PyAudio devices and exit")
    args = ap.parse_args()

    if args.selftest:
        return selftest()
    if args.list_devices:
        return list_devices()
    return run_gui()


if __name__ == "__main__":
    raise SystemExit(main())

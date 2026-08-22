# Weird Fusion — Susceptibility Amplifier

*Put the unknown world inside a feedback loop, bias the loop near a transition, and measure how the world deforms the loop rather than trying to amplify the world directly.*

> Do not hype. Do not lie. Just show.

## Why this exists

This came out of an accidental connection between several old PerceptionLab fossils and a new rendering accident.

- **Slider2 / the early phase-space line** already had a real audio path: generate a tone → speaker → room → microphone → inspect the returned waveform and its delay/phase-space trajectory.
- **ConsciousField** wrapped essentially the same physical loop in much less defensible language. Strip that language away and the useful object is simply **machine → physical medium → receiver → machine**.
- Old PerceptionLab / moiré / checkerboard workflows repeatedly produced cases where small internal differences became large visible or dynamical differences because they landed in a sensitive feedback/readout geometry.
- **ANTTISBRAIN III** accidentally reintroduced a polar `1/r` slope blow-up on its reflective moons. A tiny change in the material-eye texture can be mapped through a huge local geometric Jacobian into a macroscopic visible change. AnttisBrain2 had deliberately guarded this singularity away.

The common sentence is not "waves" or "quantum" or "consciousness".

It is:

> **Make tiny differences observable by putting them where the observer/system has enormous susceptibility.**

The acoustic version is the most literal physical test of that sentence.

---

## 1. The conceptual change from Slider2

Slider2's old path was approximately:

```text
oscillator → speaker → room → microphone → measurement
```

The microphone return was observed, but it did not determine the next speaker sample. That is an *open-loop probe of a physical transfer function*.

The proposed fusion closes the loop:

```text
                     ┌─────────────────────────────┐
                     │                             │
                     ▼                             │
generator → speaker → WORLD → microphone → filter ─┤
                     ▲                             │
                     │                             │
                     └──── gain + phase ◄──────────┘
```

The `WORLD` is not an abstraction here. It is the actual speaker cone, air, room, microphone diaphragm, table, walls, objects, temperature field, and anything else coupled strongly enough to perturb the transfer function.

We are **not** primarily trying to amplify an external sound until it rises above the Focusrite / microphone noise floor.

We instead create a known macroscopic dynamical system whose behaviour depends strongly on a weakly perturbed transfer function.

---

## 2. Near-critical susceptibility

Let the acoustic plant be \(H(f)\): speaker + room + microphone + converters.
Let the controlled electronic return path be \(G(f)\).

A cartoon closed-loop response is

\[
T(f)=\frac{H(f)}{1-G(f)H(f)}.
\]

Far from the feedback threshold, a tiny environmental change

\[
H \rightarrow H+\delta H
\]

produces a tiny output change.

Near a mode where

\[
|G H| \lesssim 1
\]

and the loop phase is close to constructive, the denominator becomes small. The same tiny \(\delta H\) can then produce a much larger change in the loop's macroscopic amplitude, phase, oscillation frequency, ringdown, or mode selection.

This is the physical analogue of the broken moon:

```text
ANTTISBRAIN III
small texture perturbation
    ↓
large observation Jacobian
    ↓
large visible change

ACOUSTIC LOOP
small transfer-function perturbation
    ↓
large dynamical susceptibility
    ↓
large trajectory change
```

The amplification is not necessarily in the original variable. It is in the **sensitivity of the observer/dynamical system**.

---

## 3. Do not begin with uncontrolled positive feedback

A raw microphone → speaker loop will probably find one loud room mode, scream, clip, distort, and tell us mostly about the loudspeaker, DAC/ADC latency, microphone nonlinearities, and our ears.

The useful instrument should instead keep itself near the edge *under control*.

```text
                  external world
                        ↓
 speaker → room / object / air → microphone
    ▲                         │
    │                         ▼
    └──── controlled gain + phase
                  ▲
                  │
           EDGE CONTROLLER
```

The controller's job is to hold a selected mode at a small target amplitude while staying below runaway oscillation.

Now the primary measurement is not simply `microphone amplitude`.

It is:

> **What gain / phase / frequency correction did the controller have to apply to keep the same macroscopic orbit alive?**

That gives several possible sensor channels:

```text
required loop gain
required phase correction
resonant frequency
ringdown / effective Q
mode competition
trajectory geometry
recurrence / orbit thickness
```

A stationary object does not need to "make a sound." It only needs to alter the physical transfer function enough that the edge controller must compensate.

---

## 4. The old phase-space obsession becomes useful here

Slider2 plotted consecutive captured buffers as a 3-D delayed object. The old reason for caring about that view was muddy, but here it has a precise job.

Instead of only asking whether RMS amplitude changed, embed the returned signal as

\[
X(t)=[x(t),x(t-\tau),x(t-2\tau)].
\]

Then measure deformation of the orbit:

- centroid / radius;
- principal axes;
- phase rotation;
- orbit thickness;
- recurrence structure;
- mode splitting;
- drift of the dominant period;
- distance between a baseline attractor and the current attractor.

A perturbation may barely change gross amplitude yet strongly rotate, thicken, split or shift the reconstructed orbit.

So the working sentence becomes:

> **Do not amplify the unknown thing. Build a known dynamical system whose trajectory is easy to observe, put the unknown world inside its feedback path, and detect deformation of the trajectory.**

---

## 5. First experiment — deliberately boring

Do not begin at the noise floor. First establish that the mechanism exists and quantify its gain.

### Hardware

- audio interface (e.g. Focusrite Solo);
- one speaker;
- one microphone;
- rigid, repeatable speaker/microphone placement;
- quiet room;
- software loop with narrow-band filtering, phase control, gain control, hard limiter and emergency mute.

### Three matched arms

**A. Open-loop baseline**

```text
tone → speaker → room → mic → measurement
```

No microphone feedback.

**B. Fixed subcritical feedback**

Same acoustic level as closely as practical, but with a fixed loop gain safely below oscillation.

**C. Edge-controlled feedback**

Controller continuously adjusts loop gain / phase to hold the selected mode at the target amplitude just below self-oscillation.

The interesting quantity is not whether C changes. Everything changes. The question is whether the same physical perturbation is **more discriminable in C than A/B**.

---

## 6. Perturbation ladder

Start embarrassingly macroscopic and walk downward only if the previous rung passes.

```text
0. nothing / repeated baseline
1. open and close the door
2. move a chair
3. introduce a large cardboard sheet
4. hand 1 m from the acoustic path
5. hand 50 cm away
6. hand 20 cm away
7. stationary small object
8. small temperature / airflow perturbation
9. weak remote vibration
10. only then: things near the ordinary measurement floor
```

For every perturbation, randomise presentation order and include sham trials.

The loop must not know the label.

---

## 7. The susceptibility gain

Choose one pre-registered state-distance metric \(D\) before looking at the answer.

For example:

\[
\Delta_A = D(\text{baseline orbit},\text{perturbed orbit})
\]

for open loop and similarly \(\Delta_C\) for the edge-controlled loop.

Define

\[
G_{sus}=\frac{\Delta_C}{\max(\Delta_A,\epsilon)}.
\]

This is the physical cousin of the proposed ANTTISBRAIN geometric gain

\[
G_{geo}=\frac{\|\Delta\text{render}\|}{\|\Delta\text{eye}\|}.
\]

A large \(G_{sus}\) is not enough. We also need the baseline variance to remain controlled. A machine that amplifies its own noise even faster than the perturbation is not a detector.

A more honest discriminability quantity is therefore something like

\[
S = \frac{\mu_{pert}-\mu_{sham}}
         {\sqrt{\tfrac12(\sigma_{pert}^2+\sigma_{sham}^2)}}.
\]

The near-critical arm wins only if **discriminability** improves, not merely raw movement.

---

## 8. The central attacker: it may amplify itself, not the world

This is the whole experiment.

Near criticality also amplifies:

- ADC/DAC noise;
- microphone self-noise;
- preamp noise;
- quantisation;
- USB timing jitter;
- buffer timing;
- speaker nonlinearity;
- room thermal / convective variation;
- tiny mechanical drift;
- the controller's own errors.

So the strong claim is **not**:

> near-critical feedback is sensitive.

Of course it is.

The strong test is:

> **Can controlled susceptibility improve sensitivity to an external perturbation faster than it increases false movement caused by the instrument itself?**

If no, the scientific story dies.

The sound/art instrument may still be wonderful.

---

## 9. Controls that matter

### Electronic loopback

Replace speaker/room/microphone with direct interface output → interface input. This measures converter, buffer and controller behaviour without the physical acoustic world.

### Silent microphone

Run the analysis with the speaker muted / loop broken to estimate microphone + preamp baseline.

### Dummy acoustic change

Present the software with the same trial timing without moving anything.

### Far-from-critical control

Same physical perturbation, same measurement pipeline, but low loop susceptibility.

### Playback control

Record one microphone stream once and replay it through the analysis/controller without a live physical loop. Any "new environmental sensitivity" that survives this arm is analysis artefact.

### Level control

Keep ordinary acoustic SPL comparable when comparing conditions. Otherwise a near-critical system might simply "win" because it is louder.

---

## 10. Safety is part of the apparatus

Acoustic positive feedback can jump from quiet to painfully loud extremely quickly.

The first implementation must have, before any interesting science:

- conservative hardware/software output limit;
- narrow-band filter;
- instantaneous hard clip / limiter;
- automatic gain reduction on threshold crossing;
- watchdog mute if callback timing fails;
- obvious physical mute / unplug path;
- development at low speaker level and preferably with hearing protection / distance until bounded behaviour is verified.

**Do not use "near critical" as a reason to operate near dangerous SPL.** Criticality is a loop-gain condition, not a loudness target.

---

## 11. What would count as a real result

### Pass

Across repeated blinded/sham trials:

1. a physical perturbation that is weak or poorly discriminable in open loop becomes substantially more discriminable in the edge-controlled loop;
2. electronic-loopback and playback controls do not reproduce the effect;
3. the improvement persists across more than one acoustic mode / placement;
4. the result can be predicted from measured changes in the plant transfer function or controller correction, not only seen after plotting;
5. lowering susceptibility removes the gain.

### Interesting failure

The loop is extremely sensitive, but almost entirely to its own noise / drift.

That still gives a good instrument and a clean boundary:

> susceptibility without selectivity is not sensing.

### Creative success / scientific failure

The loop falls into rich mode-switching, beating, phase-space splitting or site-specific sound that cannot reliably discriminate controlled perturbations.

Then kill the sensor claim and keep it as a **physical generative instrument whose environment is part of its synthesis state**.

That is still a happy accident.

---

## 12. Why this belongs in `WeirdFusions`

This is not a new grand architecture. It is a collision of old things whose original stories were mostly wrong or incomplete:

```text
Slider2 phase-space visualisation
          +
ConsciousField's real speaker-room-mic path
          +
old PerceptionLab feedback / moiré amplification accidents
          +
ANTTISBRAIN III's geometric susceptibility accident
          +
Saturday's insistence on separating mechanism from metaphor
          ↓
controlled susceptibility as an instrument
```

The useful residue may be very small:

> **External perturbations can be made easier to see by placing them inside a controlled dynamical system near a high-susceptibility operating point.**

That statement is old physics/control intuition, not a novelty claim.

What is ours to test is the particular cheap apparatus, the phase-space readout, the controls, and whether anything unexpectedly useful appears when the *world itself* becomes one component of the loop.

---

## 13. First implementation target

Do not modify old Slider2 until the experiment is specified.

A clean first program should expose only:

```text
INPUT DEVICE
OUTPUT DEVICE
MODE FREQUENCY
TARGET RMS
MAX OUTPUT
FEEDBACK GAIN
PHASE DELAY
EDGE CONTROLLER ON/OFF
EMERGENCY MUTE

plots:
  waveform
  spectrum
  phase-space orbit
  controller gain
  controller phase
  orbit distance from baseline
```

And write one CSV row per analysis window:

```text
time,
trial_id,
arm,
label_hidden,
freq,
rms,
feedback_gain,
phase_correction,
peak_freq,
q_estimate,
orbit_distance,
clip_count,
xrun_count
```

No "quantum" detector. No crystal harmonics. No meaning assigned to a shape before the controls say it carries information.

Just a physical loop, its state, and an attacker.

---

## One-line version

> **Build a quiet macroscopic oscillator at the edge of instability, put the external world inside its feedback path, and watch how tiny changes in the world deform the oscillator's trajectory.**

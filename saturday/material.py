"""Small event-driven computational material.

The point is deliberately modest: make MASS, ROTATE and LATCH local
materials coexist on a sparse ROUTE graph and let waves both read and
change that material.

This is not a brain simulator and the clock law is not a claim about
General Relativity.  The useful abstraction is that local history can
change local dynamical time and therefore change how later waves are
transformed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import cmath
import heapq
import math
from typing import Dict, Iterable, List, Optional, Tuple


class Kind(str, Enum):
    MASS = "mass"
    ROTATE = "rotate"
    LATCH = "latch"
    PASS = "pass"


@dataclass
class Cell:
    """One local piece of dynamical material.

    Every cell carries a complex fast state ``z`` and a non-negative
    slow ``mass``.  MASS/ROTATE/LATCH differ in their constitutive
    dynamics, while ``mass`` controls the local clock

        gamma = 1 / (1 + kappa * mass).

    The slow mass relaxes in ordinary/global time.  The fast state
    evolves in accumulated local time.  Because the integral of gamma is
    analytic while mass decays exponentially, a quiet cell can sleep and
    be materialized exactly only when an event next touches it.
    """

    kind: Kind
    alpha: float = 0.08
    omega: float = 1.0
    tau_mass: float = 20.0
    kappa: float = 4.0
    mass_write: Optional[float] = None
    latch_threshold: float = 1.2
    base_dwell: float = 1.0
    direct: float = 0.55
    readout: float = 0.45

    z: complex = 0j
    mass: float = 0.0
    latch: int = -1
    last_t: float = 0.0
    materializations: int = 0
    events_seen: int = 0

    def __post_init__(self) -> None:
        if self.mass_write is None:
            self.mass_write = {
                Kind.MASS: 1.0,
                Kind.ROTATE: 0.12,
                Kind.LATCH: 0.05,
                Kind.PASS: 0.0,
            }[self.kind]

    @property
    def gamma(self) -> float:
        """Current local clock rate."""
        return 1.0 / (1.0 + self.kappa * self.mass)

    def _proper_dt(self, dt: float) -> float:
        """Exact local time accumulated while mass relaxes for ``dt``.

        If m(t) = m0 exp(-t/tau), then

            integral dt / (1 + kappa*m(t))

        has the closed form used below.  This is the tiny trick that
        makes quiet periods genuinely lazy instead of simulated by many
        no-op ticks.
        """
        if dt <= 0.0:
            return 0.0
        a = self.kappa * self.mass
        return dt + self.tau_mass * (
            math.log1p(a * math.exp(-dt / self.tau_mass)) - math.log1p(a)
        )

    def materialize(self, t: float) -> None:
        """Advance this cell from its last touched time to ``t`` exactly."""
        if t < self.last_t - 1e-12:
            raise ValueError("cell cannot be materialized backwards in time")
        dt = t - self.last_t
        if dt <= 0.0:
            return

        local_dt = self._proper_dt(dt)
        if self.kind is Kind.ROTATE:
            self.z *= cmath.exp(complex(-self.alpha, self.omega) * local_dt)
        else:
            self.z *= math.exp(-self.alpha * local_dt)

        self.mass *= math.exp(-dt / self.tau_mass)
        self.last_t = t
        self.materializations += 1

    def process(self, wave: complex, t: float) -> Tuple[complex, float, float]:
        """Let one wave packet interact with this material.

        Returns ``(output_wave, dwell_time, gamma_before_write)``.
        The incoming wave changes both fast state and, depending on cell
        kind, slower material state.
        """
        self.materialize(t)
        self.events_seen += 1
        gamma_before = self.gamma

        if self.kind is Kind.LATCH and abs(wave.real) >= self.latch_threshold:
            self.latch = 1 if wave.real >= 0.0 else -1

        # The wave becomes part of the local fast state.
        self.z += wave

        gate = 1.0
        if self.kind is Kind.LATCH:
            gate = 1.0 if self.latch > 0 else 0.2

        output = gate * (self.direct * wave + self.readout * self.z)

        # MASS is intentionally a low-bandwidth material: existing mass
        # attenuates an arriving fast disturbance and also increases dwell.
        if self.kind is Kind.MASS:
            output *= math.sqrt(gamma_before)

        # A wave leaves a slower residue.  Different material types write
        # that residue with different strength.
        self.mass += float(self.mass_write) * (abs(wave) ** 2)

        # Lower local clock -> longer global residence time.
        dwell = self.base_dwell / max(gamma_before, 1e-12)
        return output, dwell, gamma_before


@dataclass
class Edge:
    """Sparse ROUTE connection with slow use-dependent structure."""

    src: str
    dst: str
    delay: float = 1.0
    coupling: float = 0.8
    plasticity: float = 0.0
    max_coupling: float = 1.0
    trace: float = 0.0
    tau_trace: float = 50.0
    last_t: float = 0.0

    def transmit(self, wave: complex, t: float) -> complex:
        dt = t - self.last_t
        if dt > 0.0:
            self.trace *= math.exp(-dt / self.tau_trace)

        # The present wave sees the old structure; its passage then leaves
        # a slow structural consequence for later waves.
        old_coupling = self.coupling
        energy = abs(wave) ** 2
        self.trace += energy
        if self.plasticity:
            self.coupling += (
                self.plasticity * energy * (self.max_coupling - self.coupling)
            )
        self.last_t = t
        return old_coupling * wave


@dataclass(order=True)
class _Event:
    time: float
    seq: int
    node: str = field(compare=False)
    amp: complex = field(compare=False)
    ttl: int = field(compare=False, default=64)


class Medium:
    """A sparse heterogeneous material driven by timestamped wave events."""

    def __init__(self) -> None:
        self.cells: Dict[str, Cell] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}
        self.outgoing: Dict[str, List[str]] = {}
        self.receivers: set[str] = set()
        self._seq = 0

    # Higher-level code is allowed to manufacture and remove material.
    def add_cell(self, name: str, cell: Cell, *, receiver: bool = False) -> None:
        self.cells[name] = cell
        self.outgoing.setdefault(name, [])
        if receiver:
            self.receivers.add(name)

    def remove_cell(self, name: str) -> None:
        self.cells.pop(name, None)
        self.receivers.discard(name)
        for src, dst in list(self.edges):
            if src == name or dst == name:
                self.disconnect(src, dst)
        self.outgoing.pop(name, None)

    def connect(self, src: str, dst: str, **edge_kwargs: float) -> None:
        if src not in self.cells or dst not in self.cells:
            raise KeyError("both endpoint cells must exist before connect()")
        if (src, dst) in self.edges:
            raise ValueError(f"edge {src!r}->{dst!r} already exists")
        self.edges[(src, dst)] = Edge(src, dst, **edge_kwargs)
        self.outgoing.setdefault(src, []).append(dst)

    def disconnect(self, src: str, dst: str) -> None:
        self.edges.pop((src, dst), None)
        if src in self.outgoing and dst in self.outgoing[src]:
            self.outgoing[src].remove(dst)

    def run(
        self,
        injections: Iterable[Tuple[float, str, complex]],
        *,
        until: float = math.inf,
    ) -> List[Tuple[float, str, complex]]:
        """Propagate timestamped wave packets until they hit receivers.

        Directed graphs are the intended first use. ``ttl`` is kept on
        internal events so later experiments can safely introduce cycles.
        """
        queue: List[_Event] = []
        received: List[Tuple[float, str, complex]] = []

        for t, node, amp in injections:
            if node not in self.cells:
                raise KeyError(node)
            self._seq += 1
            heapq.heappush(queue, _Event(float(t), self._seq, node, complex(amp)))

        while queue:
            event = heapq.heappop(queue)
            if event.time > until:
                break

            if event.node in self.receivers:
                received.append((event.time, event.node, event.amp))
                continue

            cell = self.cells[event.node]
            out_wave, dwell, _ = cell.process(event.amp, event.time)
            if event.ttl <= 0:
                continue

            for dst in self.outgoing.get(event.node, []):
                edge = self.edges[(event.node, dst)]
                routed = edge.transmit(out_wave, event.time)
                self._seq += 1
                heapq.heappush(
                    queue,
                    _Event(
                        event.time + dwell + edge.delay,
                        self._seq,
                        dst,
                        routed,
                        event.ttl - 1,
                    ),
                )

        return received

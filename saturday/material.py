"""Small event-driven computational material.

The point is deliberately modest: make several local dynamical capabilities
coexist on a sparse ROUTE graph and let waves both read and change that material.

This is not a brain simulator and the clock law is not a claim about General
Relativity. The useful abstraction is that local history can change local
dynamical time while transport, coupling, and readout remain separately
inspectable mechanisms.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import cmath
import heapq
import math
from typing import Dict, Iterable, List, Optional, Tuple


class Kind(str, Enum):
    """Convenience presets, not four mutually exclusive substances.

    ROTATE has one strict dynamical meaning here: its free linear dynamics
    contain one complex-conjugate pole pair. MASS is a slow state every Cell
    may carry; LATCH is persistent configuration that routes/transforms later
    events.
    """

    MASS = "mass"
    ROTATE = "rotate"
    LATCH = "latch"
    PASS = "pass"


@dataclass
class Cell:
    """One local piece of dynamical material.

    Every cell carries a complex fast state ``z`` and a non-negative slow
    ``mass``. ``mass`` controls only the local execution clock

        gamma = 1 / (1 + kappa * mass).

    It does NOT directly change propagation delay, edge coupling, or signal
    amplitude. Those are separate mechanisms.

    The slow mass relaxes in ordinary/global time. The fast state evolves in
    accumulated local time. Because the integral of gamma is analytic while
    mass decays exponentially, a quiet cell can sleep and be materialized only
    when an event next touches it.
    """

    kind: Kind
    alpha: float = 0.08
    omega: float = 1.0
    tau_mass: float = 20.0
    kappa: float = 4.0
    mass_write: Optional[float] = None
    latch_threshold: float = 1.2
    base_compute: float = 1.0
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
        """Current local execution-clock rate."""
        return 1.0 / (1.0 + self.kappa * self.mass)

    def _proper_dt(self, dt: float) -> float:
        """Exact local time accumulated while mass relaxes for ``dt``."""
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
            # Pole structure: -alpha +/- i*omega.
            self.z *= cmath.exp(complex(-self.alpha, self.omega) * local_dt)
        else:
            self.z *= math.exp(-self.alpha * local_dt)

        self.mass *= math.exp(-dt / self.tau_mass)
        self.last_t = t
        self.materializations += 1

    def process(self, wave: complex, t: float) -> Tuple[complex, float, float]:
        """Let one wave packet interact with this material.

        Returns ``(output_wave, compute_time, gamma_before_write)``.
        ``compute_time`` is execution latency. Edge propagation time is kept
        separately by Medium and is never inferred from gamma.
        """
        self.materialize(t)
        self.events_seen += 1
        gamma_before = self.gamma

        if self.kind is Kind.LATCH and abs(wave.real) >= self.latch_threshold:
            self.latch = 1 if wave.real >= 0.0 else -1

        self.z += wave
        output = self.direct * wave + self.readout * self.z

        # MASS is cross-cutting state: every cell may write some slow residue.
        self.mass += float(self.mass_write) * (abs(wave) ** 2)

        # gamma controls execution latency only.
        compute_time = self.base_compute / max(gamma_before, 1e-12)
        return output, compute_time, gamma_before


@dataclass
class Edge:
    """Sparse ROUTE with path delay, coupling, and a decaying use trace.

    ``required_latch`` makes persistent configuration able to select topology:
    an edge is live only when the source cell's latch matches that sign.
    """

    src: str
    dst: str
    delay: float = 1.0
    coupling: float = 0.8
    plasticity: float = 0.0
    trace: float = 0.0
    tau_trace: float = 50.0
    required_latch: Optional[int] = None
    last_t: float = 0.0
    initial_coupling: float = field(init=False)

    def __post_init__(self) -> None:
        self.initial_coupling = self.coupling

    def decay_trace(self, t: float) -> None:
        dt = t - self.last_t
        if dt > 0.0:
            self.trace *= math.exp(-dt / self.tau_trace)
            self.last_t = t

    def transmit(self, wave: complex, t: float) -> complex:
        """Transmit through current structure, then record route use."""
        self.decay_trace(t)
        old_coupling = self.coupling
        self.trace += abs(wave) ** 2
        return old_coupling * wave


@dataclass(order=True)
class _Event:
    time: float
    seq: int
    node: str = field(compare=False)
    amp: complex = field(compare=False)
    ttl: int = field(compare=False, default=64)
    origin_time: float = field(compare=False, default=0.0)
    compute_elapsed: float = field(compare=False, default=0.0)
    transport_elapsed: float = field(compare=False, default=0.0)
    hops: int = field(compare=False, default=0)


@dataclass(frozen=True)
class Observation:
    """One receiver observation with timing mechanisms separated."""

    time: float
    node: str
    amp: complex
    origin_time: float
    compute_time: float
    transport_time: float
    hops: int

    @property
    def total_delay(self) -> float:
        return self.time - self.origin_time


class Medium:
    """A sparse heterogeneous material driven by timestamped wave events."""

    def __init__(self) -> None:
        self.cells: Dict[str, Cell] = {}
        self.edges: Dict[Tuple[str, str], Edge] = {}
        self.outgoing: Dict[str, List[str]] = {}
        # receiver name -> whether observing terminates propagation
        self.receivers: Dict[str, bool] = {}
        self._seq = 0

    def add_cell(
        self,
        name: str,
        cell: Cell,
        *,
        receiver: bool = False,
        absorb: bool = True,
    ) -> None:
        self.cells[name] = cell
        self.outgoing.setdefault(name, [])
        if receiver:
            self.receivers[name] = bool(absorb)

    def remove_cell(self, name: str) -> None:
        self.cells.pop(name, None)
        self.receivers.pop(name, None)
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

    def _edge_enabled(self, src: str, edge: Edge) -> bool:
        if edge.required_latch is None:
            return True
        return self.cells[src].latch == edge.required_latch

    def _rebalance_outgoing(self, src: str, t: float) -> None:
        """Competitive plasticity under a fixed outgoing coupling budget.

        Only plastic edges participate. Their decaying traces bias how the
        initial total budget is divided; strengthening one therefore weakens
        competitors rather than monotonically saturating every used route.
        """
        edges = [
            self.edges[(src, dst)]
            for dst in self.outgoing.get(src, [])
            if self.edges[(src, dst)].plasticity > 0.0
        ]
        if len(edges) < 2:
            return

        for edge in edges:
            edge.decay_trace(t)

        budget = sum(edge.initial_coupling for edge in edges)
        scores = [
            edge.initial_coupling * (1.0 + edge.plasticity * edge.trace)
            for edge in edges
        ]
        denom = sum(scores)
        if denom <= 0.0:
            return

        for edge, score in zip(edges, scores):
            edge.coupling = budget * score / denom

    def run(
        self,
        injections: Iterable[Tuple[float, str, complex]],
        *,
        until: float = math.inf,
    ) -> List[Observation]:
        """Propagate timestamped wave packets and record receiver observations.

        A receiver may be absorbing (default) or non-absorbing. Non-absorbing
        receivers are inside the causal loop: they are observed and then keep
        processing/forwarding the event. ``ttl`` prevents accidental infinite
        recurrence when cycles are introduced.
        """
        queue: List[_Event] = []
        received: List[Observation] = []

        for t, node, amp in injections:
            if node not in self.cells:
                raise KeyError(node)
            self._seq += 1
            heapq.heappush(
                queue,
                _Event(
                    float(t),
                    self._seq,
                    node,
                    complex(amp),
                    origin_time=float(t),
                ),
            )

        while queue:
            event = heapq.heappop(queue)
            if event.time > until:
                break

            if event.node in self.receivers:
                received.append(
                    Observation(
                        time=event.time,
                        node=event.node,
                        amp=event.amp,
                        origin_time=event.origin_time,
                        compute_time=event.compute_elapsed,
                        transport_time=event.transport_elapsed,
                        hops=event.hops,
                    )
                )
                if self.receivers[event.node]:
                    continue

            cell = self.cells[event.node]
            out_wave, compute_time, _ = cell.process(event.amp, event.time)
            if event.ttl <= 0:
                continue

            transmissions = []
            for dst in self.outgoing.get(event.node, []):
                edge = self.edges[(event.node, dst)]
                if not self._edge_enabled(event.node, edge):
                    continue
                routed = edge.transmit(out_wave, event.time)
                transmissions.append((edge, dst, routed))

            # Rebalance after every live route saw the same pre-update structure.
            self._rebalance_outgoing(event.node, event.time)

            for edge, dst, routed in transmissions:
                self._seq += 1
                heapq.heappush(
                    queue,
                    _Event(
                        event.time + compute_time + edge.delay,
                        self._seq,
                        dst,
                        routed,
                        event.ttl - 1,
                        event.origin_time,
                        event.compute_elapsed + compute_time,
                        event.transport_elapsed + edge.delay,
                        event.hops + 1,
                    ),
                )

        return received

"""Reproducible first Saturday machine.

The experiment separates:
1. fast complex wave state,
2. relaxing MASS that changes local execution time,
3. persistent LATCH configuration that selects a route,
4. competitive ROUTE coupling under a fixed budget.

Transport delay, execution delay, and coupling are reported separately.
"""

from __future__ import annotations

from typing import Dict, Any

from .material import Cell, Kind, Medium


def build_medium() -> Medium:
    medium = Medium()

    medium.add_cell(
        "source",
        Cell(Kind.PASS, alpha=0.30, base_compute=0.20, direct=0.90, readout=0.10),
    )
    medium.add_cell(
        "mass",
        Cell(
            Kind.MASS,
            alpha=0.10,
            tau_mass=25.0,
            kappa=3.0,
            mass_write=0.80,
            base_compute=0.50,
        ),
    )
    medium.add_cell(
        "rotate",
        Cell(
            Kind.ROTATE,
            alpha=0.04,
            omega=0.50,
            tau_mass=20.0,
            kappa=1.0,
            mass_write=0.05,
            base_compute=0.40,
        ),
    )
    medium.add_cell(
        "latch",
        Cell(
            Kind.LATCH,
            alpha=0.08,
            latch_threshold=0.60,
            tau_mass=50.0,
            kappa=0.50,
            mass_write=0.02,
            base_compute=0.30,
        ),
    )
    medium.add_cell("out_pos", Cell(Kind.PASS), receiver=True)
    medium.add_cell("out_neg", Cell(Kind.PASS), receiver=True)

    for src, dst in (
        ("source", "mass"),
        ("mass", "rotate"),
        ("rotate", "latch"),
    ):
        medium.connect(src, dst, delay=0.50, coupling=0.80)

    # LATCH is configuration, not a gain: it selects which route exists.
    # The two alternatives share a fixed coupling budget and compete by use.
    medium.connect(
        "latch",
        "out_pos",
        delay=0.50,
        coupling=0.40,
        plasticity=0.10,
        required_latch=1,
    )
    medium.connect(
        "latch",
        "out_neg",
        delay=0.50,
        coupling=0.40,
        plasticity=0.10,
        required_latch=-1,
    )

    return medium


def _single_probe(medium: Medium, t: float, amplitude: float = 0.30) -> Dict[str, Any]:
    arrivals = medium.run([(t, "source", complex(amplitude, 0.0))])
    if len(arrivals) != 1:
        raise RuntimeError(f"expected one receiver arrival, got {len(arrivals)}")
    obs = arrivals[0]
    return {
        "injected_at": t,
        "arrival_at": obs.time,
        "receiver": obs.node,
        "delay": obs.total_delay,
        "compute_delay": obs.compute_time,
        "transport_delay": obs.transport_time,
        "amplitude": abs(obs.amp),
        "phase": __import__("cmath").phase(obs.amp),
    }


def run_story() -> Dict[str, Any]:
    """Run baseline -> conditioning -> immediate probe -> long-silence probe."""
    medium = build_medium()

    baseline = _single_probe(medium, 0.0)

    # Strong positive waves flip the latch and repeatedly use the + route.
    conditioning = [(10.0 + 2.0 * i, "source", 2.5 + 0j) for i in range(6)]
    conditioning_obs = medium.run(conditioning)
    conditioning_end = max(obs.time for obs in conditioning_obs)

    # Bring slow state to one shared measurement time before reading it.
    for name in ("source", "mass", "rotate", "latch"):
        medium.cells[name].materialize(conditioning_end)

    after_conditioning = {
        "at": conditioning_end,
        "mass": medium.cells["mass"].mass,
        "mass_gamma": medium.cells["mass"].gamma,
        "latch": medium.cells["latch"].latch,
        "route_couplings": {
            f"{src}->{dst}": edge.coupling
            for (src, dst), edge in medium.edges.items()
        },
    }

    immediate_t = conditioning_end + 1.0
    immediate = _single_probe(medium, immediate_t)

    before_silence_counts = {
        name: cell.materializations for name, cell in medium.cells.items()
    }

    late_t = immediate["arrival_at"] + 175.0
    late = _single_probe(medium, late_t)

    after_silence_counts = {
        name: cell.materializations for name, cell in medium.cells.items()
    }

    medium.cells["mass"].materialize(late["arrival_at"])

    final = {
        "at": late["arrival_at"],
        "mass": medium.cells["mass"].mass,
        "mass_gamma": medium.cells["mass"].gamma,
        "latch": medium.cells["latch"].latch,
        "route_couplings": {
            f"{src}->{dst}": edge.coupling
            for (src, dst), edge in medium.edges.items()
        },
    }

    return {
        "baseline": baseline,
        "after_conditioning": after_conditioning,
        "immediate_probe": immediate,
        "late_probe": late,
        "materializations_before_late_probe": before_silence_counts,
        "materializations_after_late_probe": after_silence_counts,
        "final": final,
    }

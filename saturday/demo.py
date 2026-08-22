"""Reproducible first Saturday machine.

The experiment separates three timescales:

1. fast complex wave state,
2. relaxing local MASS / persistent LATCH state,
3. slow ROUTE coupling changed by repeated traffic.

A weak probe is measured before conditioning, immediately after a train of
strong waves, and again after a long silent interval.
"""

from __future__ import annotations

from typing import Dict, Any

from .material import Cell, Kind, Medium


def build_medium() -> Medium:
    medium = Medium()

    medium.add_cell(
        "source",
        Cell(Kind.PASS, alpha=0.30, base_dwell=0.20, direct=0.90, readout=0.10),
    )
    medium.add_cell(
        "mass",
        Cell(
            Kind.MASS,
            alpha=0.10,
            tau_mass=25.0,
            kappa=3.0,
            mass_write=0.80,
            base_dwell=0.50,
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
            base_dwell=0.40,
        ),
    )
    medium.add_cell(
        "latch",
        Cell(
            Kind.LATCH,
            alpha=0.08,
            latch_threshold=0.80,
            tau_mass=50.0,
            kappa=0.50,
            mass_write=0.02,
            base_dwell=0.30,
        ),
    )
    medium.add_cell("out", Cell(Kind.PASS), receiver=True)

    for src, dst in (
        ("source", "mass"),
        ("mass", "rotate"),
        ("rotate", "latch"),
        ("latch", "out"),
    ):
        medium.connect(
            src,
            dst,
            delay=0.50,
            coupling=0.80,
            plasticity=0.02,
            max_coupling=0.98,
        )

    return medium


def _single_probe(medium: Medium, t: float, amplitude: float = 0.30) -> Dict[str, Any]:
    arrivals = medium.run([(t, "source", complex(amplitude, 0.0))])
    if len(arrivals) != 1:
        raise RuntimeError(f"expected one receiver arrival, got {len(arrivals)}")
    arrival_t, _, wave = arrivals[0]
    return {
        "injected_at": t,
        "arrival_at": arrival_t,
        "delay": arrival_t - t,
        "amplitude": abs(wave),
        "phase": __import__("cmath").phase(wave),
    }


def run_story() -> Dict[str, Any]:
    """Run baseline -> conditioning -> immediate probe -> long-silence probe."""
    medium = build_medium()

    baseline = _single_probe(medium, 0.0)

    # A short history writes all three slower forms:
    # MASS residue, LATCH state, and use-dependent ROUTE coupling.
    conditioning = [(10.0 + 2.0 * i, "source", 2.5 + 0j) for i in range(6)]
    medium.run(conditioning)

    after_conditioning = {
        "mass": medium.cells["mass"].mass,
        "mass_gamma": medium.cells["mass"].gamma,
        "latch": medium.cells["latch"].latch,
        "route_couplings": {
            f"{src}->{dst}": edge.coupling
            for (src, dst), edge in medium.edges.items()
        },
    }

    immediate = _single_probe(medium, 25.0)

    # Nothing is ticked between t=25 and t=200.  The next event causes each
    # touched cell to analytically materialize its quiet interval.
    before_silence_counts = {
        name: cell.materializations for name, cell in medium.cells.items()
    }
    late = _single_probe(medium, 200.0)
    after_silence_counts = {
        name: cell.materializations for name, cell in medium.cells.items()
    }

    final = {
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

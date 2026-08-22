from __future__ import annotations

from pprint import pprint

from saturday.demo import run_story


def _probe_line(label: str, p: dict) -> str:
    return (
        f"{label:<15}: receiver={p['receiver']:<7} "
        f"total={p['delay']:.4f}  compute={p['compute_delay']:.4f}  "
        f"transport={p['transport_delay']:.4f}  |y|={p['amplitude']:.6f}  "
        f"phase={p['phase']:+.4f}"
    )


def main() -> None:
    result = run_story()

    print("SATURDAY — FIRST HETEROGENEOUS MATERIAL")
    print("waves modify matter -> matter modifies future waves -> repeated waves modify structure")
    print()

    b = result["baseline"]
    i = result["immediate_probe"]
    l = result["late_probe"]
    c = result["after_conditioning"]
    f = result["final"]

    print(_probe_line("baseline probe", b))
    print(f"after train    : MASS={c['mass']:.4f}  gamma={c['mass_gamma']:.5f}  LATCH={c['latch']:+d}")
    print(_probe_line("immediate probe", i))
    print(_probe_line("late probe", l))
    print(f"after silence  : MASS={f['mass']:.4f}  gamma={f['mass_gamma']:.5f}  LATCH={f['latch']:+d}")
    print()

    print("route couplings after conditioning:")
    pprint(c["route_couplings"])
    print("route couplings after late probe:")
    pprint(f["route_couplings"])
    print()

    print("materialization counts before and after the late probe:")
    print("  no events were executed during the silent interval itself")
    pprint({
        "before": result["materializations_before_late_probe"],
        "after": result["materializations_after_late_probe"],
    })


if __name__ == "__main__":
    main()

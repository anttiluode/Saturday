from __future__ import annotations

from pprint import pprint

from saturday.demo import run_story


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

    print(f"baseline probe : delay={b['delay']:.4f}  |y|={b['amplitude']:.6f}  phase={b['phase']:+.4f}")
    print(f"after train    : MASS={c['mass']:.4f}  gamma={c['mass_gamma']:.5f}  LATCH={c['latch']:+d}")
    print(f"immediate probe: delay={i['delay']:.4f}  |y|={i['amplitude']:.6f}  phase={i['phase']:+.4f}")
    print(f"late probe     : delay={l['delay']:.4f}  |y|={l['amplitude']:.6f}  phase={l['phase']:+.4f}")
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

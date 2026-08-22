import math
import unittest

from saturday.demo import run_story
from saturday.material import Cell, Kind, Medium


class MaterialTests(unittest.TestCase):
    def test_lazy_materialization_matches_small_steps(self):
        one_jump = Cell(Kind.MASS, alpha=0.13, tau_mass=17.0, kappa=2.5)
        small_steps = Cell(Kind.MASS, alpha=0.13, tau_mass=17.0, kappa=2.5)
        for cell in (one_jump, small_steps):
            cell.z = 1.25 - 0.4j
            cell.mass = 2.1

        one_jump.materialize(40.0)
        for t in range(1, 41):
            small_steps.materialize(float(t))

        self.assertAlmostEqual(one_jump.mass, small_steps.mass, places=12)
        self.assertAlmostEqual(one_jump.z.real, small_steps.z.real, places=12)
        self.assertAlmostEqual(one_jump.z.imag, small_steps.z.imag, places=12)
        self.assertEqual(one_jump.materializations, 1)
        self.assertEqual(small_steps.materializations, 40)

    def test_rotate_means_complex_conjugate_pole_pair(self):
        cell = Cell(
            Kind.ROTATE,
            alpha=0.0,
            omega=math.pi / 2.0,
            tau_mass=10.0,
            kappa=0.0,
        )
        cell.z = 1.0 + 0j
        cell.materialize(1.0)
        self.assertAlmostEqual(cell.z.real, 0.0, places=12)
        self.assertAlmostEqual(cell.z.imag, 1.0, places=12)

    def test_clock_transport_and_amplitude_are_separate(self):
        medium = Medium()
        mass = Cell(
            Kind.MASS,
            kappa=1.0,
            mass_write=0.0,
            base_compute=2.0,
            direct=1.0,
            readout=0.0,
        )
        mass.mass = 1.0  # gamma = 0.5
        medium.add_cell("mass", mass)
        medium.add_cell("out", Cell(Kind.PASS), receiver=True)
        medium.connect("mass", "out", delay=3.0, coupling=1.0)

        obs = medium.run([(0.0, "mass", 1.0 + 0j)])[0]
        self.assertAlmostEqual(obs.compute_time, 4.0)
        self.assertAlmostEqual(obs.transport_time, 3.0)
        self.assertAlmostEqual(obs.total_delay, 7.0)
        self.assertAlmostEqual(abs(obs.amp), 1.0)

    def test_latch_is_persistent_configuration_that_selects_route(self):
        medium = Medium()
        medium.add_cell(
            "switch",
            Cell(
                Kind.LATCH,
                latch_threshold=0.5,
                base_compute=0.0,
                direct=1.0,
                readout=0.0,
            ),
        )
        medium.add_cell("pos", Cell(Kind.PASS), receiver=True)
        medium.add_cell("neg", Cell(Kind.PASS), receiver=True)
        medium.connect("switch", "pos", delay=0.0, coupling=1.0, required_latch=1)
        medium.connect("switch", "neg", delay=0.0, coupling=1.0, required_latch=-1)

        before = medium.run([(0.0, "switch", 0.1 + 0j)])[0]
        self.assertEqual(before.node, "neg")

        medium.run([(1.0, "switch", 1.0 + 0j)])
        medium.cells["switch"].materialize(1_000.0)
        self.assertEqual(medium.cells["switch"].latch, 1)

        after = medium.run([(1_001.0, "switch", 0.1 + 0j)])[0]
        self.assertEqual(after.node, "pos")

    def test_route_plasticity_competes_under_fixed_budget(self):
        medium = Medium()
        medium.add_cell(
            "a",
            Cell(Kind.PASS, base_compute=0.0, direct=1.0, readout=0.0),
        )
        medium.add_cell("b", Cell(Kind.PASS), receiver=True)
        medium.add_cell("c", Cell(Kind.PASS), receiver=True)
        medium.connect(
            "a", "b", delay=0.0, coupling=0.4, plasticity=0.2, required_latch=1
        )
        medium.connect(
            "a", "c", delay=0.0, coupling=0.4, plasticity=0.2, required_latch=-1
        )

        medium.cells["a"].latch = 1
        initial_budget = sum(e.coupling for e in medium.edges.values())
        for t in range(8):
            medium.run([(float(t), "a", 1.0 + 0j)])

        used = medium.edges[("a", "b")].coupling
        unused = medium.edges[("a", "c")].coupling
        self.assertGreater(used, 0.4)
        self.assertLess(unused, 0.4)
        self.assertAlmostEqual(used + unused, initial_budget, places=12)

    def test_receiver_can_live_inside_causal_loop(self):
        medium = Medium()
        medium.add_cell(
            "a", Cell(Kind.PASS, base_compute=0.0, direct=1.0, readout=0.0)
        )
        medium.add_cell(
            "r",
            Cell(Kind.PASS, base_compute=0.0, direct=1.0, readout=0.0),
            receiver=True,
            absorb=False,
        )
        medium.connect("a", "r", delay=1.0, coupling=1.0)
        medium.connect("r", "a", delay=1.0, coupling=1.0)

        obs = medium.run([(0.0, "a", 1.0 + 0j)], until=5.0)
        self.assertEqual([o.time for o in obs], [1.0, 3.0, 5.0])

    def test_first_machine_separates_relaxing_and_persistent_history(self):
        result = run_story()
        baseline = result["baseline"]
        immediate = result["immediate_probe"]
        late = result["late_probe"]
        conditioned = result["after_conditioning"]
        final = result["final"]

        self.assertLess(conditioned["mass_gamma"], 0.2)
        self.assertGreater(immediate["compute_delay"], baseline["compute_delay"] * 3.0)
        self.assertAlmostEqual(
            immediate["transport_delay"], baseline["transport_delay"], places=12
        )

        self.assertGreater(final["mass_gamma"], conditioned["mass_gamma"])
        self.assertLess(late["compute_delay"], immediate["compute_delay"])

        self.assertEqual(baseline["receiver"], "out_neg")
        self.assertEqual(immediate["receiver"], "out_pos")
        self.assertEqual(late["receiver"], "out_pos")
        self.assertEqual(conditioned["latch"], 1)
        self.assertEqual(final["latch"], 1)

        couplings = final["route_couplings"]
        self.assertGreater(couplings["latch->out_pos"], couplings["latch->out_neg"])
        self.assertAlmostEqual(
            couplings["latch->out_pos"] + couplings["latch->out_neg"],
            0.8,
            places=12,
        )


if __name__ == "__main__":
    unittest.main()

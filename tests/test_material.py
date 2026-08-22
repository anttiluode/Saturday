import math
import unittest

from saturday.demo import run_story
from saturday.material import Cell, Edge, Kind


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

    def test_rotate_is_a_distinct_local_dynamics(self):
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

    def test_latch_survives_silence(self):
        cell = Cell(Kind.LATCH, latch_threshold=0.5, alpha=0.2)
        cell.process(1.0 + 0j, 0.0)
        self.assertEqual(cell.latch, 1)
        cell.materialize(1_000.0)
        self.assertEqual(cell.latch, 1)

    def test_route_is_changed_by_repeated_waves(self):
        edge = Edge("a", "b", coupling=0.5, plasticity=0.1, max_coupling=0.9)
        for t in range(8):
            edge.transmit(1.0 + 0j, float(t))
        self.assertGreater(edge.coupling, 0.5)
        self.assertLessEqual(edge.coupling, 0.9)

    def test_first_machine_separates_relaxing_and_persistent_history(self):
        result = run_story()
        baseline = result["baseline"]
        immediate = result["immediate_probe"]
        late = result["late_probe"]
        conditioned = result["after_conditioning"]
        final = result["final"]

        # Conditioning creates a temporary slow region.
        self.assertLess(conditioned["mass_gamma"], 0.1)
        self.assertGreater(immediate["delay"], baseline["delay"] * 5.0)

        # MASS relaxes, so a much later probe speeds up again.
        self.assertGreater(final["mass_gamma"], conditioned["mass_gamma"])
        self.assertLess(late["delay"], immediate["delay"])

        # LATCH and structural route changes outlive the MASS transient.
        self.assertEqual(conditioned["latch"], 1)
        self.assertEqual(final["latch"], 1)
        for coupling in final["route_couplings"].values():
            self.assertGreater(coupling, 0.8)


if __name__ == "__main__":
    unittest.main()

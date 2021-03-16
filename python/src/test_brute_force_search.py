import unittest

from src.netlist import Netlist, BaseNetlistFile
from src.brute_force_search import BruteForceCandidateGenerator
from src.circuit_search_common import Range, Param
from tests.mock_file import MockFile
from tests.test_netlist import TEST_NETLIST


class TestBruteForceSearch(unittest.TestCase):

    def setUp(self):
        self.ref_netlist_file = MockFile()
        self.ref_netlist_file.write(TEST_NETLIST)
        self.ref_netlist = Netlist.create(BaseNetlistFile(self.ref_netlist_file))

    def test_single_candidate_generator(self):
        for simulations_per_iterations in [1, 10]:
            candidate_generator = BruteForceCandidateGenerator.create(
                reference_netlist=self.ref_netlist,
                width_range=Range(Param.WIDTH, 120e-9, 120e-9, 5e-9),
                length_range=Range(Param.LENGTH, 45e-9, 45e-9, 5e-9),
                fingers_range=Range(Param.FINGERS, 1, 1, 1),
                simulations_per_iteration=simulations_per_iterations
            )

            initial_population = candidate_generator.get_initial_population()
            self.assertEqual(len(initial_population), 1)
            self.assertEqual(
                initial_population[0],
                self.ref_netlist.mutate("INVX1_3_0", (120e-9, 120e-9), (45e-9, 45e-9), (1, 1))
            )
            self.assertEqual(len(candidate_generator.get_next_population(tuple(), dict())), 0)

    def test_width_only(self):
        candidate_generator = BruteForceCandidateGenerator.create(
            reference_netlist=self.ref_netlist,
            width_range=Range(Param.WIDTH, 120e-9, 125e-9, 5e-9),
            length_range=Range(Param.LENGTH, 45e-9, 45e-9, 5e-9),
            fingers_range=Range(Param.FINGERS, 1, 1, 1),
            simulations_per_iteration=2
        )

        initial_population = candidate_generator.get_initial_population()
        self.assertEqual(len(initial_population), 2)

        all_candidates = []
        all_candidates.extend(initial_population)

        def next_population_func():
            p = candidate_generator.get_next_population(tuple(), dict())
            if len(p) == 0:
                raise StopIteration
            return p

        for next_population in iter(next_population_func, []):
            self.assertEqual(len(next_population), 2)
            all_candidates.extend(next_population)

        expected_candidates = [
            self.ref_netlist.mutate("INVX1_3_0", (120e-9, 120e-9), (45e-9, 45e-9), (1, 1)),
            self.ref_netlist.mutate("INVX1_3_1", (125e-9, 120e-9), (45e-9, 45e-9), (1, 1)),
            self.ref_netlist.mutate("INVX1_3_0", (120e-9, 125e-9), (45e-9, 45e-9), (1, 1)),
            self.ref_netlist.mutate("INVX1_3_1", (125e-9, 125e-9), (45e-9, 45e-9), (1, 1)),
        ]
        self.assertListEqual(all_candidates, expected_candidates)

    def test_length_only(self):
        candidate_generator = BruteForceCandidateGenerator.create(
            reference_netlist=self.ref_netlist,
            width_range=Range(Param.WIDTH, 120e-9, 120e-9, 5e-9),
            length_range=Range(Param.LENGTH, 45e-9, 50e-9, 5e-9),
            fingers_range=Range(Param.FINGERS, 1, 1, 1),
            simulations_per_iteration=2
        )

        initial_population = candidate_generator.get_initial_population()
        self.assertEqual(len(initial_population), 2)

        all_candidates = []
        all_candidates.extend(initial_population)

        def next_population_func():
            p = candidate_generator.get_next_population(tuple(), dict())
            if len(p) == 0:
                raise StopIteration
            return p

        for next_population in iter(next_population_func, []):
            self.assertEqual(len(next_population), 2)
            all_candidates.extend(next_population)

        expected_candidates = [
            self.ref_netlist.mutate("INVX1_3_0", (120e-9, 120e-9), (45e-9, 45e-9), (1, 1)),
            self.ref_netlist.mutate("INVX1_3_1", (120e-9, 120e-9), (50e-9, 45e-9), (1, 1)),
            self.ref_netlist.mutate("INVX1_3_0", (120e-9, 120e-9), (45e-9, 50e-9), (1, 1)),
            self.ref_netlist.mutate("INVX1_3_1", (120e-9, 120e-9), (50e-9, 50e-9), (1, 1)),
        ]
        self.assertListEqual(all_candidates, expected_candidates)

    def test_fingers_only(self):
        candidate_generator = BruteForceCandidateGenerator.create(
            reference_netlist=self.ref_netlist,
            width_range=Range(Param.WIDTH, 120e-9, 120e-9, 5e-9),
            length_range=Range(Param.LENGTH, 45e-9, 45e-9, 5e-9),
            fingers_range=Range(Param.FINGERS, 1, 2, 1),
            simulations_per_iteration=2
        )

        initial_population = candidate_generator.get_initial_population()
        self.assertEqual(len(initial_population), 2)

        all_candidates = []
        all_candidates.extend(initial_population)

        def next_population_func():
            p = candidate_generator.get_next_population(tuple(), dict())
            if len(p) == 0:
                raise StopIteration
            return p

        for next_population in iter(next_population_func, []):
            self.assertEqual(len(next_population), 2)
            all_candidates.extend(next_population)

        expected_candidates = [
            self.ref_netlist.mutate("INVX1_3_0", (120e-9, 120e-9), (45e-9, 45e-9), (1, 1)),
            self.ref_netlist.mutate("INVX1_3_1", (120e-9, 120e-9), (45e-9, 45e-9), (2, 1)),
            self.ref_netlist.mutate("INVX1_3_0", (120e-9, 120e-9), (45e-9, 45e-9), (1, 2)),
            self.ref_netlist.mutate("INVX1_3_1", (120e-9, 120e-9), (45e-9, 45e-9), (2, 2)),
        ]
        self.assertListEqual(all_candidates, expected_candidates)

    def test_all_params(self):
        candidate_generator = BruteForceCandidateGenerator.create(
            reference_netlist=self.ref_netlist,
            width_range=Range(Param.WIDTH, 120e-9, 125e-9, 5e-9),
            length_range=Range(Param.LENGTH, 45e-9, 50e-9, 5e-9),
            fingers_range=Range(Param.FINGERS, 1, 2, 1),
            simulations_per_iteration=2
        )

        initial_population = candidate_generator.get_initial_population()
        self.assertEqual(len(initial_population), 2)

        all_candidates = []
        all_candidates.extend(initial_population)

        def next_population_func():
            p = candidate_generator.get_next_population(tuple(), dict())
            if len(p) == 0:
                raise StopIteration
            return p

        for next_population in iter(next_population_func, []):
            self.assertEqual(len(next_population), 2)
            all_candidates.extend(next_population)

        # Too many combinations to test, so check a few key indices and make sure there are no duplicates
        self.assertEqual(
            all_candidates[0],
            self.ref_netlist.mutate("INVX1_3_0", (120e-9, 120e-9), (45e-9, 45e-9), (1, 1))
        )
        self.assertEqual(
            all_candidates[31],
            self.ref_netlist.mutate("INVX1_3_1", (125e-9, 125e-9), (50e-9, 50e-9), (2, 1))
        )
        self.assertEqual(
            all_candidates[-1],
            self.ref_netlist.mutate("INVX1_3_1", (125e-9, 125e-9), (50e-9, 50e-9), (2, 2))
        )
        self.assertEqual(len(all_candidates), 64)
        self.assertEqual(len(set(all_candidates)), 64)

import unittest
from decimal import Decimal

from src.circuit_search_common import Range, Param
from src.netlist import Netlist, BaseNetlistFile
from src.genetic_search import GeneticCandidateGenerator
from src.file_io import MockFile
from tests.test_netlist import TEST_NETLIST


class TestGeneticSearch(unittest.TestCase):
    def setUp(self):
        self.ref_netlist_file = MockFile()
        self.ref_netlist_file.write(TEST_NETLIST)
        self.ref_netlist = Netlist.create(BaseNetlistFile.create(self.ref_netlist_file))

        self.candidate_generator = GeneticCandidateGenerator.create(
            num_individuals=100,
            elitism=True,
            npoints=2,
            alpha=0.6,
            pmutation=0.25,
            mutation_std_deviation=5.0,
            width_range=Range(Param.WIDTH, Decimal('120e-9'), Decimal('10e-6'), Decimal('5e-9')),
            length_range=Range(Param.LENGTH, Decimal('45e-9'), Decimal('45e-9'), Decimal('5e-9')),
            fingers_range=Range(Param.FINGERS, 1, 2, 1),
            reference_netlist=self.ref_netlist,
            seed=1234,
        )

    def test_genetic_candidate_generator(self):
        # pylint: disable=protected-access

        # Test computed members
        self.assertEqual(len(self.candidate_generator._range_info.widths), 1977)
        self.assertEqual(len(self.candidate_generator._range_info.lengths), 1)
        self.assertEqual(len(self.candidate_generator._range_info.fingers), 2)
        self.assertEqual(self.candidate_generator._search_params, {Param.WIDTH, Param.FINGERS})
        self.assertEqual(self.candidate_generator._ndevices, 2)
        self.assertEqual(self.candidate_generator._id_num_digits, 2)

        initial_population = self.candidate_generator.get_initial_population()
        self.assertEqual(len(initial_population), 100)

        self.assertTrue(
            all(
                120e-9 <= width <= 10e-6
                for candidate in initial_population
                for width in candidate.device_widths
            )
        )
        self.assertTrue(
            all(
                45e-9 <= length <= 45e-9
                for candidate in initial_population
                for length in candidate.device_lengths
            )
        )
        self.assertTrue(
            all(
                1 <= finger <= 2
                for candidate in initial_population
                for finger in candidate.device_fingers
            )
        )

        cost_map = {candidate.key(): idx + 1 for idx, candidate in enumerate(initial_population)}
        next_population = self.candidate_generator.get_next_population(initial_population, cost_map)
        self.assertEqual(len(next_population), 100)
        self.assertEqual(len(set(next_population)), 100)  # no duplicates

        # Test elitism
        self.assertIn(initial_population[0], next_population)

        self.assertTrue(
            all(
                120e-9 <= width <= 10e-6
                for candidate in next_population
                for width in candidate.device_widths
            )
        )
        self.assertTrue(
            all(
                45e-9 <= length <= 45e-9
                for candidate in next_population
                for length in candidate.device_lengths
            )
        )
        self.assertTrue(
            all(
                1 <= finger <= 2
                for candidate in next_population
                for finger in candidate.device_fingers
            )
        )

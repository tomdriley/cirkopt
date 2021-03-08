import unittest

from src.netlist import Netlist, BaseNetlistFile
from src.genetic_search import GeneticCandidateGenerator
from tests.mock_file import MockFile

TEST_NETLIST = """
** Library name: gsclib045
** Cell name: INVX1
** View name: schematic
.subckt INVX1 A Y VDD VSS
*.PININFO  VSS:I VDD:I A:I Y:O
** Above line required by Conformal LEC - DO NOT DELETE

mp0 Y A VDD VDD g45p1svt L=45e-9 W=90e-9 AD=54.6e-15 AS=54.6e-15 PD=1.06e-6 PS=1.06e-6 NRD=358.974e-3 NRS=358.974e-3 M=1
mn0 Y A VSS VSS g45n1svt L=45e-9 W=90e-9 AD=36.4e-15 AS=36.4e-15 PD=800e-9 PS=800e-9 NRD=538.462e-3 NRS=538.462e-3 M=2
.ends INVX1
"""


class TestGeneticSearch(unittest.TestCase):

    def setUp(self):
        self.ref_netlist_file = MockFile()
        self.ref_netlist_file.write(TEST_NETLIST)
        self.ref_netlist = Netlist.create(BaseNetlistFile(self.ref_netlist_file))

        def netlist_persister(netlist: Netlist):
            netlist.persist(MockFile())

        self.candidate_generator = GeneticCandidateGenerator.create(
            num_individuals=100,
            elitism=True,
            npoints=2,
            alpha=0.5,
            pmutation=0.25,
            mutation_std_deviation=1.0,
            min_width=45e-9,
            max_width=300e-9,
            min_length=45e-9,
            max_length=300e-9,
            min_fingers=1,
            max_fingers=3,
            precision=5e-9,
            reference_netlist=self.ref_netlist,
            netlist_persister=netlist_persister,
            seed=1234
        )

    def test_genetic_candidate_generator(self):
        # pylint: disable=protected-access

        # Test computed members
        self.assertEqual(self.candidate_generator._bounds.max_width, 60)
        self.assertEqual(self.candidate_generator._bounds.max_length, 60)
        self.assertEqual(self.candidate_generator._bounds.min_width, 9)
        self.assertEqual(self.candidate_generator._bounds.min_length, 9)
        self.assertEqual(self.candidate_generator._number_of_devices, 2)
        self.assertEqual(self.candidate_generator._id_num_digits, 2)

        initial_population = self.candidate_generator.get_initial_population()
        self.assertEqual(len(initial_population), 100)

        self.assertTrue(
            all(45e-9 <= width <= 300e-9 for candidate in initial_population for width in candidate.device_widths)
        )
        self.assertTrue(
            all(45e-9 <= length <= 300e-9 for candidate in initial_population for length in candidate.device_lengths)
        )
        self.assertTrue(
            all(1 <= finger <= 3 for candidate in initial_population for finger in candidate.device_fingers)
        )

        cost_map = {candidate.key(): idx + 1 for idx, candidate in enumerate(initial_population)}
        next_population = self.candidate_generator.get_next_population(initial_population, cost_map)
        self.assertEqual(len(next_population), 100)
        self.assertEqual(len(set(next_population)), 100)  # no duplicates

        # Test elitism
        self.assertEqual(initial_population[0], next_population[0])

        self.assertTrue(
            all(45e-9 <= width <= 300e-9 for candidate in next_population for width in candidate.device_widths)
        )
        self.assertTrue(
            all(45e-9 <= length <= 300e-9 for candidate in next_population for length in candidate.device_lengths)
        )
        self.assertTrue(
            all(1 <= finger <= 3 for candidate in next_population for finger in candidate.device_fingers)
        )

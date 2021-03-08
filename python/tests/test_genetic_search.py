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
        self.ref_netlist = Netlist(BaseNetlistFile(self.ref_netlist_file))

        def netlist_persister(netlist: Netlist):
            netlist.persist(MockFile())

        self.candidate_generator = GeneticCandidateGenerator.create(
            num_individuals=10,
            elitism=True,
            npoints=2,
            alpha=0.5,
            pmutation=0.25,
            mutation_std_deviation=1.0,
            min_width=45e-9,
            max_width=300e-9,
            min_length=45e-9,
            max_length=300e-9,
            precision=5e-9,
            fingers_values=(1, 2, 3),
            reference_netlist=self.ref_netlist,
            netlist_persister=netlist_persister,
            seed=1234
        )

    def test_genetic_candidate_generator(self):
        # pylint: disable=protected-access
        self.assertEqual(self.candidate_generator._max_width, 60)

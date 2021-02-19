import os.path

from src.file_io import File
from src.liberty_parser import LibertyParser
from src.liberate_grapher import graph_cell_delay
from src.netlist import BaseNetlistFile, Netlist
from src.single_param_sweep import NoopCostFunction, Param, \
    ParamSweepCandidateGenerator, SingleParamSweep


def main():
    # # TODO: use command line args instead of hard coding
    curr_path = os.path.abspath(os.path.dirname(__file__))
    sim_result_path = os.path.join(curr_path, "../../liberate/{}/{}.ldb")
    sim_file = File(sim_result_path)


    reference_netlist_name = "INVX1"
    reference_netlist_path = os.path.join(
        curr_path,
        f"../../liberate/netlist_wrk/{reference_netlist_name}.sp"
    )
    reference_netlist_file = File(reference_netlist_path)
    base_netlist_file = BaseNetlistFile(reference_netlist_file)
    reference_netlist = Netlist(base_netlist_file)

    def persist_netlist_in_run_dir(netlist: Netlist):
        path = os.path.join(curr_path, f"../../liberate/netlist_test/{netlist.cell_name}.sp")
        netlist_file = File(path)
        netlist.persist(netlist_file)

    widths = [i * 100e-9 for i in range(2, 11)]

    # TODO: add some mechanism to parametrize new W/L/M values via command line
    candidate_generator = ParamSweepCandidateGenerator(
        reference_netlist=reference_netlist,
        netlist_persister=persist_netlist_in_run_dir,
        param=Param.WIDTH,
        values=widths
    )
    cost_function = NoopCostFunction()
    liberty_parser = LibertyParser()
    single_param_sweep = SingleParamSweep(
        cost_function,
        candidate_generator,
        liberty_parser,
        sim_file
    )
    # single_param_sweep.search()

    # Graph the results of simulation
    graph_cell_delay(
        sim_file=sim_file,
        pin="Y",
        delay_index=(0, 1),
        x_axis=widths,
        x_axis_title="Width",
        out_path="out/sweep-width.png"
    )


if __name__ == '__main__':
    main()

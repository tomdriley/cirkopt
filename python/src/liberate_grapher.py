from typing import Sequence, Tuple

import matplotlib.pyplot as plt

from src.file_io import IFile
from src.liberty_parser import LibertyParser
from src.utils import single


def graph_cell_delay(
        sim_file: IFile,
        pin: str,
        delay_index: Tuple[int, int],
        x_axis: Sequence[float],
        x_axis_title: str,
        out_path: str
) -> None:
    liberty_parser = LibertyParser()
    library = liberty_parser.parse(sim_file)

    di1, di2 = delay_index
    rise_times = [
        single(lambda p: p.name == pin, cell.pin).timing[0].cell_rise[0].values[di1][di2]
        for cell in library.cell
    ]
    fall_times = [
        single(lambda p: p.name == pin, cell.pin).timing[0].cell_fall[0].values[di1][di2]
        for cell in library.cell
    ]

    assert len({len(rise_times), len(fall_times), len(x_axis)}) == 1

    plt.figure()
    plt.title(f"{x_axis_title} vs Rise and Fall time")
    plt.plot(x_axis, rise_times, 'b')
    plt.plot(x_axis, fall_times, 'g')
    plt.legend(['cell rise', 'cell fall'])
    plt.ylabel('Delay')
    plt.xlabel(x_axis_title)
    plt.tight_layout()
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.savefig(out_path)

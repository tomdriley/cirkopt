import math

import matplotlib.pyplot as plt
import numpy as np
from control.matlab import feedback, series, stepinfo, step, tf


def Q2_perfFCN(Kp, Ti, Td, show_plot=False):
    G = Kp * tf([Ti * Td, Ti, 1], [Ti, 0])
    F = tf(1, [1, 6, 11, 6, 0])

    sys = feedback(series(G, F), 1)
    sysinf = stepinfo(sys)

    t = np.arange(start=0.0, stop=100.0, step=0.01)
    y, T = step(sys, t)

    if show_plot:
        plt.figure()
        plt.title(f"Step Response for Kp={Kp}, Ti={Ti}, Td={Td}")
        plt.plot(T, y, 'b')
        plt.xlabel('Time')
        plt.ylabel('Magnitude')
        plt.tight_layout()
        ax = plt.gca()
        ax.set_axisbelow(True)
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
        plt.savefig(f"out/step_response_{round(Kp * 100)}_{round(Ti * 100)}_{round(Td * 100)}.png")

    ones = np.ones_like(y)
    ISE = np.sum((y - ones) ** 2)
    Tr = sysinf['RiseTime']
    Ts = sysinf['SettlingTime']
    Mp = sysinf['Overshoot']

    assert (not math.isnan(ISE))
    assert (not math.isnan(Tr))
    assert (not math.isnan(Ts))
    assert (not math.isnan(Mp))

    return ISE, Tr, Ts, Mp

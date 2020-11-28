import argparse
import random

import matplotlib.pyplot as plt
import numpy as np
from a3_q2_aco import optimize


def main(settings):
    simstats = {}
    for nants, qpersistence, p0, online in settings:
        print("\n")
        # Make results comparable
        random.seed(123456789)
        np.random.seed(123456789)

        stats = list(optimize(Q=100, nants=nants, maxitr=400, qpersistence=qpersistence, p0=p0, online=online))
        print("\n---------------------------Results---------------------------")

        best_distance_per_iteration = [best for _, best, _ in stats]
        best_per_iteration = [best for _, _, best in stats]

        print(f"\nLast solution:\n\t{best_per_iteration[-1]} -> {best_distance_per_iteration[-1]}")
        legend = f'{nants}-{qpersistence}-{p0}-{online}'
        simstats[legend] = best_distance_per_iteration

    plt.figure()
    plt.title("Distance vs Iteration")
    colours = ['b', 'g', 'r', 'c', 'm']
    legend = []
    for idx, key in enumerate(simstats.keys()):
        best_distance_per_iteration = simstats[key]
        legend.append(key)
        plt.plot(best_distance_per_iteration, colours[idx % len(colours)])

    plt.legend(legend)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.tight_layout()
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.savefig("out/distance_vs_iteration.png")


def str2bool(s):
    if s in ['true', 'True', 't', 'T']:
        return True
    else:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run ACO Algorithm and plot Distance vs Iteration.')
    parser.add_argument('--nants', type=int, nargs='+', help='Ant population sizes for each simulation')
    parser.add_argument('--qpersistence', type=float, nargs='+',
                        help='Pheromone Persistence Constant for each simulation')
    parser.add_argument('--p0', type=float, nargs='+', help='State Transition Probability for each simulation')
    parser.add_argument('--online', type=str2bool, nargs='+',
                        help='Whether each simulation should use online or offline pheromone updates')
    args = parser.parse_args()

    nants = args.nants
    qpersistence = args.qpersistence
    p0 = args.p0
    online = args.online

    lengths = set(map(lambda x: len(x), [nants, qpersistence, p0, online]))
    if len(lengths) != 1:
        raise Exception("nants, qpersistence, p0, online command line lists must all be same length.")

    main(zip(nants, qpersistence, p0, online))

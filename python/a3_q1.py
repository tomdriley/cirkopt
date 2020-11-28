import argparse

import matplotlib.pyplot as plt
import numpy as np
from a3_q1_ga import optimize, chromosome_to_floats
from perffcn_a3 import Q2_perfFCN as perffcn


def main(simulations):
    simstats = {}
    for pop_size, ngenerations, pcrossover, pmutation in simulations:
        # Make results comparable
        np.random.seed(123456789)

        print("\n")
        stats = list(optimize(pop_size, ngenerations, pcrossover, pmutation))
        print("\n---------------------------Results---------------------------")

        best_fitness_per_iteration = [best_fitness for _, best_fitness, _ in stats]
        best_per_iteration = [chromosome_to_floats(c) for _, _, c in stats]

        Kp, Ti, Td = best_per_iteration[-1]
        ISE, Tr, Ts, Mp = perffcn(Kp, Ti, Td, show_plot=True)
        print(f"\nBest solution: Kp={Kp}, Ti={Ti}, Td={Td} -> ISE={ISE}, Tr={Tr}, Ts={Ts}, Mp={Mp}")

        legend = f'{pop_size}-{ngenerations}-{pcrossover}-{pmutation}'
        simstats[legend] = best_fitness_per_iteration

    plt.figure()
    plt.title("Fitness vs Iteration")

    colours = ['b', 'g', 'r', 'c', 'm']
    legend = []
    for idx, key in enumerate(simstats.keys()):
        best_fitness_per_iteration = simstats[key]
        legend.append(key)
        plt.plot(best_fitness_per_iteration, colours[idx % len(colours)])

    plt.legend(legend)
    plt.xlabel('Iteration')
    plt.ylabel('Fitness')
    plt.tight_layout()
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.minorticks_on()
    ax.grid(which='major', linestyle='-', linewidth='0.5', color='red')
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    plt.savefig("out/fitness_vs_iteration.png")


if __name__ == '__main__':
    # Gives good results: --nants 15 20 --qpersistence 0.50 0.60 --p0 0.30 0.35 --online true true
    parser = argparse.ArgumentParser(description='Run Genetic Algorithm and plot Fitness vs Iteration.')
    parser.add_argument('--pop_size', type=int, nargs='+', help='Population sizes for each simulation')
    parser.add_argument('--ngenerations', type=int, nargs='+', help='Number of generations for each simulation')
    parser.add_argument('--pcrossover', type=float, nargs='+', help='Crossover probability for each simulation')
    parser.add_argument('--pmutation', type=float, nargs='+', help='Mutation rate for each simulation')
    args = parser.parse_args()

    pop_size = args.pop_size
    ngenerations = args.ngenerations
    pcrossover = args.pcrossover
    pmutation = args.pmutation

    lengths = set(map(lambda x: len(x), [pop_size, ngenerations, pcrossover, pmutation]))
    if len(lengths) != 1:
        raise Exception("pop_size, ngenerations, pcrossover, pmutation command line lists must all be same length.")

    main(zip(pop_size, ngenerations, pcrossover, pmutation))

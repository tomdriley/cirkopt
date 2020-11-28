import multiprocessing as mp
import time

import numpy as np
from perffcn_a3 import Q2_perfFCN as perffcn

KP_FP_MIN = 200
KP_FP_MAX = 1800
TI_FP_MIN = 105
TI_FP_MAX = 942
TD_FP_MIN = 26
TD_FP_MAX = 237
LEN_CHROMOSOME = 29


def int_to_bin(i, n):
    return np.array(list(np.binary_repr(i).zfill(n))).astype(np.int8)


def bin_to_gray(bits):
    def xor(a, b):
        return 0 if a == b else 1

    gray = np.zeros_like(bits)
    # MSB is the same
    gray[0] = bits[0]

    for i in range(1, len(gray)):
        gray[i] = xor(bits[i - 1], bits[i])
    return gray


def gray_to_bin(gray):
    def flip(a):
        return 0 if a == 1 else 1

    bits = np.zeros_like(gray)
    # MSB is the same
    bits[0] = gray[0]

    for i in range(1, len(bits)):
        if gray[i] == 0:
            bits[i] = bits[i - 1]
        else:
            bits[i] = flip(bits[i - 1])
    return bits


def floats_to_chromosome(Kp, Ti, Td):
    """
    :param Kp: float in range [2, 18], precision of 2 decimal points
    :param Ti: float in range [1.05, 9.42], precision of 2 decimal points
    :param Td: float in range [0.26, 2.37], precision of 2 decimal points
    :return: numpy boolean array as a 2 decimal precision encoding of the parameters
    """

    # Convert values to fixed point (2 decimal precision)
    # Ensure values are in supported ranges
    Kp_fp = max(min(int(round(Kp * 100)), KP_FP_MAX), KP_FP_MIN) - KP_FP_MIN
    Ti_fp = max(min(int(round(Ti * 100)), TI_FP_MAX), TI_FP_MIN) - TI_FP_MIN
    Td_fp = max(min(int(round(Td * 100)), TD_FP_MAX), TD_FP_MIN) - TD_FP_MIN

    # Number of bits = log2((18-2)*100) + log2((9.42-1.05)*100) + log2((2.37-0.26)*100)
    # Number of bits = 10.6 + 9.7 + 7.7
    # Number of bits = 11 + 10 + 8 = 29
    Kp_bits = int_to_bin(Kp_fp, 11)
    Ti_bits = int_to_bin(Ti_fp, 10)
    Td_bits = int_to_bin(Td_fp, 8)

    Kp_gray_bits = bin_to_gray(Kp_bits)
    Ti_gray_bits = bin_to_gray(Ti_bits)
    Td_gray_bits = bin_to_gray(Td_bits)

    return np.concatenate([Kp_gray_bits, Ti_gray_bits, Td_gray_bits])


def chromosome_to_floats(chromosome):
    """
    :param chromosome: binary representation of Kp, Ti, Td
    :return:
      Kp: float in range [2, 18], precision of 2 decimal points
      Ti: float in range [1.05, 9.42], precision of 2 decimal points
      Td: float in range [1.05, 9.42], precision of 2 decimal points
    """
    Kp_gray_bits = chromosome[:11]
    Ti_gray_bits = chromosome[11:21]
    Td_gray_bits = chromosome[21:]

    Kp_bits = gray_to_bin(Kp_gray_bits)
    Ti_bits = gray_to_bin(Ti_gray_bits)
    Td_bits = gray_to_bin(Td_gray_bits)

    Kp_fp = Kp_bits.dot(1 << np.arange(Kp_bits.shape[-1] - 1, -1, -1))
    Ti_fp = Ti_bits.dot(1 << np.arange(Ti_bits.shape[-1] - 1, -1, -1))
    Td_bits = Td_bits.dot(1 << np.arange(Td_bits.shape[-1] - 1, -1, -1))

    Kp = max(min(Kp_fp + KP_FP_MIN, KP_FP_MAX), KP_FP_MIN) / 100.0
    Ti = max(min(Ti_fp + TI_FP_MIN, TI_FP_MAX), TI_FP_MIN) / 100.0
    Td = max(min(Td_bits + TD_FP_MIN, TD_FP_MAX), TD_FP_MIN) / 100.0

    return Kp, Ti, Td


def fitness(ISE, tr, ts, Mp):
    return 1 / (ISE + (100 * tr) + (5 * ts) + (2 * Mp))


def evaluate(chromosome):
    Kp, Ti, Td = chromosome_to_floats(chromosome)
    try:
        ISE, tr, ts, Mp = perffcn(Kp, Ti, Td)
        return fitness(ISE, tr, ts, Mp)
    except IndexError as error:
        global num_errors
        # print(f"Inputs {(Kp, Ti, Td)} triggered 'IndexError: {error}'")
        return 0.0


def optimize(pop_size, ngenerations, pcrossover, pmutation):
    print(
        f"Initializing GA with population size of {pop_size}, {ngenerations} generations, {pcrossover} crossover rate, and {pmutation} mutation rate")
    num_errors = 0
    with mp.Pool() as process_pool:
        # Random initial population
        population = np.random.randint(low=0, high=2, size=(pop_size, LEN_CHROMOSOME), dtype=np.int8)
        times = []

        for n in range(ngenerations):
            pct_done = round(n / ngenerations * 100)
            print(f"\rProgress {pct_done}%", end="", flush=True)

            start = time.time()

            fitness = np.asarray(process_pool.map(evaluate, population))
            tfitness = np.sum(fitness)
            probabilities = fitness / tfitness
            num_errors += (pop_size - np.count_nonzero(fitness))

            offspring = np.zeros_like(population)
            next_child = 0
            while next_child < pop_size - 2:
                parent_a_idx, parent_b_idx = np.random.choice(
                    a=np.arange(start=0, stop=pop_size, dtype=np.int8),
                    size=2,
                    replace=False,
                    p=probabilities
                )
                parent_a = population[parent_a_idx]
                parent_b = population[parent_b_idx]

                child_a = np.copy(parent_a)
                child_b = np.copy(parent_b)

                if np.random.uniform() <= pcrossover:
                    # uniform cross over
                    for i in range(LEN_CHROMOSOME):
                        if np.random.uniform() < 0.5:
                            tmp = child_a[i]
                            child_a[i] = child_b[i]
                            child_b[i] = tmp

                offspring[next_child] = child_a
                offspring[next_child + 1] = child_b
                next_child += 2

            for child_idx in range(pop_size - 2):
                child = offspring[child_idx]
                # bit flip mutation
                for i in range(LEN_CHROMOSOME):
                    if np.random.uniform() < pmutation:
                        if child[i] == 1:
                            child[i] = 0
                        else:
                            child[i] = 1

            # Add top 2 individuals
            idx_of_best, idx_of_second_best = fitness.argsort()[-2:][::-1]
            offspring[pop_size - 2] = population[idx_of_best]
            offspring[pop_size - 1] = population[idx_of_second_best]

            # yield len(np.unique(offspring, axis=0)), population[top_2[0]]
            yield tfitness / pop_size, fitness[idx_of_best], population[idx_of_best]

            np.random.shuffle(offspring)
            population = offspring

            end = time.time()
            times.append(end - start)

        print(f"\rProgress 100%", flush=True)
        print("GA Completed in {:.2f} seconds ({:.2f} seconds/iteration)".format(sum(times), sum(times) / len(times)))
        print(f"Number of unstable system errors: {num_errors}")

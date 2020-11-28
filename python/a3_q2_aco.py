import multiprocessing as mp
import random
import time
from functools import partial
from math import sqrt
from typing import Iterator, List, Tuple

import numpy as np

NCITIES = 29

coordinates = (
    (1150, 1760),
    (630, 1660),
    (40, 2090),
    (750, 1100),
    (750, 2030),
    (1030, 2070),
    (1650, 650),
    (1490, 1630),
    (790, 2260),
    (710, 1310),
    (840, 550),
    (1170, 2300),
    (970, 1340),
    (510, 700),
    (750, 900),
    (1280, 1200),
    (230, 590),
    (460, 860),
    (1040, 950),
    (590, 1390),
    (830, 1770),
    (490, 500),
    (1840, 1240),
    (1260, 1500),
    (1280, 790),
    (490, 2130),
    (1460, 1420),
    (1260, 1910),
    (360, 1980)
)


class Ant:
    """
    A helper class containing most of the
    """

    def __init__(self, start: int) -> None:
        """
        :param start: 0-indexed starting city
        """
        self.start = start
        self.path = [start]

        self.rand = np.random.RandomState(random.randint(0, 2 ** 32))

    def reset(self, start: int):
        self.start = start
        self.path = [self.start]

    def not_visited(self, city: int):
        """
        :param city: index of city in coordinates (0-indexed)
        :return: whether this ant has already visited this city
        """
        return city not in self.path or (len(self.path) == NCITIES and city == self.start)

    def choose_city(self, options: List[int], pheromones: List[List[float]], q0: float) -> int:
        source = self.path[-1]

        tpheromones = [pheromones[min(source, dest)][max(source, dest)] for dest in options]

        if self.rand.uniform() <= q0:
            city, _ = max(zip(options, tpheromones), key=lambda idx_and_pheromone: idx_and_pheromone[1])
            return city

        spheromones = sum(tpheromones)
        if spheromones == 0:
            # print(f"{len(tpheromones)} are 0")
            return self.rand.choice(options)

        probabilities = [pheromone / spheromones for pheromone in tpheromones]

        return self.rand.choice(np.asarray(options), size=1, p=np.asarray(probabilities))[0]

    def build_solution(self, pheromones: List[List[float]], q0: float) -> List[int]:
        for _ in range(NCITIES):
            options = [i for i in range(NCITIES) if self.not_visited(i)]
            next_city = self.choose_city(options, pheromones, q0)
            self.path.append(next_city)
        return self.path


def distance(source: int, destination: int):
    """
    :param source: index of source city in coordinates (0-indexed)
    :param destination: index of destination city in coordinates (0-indexed)
    :return: euclidean distance
    """
    x1, y1 = coordinates[source]
    x2, y2 = coordinates[destination]
    return sqrt(((x1 - x2) ** 2) + ((y1 - y2) ** 2))


def sdistance(solution: List[int]):
    psum = 0
    for idx in range(1, len(solution)):
        psum += distance(solution[idx - 1], solution[idx])
    return psum


def online_delayed_pheromone_update(Q: float, pheromones: List[List[float]], paths: List[List[int]],
                                    distances: List[float]):
    tdistance = sum(distances)
    for path, dist in zip(paths, distances):
        # Don't update pheromone trail between last city and starting city
        delta = (dist / tdistance) * Q
        for idx in range(1, len(path) - 1):
            source = path[idx - 1]
            destination = path[idx]

            L = distance(source, destination)
            i = min(source, destination)
            j = max(source, destination)

            pheromones[i][j] += Q / L


def offline_pheromone_update(Q: float, pheromones: List[List[float]], paths: List[List[int]], distances: List[float]):
    best_path, best_distance = min(zip(paths, distances), key=lambda path_and_distance: path_and_distance[1])
    for idx in range(1, len(best_path) - 1):
        source = best_path[idx - 1]
        destination = best_path[idx]

        L = distance(source, destination)
        i = min(source, destination)
        j = max(source, destination)

        pheromones[i][j] += Q / L


def build_solution(ant: Ant, data: Tuple[List[List[float]], float]) -> List[int]:
    pheromones, q0 = data
    return ant.build_solution(pheromones, q0)


def optimize(
        nants: int,
        maxitr: int,
        Q: float,
        qpersistence: float,
        p0: float,
        online: bool
) -> Iterator[Tuple[float, float, List[int]]]:
    update = "online" if online else "offline"
    print(
        f"Initializing {update} ACS with {nants} ants, {maxitr} iterations, {qpersistence} pheromone persistence and {p0} transition probability")

    starting_cities = np.random.choice(range(NCITIES), size=nants, replace=nants > NCITIES)
    ants = [Ant(start) for start in starting_cities]

    # Initialize pheromone with small random amount
    pheromones = [[0.0 for _ in range(NCITIES)] for _ in range(NCITIES)]
    for i in range(NCITIES - 1):
        for j in range(i + 1, NCITIES):
            pheromones[i][j] = np.random.uniform(0.0, Q / 4.0)

    times = []
    with mp.Pool() as process_pool:
        for itr in range(maxitr):
            pct_done = round(itr / maxitr * 100)
            print(f"\rProgress {pct_done}%", end="", flush=True)
            tstart = time.time() * 1000

            matrix = "\n".join((", ".join(("{:.2f}".format(col) for col in row)) for row in pheromones))

            # Construct ant solutions
            solutions = process_pool.map(partial(build_solution, data=(pheromones, p0)), ants)
            # solutions = [ant.build_solution(pheromones, q0) for ant in ants]
            distances = process_pool.map(sdistance, solutions)
            # distances = [sdistance(solution) for solution in solutions]

            # TODO: maybe do local search (optional)

            # Stats
            avg_distance = sum(distances) / len(distances)
            idx_best_solution, best_distance = min(enumerate(distances),
                                                   key=lambda idx_and_distance: idx_and_distance[1])
            best_solution = solutions[idx_best_solution]

            # Evaporation by geometric decay
            for i in range(NCITIES - 1):
                for j in range(i + 1, NCITIES):
                    pheromones[i][j] *= (1 - qpersistence)

            # Update pheromones
            if online:
                # online delayed pheromone update
                online_delayed_pheromone_update(Q, pheromones, solutions, distances)
            else:
                # offline pheromone update
                offline_pheromone_update(Q, pheromones, solutions, distances)

            yield avg_distance, best_distance, best_solution

            # if itr == 500:
            #     q0 = 1 - q0
            starting_cities = np.random.choice(range(NCITIES), size=nants, replace=nants > NCITIES)
            for ant, start in zip(ants, starting_cities):
                ant.reset(start)

            tend = time.time() * 1000
            times.append(tend - tstart)

    print(f"\rProgress 100%", flush=True)
    print("ACO Completed in {:.2f} seconds ({:.2f} ms/iteration)".format(sum(times) / 1000, sum(times) / len(times)))

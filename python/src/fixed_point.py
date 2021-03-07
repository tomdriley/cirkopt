from math import floor, ceil

from enum import Enum


class Rounding(Enum):
    UP = 1
    DOWN = 2
    HALF_UP = 3  # Round to nearest integer, round up on ties


def fixed(val: float, precision: float, rounding: Rounding = Rounding.HALF_UP) -> int:
    if precision <= 0:
        raise Exception("Precision cannot be 0")

    if rounding == Rounding.HALF_UP:
        return round(val / precision)

    if rounding == Rounding.DOWN:
        return floor(val / precision)

    if rounding == Rounding.UP:
        return ceil(val / precision)


def floating(val: int, precision: float) -> float:
    if precision <= 0:
        raise Exception("Precision cannot be 0")
    return val * precision

from math import floor, ceil

from enum import Enum


class Rounding(Enum):
    UP = 1
    DOWN = 2
    HALF_UP = 3  # Round to nearest integer, round up on ties


def quantize(val: float, precision: float, rounding: Rounding = Rounding.HALF_UP) -> int:
    if precision <= 0:
        raise ValueError("Precision cannot be 0")

    if rounding == Rounding.HALF_UP:
        return round(val / precision)

    if rounding == Rounding.DOWN:
        return floor(val / precision)

    if rounding == Rounding.UP:
        return ceil(val / precision)

    raise ValueError("rounding not one of UP, DOWN, or HALF_UP")


def scale(val: int, precision: float) -> float:
    if precision <= 0:
        raise ValueError("Precision cannot be 0")
    return val * precision

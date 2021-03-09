from decimal import Decimal
from math import floor, ceil

from enum import Enum


class Rounding(Enum):
    UP = 1
    DOWN = 2
    HALF_UP = 3  # Round to nearest integer, round up on ties


def quantize(val: float, precision: str, rounding: Rounding = Rounding.HALF_UP) -> int:
    prec = Decimal(precision)
    if prec <= 0:
        raise ValueError("Precision cannot be 0")

    quantized = float(Decimal(val) / prec)

    if rounding == Rounding.HALF_UP:
        return round(quantized)

    if rounding == Rounding.DOWN:
        return floor(quantized)

    if rounding == Rounding.UP:
        return ceil(quantized)

    raise ValueError("rounding not one of UP, DOWN, or HALF_UP")


def scale(val: int, precision: str) -> float:
    prec = Decimal(precision)
    if prec <= 0:
        raise ValueError("Precision cannot be 0")
    return float(val * prec)

from decimal import Decimal
from math import floor, ceil

from enum import Enum


class Rounding(Enum):
    UP = 1
    DOWN = 2
    TIE_EVEN = 3  # Round to nearest integer, round to even number on tie


def quantize(val: float, precision: str, rounding: Rounding = Rounding.TIE_EVEN) -> int:
    prec = Decimal(precision)
    if prec <= 0:
        raise ValueError("Precision cannot be 0")

    quantized = float(Decimal(val) / prec)

    if rounding == Rounding.TIE_EVEN:
        return round(quantized)

    if rounding == Rounding.DOWN:
        return floor(quantized)

    if rounding == Rounding.UP:
        return ceil(quantized)

    raise ValueError("rounding not one of UP, DOWN, or TIE_EVEN")


def scale(val: int, precision: str) -> float:
    prec = Decimal(precision)
    if prec <= 0:
        raise ValueError("Precision cannot be 0")
    return float(val * prec)

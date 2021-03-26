from decimal import Decimal, ROUND_UP, ROUND_HALF_EVEN, ROUND_DOWN

from enum import Enum

from src.exceptions import CirkoptValueError


class Rounding(Enum):
    UP = 1
    DOWN = 2
    TIE_EVEN = 3  # Round to nearest integer, round to even number on tie


def quantize(
        val: Decimal,
        precision: Decimal,
        _min: Decimal = Decimal('0'),
        rounding: Rounding = Rounding.TIE_EVEN
) -> int:
    if precision <= 0:
        raise CirkoptValueError("Precision cannot be 0")

    quantized = (val - _min).max(Decimal(0.0)) / precision

    if rounding == Rounding.TIE_EVEN:
        decimal_rounding = ROUND_HALF_EVEN
    elif rounding == Rounding.DOWN:
        decimal_rounding = ROUND_DOWN
    elif rounding == Rounding.UP:
        decimal_rounding = ROUND_UP
    else:
        raise CirkoptValueError("rounding not one of UP, DOWN, or TIE_EVEN")

    return int(quantized.quantize(Decimal('1.'), rounding=decimal_rounding))


def scale(val: int, precision: Decimal) -> float:
    precision = Decimal(precision)
    if precision <= 0:
        raise CirkoptValueError("Precision cannot be 0")
    return float(val * precision)

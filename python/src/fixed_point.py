def fixed(val: float, precision: float) -> int:
    if precision <= 0:
        raise Exception("Precision cannot be 0")
    return round(val / precision)


def floating(val: int, precision: float) -> float:
    if precision <= 0:
        raise Exception("Precision cannot be 0")
    return val * precision

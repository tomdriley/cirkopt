from enum import Enum
from typing import Generic, Iterator, TypeVar

from dataclasses import dataclass

T = TypeVar('T', float, int)


class Param(Enum):
    WIDTH = 1
    LENGTH = 2
    FINGERS = 3

    def __str__(self):
        return self.name.capitalize()  # pylint: disable=no-member # bug in pylint


@dataclass(frozen=True)
class Range(Generic[T]):
    param: Param
    low: T  # inclusive
    high: T  # inclusive
    step_size: T

    def __post_init__(self):
        if self.low > self.high:
            raise ValueError("Range low must be less than or equal to high")

        if len({type(self.low), type(self.high), type(self.step_size)}) != 1:
            raise ValueError("Range low, high, and step size must be the same type")

        if self.param in {Param.WIDTH, Param.LENGTH} and not isinstance(self.low, float):
            raise ValueError("Widths should be specified as floats")

        if self.param == Param.FINGERS and not isinstance(self.low, int):
            raise ValueError("Fingers should be specified as ints")

    def __iter__(self) -> Iterator[T]:
        current = self.low

        while current <= self.high:
            yield current
            current += self.step_size

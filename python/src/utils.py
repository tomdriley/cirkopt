from itertools import islice
from typing import Callable, Iterable, Iterator, Sequence, TypeVar

from src.exceptions import CirkoptException


T = TypeVar('T')


def single(predicate: Callable[[T], bool], seq: Sequence[T]) -> T:
    matches = list(filter(predicate, seq))
    if len(matches) == 0:
        raise CirkoptException('Zero items in sequence match predicate')
    if len(matches) > 1:
        raise CirkoptException('More than one item in sequence matches predicate')
    return matches[0]


def chunked(iterable: Iterable[T], n: int) -> Iterator[Sequence[T]]:
    iterable = iter(iterable)

    def next_slice():
        return tuple(islice(iterable, n))

    return iter(next_slice, tuple())

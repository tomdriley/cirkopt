from typing import Callable, Sequence, TypeVar

T = TypeVar('T')


def single(predicate: Callable[[T], bool], seq: Sequence[T]) -> T:
    matches = list(filter(predicate, seq))
    if len(matches) == 0:
        raise Exception('Zero items in sequence match predicate')
    if len(matches) > 1:
        raise Exception('More than one item in sequence matches predicate')
    return matches[0]

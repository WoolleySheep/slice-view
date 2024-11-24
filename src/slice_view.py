from __future__ import annotations

from collections.abc import Generator, Sequence
from typing import Iterator, overload


class SliceView[T](Sequence[T]):
    """Slice-like view of a sequence.

    Allows slice-like operations to be performed, without creating a copy of the
    data in the underlying sequence. If the underlying sequence changes, the
    slice view will be effected.
    """

    def __init__(
        self,
        sequence: Sequence[T],
        start: int | None = None,
        stop: int | None = None,
        step: int = 1,
    ):
        if step == 0:
            raise ValueError("step cannot be zero")

        self._sequence = sequence
        self._start = start
        self._stop = stop
        self._step = step

    def __bool__(self) -> bool:
        return self._get_start() != self._get_stop()

    def __len__(self) -> int:
        if self._step > 0:
            return max((self._get_stop() - self._get_start() - 1) // self._step, 0)
        else:
            return max((self._get_stop() - self._get_start() + 1) // self._step, 0)

    def __contains__(self, value: object) -> bool:
        return any(
            self._sequence[i] == value
            for i in range(self._get_start(), self._get_stop(), self._step)
        )

    def __iter__(self) -> Generator[T, None, None]:
        count = 0
        if self._step > 0:
            while (index := self._get_start() + count * self._step) < self._get_stop():
                yield self[index]
                count += 1
        else:
            while (index := self._get_start() + count * self._step) > self._get_stop():
                yield self[index]
                count += 1

    def __reversed__(self) -> Iterator[T]:
        count = 0
        if self._step > 0:
            while (
                index := self._get_stop() - 1 - count * self._step
            ) >= self._get_start():
                yield self[index]
                count += 1
        else:
            while (
                index := self._get_stop() + 1 - count * self._step
            ) <= self._get_start():
                yield self[index]
                count += 1

    @overload
    def __getitem__(self, index: int) -> T: ...

    @overload
    def __getitem__(self, index: slice) -> SliceView[T]: ...

    def __getitem__(self, index: int | slice) -> T | SliceView[T]:
        if isinstance(index, int):
            if index < 0:
                index = len(self) + index
                if index < 0:
                    raise IndexError("index out of range")
            index = self._get_start() + index * self._step
            return self._sequence[index]

        return SliceView[T](self, index.start, index.stop, index.step)

    def _get_start(self) -> int:
        if self._step > 0:
            if self._start is None:
                return 0
            if self._start < 0:
                return max(len(self._sequence) + self._start, 0)

            return min(self._start, len(self._sequence))

        else:
            if self._start is None:
                return len(self._sequence) - 1
            if self._start < 0:
                return max(len(self._sequence) + self._start, 0)

            return min(self._start, len(self._sequence) - 1)

    def _get_stop(self) -> int:
        if self._step > 0:
            if self._stop is None:
                return len(self._sequence)
            elif self._stop < 0:
                return max(len(self._sequence) + self._stop, 0)

            return min(self._stop, len(self._sequence))

        else:
            if self._stop is None:
                return -1
            elif self._stop < 0:
                return max(len(self._sequence) + self._stop, -1)

            return min(self._stop, len(self._sequence) - 1)

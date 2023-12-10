from __future__ import annotations
from typing import List, Iterable
import sys
from dataclasses import dataclass
from functools import total_ordering, reduce


@dataclass
@total_ordering
class Interval:
    start: int
    end: int
    offset: int = 0

    def __contains__(self, other: Interval):
        return other.start >= self.start and other.end <= self.end

    def intersects(self, other: Interval):
        return self.start <= other.end and self.end > other.start

    def segment(self, *others: Interval):
        others = sorted(others)

        segments = []
        start = self.start

        for other in others:
            if not self.intersects(other):
                continue

            if self in other:
                return [
                    Interval(
                        self.start + other.offset, self.end + other.offset, other.offset
                    ),
                ]

            if other.start > start:
                segments.append(Interval(start, other.start - 1))

            segments.append(
                Interval(
                    max(start, other.start) + other.offset,
                    min(other.end, self.end) + other.offset,
                    other.offset,
                )
            )

            start = other.end + 1

        return segments or [self]

    def __eq__(self, other: Interval):
        return self.start == other.start

    def __lt__(self, other: Interval):
        return self.start < other.start

    @classmethod
    def parse(cls, interval: str):
        destination, source, count = map(int, interval.split())

        return cls(source, source + count - 1, destination - source)


@dataclass
class Map:
    intervals: List[Interval]
    name: str

    @classmethod
    def parse(cls, intervals: str):
        lines = intervals.split("\n")

        return cls(
            [Interval.parse(interval) for interval in lines[1:]],
            lines[0].split("-to-")[1],
        )


def get_seed_locations(seeds: List[Interval], maps: List[Map]):
    values = seeds

    for map in maps:
        values = reduce(
            lambda a, b: a + b,
            [value.segment(*map.intervals) for value in values],
            [],
        )

    return [value.start for value in values]


if __name__ == "__main__":
    seeds, *intervals = open(sys.argv[1]).read()[:-1].split("\n\n")
    seeds = list(map(int, seeds.split()[1:]))
    maps = [Map.parse(intervals) for intervals in intervals]

    seed_intervals = [Interval(start, stop) for start, stop in zip(seeds, seeds)]

    locations = get_seed_locations(seed_intervals, maps)

    print("(Part 1) Minimum location:", min(*locations))

    seed_intervals = [
        Interval(start, start + length - 1)
        for start, length in zip(seeds[0::2], seeds[1::2])
    ]

    locations = get_seed_locations(seed_intervals, maps)

    print("(Part 2) Minimum location:", min(*locations))

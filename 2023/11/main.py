
from __future__ import annotations
import sys
from dataclasses import dataclass
from functools import cached_property, reduce
from typing import Set, Tuple, List

Point = Tuple[int, int]

@dataclass
class Universe:
    _image: List[str]
    galaxies: Set[Point]

    @classmethod
    def parse(cls, image: str) -> cls:
        _image = []
        galaxies: Set[Point] = set()

        for y, line in enumerate(image.split("\n")):
            _image.append(line)

            for x, char in enumerate(line):
                if char == "#":
                    galaxies.add((x, y))

        return cls(_image=_image, galaxies=galaxies)

    @cached_property
    def empty_rows(self):
        empty = []

        for index, row in enumerate(self._image):
            if "#" not in row:
                empty.append(index)

        return empty

    @cached_property
    def empty_columns(self):
        rotated = list(zip(*self._image[::-1]))
        empty = []

        for index, column in enumerate(rotated):
            if "#" not in column:
                empty.append(index)

        return empty

    def empty_column_collisions(self, x1: int, x2: int):
        collisions = []

        left = min(x1, x2)
        right = max(x1, x2)

        for column in self.empty_columns:
            if left <= column and right >= column:
                collisions.append(column)

        return collisions

    def empty_row_collisions(self, y1: int, y2: int):
        collisions = []

        top = min(y1, y2)
        bottom = max(y1, y2)

        for row in self.empty_rows:
            if top <= row and bottom >= row:
                collisions.append(row)

        return collisions

    def distances(self, empty_space_multiplier: int = 2):
        galaxy_list = list(self.galaxies)
        distance_list = []

        for index, first in enumerate(galaxy_list):
            for second in galaxy_list[index+1:]:
                x1, y1 = first
                x2, y2 = second

                collisions = len(self.empty_column_collisions(x1, x2)) + len(self.empty_row_collisions(y1, y2)) 

                distance_list.append(abs(x1 - x2) + abs(y1 - y2) - collisions + collisions * empty_space_multiplier)

        return distance_list

if __name__ == "__main__":
    image = open(sys.argv[1]).read()

    universe = Universe.parse(image)

    print("(Part 1) Sum of minimum distances:", reduce(lambda a, b: a + b, universe.distances(), 0))
    print("(Part 2) Sum of minimum distances with massive empty space:", reduce(lambda a, b: a + b, universe.distances(1_000_000), 0))
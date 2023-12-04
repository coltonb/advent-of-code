import sys
import re
from dataclasses import dataclass
from typing import List


@dataclass
class Point:
    x: int
    y: int

    def __eq__(self, other) -> bool:
        return isinstance(other, type(self)) and self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash((self.x, self.y))


@dataclass
class MatrixNumber:
    value: int
    start: Point
    end: Point

    def border(self) -> List[Point]:
        """Returns a list of all the points that make up the string's border."""

        border = [
            Point(self.start.x - 1, self.start.y - 1),
            Point(self.start.x - 1, self.start.y),
            Point(self.start.x - 1, self.start.y + 1),
        ]

        length = self.end.x - self.start.x

        for i in range(length + 1):
            border.extend(
                [
                    Point(self.start.x + i, self.start.y - 1),
                    Point(self.start.x + i, self.start.y + 1),
                ]
            )

        border.extend(
            [
                Point(self.end.x + 1, self.start.y - 1),
                Point(self.end.x + 1, self.start.y),
                Point(self.end.x + 1, self.start.y + 1),
            ]
        )

        return border


class Schematic:
    def __init__(self, schematic_lines: List[str]):
        self._matrix = []

        for line in schematic_lines:
            self._matrix.append(line)

    def value_at(self, x: int, y: int) -> str:
        if y < 0 or y >= len(self._matrix):
            return ""

        if x < 0 or x >= len(self._matrix[y]):
            return ""

        return self._matrix[y][x]

    def has_symbol(self, point: Point) -> bool:
        return bool(re.search("[^.\d]", self.value_at(point.x, point.y)))

    def gear_ratios(self) -> List[int]:
        numbers_around_gear = dict()

        for number in self.numbers():
            for border_point in number.border():
                if self.value_at(border_point.x, border_point.y) == "*":
                    numbers_around_gear[border_point] = numbers_around_gear.get(
                        border_point, []
                    ) + [number.value]

        gear_ratios = []

        for numbers in numbers_around_gear.values():
            if len(numbers) != 2:
                continue

            gear_ratios.append(numbers[0] * numbers[1])

        return gear_ratios

    def part_numbers(self) -> List[int]:
        part_numbers = []

        for number in self.numbers():
            for border_point in number.border():
                if self.has_symbol(border_point):
                    part_numbers.append(number.value)
                    break

        return part_numbers

    def numbers(self) -> List[MatrixNumber]:
        numbers = []

        for y, line in enumerate(self._matrix):
            numbers.extend(
                [
                    MatrixNumber(
                        value=int(match[0]),
                        start=Point(x=match.span()[0], y=y),
                        end=Point(x=match.span()[1] - 1, y=y),
                    )
                    for match in re.finditer("\d+", line)
                ]
            )

        return numbers


if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        schematic = Schematic([line.strip() for line in file.readlines()])

    total = sum(schematic.part_numbers())
    print("(Part 1) Sum of Part Numbers:", total)

    gear_ratio_total = sum(schematic.gear_ratios())
    print("(Part 2) Sum of Gear Ratios:", gear_ratio_total)

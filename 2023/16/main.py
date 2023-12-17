from __future__ import annotations
import sys
from dataclasses import dataclass


@dataclass
class Vector:
    x: int
    y: int

    def __add__(self, other: Vector):
        return Vector(self.x + other.x, self.y + other.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: Vector):
        return self.x == other.x and self.y == other.y


class Direction:
    RIGHT = Vector(1, 0)
    DOWN = Vector(0, 1)
    LEFT = Vector(-1, 0)
    UP = Vector(0, -1)


def parse():
    return open(sys.argv[1]).read().strip().split("\n")


MIRROR_MAP = {
    "/": {
        Direction.RIGHT: Direction.UP,
        Direction.DOWN: Direction.LEFT,
        Direction.LEFT: Direction.DOWN,
        Direction.UP: Direction.RIGHT,
    },
    "\\": {
        Direction.RIGHT: Direction.DOWN,
        Direction.DOWN: Direction.RIGHT,
        Direction.LEFT: Direction.UP,
        Direction.UP: Direction.LEFT,
    },
}


def trace_beam(layout: list[str], start=None):
    if start is None:
        start = (Direction.RIGHT, Vector(0, 0))

    visited: set[tuple[Direction, Vector]] = set()
    visited_locations: set[Vector] = set()
    stack = [start]

    while stack:
        direction, location = stack.pop()
        x, y = (location.x, location.y)

        if x < 0 or x >= len(layout[0]) or y < 0 or y >= len(layout):
            continue

        if (direction, location) in visited:
            continue

        visited.add((direction, location))
        visited_locations.add(location)

        tile = layout[y][x]

        if tile == "|":
            if direction in [Direction.LEFT, Direction.RIGHT]:
                stack.append((Direction.UP, Direction.UP + location))
                stack.append((Direction.DOWN, Direction.DOWN + location))
                continue

        if tile == "-":
            if direction in [Direction.UP, Direction.DOWN]:
                stack.append((Direction.LEFT, Direction.LEFT + location))
                stack.append((Direction.RIGHT, Direction.RIGHT + location))
                continue

        if tile in "/\\":
            next_direction = MIRROR_MAP[tile][direction]
            stack.append((next_direction, next_direction + location))
            continue

        stack.append((direction, direction + location))

    return visited_locations


layout = parse()

print("(Part 1) Energized tiles:", len(trace_beam(layout)))

maximum_energized = 0

for y in range(len(layout)):
    maximum_energized = max(
        maximum_energized, len(trace_beam(layout, (Direction.RIGHT, Vector(0, y))))
    )
    maximum_energized = max(
        maximum_energized,
        len(trace_beam(layout, (Direction.LEFT, Vector(len(layout[0]) - 1, y)))),
    )


for x in range(len(layout[0])):
    maximum_energized = max(
        maximum_energized, len(trace_beam(layout, (Direction.DOWN, Vector(x, 0))))
    )
    maximum_energized = max(
        maximum_energized,
        len(trace_beam(layout, (Direction.UP, Vector(x, len(layout) - 1)))),
    )

print("(Part 2) Maximum possible energized:", maximum_energized)

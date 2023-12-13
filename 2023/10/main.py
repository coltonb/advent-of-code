import sys
from dataclasses import dataclass
from typing import List, Set
from functools import cached_property, reduce
from enum import IntEnum


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y


@dataclass
class Grid:
    grid: List[str]

    @cached_property
    def start(self):
        for y, row in enumerate(self.grid):
            if "S" in row:
                return Point(row.index("S"), y)

    @property
    def height(self):
        return len(self.grid)

    @property
    def width(self):
        return len(self.grid[0])

    def __str__(self):
        return "\n".join(self.grid)

    def __getitem__(self, point: Point):
        if (
            point.y < 0
            or point.y >= self.height
            or point.x < 0
            or point.x >= self.width
        ):
            return None

        return self.grid[point.y][point.x]

    def debug_print(self, points: Set[Point]):
        for y in range(self.height):
            print()
            for x in range(self.width):
                point = Point(x, y)

                if point in points:
                    print("O", end="")
                    continue
                print(self[point], end="")
        print()

    def search_pipe(self, start: Point):
        point = start
        visited = set()

        while True:
            x, y = (point.x, point.y)
            current = self[point]

            if current == "." or current is None:
                return (visited, False)

            up = Point(x, y - 1)
            left = Point(x - 1, y)
            right = Point(x + 1, y)
            down = Point(x, y + 1)

            directions = [right, down, left, up]

            if len(visited) == 0:
                if current == "S":
                    if self[right] in set("-J7"):
                        direction = Direction.RIGHT
                    if self[down] in set("|LJ"):
                        direction = Direction.DOWN
                    if self[left] in set("-FL"):
                        direction = Direction.LEFT
                    if self[up] in set("|7F"):
                        direction = Direction.UP
                if current in set("-LF"):
                    direction = Direction.RIGHT
                if current in set("|7"):
                    direction = Direction.DOWN
                if current == "J":
                    direction = Direction.LEFT

                visited.add(point)
                point = directions[direction]
                continue

            direction_map = {
                "-": {
                    Direction.LEFT: Direction.LEFT,
                    Direction.RIGHT: Direction.RIGHT,
                },
                "|": {
                    Direction.UP: Direction.UP,
                    Direction.DOWN: Direction.DOWN,
                },
                "L": {
                    Direction.DOWN: Direction.RIGHT,
                    Direction.LEFT: Direction.UP,
                },
                "J": {
                    Direction.DOWN: Direction.LEFT,
                    Direction.RIGHT: Direction.UP,
                },
                "7": {
                    Direction.RIGHT: Direction.DOWN,
                    Direction.UP: Direction.LEFT,
                },
                "F": {
                    Direction.LEFT: Direction.DOWN,
                    Direction.UP: Direction.RIGHT,
                },
            }

            direction = direction_map.get(current, {}).get(direction)

            if direction is None:
                return (visited, False)

            if point in visited:
                return (visited, True)

            visited.add(point)

            point = directions[direction]

    @cached_property
    def pipe_loops(self) -> List[Set[Point]]:
        main_loop = grid.search_pipe(self.start)[0]
        visited = set(main_loop)
        cycles = [main_loop]

        for y in range(self.height):
            for x in range(self.width):
                point = Point(x, y)

                if point not in visited:
                    pipe, is_loop = grid.search_pipe(point)
                    visited = visited.union(pipe)

                    if is_loop:
                        cycles.append(pipe)

        return cycles

    @cached_property
    def pipe_enclosed_points(self):
        points = set()
        for y in range(self.height):
            open_loops = {}
            edge = None
            for x in range(self.width):
                point = Point(x, y)
                tile = self[point]

                for index, loop in enumerate(self.pipe_loops):
                    inside_loop = open_loops.get(index, False)

                    if point in loop:
                        if tile == "|":
                            open_loops[index] = not inside_loop
                            continue

                        if tile == "S":
                            edge = "L"
                        if tile in "LF":
                            edge = tile
                        if tile == "7":
                            open_loops[index] = edge == ("F" if inside_loop else "L")
                            edge = None
                        if tile == "J":
                            open_loops[index] = edge == ("L" if inside_loop else "F")
                            edge = None

                        continue

                    if inside_loop:
                        points.add(point)

        return points


if __name__ == "__main__":
    grid = Grid([line.strip() for line in open(sys.argv[1]).readlines()])
    print("(Part 1) Furthest distance:", len(grid.search_pipe(grid.start)[0]) // 2)

    print(
        "(Part 2) Tiles enclosed by loop:",
        len(grid.pipe_enclosed_points),
    )

    # grid.debug_print(reduce(lambda a, b: a.union(b), grid.pipe_loops, set()))

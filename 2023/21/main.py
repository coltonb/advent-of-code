import sys
from dataclasses import dataclass
import numpy as np


@dataclass
class Garden:
    tiles: list[str]

    @property
    def start(self):
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                if self.tiles[y][x] == "S":
                    return (x, y)

    def get(self, x: int, y: int, loop=False):
        if not loop and self.out_of_bounds(x, y):
            return "E"

        x = x % len(self.tiles[0])
        y = y % len(self.tiles)

        return self.tiles[y][x]

    def out_of_bounds(self, x: int, y: int):
        return x < 0 or x >= len(self.tiles[0]) or y < 0 or y >= len(self.tiles)

    @classmethod
    def load(cls):
        return cls(tiles=open(sys.argv[1]).read().strip().split("\n"))


garden = Garden.load()


def walk(steps: int, loop=False):
    positions = {garden.start}

    for _ in range(steps):
        next_positions = set()

        for position in positions:
            x, y = position

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                nx = x + dx
                ny = y + dy

                if garden.get(nx, ny, loop) in "S.":
                    next_positions.add((nx, ny))

        positions = next_positions

    return len(positions)


print("(Part 1) Reachable plots:", walk(64))

# The following is math I don't think I want to really understand.
# Credit: https://www.reddit.com/r/adventofcode/comments/18nevo3/comment/keao6r4/

# polynomial extrapolation
a0 = walk(65, True)
a1 = walk(65 + 131, True)
a2 = walk(65 + 2 * 131, True)

vandermonde = np.matrix([[0, 0, 1], [1, 1, 1], [4, 2, 1]])
b = np.array([a0, a1, a2])
x = np.linalg.solve(vandermonde, b).astype(np.int64)

# note that 26501365 = 202300 * 131 + 65 where 131 is the dimension of the grid
n = 202300
print("(Part 2) Reachable plots:", x[0] * n * n + x[1] * n + x[2])

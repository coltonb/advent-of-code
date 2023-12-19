import sys
import re

DigPlan = list[str]
Vector = tuple[int, int]


def load_dig_plan() -> DigPlan:
    return open(sys.argv[1]).read().strip().split("\n")


DIRECTION_TO_VECTOR: dict[str, Vector] = {
    "R": (1, 0),
    "D": (0, 1),
    "L": (-1, 0),
    "U": (0, -1),
}

INT_TO_DIRECTION: dict[int, str] = {0: "R", 1: "D", 2: "L", 3: "U"}


def area(dig_plan: DigPlan, use_hex=False) -> int:
    x, y = 0, 0
    perimeter = 1
    total = 0

    for instruction in dig_plan:
        direction, magnitude, hexadecimal = instruction.split()

        if use_hex:
            direction = INT_TO_DIRECTION[int(hexadecimal[7:8])]
            magnitude = int(hexadecimal[2:7], 16)
        else:
            magnitude = int(magnitude)

        dx, dy = DIRECTION_TO_VECTOR[direction]

        last_x = x
        last_y = y

        x += dx * magnitude
        y += dy * magnitude
        perimeter += magnitude

        if (x, y) == (0, 0):
            return abs(total) // 2 + perimeter // 2 + 1

        total += last_x * y
        total -= last_y * x


dig_plan = load_dig_plan()

print("(Part 1) Area:", area(dig_plan))
print("(Part 2) Area:", area(dig_plan, True))

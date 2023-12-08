from __future__ import annotations

import functools
import math
import re
import sys
from dataclasses import dataclass
from enum import Enum
from typing import List


class Direction(str, Enum):
    LEFT = "L"
    RIGHT = "R"


class PuzzlePart(Enum):
    PART_1 = 0
    PART_2 = 1


@dataclass
class Location:
    name: str
    left: str
    right: str

    def is_end(self, puzzle_part: PuzzlePart):
        if puzzle_part == PuzzlePart.PART_1:
            return self.name == "ZZZ"
        return self.name.endswith("Z")

    def get_location_name_from_instruction(self, instruction: Direction):
        if instruction == Direction.LEFT:
            return self.left
        return self.right

    @classmethod
    def parse(cls, content: str):
        name, left, right = re.search(
            r"^([a-zA-Z0-9]{3}) = \(([a-zA-Z0-9]{3}), ([a-zA-Z0-9]{3})\)", content
        ).groups()

        return Location(name, left, right)


@dataclass
class Map:
    instructions: List[Direction]
    locations: List[Location]

    @functools.cached_property
    def location_map(self):
        return {location.name: location for location in self.locations}

    def get_locations_matching_pattern(self, pattern: str):
        return [
            location for location in self.locations if re.search(pattern, location.name)
        ]

    def get_location_by_name(self, name: str):
        return self.location_map.get(name)

    def get_instruction(self, step: int):
        return self.instructions[step % len(self.instructions)]

    @classmethod
    def parse(cls, content: str):
        lines = content.split("\n")

        instructions = [Direction(char) for char in lines[0]]
        locations = []

        for location in lines[2:-1]:
            locations.append(Location.parse(location))

        return Map(instructions, locations)


if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        map = Map.parse(file.read())

    current_location = map.get_location_by_name("AAA")
    steps = 0

    while not current_location.is_end(PuzzlePart.PART_1):
        instruction = map.get_instruction(steps)
        steps += 1

        current_location = map.get_location_by_name(
            current_location.get_location_name_from_instruction(instruction)
        )

    print("(Part 1) Steps:", steps)

    # The input is specially crafted such that each traversal is a cycle with exactly one Z point
    # Therefore we can determine the number of steps for each starting location to finish
    # a single time, then find the LCM of those step counts to determine the step #
    # where the loops would synchronize on all "Z" locations.

    current_locations = map.get_locations_matching_pattern("A$")
    steps_by_locations = [0] * len(current_locations)

    while any(not location.is_end(PuzzlePart.PART_2) for location in current_locations):
        for index, location in enumerate(current_locations):
            if location.is_end(PuzzlePart.PART_2):
                continue

            instruction = map.get_instruction(steps_by_locations[index])
            steps_by_locations[index] += 1

            current_locations[index] = map.get_location_by_name(
                location.get_location_name_from_instruction(instruction)
            )

    print("(Part 2) Steps:", math.lcm(*steps_by_locations))

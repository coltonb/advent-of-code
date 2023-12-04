from typing import List
import re

import sys
from dataclasses import dataclass


def match_or_default(s: str, pattern: str, default=None):
    match = re.search(pattern, s)

    if not match:
        return default

    return match.groups()[0]


@dataclass
class Cubes:
    red: int
    green: int
    blue: int


@dataclass
class Game:
    id: int
    pulls: List[Cubes]

    def max_cubes_seen(self):
        max_red = 0
        max_green = 0
        max_blue = 0

        for pull in self.pulls:
            max_red = max(pull.red, max_red)
            max_green = max(pull.green, max_green)
            max_blue = max(pull.blue, max_blue)

        return Cubes(
            red=max_red,
            green=max_green,
            blue=max_blue,
        )

    def power(self):
        cubes = self.max_cubes_seen()

        return cubes.red * cubes.green * cubes.blue

    @classmethod
    def parse(cls, line: str):
        id = int(re.match("Game (\d+):", line).groups()[0])
        pulls = cls._parse_pulls(line)
        return Game(id=id, pulls=pulls)

    @classmethod
    def _parse_pulls(cls, line: str):
        pulls = re.split("Game \d+:", line)[1].split(";")

        return [
            Cubes(
                red=int(match_or_default(pull, "(\d+) red", 0)),
                green=int(match_or_default(pull, "(\d+) green", 0)),
                blue=int(match_or_default(pull, "(\d+) blue", 0)),
            )
            for pull in pulls
        ]


def game_is_possible(game: Game):
    cubes = game.max_cubes_seen()

    return cubes.red <= 12 and cubes.green <= 13 and cubes.blue <= 14


if __name__ == "__main__":
    sum = 0
    sum_of_pow = 0

    with open(sys.argv[1]) as file:
        for line in file.readlines():
            game = Game.parse(line)

            if game_is_possible(game):
                sum += game.id

            sum_of_pow += game.power()

    print("(Part 1) Sum of possible game IDs:", sum)
    print("(Part 2) Sum game powers:", sum_of_pow)

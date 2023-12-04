from typing import Optional

import re
import sys


def get_first_and_last_digit(s: str) -> int:
    integers = list(re.findall("\d", s))

    if integers:
        return int(integers[0] + integers[-1])

    raise ValueError("String contains no digits.")


WORD_DIGIT_MAP = dict(
    one="1",
    two="2",
    three="3",
    four="4",
    five="5",
    six="6",
    seven="7",
    eight="8",
    nine="9",
)
"""A map of words to the equivalent string digit."""


def word_to_digit(s: str) -> str:
    return WORD_DIGIT_MAP.get(s, s)


def get_first_and_last_digit_including_words(s: str):
    # In the puzzle input, there are gotchas like "4nine7oneighthm", where regex
    # would consume "one" from the buffer and miss "eight".
    # As such we need to use a positive lookahead to find overlapping matches.
    integers = list(
        re.findall("(?=(\d|one|two|three|four|five|six|seven|eight|nine))", s)
    )

    if not integers:
        raise ValueError("String contains no digits.")

    first = word_to_digit(integers[0])
    last = word_to_digit(integers[-1])

    return int(first + last)


if __name__ == "__main__":
    part_1_sum = 0
    part_2_sum = 0

    with open(sys.argv[1]) as file:
        for line in file.readlines():
            part_1_sum += get_first_and_last_digit(line)
            part_2_sum += get_first_and_last_digit_including_words(line)

    print("Part 1 Sum:", part_1_sum)
    print("Part 2 Sum:", part_2_sum)

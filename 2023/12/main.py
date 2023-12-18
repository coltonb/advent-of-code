"""
This code is cobbled together from my attempt + Reddit solutions.
Need to study this and make sure I fully understand it.
"""


import sys
import functools


def load():
    parsed_lines = []

    for line in open(sys.argv[1]).readlines():
        record, groups = line.strip().split(" ")

        parsed_lines.append(
            (
                tuple({"#": 2, "?": 1, ".": 0}[char] for char in record),
                tuple(int(group) for group in groups.split(",")),
            )
        )

    return parsed_lines


def match_beginning(record: tuple[int], length: int):
    return all(x > 0 for x in record[:length]) and (
        (len(record) == length) or record[length] < 2
    )


@functools.cache
def count(record: tuple[int], groups: tuple[int]):
    sum_of_groups = sum(groups)

    min_group_count = sum(x == 2 for x in record)
    max_group_count = sum(x > 0 for x in record)

    if min_group_count > sum_of_groups or max_group_count < sum_of_groups:
        return 0

    if sum_of_groups == 0:
        return 1

    if record[0] == 0:
        return count(record[1:], groups)

    if record[0] == 2:
        first_group = groups[0]
        if match_beginning(record, first_group):
            if first_group == len(record):
                return 1
            return count(record[l + 1 :], groups[1:])
        return 0

    return count(record[1:], groups) + count((2,) + record[1:], groups)


lines = load()

print(
    "(Part 1) Total possible permutations:",
    sum(count(record, groups) for record, groups in lines),
)
print(
    "(Part 2) Total possible permutations:",
    sum(count(((record + (1,)) * 5)[:-1], groups * 5) for record, groups in lines),
)

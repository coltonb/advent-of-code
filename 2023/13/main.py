import sys
from functools import reduce


def reflection_points(line: str):
    points = set()

    for i in range(len(line) - 1):
        low = i
        high = i + 1
        mirrored = True

        while low >= 0 and high < len(line):
            if line[low] != line[high]:
                mirrored = False
                break

            low -= 1
            high += 1

        if mirrored:
            points.add((i + 1, i + 2))

    return points


def vertical_reflection(lines: list[str]):
    try:
        return reduce(
            lambda acc, line: acc.intersection(reflection_points(line)),
            lines[1:],
            reflection_points(lines[0]),
        ).pop()
    except KeyError:
        return None


def vertical_reflection_smudge(lines: list[str]):
    all_points = {}

    for line in lines:
        points = reflection_points(line)

        for point in points:
            all_points[point] = all_points.get(point, 0) + 1

    for point, count in all_points.items():
        if count == len(lines) - 1:
            return point

    return None


def rotate_lines(lines: list[str]):
    return ["".join(l) for l in list(zip(*lines))]


def horizontal_reflection(lines: list[str]):
    return vertical_reflection(rotate_lines(lines))


def horizontal_reflection_smudge(lines: list[str]):
    return vertical_reflection_smudge(rotate_lines(lines))


def summarize(lines: list[str]):
    total = 0

    if interval := vertical_reflection(lines):
        total += interval[0]
    if interval := horizontal_reflection(lines):
        total += interval[0] * 100

    return total


def summarize_smudge(lines: list[str]):
    total = 0

    if interval := vertical_reflection_smudge(lines):
        total += interval[0]
    if interval := horizontal_reflection_smudge(lines):
        total += interval[0] * 100

    return total


def load_maps():
    return [group.split("\n") for group in open(sys.argv[1]).read()[:-1].split("\n\n")]


rock_maps = load_maps()

print("(Part 1) Summarization:", sum(summarize(rock_map) for rock_map in rock_maps))
print(
    "(Part 2) Summarization:", sum(summarize_smudge(rock_map) for rock_map in rock_maps)
)

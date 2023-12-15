import sys


def parse():
    return list(map(list, open(sys.argv[1]).read()[:-1].split("\n")))


def swap(l, a, b):
    val = l[a]
    l[a] = l[b]
    l[b] = val


def tilt_left(row: list[str]):
    for i in range(len(row) - 1):
        if row[i] in {"O", "#"}:
            continue

        for j in range(i + 1, len(row)):
            if row[j] == "O":
                swap(row, i, j)
                break
            if row[j] == "#":
                break


def rotate(platform: list[list[str]], n: int = 1):
    if n == 0:
        return platform

    tilted = list(zip(*platform[::-1]))

    for _ in range(n - 1):
        tilted = list(zip(*tilted[::-1]))

    return list(map(list, tilted))


def tilt_platform_left(platform: list[list[str]]):
    for row in platform:
        tilt_left(row)


def get_total_load(platform: list[list[str]]):
    load = 0

    for index, row in enumerate(platform):
        multiplier = len(platform) - index
        load += row.count("O") * multiplier

    return load


def print_platform(platform: list[list[str]]):
    print(*platform, sep="\n")
    print()


def cycle(platform: list[list[str]]):
    platform = rotate(platform, 3)

    for _ in range(4):
        tilt_platform_left(platform)
        platform = rotate(platform)

    return rotate(platform)


def hash_platform(platform: list[list[str]]):
    return hash(tuple(hash(tuple(row)) for row in platform))


platform = parse()

part_1 = rotate(platform, 3)
tilt_platform_left(part_1)

print("(Part 1) Total load:", get_total_load(rotate(part_1)))

encountered = []
loads = []

while True:
    platform_hash = hash_platform(platform)

    if platform_hash in encountered:
        loop_start = encountered.index(platform_hash)
        cycles_remaining = 1_000_000_000 - loop_start
        loop = loads[loop_start:]

        print("(Part 2) Total load after cycles:", loop[cycles_remaining % len(loop)])

        break

    encountered.append(platform_hash)
    loads.append(get_total_load(platform))
    platform = cycle(platform)

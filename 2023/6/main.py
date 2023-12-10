import sys
import math


def quadratic(a, b, c):
    return (
        (-b + math.sqrt(b**2 - 4 * a * c)) / (2 * a),
        (-b + -math.sqrt(b**2 - 4 * a * c)) / (2 * a),
    )


def get_time_to_hold_range(time, distance):
    min, max = quadratic(-1, time, -distance)

    min = math.floor(min + 1)
    max = math.ceil(max - 1)

    return (min, max)


if __name__ == "__main__":
    time_str, distance_str = open(sys.argv[1]).read().split("\n")[0:2]

    time = list(map(int, time_str.split()[1:]))
    distance = list(map(int, distance_str.split()[1:]))

    hold_time_product = 1

    for i in range(len(time)):
        min, max = get_time_to_hold_range(time[i], distance[i])
        hold_time_product *= max - min + 1

    print("(Part 1) Product of # of ways you can beat the record:", hold_time_product)

    time = int("".join(time_str.split()[1:]))
    distance = int("".join(distance_str.split()[1:]))

    min, max = get_time_to_hold_range(time, distance)

    print("(Part 2) # of ways you can be the single race:", max - min + 1)

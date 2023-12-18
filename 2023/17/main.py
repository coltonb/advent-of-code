"""
Today's code is courtesy of Reddit.
I took a stab at a non-PQ implementation that I am proud to say
was successful for the test case presented in the prompt,
but was non-optimal and took ~30 minutes to run against the puzzle
input.
"""

import sys
import heapq


def parse():
    return open(sys.argv[1]).read().strip().split("\n")


def shortest_path(city: list[str], min, max):
    queue = [(0, 0, 0, 0, 0)]
    visited = set()
    min_weights = {}

    while queue:
        weight, x, y, dx, dy = heapq.heappop(queue)

        if (x, y) == (len(city[0]) - 1, len(city) - 1):
            return weight

        if (x, y, dx, dy) in visited:
            continue

        min_weights[(x, y)] = weight
        visited.add((x, y, dx, dy))

        for dx, dy in {(1, 0), (-1, 0), (0, 1), (0, -1)} - {(dx, dy), (-dx, -dy)}:
            new_weight = weight
            new_x = x
            new_y = y

            for magnitude in range(1, max + 1):
                new_x += dx
                new_y += dy

                if (
                    new_x < 0
                    or new_x >= len(city[0])
                    or new_y < 0
                    or new_y >= len(city)
                ):
                    continue

                new_weight += int(city[new_y][new_x])

                if magnitude >= min:
                    heapq.heappush(queue, (new_weight, new_x, new_y, dx, dy))


city = parse()

print("(Part 1) Minimum heat:", shortest_path(city, 1, 3))
print("(Part 2) Minimum heat:", shortest_path(city, 4, 10))

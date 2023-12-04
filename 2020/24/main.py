import sys

# Part 1


# Parse instructions on given line and return list of instructions.
def parse_line(line):
    instructions = []
    skip = False

    for index in range(len(line)):
        char = line[index]

        if skip == True:
            skip = False
            continue
        if char == "n" or char == "s":
            instructions.append(line[index : index + 2])
            skip = True
        elif char == "\n":
            continue
        else:
            instructions.append(line[index])

    return instructions


# Get a hash key from a 3D coordinate.
def coord_key(x, y, z):
    return ",".join([str(x), str(y), str(z)])


# Hex can be represented as a 3D grid. Translates instructions to coordinates.
DIR_TO_COORD = dict(
    ne=(1, 0, -1),
    e=(1, -1, 0),
    se=(0, -1, 1),
    sw=(-1, 0, 1),
    w=(-1, 1, 0),
    nw=(0, 1, -1),
)


def count_black_tiles(tiles):
    return len([val for val in tiles.values() if val])


def part_1():
    tiles = {}

    with open(sys.argv[1]) as fp:
        for line in fp.readlines():
            x, y, z = (0, 0, 0)

            for instruction in parse_line(line):
                dx, dy, dz = DIR_TO_COORD[instruction]
                x += dx
                y += dy
                z += dz

            key = coord_key(x, y, z)
            tiles[key] = not tiles.get(key, False)

        return count_black_tiles(tiles), tiles


answer, tiles = part_1()
print("Part 1\nBlack tiles:", answer)


# Part 2
def check_adjacent(tiles, next_tiles, x, y, z, depth=0):
    key = coord_key(x, y, z)
    is_black = tiles.get(key, False)
    num_black_adjacent = 0

    for dx, dy, dz in DIR_TO_COORD.values():
        adjacent_x = x + dx
        adjacent_y = y + dy
        adjacent_z = z + dz

        # We only need to check our immediate neighbors
        if depth == 0:
            check_adjacent(
                tiles, next_tiles, adjacent_x, adjacent_y, adjacent_z, depth=1
            )

        adjacent_is_black = tiles.get(coord_key(x + dx, y + dy, z + dz), False)

        if adjacent_is_black:
            num_black_adjacent += 1

    if is_black:
        if num_black_adjacent != 0 and num_black_adjacent <= 2:
            next_tiles[key] = True
    else:
        if num_black_adjacent == 2:
            next_tiles[key] = True


def part_2(tiles, days):
    for day in range(days):
        next_tiles = {}

        for coord, is_black in tiles.items():
            if is_black:
                x, y, z = coord.split(",")

                x = int(x)
                y = int(y)
                z = int(z)

                check_adjacent(tiles, next_tiles, x, y, z)

        tiles = next_tiles

    return count_black_tiles(tiles)


print("Part 2\nBlack tiles:", part_2(tiles, 100))

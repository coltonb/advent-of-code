from typing import List
import sys


def sequence_differences(sequence: List[int]):
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def next_value(sequence: List[int]):
    if len(set(sequence)) == 1:
        return sequence[0]
    return sequence[-1] + next_value(sequence_differences(sequence))


if __name__ == "__main__":
    sequences = [
        list(map(int, line.strip().split())) for line in open(sys.argv[1]).readlines()
    ]

    sum_of_next_values = 0

    for sequence in sequences:
        sum_of_next_values += next_value(sequence)

    print("(Part 1) Sum:", sum_of_next_values)

    reversed_sequences = map(list, map(reversed, sequences))

    sum_of_previous_values = 0

    for sequence in reversed_sequences:
        sum_of_previous_values += next_value(sequence)

    print("(Part 2) Sum:", sum_of_previous_values)

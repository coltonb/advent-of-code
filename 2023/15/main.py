import sys
from collections import OrderedDict
import re

Box = OrderedDict[str, int]


def HASH_algorithm(s: str) -> int:
    current_value = 0

    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value %= 256

    return current_value


def parse() -> str:
    return open(sys.argv[1]).read().strip().split(",")


def create_boxes(initialization_sequence: str) -> list[Box]:
    boxes = [OrderedDict() for _ in range(256)]

    for step in initialization_sequence:
        label, operation, value = re.match("(.+?)([\-=])(\d+)?", step).groups()
        box_number = HASH_algorithm(label)

        if operation == "-":
            if label in boxes[box_number]:
                del boxes[box_number][label]
            continue

        boxes[box_number][label] = int(value)

    return boxes


def get_focusing_power(boxes: list[Box]) -> int:
    total = 0

    for i in range(256):
        for index, focal_length in enumerate(boxes[i].values()):
            total += (i + 1) * (index + 1) * focal_length

    return total


initialization_sequence = parse()

print("(Part 1) Sum:", sum([HASH_algorithm(step) for step in initialization_sequence]))
print(
    "(Part 2) Focusing power:",
    get_focusing_power(create_boxes(initialization_sequence)),
)

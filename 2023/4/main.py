import sys
import re
from typing import Set, List
from dataclasses import dataclass


@dataclass
class Card:
    id: int
    winning_numbers: Set[int]
    my_numbers: Set[int]

    @classmethod
    def parse(cls, line: str):
        id = int(re.search("Card\s+(\d+):", line).groups()[0])
        winning_numbers, my_numbers = [
            set(map(int, re.findall("\d+", numbers)))
            for numbers in re.split("Card\s+\d+:", line)[1].split("|")
        ]

        return Card(
            id=id,
            winning_numbers=winning_numbers,
            my_numbers=my_numbers,
        )

    @property
    def my_winning_numbers(self) -> Set[int]:
        return {number for number in self.my_numbers if number in self.winning_numbers}

    @property
    def points(self) -> int:
        my_winning_number_count = len(self.my_winning_numbers)

        if my_winning_number_count == 0:
            return 0

        return pow(2, my_winning_number_count - 1)


if __name__ == "__main__":
    total = 0
    cards: List[Card] = []

    with open(sys.argv[1]) as file:
        for line in file.readlines():
            card = Card.parse(line)
            total += card.points
            cards.append(card)

    print("(Part 1) Sum of points:", total)

    i = 0

    while len(cards) > i:
        current_card = cards[i]

        earned_cards = [
            cards[current_card.id + num]
            for num in range(len(cards[i].my_winning_numbers))
        ]

        cards.extend(earned_cards)
        i += 1

    print("(Part 2) Total scratchcards:", len(cards))

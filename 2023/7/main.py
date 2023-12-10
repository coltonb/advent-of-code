from __future__ import annotations
import sys
from typing import List
from dataclasses import dataclass
from functools import total_ordering

from enum import IntEnum


class PuzzlePart(IntEnum):
    PART_1 = 1
    PART_2 = 2


class Card(IntEnum):
    A = 14
    K = 13
    Q = 12
    J = 11
    T = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    JOKER = 1

    @classmethod
    def parse(cls, card: str, jokers_enabled: bool):
        return {
            "A": Card.A,
            "K": Card.K,
            "Q": Card.Q,
            "J": Card.J if not jokers_enabled else Card.JOKER,
            "T": Card.T,
            "9": Card.NINE,
            "8": Card.EIGHT,
            "7": Card.SEVEN,
            "6": Card.SIX,
            "5": Card.FIVE,
            "4": Card.FOUR,
            "3": Card.THREE,
            "2": Card.TWO,
        }[card]


class HandType(IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


@dataclass
@total_ordering
class Hand:
    cards: List[Card]
    bid: int

    @property
    def hand_type(self):
        groups = {}

        for card in self.cards:
            groups[card] = groups.get(card, 0) + 1

        jokers = groups.pop(Card.JOKER, 0)

        group_counts = list(sorted(groups.values(), reverse=True))

        if jokers == 5 or group_counts[0] + jokers == 5:
            return HandType.FIVE_OF_A_KIND

        if group_counts[0] + jokers == 4:
            return HandType.FOUR_OF_A_KIND

        if group_counts[0] + jokers == 3 and group_counts[1] == 2:
            return HandType.FULL_HOUSE

        if group_counts[0] + jokers == 3:
            return HandType.THREE_OF_A_KIND

        if group_counts[0] == 2 and group_counts[1] == 2:
            return HandType.TWO_PAIR

        if group_counts[0] + jokers == 2:
            return HandType.ONE_PAIR

        return HandType.HIGH_CARD

    def _lt_cards(self, other: Hand):
        for i in range(5):
            if self.cards[i] < other.cards[i]:
                return True
            if self.cards[i] > other.cards[i]:
                return False
        return False

    def __lt__(self, other: Hand):
        if self.hand_type < other.hand_type:
            return True

        if self.hand_type == other.hand_type and self._lt_cards(other):
            return True

        return False

    def __eq__(self, other: Hand):
        return self.cards == other.cards

    @classmethod
    def parse(cls, line: str, jokers_enabled: bool):
        cards, bid = line.split()

        return Hand([Card.parse(card, jokers_enabled) for card in cards], int(bid))


def print_winnings(lines, jokers_enabled: bool = False):
    hands = [Hand.parse(line, jokers_enabled) for line in lines]
    total = 0

    for index, hand in enumerate(sorted(hands)):
        total += (index + 1) * hand.bid

    print(f"Total winnings (with{'out' if not jokers_enabled else ''} jokers):", total)


if __name__ == "__main__":
    with open(sys.argv[1]) as file:
        lines = file.readlines()

    print_winnings(lines)
    print_winnings(lines, jokers_enabled=True)

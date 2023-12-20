import sys
import re
from dataclasses import dataclass


@dataclass
class Rule:
    category: str
    operator: str
    value: int
    outcome: str

    @classmethod
    def is_rule(cls, test: str):
        return "<" in test or ">" in test

    @classmethod
    def parse(cls, rule: str):
        if not cls.is_rule(rule):
            return rule

        category, operator, value, outcome = re.search(
            "([xmas])([><])(\d+):(.+)", rule
        ).groups()

        return cls(category, operator, int(value), outcome)


def parse_part(part: str):
    part = part[1:-1]
    result = {}

    for attribute in part.split(","):
        category, value = attribute.split("=")
        result[category] = int(value)

    return result


def load_rulesets_and_parts():
    rulesets, parts = open(sys.argv[1]).read().strip().split("\n\n")

    rules = {
        (parsed := re.search("(.+?){(.+?)}", ruleset).groups())[0]: [
            Rule.parse(rule) for rule in parsed[1].split(",")
        ]
        for ruleset in rulesets.split("\n")
    }

    parts = [parse_part(part) for part in parts.split("\n")]

    return rules, parts


def validate_part(part):
    ruleset = "in"
    rule = 0

    while ruleset not in "AR":
        current_rule = rulesets[ruleset][rule]

        if isinstance(current_rule, str):
            ruleset = current_rule
            rule = 0
            continue

        if (
            current_rule.operator == "<"
            and part[current_rule.category] < current_rule.value
        ) or (
            current_rule.operator == ">"
            and part[current_rule.category] > current_rule.value
        ):
            ruleset = current_rule.outcome
            rule = 0
            continue

        rule += 1

    return ruleset == "A"


rulesets, parts = load_rulesets_and_parts()

total = 0

for part in parts:
    if validate_part(part):
        total += sum(part.values())

print("(Part 1) Accepted part total:", total)

stack = [("in", 0, {"x": (1, 4000), "m": (1, 4000), "a": (1, 4000), "s": (1, 4000)})]
combinations = 0

while stack:
    ruleset, i, part = stack.pop()

    if ruleset == "A":
        combination = 1
        for interval in part.values():
            combination *= interval[1] - interval[0] + 1
        combinations += combination
        continue

    if ruleset == "R":
        continue

    rule = rulesets[ruleset][i]

    if isinstance(rule, str):
        stack.append((rule, 0, part))
        continue

    if rule.operator == "<" and part[rule.category][0] < rule.value:
        smaller = part.copy()
        smaller[rule.category] = (part[rule.category][0], rule.value - 1)
        stack.append((rule.outcome, 0, smaller))

        larger = part.copy()
        larger[rule.category] = (rule.value, part[rule.category][1])
        stack.append((ruleset, i + 1, larger))
        continue

    if rule.operator == ">" and part[rule.category][1] > rule.value:
        smaller = part.copy()
        smaller[rule.category] = (part[rule.category][0], rule.value)
        stack.append((ruleset, i + 1, smaller))

        larger = part.copy()
        larger[rule.category] = (rule.value + 1, part[rule.category][1])
        stack.append((rule.outcome, 0, larger))
        continue

print("(Part 2) Accepted part combinations:", combinations)

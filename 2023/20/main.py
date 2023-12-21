import math
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class Pulse(str, Enum):
    LOW = "low"
    HIGH = "high"


@dataclass
class Module(ABC):
    name: str
    outputs: set[str] = field(default_factory=lambda: set())
    inputs: set[str] = field(default_factory=lambda: set())

    @abstractmethod
    def receive_pulse(
        self, pulse: Pulse, sender: str
    ) -> Optional[list[tuple[str, Pulse]]]:
        ...


class ModuleFactory:
    @classmethod
    def create(cls, type: str, name: str, outputs: list[str]) -> Module:
        if type == "":
            return Broadcaster(name, outputs)
        if type == "&":
            return Conjunction(name, outputs)
        if type == "%":
            return FlipFlop(name, outputs)

    @classmethod
    def parse(cls, line: str) -> Module:
        type_and_name, outputs = line.split(" -> ")

        if type_and_name[0] not in "%&":
            type = ""
            name = type_and_name
        else:
            type = type_and_name[0]
            name = type_and_name[1:]

        outputs = set(outputs.split(", "))

        return cls.create(type, name, outputs)


@dataclass
class Broadcaster(Module):
    def receive_pulse(self, pulse, sender):
        return ([output for output in self.outputs], pulse, self.name)


@dataclass
class FlipFlop(Module):
    on: bool = False

    def receive_pulse(self, pulse, sender):
        if pulse == Pulse.HIGH:
            return

        pulse = Pulse.LOW if self.on else Pulse.HIGH
        self.on = not self.on

        return ([output for output in self.outputs], pulse, self.name)


@dataclass
class Conjunction(Module):
    _last_input: dict[str, Pulse] = field(default_factory=lambda: {})

    def receive_pulse(self, pulse, sender):
        self._last_input[sender] = pulse

        pulse = (
            Pulse.LOW
            if all(
                [
                    self._last_input.get(input, Pulse.LOW) == Pulse.HIGH
                    for input in self.inputs
                ]
            )
            else Pulse.HIGH
        )

        return ([output for output in self.outputs], pulse, self.name)


@dataclass
class Terminal(Module):
    def receive_pulse(self, pulse, sender):
        return


class Simulation:
    def __init__(self, modules: dict[str, Module]):
        self.modules = modules
        self.presses = 0
        self.low_pulses = 0
        self.high_pulses = 0
        self.pulse_queue: list[tuple[str, Pulse, str]] = []
        self.last_sent: dict[str, Pulse] = {}
        self._wire()

    def step(self, debug=False):
        modules, pulse, sender = self.pulse_queue.pop(0)

        self.last_sent[sender] = pulse

        for module in modules:
            if debug:
                print(f"{sender} -{pulse.value}-> {module}")

            if pulse == Pulse.LOW:
                self.low_pulses += 1
            else:
                self.high_pulses += 1

            output = self.modules[module].receive_pulse(pulse, sender)

            if output:
                self.pulse_queue.append(output)

    def run(self, debug=False):
        while self.pulse_queue:
            self.step(debug=debug)

    def press_button(self) -> tuple[int, int]:
        self.presses += 1
        self.pulse_queue.append((["broadcaster"], Pulse.LOW, "button"))

    def _wire(self):
        for module in list(self.modules.values()):
            for output in module.outputs:
                if output not in self.modules:
                    self.modules[output] = Terminal(output)

                output_module = self.modules[output]
                output_module.inputs.add(module.name)

    @classmethod
    def parse(cls, lines: list[str]):
        modules: dict[str, Module] = {}

        for line in lines:
            module = ModuleFactory.parse(line)
            modules[module.name] = module

        return Simulation(modules)


def parse():
    return Simulation.parse(open(sys.argv[1]).read().strip().split("\n"))


simulation = parse()

for i in range(1000):
    simulation.press_button()
    simulation.run()

print(
    "(Part 1) Product of pulses received:",
    simulation.low_pulses * simulation.high_pulses,
)

simulation = parse()

# The "rx" module is attached to single Conjunction module, which is then attached
# to four other Conjunction modules which cycle within a reasonable number of presses.
# Taking the LCM of the button press # when each sends a low pulse yields the answer.
# Consequently, this is hard-coded for convenience. Your module names may vary.
# See input.png for details

watch = ["nl", "rr", "pb", "dj"]
presses_until_low = {}

while watch:
    simulation.press_button()

    while simulation.pulse_queue:
        simulation.step()

        for module in list(watch):
            if simulation.last_sent.get(module) == Pulse.LOW:
                presses_until_low[module] = simulation.presses
                watch.remove(module)

print("(Part 2) Minimum presses:", math.lcm(*presses_until_low.values()))

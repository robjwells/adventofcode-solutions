from aoc_common import split_number_by_places
from collections import deque
from itertools import zip_longest
from operator import add, mul
from typing import Callable, Dict, List, NamedTuple, Tuple

PC_INCREMENT = 4
HALT = 99

ParameterModeList = List[int]


class Instruction(NamedTuple):
    opcode: int
    length: int
    store_result: bool
    action: Callable


class HaltExecution(Exception):
    pass


def halt_execution(*args):
    raise HaltExecution()


class IntCode:
    _PC: int
    _memory: List[int]
    _instructions: Dict[int, Instruction]
    _param_modes: Dict[int, Callable[[int], int]]
    input_queue: deque
    output_queue: deque

    def __init__(self, program: List[int]):
        self._PC = 0
        self._memory = program[:]
        self.input_queue = deque()
        self.output_queue = deque()

        self._instructions = {
            1: Instruction(1, 4, True, add),
            2: Instruction(2, 4, True, mul),
            3: Instruction(3, 2, True, self.input_queue.popleft),
            4: Instruction(4, 2, False, self.output_queue.append),
            99: Instruction(99, 1, False, halt_execution),
        }

        self._param_modes = {0: self._load, 1: lambda immediate: immediate}

    def _store(self, value: int, address: int) -> None:
        self._memory[address] = value

    def _load(self, address: int) -> int:
        return self._memory[address]

    def parse_opcode(self, full_opcode: int) -> Tuple[Instruction, ParameterModeList]:
        modes, opcode = divmod(full_opcode, 100)
        # Reverse the mode list as the modes are given in reverse order
        # in the 'full' opcode.
        mode_list = list(reversed(split_number_by_places(modes)))
        return mode_list, self._instructions[opcode]

    def load_parameters(self, parameters: List[int], modes: ParameterModeList):
        return [
            self._param_modes[mode](param)
            for param, mode in zip_longest(parameters, modes, fillvalue=0)
        ]

    def step(self) -> None:
        opcode = self._memory[self._PC]
        parameter_modes, instruction = self.parse_opcode(opcode)
        _, length, store_result, action = instruction
        args = self._memory[self._PC + 1 : self._PC + length]
        if store_result:
            parameters = self.load_parameters(args[:-1], parameter_modes)
            destination = args[-1]
            result = action(*parameters)
            self._store(result, destination)
        else:
            parameters = self.load_parameters(args, parameter_modes)
            action(*parameters)
        self._PC += length

    def run_until_halt(self) -> None:
        try:
            while True:
                self.step()
        except HaltExecution:
            pass

    @classmethod
    def execute_program(cls, input_data: List[int]) -> List[int]:
        computer = cls(input_data)
        computer.run_until_halt()
        return computer._memory

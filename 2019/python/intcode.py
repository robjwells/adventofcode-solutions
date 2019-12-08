from aoc_common import split_number_by_places
from collections import deque
from itertools import zip_longest
from operator import add, mul
from typing import Callable, Dict, List, NamedTuple, Optional, Tuple

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
    _PC_modified: bool
    _memory: List[int]
    _instructions: Dict[int, Instruction]
    _param_modes: Dict[int, Callable[[int], int]]
    _input_action: Callable[[int], None]
    _output_action: Callable[[], int]
    input_queue: deque
    output_queue: deque

    def __init__(
        self,
        program: List[int],
        input_action: Optional[Callable[[int], None]] = None,
        output_action: Optional[Callable[[], int]] = None,
    ):
        self._PC = 0
        self._PC_modified = False
        self._memory = program[:]

        self.input_queue = deque()
        self.output_queue = deque()

        if input_action is not None:
            self._input_action = input_action
        else:
            self._input_action = self.input_queue.popleft

        if output_action is not None:
            self._output_action = output_action
        else:
            self._output_action = self.output_queue.append

        self._instructions = {
            1: Instruction(1, 4, True, add),
            2: Instruction(2, 4, True, mul),
            3: Instruction(3, 2, True, self._input_action),
            4: Instruction(4, 2, False, self._output_action),
            5: Instruction(5, 3, False, self._jump_if_true),
            6: Instruction(6, 3, False, self._jump_if_false),
            7: Instruction(7, 4, True, lambda a, b: int(a < b)),
            8: Instruction(8, 4, True, lambda a, b: int(a == b)),
            99: Instruction(99, 1, False, halt_execution),
        }

        self._param_modes = {0: self._load, 1: lambda immediate: immediate}

    def _store(self, value: int, address: int) -> None:
        self._memory[address] = value

    def _load(self, address: int) -> int:
        return self._memory[address]

    def _jump_if_true(self, first: int, second: int) -> None:
        if first:
            self._PC = second
            self._PC_modified = True

    def _jump_if_false(self, first: int, second: int) -> None:
        return self._jump_if_true(not first, second)

    def parse_opcode(self, full_opcode: int) -> Tuple[ParameterModeList, Instruction]:
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

        if not self._PC_modified:
            self._PC += length
        else:
            self._PC_modified = False

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

    def pass_input(self, value: int) -> None:
        self.input_queue.append(value)

    def has_output(self) -> bool:
        return len(self.output_queue) == 0

    def read_output(self) -> int:
        return self.output_queue.popleft()


def parse_program(puzzle_input: str) -> List[int]:
    return [int(x) for x in puzzle_input.split(",")]

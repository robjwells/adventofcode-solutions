from collections import deque
from operator import add, mul
from typing import Callable, Dict, List, NamedTuple

PC_INCREMENT = 4
HALT = 99


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
            4: Instruction(
                4, 2, False, lambda src: self.output_queue.append(self._load(src))
            ),
            99: Instruction(99, 1, False, halt_execution),
        }

    def _store(self, value: int, address: int) -> None:
        self._memory[address] = value

    def _load(self, address: int) -> int:
        return self._memory[address]

    def opcode_to_function(self, opcode: int) -> Instruction:
        return self._instructions[opcode]

    def step(self) -> None:
        opcode = self._memory[self._PC]
        _, length, store_result, action = self._instructions[opcode]
        args = self._memory[self._PC + 1 : self._PC + length]
        if store_result:
            loaded_args, destination = map(self._load, args[:-1]), args[-1]
            result = action(*loaded_args)
            self._store(result, destination)
        else:
            action(*args)
        self._PC += length

    @classmethod
    def execute_program(cls, input_data: List[int]) -> List[int]:
        computer = cls(input_data)
        try:
            while True:
                computer.step()
        except HaltExecution:
            return computer._memory

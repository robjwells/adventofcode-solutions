from __future__ import annotations

from collections import deque
from operator import add, mul
from typing import (
    Callable,
    Deque,
    Dict,
    List,
    NamedTuple,
    NoReturn,
    Optional,
    Tuple,
    Union,
)

from aoc import split_number_by_places

ParameterModeList = List[int]


class Instruction(NamedTuple):
    opcode: int
    length: int
    store_result: bool
    action: Union[
        Callable[[int, int], int],
        Callable[[int, int], None],
        Callable[[int], None],
        Callable[[], int],
        Callable[[], NoReturn],
    ]


class HaltExecution(Exception):
    pass


class IntCode:
    _PC: int
    _PC_modified: bool
    _PC_pending_increment: Optional[int] = None
    _relative_addressing_base: int = 0
    _memory: List[int]
    _instructions: Dict[int, Instruction]
    _param_modes: Dict[int, Callable[[int], int]]
    _has_halted: bool = False
    input_action: Callable[[int], None]
    output_action: Callable[[], int]
    input_queue: Deque[int]
    output_queue: Deque[int]
    _description: str

    def __init__(
        self,
        program: List[int],
        input_action: Optional[Callable[[int], None]] = None,
        output_action: Optional[Callable[[], int]] = None,
        description: Optional[str] = None,
    ):
        self._PC = 0
        self._PC_modified = False
        self._memory = program[:]

        self.input_queue = deque()
        self.output_queue = deque()

        if description is not None:
            self._description = description
        else:
            self._description = f"<IntCode @ {id(self)}"

        if input_action is not None:
            self.input_action = input_action  # type: ignore
        else:
            self.input_action = self.input_queue.popleft  # type: ignore

        if output_action is not None:
            self.output_action = output_action  # type: ignore
        else:
            self.output_action = self.output_queue.append  # type: ignore

        self._instructions = {
            1: Instruction(1, 4, True, add),
            2: Instruction(2, 4, True, mul),
            3: Instruction(3, 2, True, self._input),
            4: Instruction(4, 2, False, self._output),
            5: Instruction(5, 3, False, self._jump_if_true),
            6: Instruction(6, 3, False, self._jump_if_false),
            7: Instruction(7, 4, True, lambda a, b: int(a < b)),
            8: Instruction(8, 4, True, lambda a, b: int(a == b)),
            9: Instruction(9, 2, False, self._adjust_relative_base),
            99: Instruction(99, 1, False, self._halt_execution),
        }

        self._param_modes = {
            # Direct addressing
            0: self._load,
            # Immediate addressing
            1: lambda immediate: immediate,
            # Base + offset (relative) addressing
            2: lambda offset: self._load(self._relative_addressing_base + offset),
        }

    def __repr__(self) -> str:
        return self._description

    def _ensure_memory_capacity(self, index: int) -> None:
        """Extend memory with zeroes to accommodate given index."""
        if index < len(self._memory):
            return
        new_allocation = [0 for _ in range(index * 2)]
        new_allocation[0 : len(self._memory)] = self._memory
        self._memory = new_allocation

    def _store(self, value: int, address: int) -> None:
        self._ensure_memory_capacity(address)
        self._memory[address] = value

    def _load(self, address: int) -> int:
        self._ensure_memory_capacity(address)
        return self._memory[address]

    def _halt_execution(self) -> NoReturn:
        self._has_halted = True
        raise HaltExecution()

    def has_halted(self) -> bool:
        return self._has_halted

    def _jump_if_true(self, first: int, second: int) -> None:
        if first:
            self._PC = second
            self._PC_modified = True

    def _jump_if_false(self, first: int, second: int) -> None:
        return self._jump_if_true(not first, second)

    def _adjust_relative_base(self, adjustment: int) -> None:
        self._relative_addressing_base += adjustment

    def parse_opcode(self, full_opcode: int) -> Tuple[ParameterModeList, Instruction]:
        modes, opcode = divmod(full_opcode, 100)
        # Reverse the mode list as the modes are given in reverse order
        # in the 'full' opcode.
        mode_list = list(reversed(split_number_by_places(modes)))
        if len(mode_list) < 5:
            mode_list += [0 for _ in range(5 - len(mode_list))]
        return mode_list, self._instructions[opcode]

    def _parse_destination_address(self, raw_address: int, mode: int) -> int:
        if mode == 0:
            # Direct addressing
            return raw_address
        if mode == 2:
            # Base + offset addressing
            return self._relative_addressing_base + raw_address
        raise ValueError("Unknown destination parameter mode.")

    def load_parameters(
        self, parameters: List[int], modes: ParameterModeList
    ) -> List[int]:
        return [
            self._param_modes[mode](param) for param, mode in zip(parameters, modes)
        ]

    def step(self) -> None:
        if self._PC_pending_increment is not None:
            # Handle early termination of the step function
            self._PC += self._PC_pending_increment

        opcode = self._memory[self._PC]
        parameter_modes, instruction = self.parse_opcode(opcode)
        _, length, store_result, action = instruction
        args = self._memory[self._PC + 1 : self._PC + length]
        # Ensure 1-to-1 match between parameters (in args) and modes
        parameter_modes = parameter_modes[: len(args)]

        self._PC_pending_increment = length

        if store_result:
            parameters = self.load_parameters(args[:-1], parameter_modes[:-1])
            destination = self._parse_destination_address(args[-1], parameter_modes[-1])
            result = action(*parameters)
            assert isinstance(result, int)
            self._store(result, destination)
        else:
            parameters = self.load_parameters(args, parameter_modes)
            action(*parameters)

        if not self._PC_modified:
            self._PC += length
        else:
            self._PC_modified = False
        self._PC_pending_increment = None

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
        return len(self.output_queue) != 0

    def read_output(self) -> int:
        return self.output_queue.popleft()

    def _input(self) -> int:
        return self.input_action()  # type: ignore

    def _output(self, value: int) -> None:
        self.output_action(value)  # type: ignore

    def clone(self) -> IntCode:
        new = IntCode(
            program=[],
            description=self._description,
        )
        new._memory = self._memory[:]
        new._PC = self._PC
        new._PC_modified = self._PC_modified
        new._PC_pending_increment = self._PC_pending_increment
        new._relative_addressing_base = self._relative_addressing_base
        new._has_halted = self._has_halted
        new.input_queue = deque(self.input_queue)
        new.input_action = new.input_queue.popleft
        new.output_queue = deque(self.output_queue)
        new.output_action = new.output_queue.append

        return new


def parse_program(puzzle_input: str) -> List[int]:
    return [int(x) for x in puzzle_input.split(",")]

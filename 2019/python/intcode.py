from operator import add, mul
from typing import Callable, List

PC_INCREMENT = 4
HALT = 99


class IntCode:

    _functions = {1: add, 2: mul}

    def opcode_to_function(self, opcode: int) -> Callable[[int, int], int]:
        return self._functions[opcode]

    def execute_program(self, input_data: List[int]) -> List[int]:
        data = input_data[:]
        for program_counter in range(0, len(data), PC_INCREMENT):
            opcode, *locations = data[program_counter : program_counter + PC_INCREMENT]
            if opcode == HALT:
                break
            source1, source2, destination = locations
            data[destination] = self.opcode_to_function(opcode)(
                data[source1], data[source2]
            )
        return data

from typing import List

import pytest

from intcode import IntCode


@pytest.mark.parametrize(
    "input_data,output_data",
    [
        ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
        ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
        ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
        ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]),
    ],
)
def test_execute_program(input_data: List[int], output_data: List[int]) -> None:
    assert IntCode.execute_program(input_data) == output_data

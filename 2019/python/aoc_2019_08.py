"""Day 8: Space Image Format"""
from typing import Iterator, List, Tuple

import aoc_common

DAY = 8


class SpaceImage:
    width: int
    height: int
    layers_count: int
    _data: List[int]

    def __init__(self, width: int, height: int, image_data: str) -> None:
        self.width = width
        self.height = height
        self._data = self._data_string_to_digit_list(image_data)
        layers_count = len(self._data) / (width * height)
        assert layers_count.is_integer(), (
            "Image data contains an incomplete number of layers"
            f" ({layers_count}) for the given width ({width})"
            f" and height ({height})."
        )
        self.layers_count = int(layers_count)

    @staticmethod
    def _data_string_to_digit_list(data: str) -> List[int]:
        return [int(character) for character in data.strip()]

    def __str__(self) -> str:
        return "SpaceImage(width: {w}, height: {h}, layers: {lc})".format(
            w=self.width, h=self.height, lc=self.layers_count
        )

    def __iter__(self) -> Iterator[List[int]]:
        pixels_per_layer = self.width * self.height
        for layer_index in range(self.layers_count):
            layer_start = pixels_per_layer * layer_index
            yield self._data[layer_start : layer_start + pixels_per_layer]

    @staticmethod
    def _first_non_transparent_pixel_value(pixels: Tuple[int, ...]) -> int:
        for pixel in pixels:
            if pixel != 2:
                return pixel  # First (ie on highest layer) non-transparent pixel
        return 2  # Transparent

    def compute_visible(self) -> List[List[int]]:
        visible_pixels = [
            self._first_non_transparent_pixel_value(stack) for stack in zip(*iter(self))
        ]
        return [
            visible_pixels[row_num * self.width : (row_num * self.width) + self.width]
            for row_num in range(self.height)
        ]


def test_SpaceImage() -> None:
    width, height = (3, 2)
    data = "123456789012"
    image = SpaceImage(width, height, data)

    expected_layers = [[1, 2, 3, 4, 5, 6], [7, 8, 9, 0, 1, 2]]
    assert list(image) == expected_layers


def test_compute_visible() -> None:
    width, height = (2, 2)
    data = "0222112222120000"
    image = SpaceImage(width, height, data)

    expected = [[0, 1], [1, 0]]
    assert image.compute_visible() == expected


def main(image: SpaceImage) -> Tuple[int, str]:
    # Part one
    layer_with_least_zeroes = min(image, key=lambda layer: layer.count(0))
    checksum = layer_with_least_zeroes.count(1) * layer_with_least_zeroes.count(2)

    # Part two
    rendered_image = "\n".join(
        "".join("█" if pixel else " " for pixel in row)
        for row in image.compute_visible()
    )
    return checksum, rendered_image


if __name__ == "__main__":
    image_data = aoc_common.load_puzzle_input(DAY)
    image = SpaceImage(width=25, height=6, image_data=image_data)
    part_one_solution, part_two_solution = main(image)
    assert (
        part_one_solution == 2413
    ), "Part one solution does not match known-correct answer."

    part_two_expected = """\
███   ██  ███  ████ ███
█  █ █  █ █  █    █ █  █
███  █    █  █   █  ███
█  █ █    ███   █   █  █
█  █ █  █ █    █    █  █
███   ██  █    ████ ███
""".strip()
    part_two_stripped = "\n".join(
        line.strip() for line in part_two_solution.splitlines()
    )
    assert (
        part_two_stripped == part_two_expected
    ), "Part two solution does not match saved known-correct solution."

    aoc_common.report_solution(
        puzzle_title=__doc__,
        part_one_solution=part_one_solution,
        part_two_solution="\n\n" + part_two_solution,
        # Prepend newlines to the image string to clear "Part two solution".
    )

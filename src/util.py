import random
import typing as t


NUMBER = t.Union[float, int]


def number_remap(
    value: float,
    old_min: float,
    old_max: float,
    new_min: float,
    new_max: float
) -> float:
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min


class Colors:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREY = 125, 125, 125
    RED = 240, 20, 30
    GREEN = 30, 255, 20
    BLUE = 100, 0, 255
    YELLOW = 255, 255, 0

    ColorType = t.Tuple[int, int, int]

    @staticmethod
    def random() -> ColorType:
        return (random.randint(100, 255), 0, random.randint(100, 255))

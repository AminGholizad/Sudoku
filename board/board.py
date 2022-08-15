from abc import ABC, abstractmethod

import numpy as np
from numpy.typing import NDArray

from rules.rule import Rule


class Board(ABC):

    @abstractmethod
    def set_cell_value(self, row: int, col: int, val: int) -> 'Board':
        pass

    @abstractmethod
    def get_cell_value(self, row: int, col: int) -> int:
        pass

    @abstractmethod
    def is_cell_empty(self, row: int, col: int) -> bool:
        pass

    @abstractmethod
    def valid_numbers(self, rules: list[Rule], row: int, col: int) -> NDArray[np.int_]:
        pass

    @abstractmethod
    def is_board_solved(self, rules: list[Rule]) -> bool:
        pass

    @abstractmethod
    def is_board_valid(self, rules: list[Rule]) -> bool:
        pass

    @abstractmethod
    def copy(self) -> 'Board':
        pass

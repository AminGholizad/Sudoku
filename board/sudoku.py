from functools import reduce
from typing import Optional

import numpy as np
from numpy.typing import NDArray

from rules import Rule

from .board import Board


class Sudoku(Board):
    __slots__ = 'board',

    def __init__(self, board: Optional[NDArray[np.int_] | list[list[int]] | list[int]] = None):
        if board is None:
            board = np.array([0]*81)
        self.board = np.array(board).reshape(9, 9)

    def set_cell_value(self, row: int, col: int, val: int) -> 'Sudoku':
        self.board[row, col] = val
        return self

    def get_cell_value(self, row: int, col: int) -> int:
        return self.board[row, col]

    def is_cell_empty(self, row: int, col: int) -> bool:
        return self.get_cell_value(row, col) == 0

    def valid_numbers(self, rules: list[Rule], row: int, col: int) -> NDArray[np.int_]:
        if not self.is_cell_empty(row, col):
            return np.array([])
        valid_nums = [rule.valid_numbers(
            self.board, row, col) for rule in rules]
        return reduce(lambda x, y: np.intersect1d(x, y), valid_nums)

    def is_board_solved(self, rules: list[Rule]) -> bool:
        if np.any(self.board == 0):
            return False
        return np.all([rule.is_solved(self.board) for rule in rules])

    def is_board_valid(self, rules: list[Rule]) -> bool:
        flat_board = self.board  # .reshape(81)
        if np.any(flat_board > 9) or np.any(flat_board < 0):
            return False
        return np.all([rule.is_valid(self.board) for rule in rules])

    def copy(self) -> 'Sudoku':
        return Sudoku(self.board)

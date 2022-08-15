import numpy as np
from numpy.typing import NDArray

from .rule import Rule


class RowRule(Rule):
    def valid_numbers(self, board: NDArray[np.int_], row: int, col: int) -> NDArray[np.int_]:
        return np.setdiff1d(range(1, 10), board[row, :])

    def is_valid(self, board: NDArray[np.int_]) -> bool:
        for row in board:
            _, counts = np.unique(row[row != 0], return_counts=True)
            if np.any(counts > 1):
                return False
        return True

    def is_solved(self, board: NDArray[np.int_]) -> bool:
        return np.all(np.sum(board, 0) == 45)


class ColRule(Rule):
    def valid_numbers(self, board: NDArray[np.int_], row: int, col: int) -> NDArray[np.int_]:
        return np.setdiff1d(range(1, 10), board[:, col])

    def is_valid(self, board: NDArray[np.int_]) -> bool:
        for col in board.T:
            _, counts = np.unique(col[col != 0], return_counts=True)
            if np.any(counts > 1):
                return False
        return True

    def is_solved(self, board: NDArray[np.int_]) -> bool:
        return np.all(np.sum(board, 1) == 45)


class SquareRule(Rule):
    def valid_numbers(self, board: NDArray[np.int_], row: int, col: int) -> NDArray[np.int_]:
        xl = row//3*3
        yl = col//3*3
        return np.setdiff1d(range(1, 10), board[xl:xl+3, yl:yl+3].reshape(9))

    def is_valid(self, board: NDArray[np.int_]) -> bool:
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                sq = board[i:i+3, j:j+3].reshape(9)
                _, counts = np.unique(sq[sq != 0], return_counts=True)
                if np.any(counts > 1):
                    return False
        return True

    def is_solved(self, board: NDArray[np.int_]) -> bool:
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if np.sum(board[i:i+3, j:j+3]) != 45:
                    return False
        return True

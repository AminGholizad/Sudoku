from sys import stderr
from typing import Optional

import numpy as np
from numpy.typing import NDArray


class Board:
    def __init__(self, board: Optional[NDArray[np.int_] | list[list[int]] | list[int]] = None):
        if board is None:
            board = np.array([0]*81)
        self.board = np.array(board).reshape(9, 9)

    def set_cell_value(self, row: int, col: int, val: int) -> 'Board':
        self.board[row, col] = val
        return self

    def get_value(self, row: int, col: int) -> int:
        return self.board[row, col]

    def is_cell_empty(self, row: int, col: int) -> bool:
        return self.board[row, col] == 0

    def valid_numbers(self, row: int, col: int) -> NDArray[np.int_]:
        if self.board[row, col] == 0:
            board_row = self.board[row, :]
            board_col = self.board[:, col]
            xl = row//3*3
            yl = col//3*3
            sq = self.board[xl:xl+3, yl:yl+3].reshape(9)
            return np.setdiff1d(range(1, 10), [board_row, board_col, sq])
        else:
            return np.array([])

    def copy(self) -> 'Board':
        return Board(self.board)

    def print_board(self) -> None:
        for r in range(9):
            if r % 3 == 0:
                print('-'*25)
            for c in range(9):
                if c % 3 == 0:
                    print('| ', end='')
                print(self.board[r, c], end=' ')
            print('|')
        print('-'*25)

    def is_board_solved(self) -> bool:
        if np.any(self.board == 0):
            return False
        rowSum = np.sum(self.board, 0)
        colSum = np.sum(self.board, 1)
        if np.any(rowSum != 45) or np.any(colSum != 45):
            return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                if np.sum(self.board[i:i+3, j:j+3]) != 45:
                    return False
        return True

    def is_board_valid(self) -> bool:
        b = self.board
        if np.any(b > 9) or np.any(b < 0):
            return False
        for r in b:
            x = np.sort(r[r != 0])
            if np.any(x[1:] == x[:-1]):
                return False
        for c in b.T:
            x = np.sort(c[c != 0])
            if np.any(x[1:] == x[:-1]):
                return False
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                x = self.board[i:i+3, j:j+3].reshape(9)
                x = np.sort(x[x != 0])
                if np.any(x[1:] == x[:-1]):
                    return False
        return True

    def solve(self, visual: bool = False, screen_width: int = 40, screen_height: int = 40, cell_margin: int = 6) -> Optional['Board']:
        if not self.is_board_valid():
            print("Board is not valid! Can't be solved!", file=stderr)
            return None
        if visual:
            cp, o = self.isolve_visual(
                w=screen_width, h=screen_height, m=cell_margin)
        else:
            cp, o = self.isolve()
        if o:
            return cp
        else:
            print("There is no valid solutions!", file=stderr)
            return None

    def isolve(self, ir: int = 0, ic: int = 0) -> tuple['Board', bool]:
        if self.is_board_solved():
            return self, True
        for r in range(ir, 9):
            if ir != r:
                ic = 0
            for c in range(ic, 9):
                if self.is_cell_empty(r, c):
                    for v in self.valid_numbers(r, c):
                        cp, o = self.copy().set_cell_value(r, c, v).isolve(r, c+1)
                        if o:
                            return cp, True
                    return self, False
        return self, False

    def isolve_visual(self, ir: int = 0, ic: int = 0, w: int = 40, h: int = 40, m: int = 6) -> tuple['Board', bool]:
        from gui import Grid
        Grid(self, cell_width=w, cell_height=h, cell_margin=m).display()
        if self.is_board_solved():
            return self, True
        for r in range(ir, 9):
            if ir != r:
                ic = 0
            for c in range(ic, 9):
                if self.is_cell_empty(r, c):
                    for v in self.valid_numbers(r, c):
                        cp, o = self.copy().set_cell_value(
                            r, c, v).isolve_visual(ir=r, ic=c+1, w=w, h=h, m=m)
                        if o:
                            return cp, True
                    return self, False
        return self, False

    def is_solvable(self) -> bool:
        if self.solve() is not None:
            return True
        return False


def test(iteration: int = 100, *, visual: bool = False):
    from time import time
    s = Board(np.array([[1, 0, 0, 0, 0, 0, 5, 0, 0],
                        [0, 0, 0, 8, 0, 0, 0, 0, 0],
                        [0, 0, 9, 0, 0, 0, 0, 6, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 7, 0, 0, 0, 0],
                        [0, 0, 0, 0, 4, 0, 0, 3, 0],
                        [0, 3, 0, 0, 0, 0, 0, 0, 0],
                        [2, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 0, 0, 0, 1, 0]]))
    t1 = time()
    if not visual:
        s.print_board()
    solved = None
    for _ in range(iteration):
        solved = s.solve(visual)
    t2 = time()
    if not visual:
        print(
            f'It took {(t2-t1)/iteration:0.04} seconds on average over {iteration} ireterations')
        if solved:
            solved.print_board()


if __name__ == "__main__":
    test(1, visual=False)
    test(1, visual=True)

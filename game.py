from sys import stderr
from typing import Optional

import numpy as np

from board import Board, Sudoku
from gui import Grid
from rules import ColRule, RowRule, Rule, SquareRule


class Game:
    __slots__ = 'board', 'rules'

    def __init__(self, board: Optional[Board], rules: Optional[list[Rule]] = None):
        if board is None:
            self.board = Sudoku()
        else:
            self.board = board
        self.set_rules(rules)

    def set_rules(self, rules: Optional[list[Rule]] = None) -> None:
        if rules is not None:
            self.rules = rules
        else:
            self.rules = [
                RowRule(),
                ColRule(),
                SquareRule()
            ]

    def copy(self) -> 'Game':
        return Game(self.board.copy())

    def __str__(self) -> str:
        out: str = ''
        for row in range(9):
            if row % 3 == 0:
                out += '-'*25 + '\n'
            for col in range(9):
                if col % 3 == 0:
                    out += '| '
                out += f'{self.board.board[row, col]} '
            out += '|\n'
        out += '-'*25
        return out

    def solve(self, grid: Optional[Grid] = None) -> Optional['Game']:
        if not self.board.is_board_valid(self.rules):
            print("Board is not valid! Can't be solved!", file=stderr)
            return None

        solved_board, is_solved = self.isolve(grid=grid)

        if is_solved:
            return solved_board

        print("There is no valid solutions!", file=stderr)
        return None

    def isolve(self, ir: int = 0, ic: int = 0, grid: Optional[Grid] = None) -> tuple['Game', bool]:
        if grid is not None:
            grid.update_grid(self.board).display()
        board = self.board
        rules = self.rules
        if board.is_board_solved(rules):
            return self, True
        for r in range(ir, 9):
            if ir != r:
                ic = 0
            for c in range(ic, 9):
                if board.is_cell_empty(r, c):
                    for v in board.valid_numbers(rules, r, c):
                        cp = self.copy()
                        cp.board.set_cell_value(r, c, v)
                        cp, o = cp.isolve(ir=r, ic=c+1, grid=grid)
                        if o:
                            return cp, True
                    return self, False
        return self, False

    def is_solvable(self) -> bool:
        return self.solve() is not None


def test(*, iteration: int = 1, visual: bool = False):
    from time import time
    s = Game(Sudoku(np.array([[1, 0, 0, 0, 0, 0, 5, 0, 0],
                              [0, 0, 0, 8, 0, 0, 0, 0, 0],
                              [0, 0, 9, 0, 0, 0, 0, 6, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 7, 0, 0, 0, 0],
                              [0, 0, 0, 0, 4, 0, 0, 3, 0],
                              [0, 3, 0, 0, 0, 0, 0, 0, 0],
                              [2, 0, 1, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 2, 0, 0, 0, 1, 0]])))
    grid = Grid(board=s.board, cell_width=40, cell_height=40,
                cell_margin=6) if visual else None
    t1 = time()
    if not visual:
        print(s)
    solved = None
    for _ in range(iteration):
        solved = s.solve(grid)
    t2 = time()
    if not visual:
        print(
            f'It took {(t2-t1)/iteration:0.04} seconds on average over {iteration} ireterations')
        if solved:
            print(solved)


if __name__ == "__main__":
    test(iteration=10)
    test(visual=True)

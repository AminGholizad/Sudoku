import numpy as np
from sys import stderr


class Board(object):
    def __init__(self, b=None):
        if b is None:
            b = np.array([0]*81)
        self.board = np.array(b).reshape(9, 9)

    def setCellValue(self, r, c, v):
        self.board[r, c] = v
        return self

    def getValue(self, r, c):
        return self.board[r, c]

    def isCellEmpty(self, r, c):
        return self.board[r, c] == 0

    def validNumbers(self, r, c):
        if self.board[r, c] == 0:
            row = self.board[r, :]
            col = self.board[:, c]
            xl = r//3*3
            yl = c//3*3
            sq = self.board[xl:xl+3, yl:yl+3].reshape(9)
            return np.setdiff1d(range(1, 10), [row, col, sq])
        else:
            return np.array([])

    def copy(self):
        return Board(self.board)

    def printBoard(self):
        for r in range(9):
            if r % 3 == 0:
                print('-'*25)
            for c in range(9):
                if c % 3 == 0:
                    print('| ', end='')
                print(self.board[r, c], end=' ')
            print('|')
        print('-'*25)

    def isBoardSolved(self):
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

    def isBoardValid(self):
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

    def solve(self, visual=False, w=40, h=40, m=6):
        if not self.isBoardValid():
            print("Board is not valid! Can't be solved!", file=stderr)
            return None
        if visual:
            cp, o = self.isolveVisual(w=w, h=h, m=m)
        else:
            cp, o = self.isolve()
        if o:
            return cp
        else:
            print("There is no valid solutions!", file=stderr)
            return None

    def isolve(self, ir=0, ic=0):
        if self.isBoardSolved():
            return self, True
        for r in range(ir, 9):
            if ir != r:
                ic = 0
            for c in range(ic, 9):
                if self.isCellEmpty(r, c):
                    for v in self.validNumbers(r, c):
                        cp, o = self.copy().setCellValue(r, c, v).isolve(r, c+1)
                        if o:
                            return cp, True
                    return self, False

    def isolveVisual(self, ir=0, ic=0, w=40, h=40, m=6):
        from gui import Grid
        Grid(self, w=w, h=h, m=m).display()
        if self.isBoardSolved():
            return self, True
        for r in range(ir, 9):
            if ir != r:
                ic = 0
            for c in range(ic, 9):
                if self.isCellEmpty(r, c):
                    for v in self.validNumbers(r, c):
                        cp, o = self.copy().setCellValue(r, c, v).isolveVisual(ir=r, ic=c+1, w=w, h=h, m=m)
                        if o:
                            return cp, True
                    return self, False

    def isSolvable(self):
        if self.solve() is not None:
            return True
        return False


def test(iter=100, visual=False):
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
        s.printBoard()
    for i in range(iter):
        solved = s.solve(visual)
    t2 = time()
    if not visual:
        print(
            f'It took {(t2-t1)/iter:0.04} seconds on average over {iter} ireterations')
        solved.printBoard()


if __name__ == "__main__":
    test(1, True)

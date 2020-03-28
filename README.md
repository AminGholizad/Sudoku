# Sudoku
Sudoku Solver with backtracking algorithm

# Features
1. A fast Sudoku solver using backtracking algorithm.
2. The board is implemented in numpy arrays for speed gain.
3. A simple GUI is implemented in pygame.

# GUI usage
There are two modes play mode and design mode. In play mode select a cell with mouse click and input your guess. You can remove your guess  with backspace. Use enter key to check your guess if its valid it will become permanent and if its not valid it will be removed. you can use space key to simulate backtracking algorithm to solve the rest of the puzzle.
Press ctrl+n to enter design mode. In this mode you can set a cell value without pressing enter if a solution exists it will be shown in the cell otherwise it will be removed. After completing the design press ctrl+s to enter play mode.

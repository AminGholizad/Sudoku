from enum import Enum, auto
from time import time

import pygame

from board import Board, Sudoku


class Mode(Enum):
    PLAY = auto()
    DESIGN = auto()


class Grid:
    __slots__ = 'cell_width', 'cell_height', 'cell_margin', 'selected', 'mode', 'grid'

    def __init__(self, board: Board, cell_width: int = 40, cell_height: int = 40, cell_margin: int = 6):
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_margin = cell_margin
        self.selected: tuple[int, int] | None = None
        self.mode = Mode.PLAY
        self.update_grid(board)

    def set_selected(self, new_row: int, new_col: int) -> 'Grid':
        try:
            row, col = self.get_selected()
            self.grid[row][col].deselect()
        except ValueError:
            pass
        self.grid[new_row][new_col].select()
        self.selected = (new_row, new_col)
        return self

    def get_selected(self) -> tuple[int, int]:
        if self.selected is None:
            raise ValueError
        return self.selected

    def draw_screen(self, screen: pygame.surface.Surface) -> None:
        for row in range(9):
            screen_row = pygame.Surface((self.get_width(), self.cell_height))
            screen_row.fill((0, 0, 0))
            for col in range(9):
                self.grid[row][col].draw(screen_row)
            screen.blit(
                screen_row, (self.cell_margin//2, self.cell_height*row+self.cell_margin*(row//3+1)))

    def display(self, duration: float = 0.01) -> None:
        pygame.init()
        screen = pygame.display.set_mode(self.get_size())
        pygame.display.set_caption('Soduku')
        clock = pygame.time.Clock()
        fps_max = 60
        done = False
        end = time()+duration
        while not done and time() < end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    break
            self.draw_screen(screen)
            pygame.display.flip()
            clock.tick(fps_max)

    def selected_cell_from_position(self, pos: tuple[int, int]) -> tuple[int, int]:
        row = pos[1]//(self.cell_height+self.cell_margin//2)
        col = pos[0]//(self.cell_width+self.cell_margin//2)
        return (row, col)

    def update_selected(self, val: int) -> 'Grid':
        self.update_selected_temp(val)
        if self.mode == Mode.DESIGN:
            self.update_selected_value(True)
        return self

    def update_selected_temp(self, val: int) -> 'Grid':
        row, col = self.get_selected()
        self.grid[row][col].set_temp_val(val)
        return self

    def get_selected_temp(self) -> int:
        if self.selected is None:
            return 0
        row, col = self.get_selected()
        return self.grid[row][col].get_temp()

    def update_selected_value(self, is_solvable: bool) -> 'Grid':
        row, col = self.get_selected()
        if is_solvable:
            self.grid[row][col].accept_temp()
        else:
            self.grid[row][col].reject_temp()
        return self

    def get_board_from_grid(self) -> Board:
        return Sudoku([cel.value for row in self.grid for cel in row])

    def update_grid(self, board: Board) -> 'Grid':
        self.grid = [[Cell(r, c, value=board.get_cell_value(r, c), width=self.cell_width, height=self.cell_height, margin=self.cell_margin)
                      for c in range(9)] for r in range(9)]
        return self

    def design_mode(self) -> 'Grid':
        self.mode = Mode.DESIGN
        return self

    def play_mode(self) -> 'Grid':
        self.mode = Mode.PLAY
        return self

    def get_size(self) -> tuple[int, int]:
        return (self.get_width(), self.get_height())

    def get_width(self) -> int:
        return self.cell_width*9+self.cell_margin*5

    def get_height(self) -> int:
        return self.cell_height*9+self.cell_margin*5


class Cell:
    __slots__ = 'value', 'temp_val', 'row', 'col', 'back_ground_color', 'width', 'height', 'margin'

    def __init__(self, row: int, col: int, width: int = 40, height: int = 40, margin: int = 6, value: int = 0, temp_val: int = 0):
        self.value = value
        self.temp_val = temp_val
        self.row = row
        self.col = col
        self.back_ground_color = (0, 0, 0)
        self.width = width
        self.height = height
        self.margin = margin

    def set_temp_val(self, val: int) -> None:
        self.temp_val = val

    def get_temp(self) -> int:
        return self.temp_val

    def accept_temp(self) -> None:
        self.value = self.temp_val

    def reject_temp(self) -> None:
        self.temp_val = 0

    def draw(self, row: pygame.surface.Surface) -> None:
        box = pygame.Surface((self.width, self.height))
        box.fill(self.back_ground_color)
        innerBox = pygame.Surface(
            (box.get_width()-self.margin, box.get_height()-self.margin))
        innerBox.fill((255, 255, 255))
        box.blit(innerBox, (self.margin//2, self.margin//2))

        if self.value != 0:
            font = pygame.font.SysFont("comicsansms", box.get_height())
            text = font.render(str(self.value), True, (0, 0, 0))
            box.blit(text, (box.get_width() // 2 - text.get_width()//2,
                            box.get_height() // 2 - text.get_height()//2))
        elif self.temp_val != 0:
            font = pygame.font.SysFont("comicsansms", box.get_height()//2)
            text = font.render(str(self.temp_val), True, (128, 128, 128))
            box.blit(text, (box.get_width() // 4 - text.get_width()//2,
                            box.get_height() // 4 - text.get_height()//2))
        row.blit(box, (self.width*(self.col)+self.margin *
                       (self.col//3+1), self.margin//2))

    def select(self) -> None:
        self.back_ground_color = (255, 0, 0)

    def deselect(self) -> None:
        self.back_ground_color = (0, 0, 0)

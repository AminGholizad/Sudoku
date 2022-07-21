from enum import Enum, auto
from time import time

import pygame

from sudoku import Board


class Mode(Enum):
    PLAY = auto()
    DESIGN = auto()


class Grid:
    def __init__(self, board: Board, cell_width: int = 40, cell_height: int = 40, cell_margin: int = 6):
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.cell_margin = cell_margin
        self.selected: tuple[int, int] | None = None
        self.mode = Mode.PLAY
        self.update_board(board)

    def draw(self, screen: pygame.surface.Surface) -> None:
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
            self.draw(screen)
            pygame.display.flip()
            clock.tick(fps_max)

    def select_cell(self, pos: tuple[int, int]) -> None:
        new_row = pos[1]//(self.cell_height+self.cell_margin//2)
        new_col = pos[0]//(self.cell_width+self.cell_margin//2)
        if self.board.get_value(new_row, new_col) == 0:
            if self.selected:
                row, col = self.selected
                self.grid[row][col].deselect()
            self.grid[new_row][new_col].select()
            self.selected = (new_row, new_col)

    def update_selected(self, val: int) -> None:
        if self.mode == Mode.PLAY:
            self.update_selected_temp(val)
        elif self.mode == Mode.DESIGN:
            self.update_selected_temp(val, forced=True)
            self.update_selected_value()

    def update_selected_temp(self, val: int, forced: bool = False) -> None:
        if self.selected:
            row, col = self.selected
            self.grid[row][col].set_temp_val(val, forced=forced)

    def update_selected_value(self) -> None:
        if self.selected:
            row, col = self.selected
            board_copy = self.board.copy()
            board_copy.set_cell_value(row, col, self.grid[row][col].get_temp())
            if board_copy.is_solvable():
                self.board.set_cell_value(
                    row, col, board_copy.get_value(row, col))
                self.grid[row][col].accept_temp()
            else:
                self.grid[row][col].reject_temp()

    def update_board(self, b: Board) -> None:
        self.board = b.copy()
        self.grid = [[Cell(r, c, value=b.get_value(r, c), width=self.cell_width, height=self.cell_height, margin=self.cell_margin)
                      for c in range(9)] for r in range(9)]

    def design_mode(self) -> None:
        self.update_board(Board([0]*81))
        self.mode = Mode.DESIGN

    def play_mode(self) -> None:
        self.mode = Mode.PLAY

    def get_size(self) -> tuple[int, int]:
        return (self.get_width(), self.get_height())

    def get_width(self) -> int:
        return self.cell_width*9+self.cell_margin*5

    def get_height(self) -> int:
        return self.cell_height*9+self.cell_margin*5


class Cell:
    def __init__(self, row: int, col: int, width: int = 40, height: int = 40, margin: int = 6, value: int = 0, temp_val: int = 0):
        self.value = value
        self.temp_val = temp_val
        self.row = row
        self.col = col
        self.back_ground_color = (0, 0, 0)
        self.width = width
        self.height = height
        self.margin = margin

    def set_temp_val(self, val: int, forced: bool = False) -> None:
        if self.value == 0:
            self.temp_val = val
        elif forced:
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


def runGame() -> None:
    grid = Grid(Board([[1, 0, 0, 0, 0, 0, 5, 0, 0],
                       [0, 0, 0, 8, 0, 0, 0, 0, 0],
                       [0, 0, 9, 0, 0, 0, 0, 6, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 7, 0, 0, 0, 0],
                       [0, 0, 0, 0, 4, 0, 0, 3, 0],
                       [0, 3, 0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 1, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 2, 0, 0, 0, 1, 0]]), cell_width=40, cell_height=40, cell_margin=2)

    pygame.init()
    screen = pygame.display.set_mode(grid.get_size())
    pygame.display.set_caption('Soduku')
    clock = pygame.time.Clock()
    fps_max = 60
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                break

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                pos = pygame.mouse.get_pos()
                grid.select_cell(pos)

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_1, pygame.K_KP1):
                    grid.update_selected(1)
                if event.key in (pygame.K_2, pygame.K_KP2):
                    grid.update_selected(2)
                if event.key in (pygame.K_3, pygame.K_KP3):
                    grid.update_selected(3)
                if event.key in (pygame.K_4, pygame.K_KP4):
                    grid.update_selected(4)
                if event.key in (pygame.K_5, pygame.K_KP5):
                    grid.update_selected(5)
                if event.key in (pygame.K_6, pygame.K_KP6):
                    grid.update_selected(6)
                if event.key in (pygame.K_7, pygame.K_KP7):
                    grid.update_selected(7)
                if event.key in (pygame.K_8, pygame.K_KP8):
                    grid.update_selected(8)
                if event.key in (pygame.K_9, pygame.K_KP9):
                    grid.update_selected(9)
                if event.key in (pygame.K_KP_ENTER, pygame.K_RETURN):
                    grid.update_selected_value()
                if event.key == pygame.K_n and pygame.key.get_mods() and pygame.KMOD_SHIFT:
                    grid.design_mode()
                if event.key == pygame.K_s and pygame.key.get_mods() and pygame.KMOD_SHIFT:
                    grid.play_mode()
                if event.key == pygame.K_SPACE:
                    grid.play_mode()
                    b = grid.board.solve(
                        visual=True, screen_width=grid.cell_width, screen_height=grid.cell_height, cell_margin=grid.cell_margin)
                    if b:
                        grid.update_board(b)

                if event.key == pygame.K_BACKSPACE:
                    grid.update_selected(0)

                if event.key == pygame.K_ESCAPE:
                    done = True
                    break

        grid.draw(screen)
        if grid.mode == Mode.DESIGN:
            font = pygame.font.SysFont("comicsansms", 12)
            text = font.render("design mode", True, (0, 128, 0))
            screen.blit(text, (screen.get_width()-text.get_width(),
                               screen.get_height()-text.get_height()))
        pygame.display.flip()
        clock.tick(fps_max)


if __name__ == "__main__":
    runGame()

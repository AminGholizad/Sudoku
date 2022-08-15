import pygame

from board.sudoku import Sudoku
from game import Game
from gui import Grid, Mode


def runGame() -> None:
    game = Game(Sudoku([[1, 0, 0, 0, 0, 0, 5, 0, 0],
                        [0, 0, 0, 8, 0, 0, 0, 0, 0],
                        [0, 0, 9, 0, 0, 0, 0, 6, 0],
                        [0, 0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 7, 0, 0, 0, 0],
                        [0, 0, 0, 0, 4, 0, 0, 3, 0],
                        [0, 3, 0, 0, 0, 0, 0, 0, 0],
                        [2, 0, 1, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 2, 0, 0, 0, 1, 0]]))
    grid = Grid(game.board,
                cell_width=40, cell_height=40, cell_margin=2)

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
                (selected_row, selected_col) = grid.selected_cell_from_position(pos)
                if grid.mode == Mode.DESIGN or game.board.is_cell_empty(selected_row, selected_col):
                    grid.set_selected(selected_row, selected_col)

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
                    row, col = grid.get_selected()
                    game_copy = game.copy()
                    game_copy.board.set_cell_value(
                        row, col, grid.get_selected_temp())
                    grid.update_selected_value(game_copy.is_solvable())
                if event.key == pygame.K_n and pygame.key.get_mods() and pygame.KMOD_SHIFT:
                    grid.design_mode()
                if event.key == pygame.K_s and pygame.key.get_mods() and pygame.KMOD_SHIFT:
                    game = Game(grid.get_board_from_grid())
                    grid.play_mode()
                if event.key == pygame.K_SPACE:
                    grid.play_mode()
                    game = Game(grid.get_board_from_grid())
                    solved_game = game.solve(grid)
                    if solved_game is not None:
                        grid.update_grid(solved_game.board)

                if event.key == pygame.K_BACKSPACE:
                    grid.update_selected(0)

                if event.key == pygame.K_ESCAPE:
                    done = True
                    break

        grid.draw_screen(screen)
        if grid.mode == Mode.DESIGN:
            font = pygame.font.SysFont("comicsansms", 12)
            text = font.render("design mode", True, (0, 128, 0))
            screen.blit(text, (screen.get_width()-text.get_width(),
                               screen.get_height()-text.get_height()))
        pygame.display.flip()
        clock.tick(fps_max)


if __name__ == "__main__":
    runGame()

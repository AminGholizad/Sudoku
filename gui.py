import pygame
import os
from time import time


class Grid(object):
    play = 1
    design = 2

    def __init__(self, b, w=40, h=40, m=6):
        self.cellWidth = w
        self.cellHeight = h
        self.margin = m
        self.selected = []
        self.mode = Grid.play
        self.updateBoard(b)

    def draw(self, screen):
        for r in range(9):
            row = pygame.Surface((self.get_width(), self.cellHeight))
            row.fill((0, 0, 0))
            for c in range(9):
                self.grid[r][c].draw(row)
            screen.blit(
                row, (self.margin//2, self.cellHeight*r+self.margin*(r//3+1)))

    def display(self, duration=0.01):
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

    def selectCell(self, pos):
        r = pos[1]//(self.cellHeight+self.margin//2)
        c = pos[0]//(self.cellWidth+self.margin//2)
        if self.board.getValue(r, c) == 0:
            if self.selected:
                x, y = self.selected
                self.grid[x][y].deselect()
            self.grid[r][c].select()
            self.selected = [r, c]

    def selectedUpdate(self, t):
        if self.mode == Grid.play:
            self.selectedTemp(t)
        elif self.mode == Grid.design:
            self.selectedTemp(t, forced=True)
            self.selectedValue()

    def selectedTemp(self, t, forced=False):
        if self.selected:
            x, y = self.selected
            self.grid[x][y].setTemp(t, forced=forced)

    def selectedValue(self):
        if self.selected:
            x, y = self.selected
            b = self.board.copy()
            b.setCellValue(x, y, self.grid[x][y].getTemp())
            if b.isSolvable():
                self.board.setCellValue(x, y, b.getValue(x, y))
                self.grid[x][y].acceptTemp()
            else:
                self.grid[x][y].rejectTemp()

    def updateBoard(self, b):
        self.board = b.copy()
        self.grid = [[Cell(r, c, v=b.getValue(r, c), w=self.cellWidth, h=self.cellHeight, m=self.margin)
                      for c in range(9)] for r in range(9)]

    def designMode(self):
        from Sudoku import Board
        self.updateBoard(Board([0]*81))
        self.mode = Grid.design

    def playMode(self):
        self.mode = Grid.play

    def get_size(self):
        return (self.get_width(), self.get_height())

    def get_width(self):
        return self.cellWidth*9+self.margin*5

    def get_height(self):
        return self.cellHeight*9+self.margin*5


class Cell(object):
    def __init__(self, r, c, w=40, h=40, m=6, v=0, t=0):
        self.value = v
        self.temp = t
        self.row = r
        self.col = c
        self.bg = (0, 0, 0)
        self.width = w
        self.height = h
        self.margin = m

    def setValue(self, v):
        self.value = v

    def setTemp(self, t, forced=False):
        if self.value == 0:
            self.temp = t
        elif forced:
            self.temp = t

    def getTemp(self):
        return self.temp

    def acceptTemp(self):
        self.value = self.temp

    def rejectTemp(self):
        self.temp = 0

    def draw(self, row):
        box = pygame.Surface((self.width, self.height))
        box.fill(self.bg)
        innerBox = pygame.Surface(
            (box.get_width()-self.margin, box.get_height()-self.margin))
        innerBox.fill((255, 255, 255))
        box.blit(innerBox, (self.margin//2, self.margin//2))

        if self.value != 0:
            font = pygame.font.SysFont("comicsansms", box.get_height())
            text = font.render(str(self.value), True, (0, 0, 0))
            box.blit(text, (box.get_width() // 2 - text.get_width()//2,
                            box.get_height() // 2 - text.get_height()//2))
        elif self.temp != 0:
            font = pygame.font.SysFont("comicsansms", box.get_height()//2)
            text = font.render(str(self.temp), True, (128, 128, 128))
            box.blit(text, (box.get_width() // 4 - text.get_width()//2,
                            box.get_height() // 4 - text.get_height()//2))
        row.blit(box, (self.width*(self.col)+self.margin *
                       (self.col//3+1), self.margin//2))

    def select(self):
        self.bg = (255, 0, 0)

    def deselect(self):
        self.bg = (0, 0, 0)


def runGame():
    from Sudoku import Board
    grid = Grid(Board([[1, 0, 0, 0, 0, 0, 5, 0, 0],
                       [0, 0, 0, 8, 0, 0, 0, 0, 0],
                       [0, 0, 9, 0, 0, 0, 0, 6, 0],
                       [0, 0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 7, 0, 0, 0, 0],
                       [0, 0, 0, 0, 4, 0, 0, 3, 0],
                       [0, 3, 0, 0, 0, 0, 0, 0, 0],
                       [2, 0, 1, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 2, 0, 0, 0, 1, 0]]), w=40, h=40, m=2)

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
                grid.selectCell(pos)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    grid.selectedUpdate(1)
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    grid.selectedUpdate(2)
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    grid.selectedUpdate(3)
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    grid.selectedUpdate(4)
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    grid.selectedUpdate(5)
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    grid.selectedUpdate(6)
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    grid.selectedUpdate(7)
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    grid.selectedUpdate(8)
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    grid.selectedUpdate(9)

                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:
                    grid.selectedValue()
                if event.key == pygame.K_n and pygame.key.get_mods() and pygame.KMOD_SHIFT:
                    grid.designMode()
                if event.key == pygame.K_s and pygame.key.get_mods() and pygame.KMOD_SHIFT:
                    grid.playMode()
                if event.key == pygame.K_SPACE:
                    grid.playMode()
                    b = grid.board.solve(
                        visual=True, w=grid.cellWidth, h=grid.cellHeight, m=grid.margin)
                    grid.updateBoard(b)

                if event.key == pygame.K_BACKSPACE:
                    grid.selectedUpdate(0)

                if event.key == pygame.K_ESCAPE:
                    done = True
                    break

        grid.draw(screen)
        if grid.mode == Grid.design:
            font = pygame.font.SysFont("comicsansms", 12)
            text = font.render("design mode", True, (0, 128, 0))
            screen.blit(text, (screen.get_width()-text.get_width(),
                               screen.get_height()-text.get_height()))
        pygame.display.flip()
        clock.tick(fps_max)


if __name__ == "__main__":
    runGame()

import os
import sys
import pygame as pg  # Set alias
from pygame.locals import *

# COLORS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# WINDOW SETTINGS
WINDOW_SIZE = WIDTH, HEIGHT = 400, 400
FOOTER_HEIGHT = 45

# BOARD STYLES
BOARD_COLOR = WHITE
LINE_COLOR = BLACK
LINE_THICKNESS = 4
MARKS_SCALE = 0.66  # Scale of our X and O marks relative to a field size


class TicTacToe:
    def __init__(self):
        # Set window position so it doesn´t initialize over my IDE
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 80)
        pg.init()                                                   # Initializes all pygame modules
        self.screen = pg.display.set_mode((WIDTH, HEIGHT + FOOTER_HEIGHT))     # Init window
        pg.display.set_caption('Tic Tac Toe')                       # Set window title
        self.x = pg.image.load('res/X_modified.png')
        self.x = pg.transform.scale(self.x, (WIDTH / 3 * MARKS_SCALE, HEIGHT / 3 * MARKS_SCALE))
        self.o = pg.image.load('res/o_modified.png')
        self.o = pg.transform.scale(self.o, (WIDTH / 3 * MARKS_SCALE, HEIGHT / 3 * MARKS_SCALE))
        self.mark_rect = self.x.get_rect()

        self.curr_player = 'X'
        self.other_player = 'O'

        self.draw_board()
        self.draw_marks('X', 0, 0)
        self.main_loop()

    def draw_board(self):
        self.screen.fill(BOARD_COLOR)
        for x in range(1, 3):
            pg.draw.line(self.screen, LINE_COLOR, (x * WIDTH / 3, 0), (x * WIDTH / 3, HEIGHT), LINE_THICKNESS)
        for y in range(1, 4):
            pg.draw.line(self.screen, LINE_COLOR, (0, y * HEIGHT / 3), (WIDTH, y * HEIGHT / 3), LINE_THICKNESS)

    def draw_marks(self, xo, x_tile, y_tile):
        self.screen.blit(self.x if (xo == 'X') else self.o,
                         (WIDTH / 3 * x_tile + WIDTH / 6 - self.mark_rect.width / 2,
                          HEIGHT / 3 * y_tile + HEIGHT / 6 - self.mark_rect.height / 2))

    @staticmethod
    def click():
        x_pos, y_pos = pg.mouse.get_pos()
        x_tile = 3 if (x_pos > WIDTH / 3 * 2) else 2 if (x_pos > WIDTH / 3) else 1
        y_tile = 3 if (y_pos > HEIGHT / 3 * 2) else 2 if (y_pos > HEIGHT / 3) else 1
        y_tile = 4 if (y_pos > HEIGHT) else y_tile
        print(x_tile, y_tile)

    def main_loop(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == MOUSEBUTTONDOWN:
                    self.click()
                    # if self.won or self.draw:
                    #   self.show_endscreen
            pg.display.flip()


if __name__ == '__main__':
    game = TicTacToe()  # Instantiates our Tic Tac Toe game
    pg.quit()
    print('Exiting successfully')
    sys.exit()

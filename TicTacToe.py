import os
import sys
import json
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
        # Initializes all pygame modules
        pg.init()
        # Init window and set window title
        self.screen = pg.display.set_mode((WIDTH, HEIGHT + FOOTER_HEIGHT))
        pg.display.set_caption('Tic Tac Toe')
        # Load and scale mark images
        self.x = pg.image.load('res/X_modified.png')
        self.x = pg.transform.scale(self.x, (WIDTH / 3 * MARKS_SCALE, HEIGHT / 3 * MARKS_SCALE))
        self.o = pg.image.load('res/o_modified.png')
        self.o = pg.transform.scale(self.o, (WIDTH / 3 * MARKS_SCALE, HEIGHT / 3 * MARKS_SCALE))
        self.mark_rect = self.x.get_rect()

        # Init game vars
        self.next_player = 1
        self.player1 = 'X'
        self.player2 = 'O'
        self.state_json = json.loads("""{"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, 
                                         "8": 0, "9": 0}""")

        # Draw the board and enter the main loop
        self.draw_board()
        self.main_loop()

    def draw_board(self):
        """ Draws the game board """
        self.screen.fill(BOARD_COLOR)
        for x in range(1, 3):
            pg.draw.line(self.screen, LINE_COLOR, (x * WIDTH / 3, 0), (x * WIDTH / 3, HEIGHT), LINE_THICKNESS)
        for y in range(1, 4):
            pg.draw.line(self.screen, LINE_COLOR, (0, y * HEIGHT / 3), (WIDTH, y * HEIGHT / 3), LINE_THICKNESS)

    def draw_marks(self, player, x_tile, y_tile):
        """ Draws a centered mark of the current player on the board """
        self.screen.blit(self.x if (player == 1) else self.o,
                         (WIDTH / 3 * x_tile + WIDTH / 6 - self.mark_rect.width / 2,
                          HEIGHT / 3 * y_tile + HEIGHT / 6 - self.mark_rect.height / 2))

    def click(self):
        """ Get the tile number when we click the board and execute it/the follow up methods """
        x_pos, y_pos = pg.mouse.get_pos()
        x_tile = 2 if (x_pos > WIDTH / 3 * 2) else 1 if (x_pos > WIDTH / 3) else 0
        y_tile = 2 if (y_pos > HEIGHT / 3 * 2) else 1 if (y_pos > HEIGHT / 3) else 0
        y_tile = 3 if (y_pos > HEIGHT) else y_tile
        tile_no = 3 * y_tile + x_tile + 1
        if self.state_json[str(tile_no)] == 0:
            # If the clicked tile is empty: Draw current players mark,
            # insert it into the game state json and swap current player
            self.draw_marks(self.next_player, x_tile, y_tile)
            self.state_json[str(tile_no)] = self.next_player
            self.next_player = 1 if (self.next_player == 2) else 2

    def main_loop(self):
        """ Main loop, interaction listener and updating our screen """
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
    pg.quit()           # Program continues if we click the X/close button, unload all pygame modules

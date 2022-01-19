import copy
import json
import os
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

# INIT GAME STATE
INIT_GAME_STATE_JSON = json.loads("""{"1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0, "7": 0, 
                                         "8": 0, "9": 0}""")


class TicTacToe:
    def __init__(self):
        # Set window position so it doesn´t initialize over my IDE
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (30, 80)
        # Initializes all pygame modules
        pg.init()
        # Init window and set window title
        self.screen = pg.display.set_mode((WIDTH, HEIGHT + FOOTER_HEIGHT))
        pg.display.set_caption('Tic Tac Toe')
        # Init font
        self.myfont = pg.font.SysFont('monospace', 15)
        self.label = None       # Placeholder
        self.label_rect = None  # Placeholder
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
        self.game_ended = False
        self.state_json = copy.deepcopy(INIT_GAME_STATE_JSON)

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
        self.render_text_or_new_game()

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
        try:    # Catch KeyError which happens when we click the bottom tile
            if self.state_json[str(tile_no)] == 0:
                # If the clicked tile is empty: Draw current players mark,
                # insert it into the game state json and swap current player
                self.draw_marks(self.next_player, x_tile, y_tile)
                self.state_json[str(tile_no)] = self.next_player
                if self.check_win_draw():
                    return  # Quit function to avoid overwriting the win message
                self.next_player = 1 if (self.next_player == 2) else 2
                self.render_text_or_new_game()
        except KeyError:
            # Make restart "button" available if the match ended
            if self.game_ended:
                self.game_ended = False
                del self.state_json
                self.state_json = copy.deepcopy(INIT_GAME_STATE_JSON)
                self.redraw()

    def check_win_draw(self):
        """ Checks if a player won or all tiles are taken = draw. Returns True if this happens """
        for player in (1, 2):
            if self.state_json['1'] == player and self.state_json['2'] == player and self.state_json['3'] == player or \
               self.state_json['4'] == player and self.state_json['5'] == player and self.state_json['6'] == player or \
               self.state_json['7'] == player and self.state_json['8'] == player and self.state_json['9'] == player or \
               self.state_json['1'] == player and self.state_json['4'] == player and self.state_json['7'] == player or \
               self.state_json['2'] == player and self.state_json['5'] == player and self.state_json['8'] == player or \
               self.state_json['3'] == player and self.state_json['6'] == player and self.state_json['9'] == player or \
               self.state_json['1'] == player and self.state_json['5'] == player and self.state_json['9'] == player or \
               self.state_json['3'] == player and self.state_json['5'] == player and self.state_json['7'] == player:

                self.render_text_or_new_game(f'Spieler {self.player1 if (player == 1) else self.player2} gewinnt! Klick hier für Neustart')
                self.game_ended = True
                return True    # Don´t continue checking on draw if someone won
        for tile in self.state_json:
            if self.state_json[tile] == 0:
                return     # Exit function if a tile has not been "captured" by a player yet
        self.render_text_or_new_game(f'Unentschieden! Klick hier für Neustart')   # Otherwise print draw notification
        self.game_ended = True
        return True

    def render_text_or_new_game(self, text=None):
        # Overwrite old text if set = not on startup
        if self.label_rect is not None:
            pg.draw.rect(self.screen, BOARD_COLOR, (WIDTH / 2 - self.label_rect.width / 2, HEIGHT + FOOTER_HEIGHT / 2 - self.label_rect.height / 2,
                                                    self.label_rect.width, self.label_rect.height))
        if not text:
            self.label = self.myfont.render(f'Spieler {self.player1 if (self.next_player == 1) else self.player2} am Zug!', True, BLACK)
        else:
            self.label = self.myfont.render(text, True, BLACK)
        self.label_rect = self.label.get_rect()
        self.screen.blit(self.label, (WIDTH / 2 - self.label_rect.width / 2, HEIGHT + FOOTER_HEIGHT / 2 - self.label_rect.height / 2))

    def redraw(self):
        self.draw_board()

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

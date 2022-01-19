import sys
import pygame as pg  # Set alias
from pygame.locals import *

WINDOW_SIZE = WIDTH, HEIGHT = 500, 500
speed = [2, 2]
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class TicTacToe:
    def __init__(self):
        pg.init()  # Initializes all pygame modules
        self.screen = pg.display.set_mode((WIDTH, HEIGHT + 45))  # Init window
        pg.display.set_caption('Tic Tac Toe')  # Set window title
        field = pg.image.load('res/field.jpg')
        self.background = pg.transform.scale(field, WINDOW_SIZE)
        pg.draw.line(self.screen, (0, 0, 0), (50, 50), (250, 250))

        self.screen.blit(self.background, (0, 0))
        self.main_loop()

    @staticmethod
    def click():
        x_pos, y_pos = pg.mouse.get_pos()
        tile = (x_pos > WIDTH / 3 * 2) ? 3 : 2
        print(x_pos, y_pos)

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

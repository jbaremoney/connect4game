'''
JACK BARETZ
minimax with alpha beta pruning to play connect 4
'''

import pygame as pg
import sys
import math
import numpy as np

def runGame(self):
    board = self.makeBoard()
    self.printBoard(board)
    game_over = False
    turn = 0

    pg.init()

    self.drawBoard(board)

    pg.display.update()

    myFont = pg.font.SysFont("monospace", 75)
    game_over = False
    while not game_over:

        for event in pg.event.get():
            if event.type == pg.QUIT:
                sys.exit()

            # moving mouse
            if event.type == pg.MOUSEMOTION:
                pg.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SLOTSIZE))
                xclick = event.pos[0]

                if turn == 0:
                    pg.draw.circle(self.screen, self.TURQUOISE, (xclick, int(self.SLOTSIZE / 2)), self.RADIUS)

                else:
                    pg.draw.circle(self.screen, self.YELLOW, (xclick, int(self.SLOTSIZE / 2)), self.RADIUS)
            pg.display.update()

            # clicking
            if event.type == pg.MOUSEBUTTONDOWN:

                pg.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SLOTSIZE))

                # player 1
                if turn == 0:
                    xclick = event.pos[0]
                    columns = int(math.floor(xclick / self.SLOTSIZE))

                    if self.isValidMove(board, columns):
                        row = self.getDropRow(board, columns)
                        self.dropPiece(board, row, columns, 1)

                        if self.winMove(board, 1):
                            label = myFont.render("Player 1 wins!!", 1, self.TURQUOISE)
                            self.screen.blit(label, (40, 10))
                            game_over = True


                # player 2
                else:

                    columnTup = self.negamax(board, 5, -np.inf, np.inf, 2)
                    column = columnTup[0]

                    if self.isValidMove(board, column):
                        row = self.getDropRow(board, column)
                        self.dropPiece(board, row, column, 2)

                        if self.winMove(board, 2):
                            label = myFont.render("Player 2 wins!!", 1, self.YELLOW)
                            self.screen.blit(label, (40, 10))
                            game_over = True

                self.printBoard(board)
                self.drawBoard(board)

                turn += 1
                turn = turn % 2

                if game_over:
                    pg.time.wait(3000)


import numpy as np
import pygame as pg
import sys
import math
import random

class Connect4():
    PURPLE = (160, 32, 240)
    BLACK = (0, 0, 0)
    TURQUOISE = (48, 213, 200)
    YELLOW = (255, 255, 0)

    WINDOWLENGTH = 4

    EMPTY = 0
    PLAYERPIECE = 1
    AGENTPIECE = 2

    NUMROWS = 6
    NUMCOLUMNS = 7

    def makeBoard(self):
        board = np.zeros((self.NUMROWS, self.NUMCOLUMNS))
        return board

    # action
    def dropPiece(self, board, row, column, piece):
        board[row][column] = piece

    # check
    def isValidMove(self, board, columns):
        return board[self.NUMROWS - 1][columns] == 0

    # finding open
    def getDropRow(self, board, columns):
        for r in range(self.NUMROWS):
            if board[r][columns] == 0:
                return r

    # have to flip it
    def printBoard(self, board):
        print(np.flip(board, 0))

    # check if won game,  TERMINAL TEST

    def winMove(self, board, piece):
        # horizontal check

        for c in range(self.NUMCOLUMNS - 3):
            for r in range(self.NUMROWS):
                if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][
                    c + 3] == piece:
                    return True

        # vertical check
        for c in range(self.NUMCOLUMNS):
            for r in range(self.NUMROWS - 3):
                if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][
                    c] == piece:
                    return True

        # bottom left to top right
        for c in range(self.NUMCOLUMNS - 3):
            for r in range(self.NUMROWS - 3):
                if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and \
                        board[r + 3][
                            c + 3] == piece:
                    return True

        # top left to bottom right
        for c in range(self.NUMCOLUMNS - 3):
            for r in range(3, self.NUMROWS):
                if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and \
                        board[r - 3][
                            c + 3] == piece:
                    return True

    def drawBoard(self, board):
        for c in range(self.NUMCOLUMNS):
            for r in range(self.NUMROWS):
                pg.draw.rect(self.screen, self.PURPLE, (c * self.SLOTSIZE, r * self.SLOTSIZE + self.SLOTSIZE, self.SLOTSIZE, self.SLOTSIZE))
                pg.draw.circle(self.screen, self.BLACK, (
                    int(c * self.SLOTSIZE + self.SLOTSIZE / 2), int(r * self.SLOTSIZE + self.SLOTSIZE + self.SLOTSIZE / 2)), self.RADIUS)

        for c in range(self.NUMCOLUMNS):
            for r in range(self.NUMROWS):
                if board[r][c] == 1:
                    pg.draw.circle(self.screen, self.TURQUOISE, (
                        int(c * self.SLOTSIZE + self.SLOTSIZE / 2), self.height - int(r * self.SLOTSIZE + self.SLOTSIZE / 2)), self.RADIUS)
                elif board[r][c] == 2:
                    pg.draw.circle(self.screen, self.YELLOW, (
                        int(c * self.SLOTSIZE + self.SLOTSIZE / 2), self.height - int(r * self.SLOTSIZE + self.SLOTSIZE / 2)), self.RADIUS)
        pg.display.update()


    def getValidLocations(self, board):
        valid_locations = []
        for col in range(self.NUMCOLUMNS):
            if board[self.NUMROWS - 1][col] == 0:  # top row check
                valid_locations.append(col)
        return valid_locations

    def evaluate_window(self, window, piece):
        score = 0
        opp_piece = self.PLAYERPIECE
        if piece == self.PLAYERPIECE:
            opp_piece = self.AGENTPIECE

        if window.count(piece) == 4:
            score += 100
        elif window.count(piece) == 3 and window.count(self.EMPTY) == 1:
            score += 5
        elif window.count(piece) == 2 and window.count(self.EMPTY) == 2:
            score += 2

        if window.count(opp_piece) == 3 and window.count(self.EMPTY) == 1:
            score -= 4



        return score

    def score_position(self, board, piece):
        score = 0

        # center
        center_array = [int(i) for i in list(board[:, self.NUMCOLUMNS // 2])]
        center_count = center_array.count(piece)
        score += center_count * 3

        # horizontal
        for r in range(self.NUMROWS):
            row_array = [int(i) for i in list(board[r, :])]
            for c in range(self.NUMCOLUMNS - 3):
                window = row_array[c:c + self.WINDOWLENGTH]
                score += self.evaluate_window(window, piece)

        # vertical
        for c in range(self.NUMCOLUMNS):
            col_array = [int(i) for i in list(board[:, c])]
            for r in range(self.NUMROWS - 3):
                window = col_array[r:r + self.WINDOWLENGTH]
                score += self.evaluate_window(window, piece)

        # positive slope
        for r in range(self.NUMROWS - 3):
            for c in range(self.NUMCOLUMNS - 3):
                window = [board[r + i][c + i] for i in range(self.WINDOWLENGTH)]
                score += self.evaluate_window(window, piece)
        # negative
        for r in range(self.NUMROWS - 3):
            for c in range(self.NUMCOLUMNS - 3):
                window = [board[r + 3 - i][c + i] for i in range(self.WINDOWLENGTH)]
                score += self.evaluate_window(window, piece)

        return score


    def negamax(self, board, depth, alpha, beta, player):
        valid_locations = self.getValidLocations(board)
        is_terminal = self.winMove(board, player) or len(valid_locations) == 0

        # terminal or maximum depth base case
        if depth == 0 or is_terminal:
            if is_terminal:
                if self.winMove(board, player):

                    return (None, float('inf'))
                else:
                    # Draw
                    return (None, 0)
            else:
                # depth is zero
                return (None, self.score_position(board, player))

        value = -float('inf')
        column = None
        for col in valid_locations:
            row = self.getDropRow(board, col)
            b_copy = board.copy()
            self.dropPiece(b_copy, row, col, player)
            # tuple
            _, temp_score = self.negamax(b_copy, depth - 1, -beta, -alpha, player % 2 + 1)
            new_score = -temp_score
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break  # Prune

        return column, value

    # could be whatever
    SLOTSIZE = 100

    width = NUMCOLUMNS * SLOTSIZE
    height = (NUMROWS + 1) * SLOTSIZE

    size = (width, height)

    RADIUS = int(SLOTSIZE / 2 - 5)

    screen = pg.display.set_mode(size)

    # run it
    def runGame(self):
        board = self.makeBoard()
        self.printBoard(board)
        game_over = False
        turn = 0

        pg.init()
        self.drawBoard(board)
        pg.display.update()
        myFont = pg.font.SysFont("monospace", 75)

        while not game_over:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()

                # handle Player 1's move on mouse click
                if event.type == pg.MOUSEBUTTONDOWN and turn == 0:

                    pg.draw.rect(self.screen, self.BLACK, (0, 0, self.width, self.SLOTSIZE))
                    posx = event.pos[0]
                    column = int(math.floor(posx / self.SLOTSIZE))

                    if self.isValidMove(board, column):
                        row = self.getDropRow(board, column)
                        self.dropPiece(board, row, column, 1)

                        if self.winMove(board, 1):
                            label = myFont.render("Player 1 wins!!", 1, self.TURQUOISE)
                            self.screen.blit(label, (40, 10))
                            game_over = True

                        turn = 1  # switch to Player 2
                        self.printBoard(board)
                        self.drawBoard(board)
                        pg.display.update()

                    if game_over:
                        break


            if turn == 1 and not game_over:  # checks if it's Player 2's turn and the game is not over
                column, _ = self.negamax(board, 5, -np.inf, np.inf, 2)
                if column is not None and self.isValidMove(board, column):
                    pg.time.wait(500)  # delay to make more realistic
                    row = self.getDropRow(board, column)
                    self.dropPiece(board, row, column, 2)

                    if self.winMove(board, 2):
                        label = myFont.render("Player 2 wins!!", 1, self.YELLOW)
                        self.screen.blit(label, (40, 10))
                        game_over = True

                    turn = 0  # switch back to Player 1
                    self.printBoard(board)
                    self.drawBoard(board)
                    pg.display.update()

                if game_over:
                    pg.time.wait(3000)


game = Connect4()
game.runGame()



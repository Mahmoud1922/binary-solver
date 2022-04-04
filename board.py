
import pygame

from pysmt.shortcuts import Symbol, And, Not, is_sat
from cube import Cube, EMPTY

class Board:

    def __init__(self, dimension, zeros, ones, width, height):
        self.message = "Press F5 to start solution"
        # build the board out of zeros and ones
        self.board = [[EMPTY for i in range(dimension)]
                      for j in range(dimension)]

        for i, j in ones:
            self.board[i - 1][j - 1] = '1'
        for i, j in zeros:
            self.board[i - 1][j - 1] = '0'

        assert len(set(ones).intersection(set(zeros))) == 0

        self.width = width
        self.height = height
        self.selected = None

        self.rows = dimension
        self.cols = dimension
        self.cubes = [[Cube(self.board[i][j], i, j, self.rows, width, height)
                       for j in range(dimension)] for i in range(dimension)]
        
        # Callbacks to be called whenever the board is modified
        self.update_callbacks = []

    def add_callback(self, callback):
        self.update_callbacks.append(callback)

    def _draw_message(self, win):
        fnt = pygame.font.SysFont("comicsans", 24)

        gap = self.width / self.cols
        x = gap / 4
        y = self.rows * gap

        text = fnt.render(str(self.message), 1, (0, 0, 0))
        win.blit(text, (x,
                        y + (gap / 2 - text.get_height() / 2)))
    
    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / self.rows
        for i in range(self.rows + 1):
            # if i % 3 == 0 and i != 0:
            #     thick = 4
            # else:
            thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap),
                             (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0),
                             (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

        self._draw_message(win)

    def redraw_window(self, win):
        win.fill((255, 255, 255))
        # Draw board
        self.draw(win)

    def update_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = self.cubes[i][j].value

    def update_view(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].value = self.board[i][j]

    def clear(self):
        row, col = self.selected
        self.cubes[row][col].value = EMPTY

    def place(self, val):
        row, col = self.selected
        self.cubes[row][col].value = val
        print("Setting cube value: (", row, ", ", col, "): ", val)
        self.update_board()

        return True

    def put_message(self, msg):
        self.message = msg

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def move_up(self):
        (row, col) = self.selected
        if row != 0:
            self.cubes[row][col].selected = False
            self.cubes[row - 1][col].selected = True
            self.selected = (row - 1, col)

    def move_down(self):
        (row, col) = self.selected
        if row != self.rows - 1:
            self.cubes[row][col].selected = False
            self.cubes[row + 1][col].selected = True
            self.selected = (row + 1, col)

    def move_left(self):
        (row, col) = self.selected
        if col != 0:
            self.cubes[row][col].selected = False
            self.cubes[row][col - 1].selected = True
            self.selected = (row, col - 1)

    def move_right(self):
        (row, col) = self.selected
        if col != self.cols - 1:
            self.cubes[row][col].selected = False
            self.cubes[row][col + 1].selected = True
            self.selected = (row, col + 1)

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].value = val

    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / self.rows
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None
    
    def put(self, symbol, i, j):
        """
        Method put symbol in position (i,j) in the board

        :param symbol is either '1' or '0' (maybe sometimes EMPTY?)
        :param i is row number in the board
        :param j is column number in the board
        """
        if i in range(len(self.board)) and j in range(len(self.board)):
            if self.board[i][j] == EMPTY:
                for callback in self.update_callbacks:
                    callback(symbol, i, j)
            self.board[i][j] = symbol
    
    def transpose(self):
        self.board = [[self.board[j][i]
                       for j in range(self.rows)] for i in range(self.cols)]

    def pretty_print(self):
        # pretty print
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in self.board]))

    def is_board_solved(self):
        """
        Method checks whether the board has been solved
        :return True iff there are no more empty EMPTY positions left in the board
        """
        for row in self.board:
            for element in row:
                if element == EMPTY:
                    return False
        return True

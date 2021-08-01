# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pygame

from pysmt.shortcuts import Symbol, And, Not, is_sat

pygame.font.init()

EMPTY = '_'


class Cube:

    def __init__(self, value, row, col, dimension, width, height):
        self.value = value
        self.row = row
        self.col = col
        self.dimension = dimension
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / self.dimension
        x = self.col * gap
        y = self.row * gap

        if self.value != '_':
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        assert(val in {'0', '1', '_'})
        self.value = val

class Board:

    def __init__(self, dimension, zeros, ones, width, height):
        # build the board out of zeros and ones
        self.board = [[EMPTY for i in range(dimension)] for j in range(dimension)]

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

    def update_board(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.board[i][j] = self.cubes[i][j].value

    def update_view(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].set(self.board[i][j])

    def clear(self):
        row, col = self.selected
        self.cubes[row][col].set(EMPTY)

    def place(self, val):
        row, col = self.selected
        self.cubes[row][col].set(val)
        print("Setting cube value: (", row, ", ", col, "): ", val)
        self.update_board()

        return True

    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False

        self.cubes[row][col].selected = True
        self.selected = (row, col)

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set(val)

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / self.rows
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

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

    # --------------------------------- Solver ------------------------------------
    def is_board_solved(self):
        for row in self.board:
            for element in row:
                if element == '_':
                    return False
        return True

    def put(self, symbol, i, j):
        if i in range(len(self.board)) and j in range(len(self.board)):
            self.board[i][j] = symbol

    def solve_adjacent(self):
        for i in range(self.rows):
            for j in range(self.cols - 1):
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] == '1':
                    self.put('0', i, j - 1)
                    self.put('0', i, j + 2)
                if self.board[i][j] == self.board[i][j + 1] and self.board[i][j] == '0':
                    self.put('1', i, j - 1)
                    self.put('1', i, j + 2)

    def solve_empty_middle(self):
        for i in range(self.rows):
            for j in range(self.cols - 2):
                if self.board[i][j] == self.board[i][j + 2] and self.board[i][j] == '1':
                    self.put('0', i, j + 1)
                if self.board[i][j] == self.board[i][j + 2] and self.board[i][j] == '0':
                    self.put('1', i, j + 1)

    def solve_one_remaining(self):
        for i in range(self.rows):
            number_of_empties = 0
            number_of_ones = 0
            number_of_zeros = 0
            location_of_empty = (0, 0)
            # find the only empty one
            for j in range(self.cols):
                if self.board[i][j] == '_':
                    if number_of_empties == 0:
                        number_of_empties = 1
                        location_of_empty = (i, j)
                    else:
                        number_of_empties = 2
                        break
                elif self.board[i][j] == '0':
                    number_of_zeros += 1
                else:
                    number_of_ones += 1

            # fill the empty place
            if number_of_empties == 1:
                if number_of_zeros > number_of_ones:
                    self.put('1', location_of_empty[0], location_of_empty[1])
                else:
                    self.put('0', location_of_empty[0], location_of_empty[1])

    def solve_half_full(self):
        max_number_of_a_symbol = self.rows / 2

        for i in range(self.rows):
            zeros = 0
            ones = 0
            for j in range(self.cols):
                if self.board[i][j] == '0':
                    zeros += 1
                elif self.board[i][j] == '1':
                    ones += 1
            if zeros == max_number_of_a_symbol:
                for j in range(self.cols):
                    if self.board[i][j] == '_':
                        self.put('1', i, j)
            if ones == max_number_of_a_symbol:
                for j in range(self.cols):
                    if self.board[i][j] == '_':
                        self.put('0', i, j)

    def solve(self, depth):

        if depth == 0:
            print("Maximum depth reached, finding solution failed!!!\n")
            return

        # solve one of the items, by applying a row rule
        self.solve_adjacent()
        self.solve_empty_middle()
        self.solve_one_remaining()
        self.solve_half_full()

        # solve transposed matrix by applying same row rule
        self.board = [[self.board[j][i] for j in range(self.rows)] for i in range(self.cols)]

        self.solve_adjacent()
        self.solve_empty_middle()
        self.solve_one_remaining()
        self.solve_half_full()

        # transpose result
        self.board = [[self.board[j][i] for j in range(self.rows)] for i in range(self.cols)]

        # recurse ...
        if self.is_board_solved():
            print("Solution found at depth " + str(depth) + "!!!")
        else:
            self.solve(depth - 1)

    def pretty_print(self):
        # pretty print
        # print(self.board)
        print('\n'.join([''.join(['{:4}'.format(item) for item in row])
                         for row in self.board]))


def redraw_window(win, board):
    win.fill((255, 255, 255))
    # Draw grid and board
    board.draw(win)


def main():
    # information about the initial setup
    dimension = 8
    ones_list = {}
    zeros_list = {}

    # make initial board from 0s and 1s
    board = Board(dimension, zeros_list, ones_list, 540, 540)
    # print full initial board
    print("Initial board:")
    board.pretty_print()

    # Make window
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Binary puzzle solver")
    key = None
    run = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_0:
                    key = '0'
                if event.key == pygame.K_1:
                    key = '1'
                if event.key == pygame.K_F5:
                    board.update_board()
                    print("=====================================================")
                    print("solving puzzle:")
                    board.pretty_print()
                    board.solve(dimension ** 2)
                    board.update_view()
                    print("solved board:")
                    board.pretty_print()
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].value != '_':
                        key = None

                        if board.is_board_solved():
                            print("Puzzle solved!!!")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_window(win, board)
        pygame.display.update()

    # print full sovled board
    print("Solved board:")
    board.pretty_print()


if __name__ == '__main__':
    main()
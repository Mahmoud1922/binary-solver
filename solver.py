
from board import Board
from cube import EMPTY

class Solver:
    def __init__(self, board):
        # build the board out of zeros and ones
        self.board = board
        self.is_board_updated = False

    def update_callback(self, symbol, i, j):
        self.is_board_updated = True

    def solve_adjacent(self):
        """
        Method for every quadruple '_ 1 1 _' and '_ 0 0 _' fills the empty places with
        '0' and '1' respectively
        """
        for i in range(self.board.rows):
            for j in range(self.board.cols - 1):
                if self.board.board[i][j] == self.board.board[i][j + 1]:
                    if self.board.board[i][j] == '1':
                        self.board.put('0', i, j - 1)
                        self.board.put('0', i, j + 2)
                    elif self.board.board[i][j] == '0':
                        self.board.put('1', i, j - 1)
                        self.board.put('1', i, j + 2)

    def solve_empty_middle(self):
        """
        Solve every triple in a row: '1 _ 1' and '0 _ 0' by filling with 0 and 1 respectively
        """
        for i in range(self.board.rows):
            for j in range(self.board.cols - 2):
                if self.board.board[i][j] == self.board.board[i][j + 2]:
                    if self.board.board[i][j] == '1':
                        self.board.put('0', i, j + 1)
                    elif self.board.board[i][j] == '0':
                        self.board.put('1', i, j + 1)

    def solve_one_remaining(self):
        """
        Method find all rows which have only one place unfilled and solve the remaining one
        """

        for i in range(self.board.rows):
            number_of_empties = 0
            number_of_ones = 0
            number_of_zeros = 0
            location_of_empty = (0, 0)
            # find the only empty one
            for j in range(self.board.cols):
                if self.board.board[i][j] == EMPTY:
                    if number_of_empties == 0:
                        number_of_empties = 1
                        location_of_empty = (i, j)
                    else:
                        number_of_empties = 2
                        break
                elif self.board.board[i][j] == '0':
                    number_of_zeros += 1
                else:
                    number_of_ones += 1

            # fill the empty place
            if number_of_empties == 1:
                if number_of_zeros > number_of_ones:
                    self.board.put('1', location_of_empty[0], location_of_empty[1])
                else:
                    self.board.put('0', location_of_empty[0], location_of_empty[1])

    def solve_half_full(self):
        """
        Method which solves the board whenever all possible instances of either 1 or 0 
        are already placed (by filling the rest with 0 or 1 respectively)
        """
        max_number_of_a_symbol = self.board.rows / 2

        for i in range(self.board.rows):
            zeros = 0
            ones = 0
            for j in range(self.board.cols):
                if self.board.board[i][j] == '0':
                    zeros += 1
                elif self.board.board[i][j] == '1':
                    ones += 1
            if zeros == max_number_of_a_symbol:
                for j in range(self.board.cols):
                    if self.board.board[i][j] == EMPTY:
                        self.put('1', i, j)
            if ones == max_number_of_a_symbol:
                for j in range(self.board.cols):
                    if self.board.board[i][j] == EMPTY:
                        self.board.put('0', i, j)

    # Returns False if absolutely no progress was made on the first call
    def _solve(self, first_call=False):

        self.is_board_updated = False

        # solve one of the items, by applying a row rule
        self.solve_adjacent()
        self.solve_empty_middle()
        self.solve_one_remaining()
        self.solve_half_full()

        # solve transposed matrix by applying same row rule
        self.board.transpose()

        self.solve_adjacent()
        self.solve_empty_middle()
        self.solve_one_remaining()
        self.solve_half_full()

        # transpose result
        self.board.transpose()

        # recurse ...
        if first_call and not self.is_board_updated:
            print("No progress made with heuristics!!!\n")
            return False
        elif not self.is_board_updated:
            print("Finding a solutions with heuristics stopped!!!\n")
            return False
        elif self.board.is_board_solved():
            print("Solution found!!!")
            return True
        else:
            return self._solve()

    def solve(self):
        return self._solve(first_call=True)

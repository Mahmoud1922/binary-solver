
from board import Board
from row_formula import RowFormula
from cube import EMPTY

class SMT_Solver:
    def __init__(self, board):
        # build the board out of zeros and ones
        self.board = board
        self.is_board_updated = False

    def update_callback(self, symbol, i, j):
        self.is_board_updated = True

    def solve_rows(self):
        for i in range(self.board.rows):
            row_formula = RowFormula(self.board.rows)
            row_formula.fill_in(self.board.board[i])
            if row_formula.is_satisfiable():
                solution = row_formula.get_solution()
                if self.board.board[i] != solution:
                    for j in range(self.board.cols):
                        if self.board.board[i][j] == EMPTY and solution[j] != EMPTY:
                            self.board.put(solution[j], i, j)
            else:
                # Not satisfiable!
                return False
        return True

    def _solve(self, first_call=False):

        self.is_board_updated = False

        # solve one of the items, by applying a row rule
        result = self.solve_rows()

        if not result:
            return "not satisfiable!"

        # solve transposed matrix by applying same row rule
        self.board.transpose()

        result = self.solve_rows()

        if not result:
            return "not satisfiable!"

        # transpose result
        self.board.transpose()

        # recurse ...
        if first_call and not self.is_board_updated:
            print("No progress, board has multiple solutions!!!\n")
            return "multiple solutions possible!"
        elif not self.is_board_updated:
            print("Finding a solutions with SMT solver stopped!!!\n")
            return "multiple solutions possible!"
        elif self.board.is_board_solved():
            print("Solution found!!!")
            return ""
        else:
            return self._solve()
    
    def solve(self):
        return self._solve(first_call=True)

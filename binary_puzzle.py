# Main file for the binary solver
import pygame

from board import Board
from solver import Solver
from smt_solver import SMT_Solver
from cube import EMPTY


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

    # define solvers
    solver = Solver(board)
    board.add_callback(solver.update_callback)

    # define solvers
    smt_solver = SMT_Solver(board)
    board.add_callback(smt_solver.update_callback)

    # Make window
    pygame.font.init()
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
                if event.key == pygame.K_UP:
                    key = None
                    board.move_up()
                if event.key == pygame.K_DOWN:
                    key = None
                    board.move_down()
                if event.key == pygame.K_LEFT:
                    key = None
                    board.move_left()
                if event.key == pygame.K_RIGHT:
                    key = None
                    board.move_right()
                if event.key == pygame.K_F5:
                    board.update_board()
                    print("=====================================================")
                    board.put_message("Solving puzzle ...")
                    board.redraw_window(win)
                    pygame.display.update()
                    board.pretty_print()
                    result = solver.solve()
                    if result:
                        board.update_view()
                        board.put_message("Solved board!")
                        board.pretty_print()
                    else:
                        board.update_view()
                        board.put_message(
                            "Not solvable via conventional methods, try F6")
                if event.key == pygame.K_F6:
                    board.update_board()
                    print("=====================================================")
                    board.put_message("Solving puzzle with SMT ...")
                    board.redraw_window(win)
                    pygame.display.update()
                    board.pretty_print()
                    result = smt_solver.solve()
                    if result == "":
                        board.update_view()
                        board.put_message("Solved board with SMT!")
                        board.pretty_print()
                    else:
                        board.update_view()
                        board.put_message(
                            "Puzzle cannot be solved because " + result)

                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.cubes[i][j].value != EMPTY:
                        key = None

                        if board.is_board_solved():
                            board.put_message("Puzzle solved!!!")
                            run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        board.redraw_window(win)
        pygame.display.update()

    # print full solved board
    print("Solved board:")
    board.pretty_print()


if __name__ == '__main__':
    main()

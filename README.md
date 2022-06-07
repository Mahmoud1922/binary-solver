# binary-solver

A while ago I was introduced to binary puzzles: (https://www.binarypuzzle.com) but while solving some "very hard" puzzles I noticed there is no way to proceed.
My guess was multiple solutions exist for these puzzles. To prove that I wrote this program. A part of the code is hijacked from somewhere, I do not remeber where anymore!

The solver employs some heuristics as well as an SMT solver as last resort.

This program depends on [pygame](https://www.pygame.org/wiki/GettingStarted#Pygame%20Installation) and [smt_solver](https://pypi.org/project/PySMT/) packages.
I used [Z3](https://github.com/Z3Prover/z3/) for SAT solving.

## How to use

0. Set the puzzle dimension in the file [binary_puzzle.py](https://github.com/Mahmoud1922/binary-solver/blob/master/binary_puzzle.py#L12), and run it.
1. Fill out the initial known values by entering 0s and 1s in the corresponding cells.
2. Press F5 to start the solution using heuristics. This only solves the most obvious cells.
3. Press F6 to solve using the SMT solver.
4. In case no more progress is possible, check the messages in the terminal.

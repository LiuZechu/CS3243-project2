#!/usr/bin/env python2

import subprocess

"""
HOW IT WORKS:
    ./runner.py <test input num>
For example, typing:
    ./runner.py 1
Translates to executing:
    python CS3243_P2_Sudoku_13.py public_tests_p2_sudoku/input1.txt output1.txt
"""

sudoku = "CS3243_P2_Sudoku_13.py"
input = "input"
output = "output"
extension = ".txt"

for i in range(1, 5):
    subprocess.call(["python2", sudoku, input + str(i) + extension, output + str(i) + extension])

#!/usr/bin/env python2

import subprocess

"""
HOW IT WORKS:
    ./runall.py
Translates to executing:
    python CS3243_P2_Sudoku_13.py input{i}.txt output{i}.txt # for i \in [1, 5]
"""

sudoku = "CS3243_P2_Sudoku_13.py"
input = "input"
output = "output"
extension = ".txt"

for i in range(1, 5):
    subprocess.call(["python2", sudoku, input + str(i) + extension, output + str(i) + extension])

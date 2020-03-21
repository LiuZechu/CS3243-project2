#!/usr/bin/env python2

import sys
import os
import subprocess
import time

"""
HOW IT WORKS:
    ./runner.py <test input num>
For example, typing:
    ./runner.py 1
Translates to executing:
    python CS3243_P2_Sudoku_13.py public_tests_p2_sudoku/input1.txt output1.txt
"""

# argv[0] represents input number of test case
if len(sys.argv) != 1:
    print("Wrong number of arguments! Try: ./runner.py <test input num>")

input_num = sys.argv[0]
file_name = "CS3243_P2_Sudoku_13.py"

input_path = "public_tests_p2_sudoku/input{n}.txt".format(n=input_num)
output_file = "output{n}.txt".format(n=input_num)

# clean previous outputs
if os.path.isfile(output_file):
    os.remove(output_file)
f = open(output_file, "w+")

# start a timer
start = time.time()

# run program
print("Running {filename} on input{n}.txt".format(filename=file_name, n=input_num))
subprocess.call(["python", filename, input_path, output_file])
end = time.time()
print("Completed.\nDuration: {0} seconds".format(round(end-start, 2)))

# check answer for correctness
lines = f.readlines()
f.close()

answer_file = open("file2.txt","r")
is_different = False
for line1 in f:
    for line2 in answer_file:
        if line1 == line2:
            print("SAME\n")
        else:
            print(line1 + line2)
            is_different = True
if not is_different:
    print("The solution is correct!")

f.close()
answer_file.close()
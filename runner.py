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

# argv[1] represents input number of test case
if len(sys.argv) != 2:
    print("Wrong number of arguments! Try: ./runner.py <test input num>")

input_num = sys.argv[1]
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
subprocess.call(["python", file_name, input_path, output_file])
end = time.time()
print("Completed.\nDuration: {0} seconds".format(round(end-start, 2)))

# check answer for correctness
answer_file = open("public_tests_p2_sudoku/output{n}.txt".format(n=input_num),"r")
result = []
answer = []
print("Your output is:")
for line in f:
    print line,
    result.append(line)

for line in answer_file:
    answer.append(line)

is_different = False

for index in range(0, len(result)):
    if result[index] == answer[index]:
        print("line {n} is correct".format(n=index))
    else:
        print("line {n} is different".format(n=index))    
        print "result: " + str(result[index]),
        print "expected: " + str(answer[index]),
        is_different = True

if not is_different:
    print("The solution is correct!")

f.close()
answer_file.close()
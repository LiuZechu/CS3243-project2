#!/usr/bin/env python2
import sys
import os
import subprocess
import time
import random
from random import randrange
from CS3243_P2_Sudoku_13 import Sudoku

"""
To run the experiments, run ./experiment.py in the terminal.
"""

###################### SEEDING RANDOM GENERATOR ###############
random.seed(20)

################### TESTCASES ######################
# read test cases from csv file
def read_test_cases_from_file(file_name):
    try:
        input_file = open(file_name, 'r')
    except IOError:
        raise IOError("Input file not found!")

    puzzles = []
    lines = input_file.readlines()

    number_of_empty_cells = 1
    for line in lines:
        # initialise empty puzzle
        puzzle = [[0 for i in range(9)] for j in range(9)]
        i, j = 0, 0
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0
            elif number == '.':
                puzzle[i][j] = 0
                j += 1
                if j == 9:
                    i += 1
                    j = 0

        if i == 0:
            continue

        # # randomely change increasing number of cells to 0
        # # TODO: make sure the resultant puzzle is solvable
        # used_positions = set()

        # # TODO: change this hard coded part for exp 2
        # if file_name == "experiment_inputs_2.csv":
        #     number_of_empty_cells = 60

        # for k in range(number_of_empty_cells):
        #     row = randrange(9)
        #     col = randrange(9)
        #     while (row, col) in used_positions:
        #         row = randrange(9)
        #         col = randrange(9)
        #     puzzle[row][col] = 0
        #     used_positions.add((row, col))
        # number_of_empty_cells += 1

        puzzles.append(puzzle)

    print(puzzles)
    return puzzles

###################### UTILITY FUNCTIONS ######################
# This function returns an array of [time_taken, number_of_backtracking_calls]
def run_and_generate_stats(puzzle):
    start = time.time()
    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()
    end = time.time()
    duration = round(end - start, 6)
    number_of_backtracking_calls = sudoku.counter
    return [duration, number_of_backtracking_calls]

############### EXPERIMENT ###############
puzzles = read_test_cases_from_file("experiment_inputs_3.csv")

###### Write into a CSV file ######
variant_1_output = "variant_1_output.csv"
variant_2_output = "variant_2_output.csv"
variant_3_output = "variant_3_output.csv"
output_file = variant_3_output

# clean previous outputs
if os.path.isfile(output_file):
    os.remove(output_file)

delimiter = ","
table_headings = "Puzzle #,Time Taken,Backtracking Calls\n"
with open(output_file, 'w+') as f:
    f.write(table_headings)
    counter = 1
    for puzzle in puzzles:
        stats = run_and_generate_stats(puzzle)
        duration = stats[0]
        number_of_backtracking_calls = stats[1]
        f.write(str(counter) + delimiter + str(duration) + delimiter + str(number_of_backtracking_calls) + "\n")
        print("Puzzle {} takes ".format(counter) + str(duration) + " seconds")
        counter += 1

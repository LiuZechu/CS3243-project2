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
random.seed(30)

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

        # randomely change increasing number of cells to 0
        # TODO: make sure the resultant puzzle is solvable
        used_positions = set()

        # TODO: change this hard coded part for exp 2
        if file_name == "experiment_inputs_2.csv":
            number_of_empty_cells = 50

        for k in range(number_of_empty_cells):
            row = randrange(9)
            col = randrange(9)
            while (row, col) in used_positions:
                row = randrange(9)
                col = randrange(9)
            puzzle[row][col] = 0
            used_positions.add((row, col))
        number_of_empty_cells += 1

        puzzles.append(puzzle)

    print(puzzles)
    return puzzles

###################### UTILITY FUNCTIONS ######################
# This function returns an array of [time_taken, number_of_backtracking_calls] NO
# This function returns time_taken
def run_and_generate_stats(puzzle):
    start = time.time()
    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()
    end = time.time()
    duration = round(end - start, 6)
    return duration

############### EXPERIMENT 1: TIME AGAINST SOLUTION DEPTH ###############
# puzzles = read_test_cases_from_file("experiment_inputs_1.csv")

# counter = 1
# for puzzle in puzzles:
#     duration = run_and_generate_stats(puzzle)
#     print("solution depth {} takes ".format(counter) + str(duration) + " seconds")
#     counter += 1

############### EXPERIMENT 2: HISTOGRAM ###############
puzzles = read_test_cases_from_file("experiment_inputs_2.csv")

###### Write into a CSV file ######
output_file = "experiment_2_output.csv"

# clean previous outputs
if os.path.isfile(output_file):
    os.remove(output_file)

delimiter = ","
table_headings = "Numer of Empty Cells,Time Taken\n"
with open(output_file, 'w+') as f:
    counter = 1
    for puzzle in puzzles:
        duration = run_and_generate_stats(puzzle)
        f.write(str(counter) + delimiter + str(duration) + "\n")
        print("solution depth {} takes ".format(counter) + str(duration) + " seconds")
        counter += 1




# ############### EXPERIMENT 1: TIME AGAINST SOLUTION DEPTH ###############

# """
# Run the algorithm under experiment using randomly generated sudoku puzzles with
# 0 - N empty cells. Generate a csv file with time against solution depth (number of empty cells)
# """

# print("\nThis script takes around 2-3 mins to complete.")
# print("\n===============================")
# print("BEGINNING EXPERIMENT 1:")
# print("===============================\n")

# inputs_for_3x3 = [initial_state_3_1, initial_state_3_2, initial_state_3_3]
# inputs_for_4x4 = [initial_state_4_custom]

# # Run BFS, Euclidean, Manhattan, Linear Conflict on 3x3 puzzle
# print("Running 3x3 public testcases...")
# algos_3x3 = [BfsPuzzle, EuclideanPuzzle, ManhattanPuzzle, LinearConflictPuzzle]
# results_3x3 = test_algos_for_size_n(algos_3x3, inputs_for_3x3, goal_state_3)
# print("3x3 clear")

# # Run BFS, Euclidean, Manhattan, Linear Conflict on 4x4 puzzle
# print("Running 4x4 custom testcase...")
# algos_4x4 = [BfsPuzzle, EuclideanPuzzle, ManhattanPuzzle, LinearConflictPuzzle]
# results_4x4 = test_algos_for_size_n(algos_4x4, inputs_for_4x4, goal_state_4)
# print("4x4 clear")

# ###### Write into a CSV file ######
# output_file = "experiment_1_output.csv"

# # clean previous outputs
# if os.path.isfile(output_file):
#     os.remove(output_file)

# delimiter = ","
# algorithm_names = ["BFS", "Euclidean", "Manhattan", "Linear Conflict"]
# table_headings = "Algorithm,Nodes expanded,Size of frontier,Number of steps,Time taken\n"
# with open(output_file, 'w+') as f:
#     # 3x3
#     num_algos = len(algos_3x3)
#     f.write("For 3x3 inputs\n")
#     f.write(table_headings)
#     for count, result in enumerate(results_3x3):
#         if (count % num_algos) == 0:
#             f.write("Input {}\n".format(count // num_algos + 1))
#         algorithm_name = algorithm_names[count % len(algorithm_names)]   
#         f.write(algorithm_name + delimiter + delimiter.join(str(x) for x in result) +'\n')

#     # 4x4
#     num_algos = len(algos_4x4)
#     f.write("For 4x4 inputs\n")
#     f.write(table_headings)
#     for count, result in enumerate(results_4x4):
#         if (count % num_algos) == 0:
#             f.write("Input {}\n".format(count // num_algos + 1))
#         algorithm_name = algorithm_names[count % len(algorithm_names)]
#         f.write(algorithm_name + delimiter + delimiter.join(str(x) for x in result) +'\n')

# print("Experiment 1 completed.\n")
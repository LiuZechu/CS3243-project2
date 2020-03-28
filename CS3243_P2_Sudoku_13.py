import sys
import copy

# Running script: given code can be run with the command:
# python file.py ./path/to/init_state.txt ./output/output.txt
from Queue import Queue


class Sudoku(object):
    # Constants
    CSV = "CSV"
    DEGREE_HEURISTIC = "DEGREE_HEURISTIC"
    FORWARD_CHECKING = "FORWARD_CHECKING"
    AC3 = "AC3"

    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        # TODO: Write your code here
        state = self.puzzle
        domains = self.get_initial_domains(state)
        self.ans = self.backtrack(domains, state)
        
        # print("ans is " + str(self.ans))

        # self.ans is a list of lists
        return self.ans

    def get_initial_domains(self, state):
        initial_domains = [[[1,2,3,4,5,6,7,8,9] for i in range(9)] for j in range(9)]
        for row in range(9):
            for col in range(9):
                if state[row][col] != 0:
                    initial_domains[row][col] = [state[row][col]]
        return initial_domains

    # TODO: Data structure (linked list?) to store unassigned variables; no need to iterate through entire array to select a variable
    # `assignment` is the same as state, as it is represented as a 9x9 2D matrix
    # `domains` is a 9x9 2D matrix, where each cell stores an array of allowable values
    def backtrack(self, domains, state):
        if self.is_assignment_complete(state):
            return state

        # print(state)

        variable = self.select_unassigned_variable(state, domains, self.CSV) # variable is a tuple of (row, col)
        row = variable[0]
        col = variable[1]

        for value in self.order_domain_values(variable, domains):
            if self.is_value_consistent(value, variable, state):
                # Removing deep copy as it is an expensive operation which can be easily resolved
                # new_state = copy.deepcopy(state)
                state[row][col] = value # assignment
                new_domains = copy.deepcopy(domains)
                new_domains[row][col] = [value]
                
                # `inferences` are reduced domains of variables
                inferences = self.inference(state, new_domains, variable, value, self.FORWARD_CHECKING)
                if inferences != []: # not failure
                    new_domains = inferences
                    result = self.backtrack(new_domains, state)
                    # successful result is a complete assignment
                    # failure is an empty list
                    if result != []: # not failure
                        return result
            # Not applicable: removing assignment {var = value} and inferences from assignment
            # is not needed because of `deepcopy`
            state[row][col] = 0 # removing assignment
        return [] # failure           

    def is_assignment_complete(self, assignment):
        is_complete = True
        for row in range(0, 9):
            for col in range(0, 9):
                if assignment[row][col] == 0:
                    is_complete = False

        return is_complete

    # returns the coordinate of the unassigned variable
    def select_unassigned_variable(self, state, domains, heuristic):

        # initialise
        position = (-1, -1)

        if heuristic == self.CSV:
            position = self.find_most_constrained_variable(state, domains)
        elif heuristic == self.DEGREE_HEURISTIC:
            position = self.find_most_constraining_variable(state, domains)
        return position

    # returns the unassigned position (row, col) 
    # that has the fewest allowable values in its domain
    def find_most_constrained_variable(self, state, domains):
        # initialise
        smallest_domain_size = 10
        position = (0, 0)
        
        for row in range(0, 9):
            for col in range(0, 9):
                if (state[row][col] == 0) and (len(domains[row][col]) < smallest_domain_size):
                    smallest_domain_size = len(domains[row][col])
                    position = (row, col)

        return position

    # TODO: Too slow currently. Intuitively, you solve sudoku using most constrained instead of most constraining.
    # returns the unassigned position (row, col) that has the highest degree.
    # Intuitively, such a tile has the most empty tiles in its row, column, and small square.
    def find_most_constraining_variable(self, state, domains):
        # initialise
        position = (-1, -1)
        max_degree = -1
        zeros_table = self.get_zeros_table(state) # preprocessing step for needed for `get_degree` to run in O(1).

        for row in range(9):
            for col in range(9):
                if (state[row][col] == 0):
                    current_degree = self.get_degree(row, col, zeros_table)
                    if current_degree > max_degree:
                        position = (row, col)
                        max_degree = current_degree

        return position

    # returns a 3x9 2D matrix.
    # The (0,0) element denotes the number of zeros in the first row.
    # The (1,0) element denotes the number of zeroes in the first column.
    # The (2,0) element denotes the number of zeroes in the first small square.
    # There are 9 columns since there are 9 rows/columns/small squares.
    def get_zeros_table(self, state):
        zeros_table = self.create_2D_array(3, 9)

        for row in range(9):
            for col in range(9):
                if (state[row][col] == 0):
                    zeros_table[0][row] += 1
                    zeros_table[1][col] += 1

                    start_row, start_col = self.get_start_row_col(row, col)
                    small_square_index = self.get_small_square_index(start_row, start_col)
                    zeros_table[2][small_square_index] += 1

        return zeros_table


    def get_degree(self, row, col, zeros_table):
        start_row, start_col = self.get_start_row_col(row, col)
        small_square_index = self.get_small_square_index(start_row, start_col)

        degree = (zeros_table[0][row] - 1) + \
                 (zeros_table[1][col] - 1) + \
                 (zeros_table[2][small_square_index] - 1)  # -1 to account for variable currently being assigned

        return degree

    # returns a list of allowable values for the specified variable in the current state
    # TODO: (delete before submission) referenced from: https://github.com/WPI-CS4341/CSP
    def order_domain_values(self, variable, domains):
        # initialise
        neighbours = self.get_neighbours(variable) # rows, columns, and small square
        value_count_tuples = []
        (row, col) = variable
        values = domains[row][col]

        for value in values:
            count = 0
            for neighbour in neighbours:
                (n_row, n_col) = neighbour
                neighbour_domain = domains[n_row][n_col]
                count += self.count_valid_values(neighbour_domain, value)
            value_count_tuples.append((value, count))

        sorted_by_count = sorted(value_count_tuples, key = lambda tup: tup[1])
        result = [value[0] for value in sorted_by_count]
        return result

    # returns a list of the variable's neighbours (assigned or not)
    def get_neighbours(self, variable):
        neighbours = []
        (row, col) = variable

        for i in range(0, 9):
            if i != row:
                neighbours.append((i, col))
            if i != col:
                neighbours.append((row, i))

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3
        for current_row in range(start_row, start_row + 3):
            for current_col in range(start_col, start_col + 3):
                if current_col != col and current_row != row:
                    neighbours.append((current_row, current_col))

        return neighbours

    def count_valid_values(self, neighbour_domain, value):
        count = 0
        for val in neighbour_domain:
            if val != value:
                count += 1
        return count

    # checks whether a variable-value assignment is consistent with the current state
    # position is a tuple (row, col)
    def is_value_consistent(self, value, position, current_state):
        row = position[0]
        col = position[1]
        new_state = copy.deepcopy(current_state)
        new_state[row][col] = value
        return self.vertical_all_different(col, new_state) and \
            self.horizontal_all_different(row, new_state) and \
            self.small_square_all_different(position, new_state)

   # checks vertical constraint at the specified column_number
    def vertical_all_different(self, column_number, state):
        elements_list = []
        for row in range(0, 9):
            if state[row][column_number] != 0:
                elements_list.append(state[row][column_number])

        # check for duplicates
        elements_set = set(elements_list)
        return len(elements_list) == len(elements_set)

    # checks horizontal constraint at the specified row_number
    def horizontal_all_different(self, row_number, state):
        elements_list = copy.deepcopy(state[row_number])
        elements_list = list(filter(lambda number: number != 0, elements_list))
        # check for duplicates
        elements_set = set(elements_list)
        return len(elements_list) == len(elements_set)

    # checks whether all elements in the 3x3 sqaure are different.
    # `position` is a tuple (row, col).
    # This method checks the constraint in the sqaure that contains this position.
    def small_square_all_different(self, position, state):
        start_row = (position[0] // 3) * 3
        start_col = (position[1] // 3) * 3
        elements_list = []
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                if state[row][col] != 0:
                    elements_list.append(state[row][col])

        # check for duplicates
        elements_set = set(elements_list)
        return len(elements_list) == len(elements_set)

    # returns the reduced domains of all variables, where
    # domains are represented as a 9x9 matrix, each cell storing a list of allowable integers
    def inference(self, state, domains, variable, value, heuristic):
        # defensive programming
        assert (heuristic == self.AC3) or (heuristic == self.FORWARD_CHECKING), \
            "Only AC3 and Forward Checking heuristics are available."

        if heuristic == self.AC3:
            return self.AC3(state, domains)
        elif heuristic == self.FORWARD_CHECKING:
            return self.forward_checking(domains, variable, value)

    # TODO: initialise queue in csp
    def AC3(self, state, domains):
        # initialisation
        queue = Queue()

        # TODO: Check position of state directly ?
        unassigned_positions = self.get_unassigned_positions(state)
        for position in unassigned_positions:
            neighbours = self.get_neighbours(position)
            for neighbour in neighbours:
                queue.put((position, neighbour))
        # for X in unassigned_positions:
        #     for Y in unassigned_positions:
        #         if X != Y:
        #             queue.put((X, Y))

        while not queue.empty():
            (X, Y) = queue.get()
            if self.revise(domains, X, Y):
                if len(domains[X[0]][X[1]]) == 0: return []
                neighbours = self.get_neighbours(X)
                neighbours.remove(Y)
                for Z in neighbours:
                    queue.put((Z, X))
        return domains


    # revises domain of X; domain is mutated.
    def revise(self, domains, X, Y):
        revised = False
        for x in domains[X[0]][X[1]]:
            revised = reduce(lambda i, j: i or x != j, domains[Y[0]][Y[1]], False)
            if revised:
                domains[X[0]][X[1]].remove(x)
        return revised

    # TODO: Forward checking should reduce domains of unassigned variables only right?
    def forward_checking(self, domains, position, value):
        domains = self.reduce_vertical_cells_domains(domains, position, value)
        if domains == []:
            return []
        domains = self.reduce_horizontal_cells_domains(domains, position, value)
        if domains == []:
            return []
        domains = self.reduce_small_square_domains(domains, position, value)
        if domains == []:
            return []
        else:
            return domains

    # remove `value` from all domains of the column of `position`, except at `position` itself
    def reduce_vertical_cells_domains(self, domains, position, value):
        row_number = position[0]
        column_number = position[1]
        for row in range(0, 9):
            if row != row_number and value in domains[row][column_number]:
                domains[row][column_number].remove(value)
                if domains[row][column_number] == []:
                    return [] # failure
        return domains        

    # remove `value` from all domains of the row of `position`, except at `position` itself
    def reduce_horizontal_cells_domains(self, domains, position, value):
        row_number = position[0]
        column_number = position[1]
        for col in range(0, 9):
            if col != column_number and value in domains[row_number][col]:
                domains[row_number][col].remove(value)
                if domains[row_number][col] == []:
                    return [] #failure
        return domains

    # remove `value` from all domains of cells in the 3x3 square containing `position`, 
    # except at `position` itself
    def reduce_small_square_domains(self, domains, position, value):
        start_row = (position[0] // 3) * 3
        start_col = (position[1] // 3) * 3
        for row in range(start_row, start_row + 3):
            for col in range(start_col, start_col + 3):
                if (not (row, col) == position) and value in domains[row][col]:
                    domains[row][col].remove(value)
                    if domains[row][col] == []:
                        return [] # failure
        return domains

    # UTILS
    def create_2D_array(self, row, col):
        return [[0 for x in range(col)] for y in range(row)]

    def get_start_row_col(self, row, col):
        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        return start_row, start_col

    def get_unassigned_positions(self, state):
        unassigned_positions = []
        for row in range(9):
            for col in range(9):
                if state[row][col] == 0:
                    unassigned_positions.append((row, col))
        return unassigned_positions

    # Index 0 denotes (0,0). 1ndex 3 denotes (3, 0) ... Index 8 denotes (6, 6).
    def get_small_square_index(self, start_row, start_col):
        return 3 * (start_row // 3) + start_col // 3

    # you may add more classes/functions if you think is useful
    # However, ensure all the classes/functions are in this file ONLY
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # STRICTLY do NOT modify the code in the main function here
    if len(sys.argv) != 3:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        print ("\nUsage: python CS3243_P2_Sudoku_XX.py input.txt output.txt\n")
        raise IOError("Input file not found!")

    puzzle = [[0 for i in range(9)] for j in range(9)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '9':
                puzzle[i][j] = int(number)
                j += 1
                if j == 9:
                    i += 1
                    j = 0

    sudoku = Sudoku(puzzle)
    ans = sudoku.solve()

    with open(sys.argv[2], 'a') as f:
        for i in range(9):
            for j in range(9):
                f.write(str(ans[i][j]) + " ")
            f.write("\n")

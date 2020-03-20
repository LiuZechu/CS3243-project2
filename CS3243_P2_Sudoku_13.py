import sys
import copy

# Running script: given code can be run with the command:
# python file.py ./path/to/init_state.txt ./output/output.txt

class Sudoku(object):
    def __init__(self, puzzle):
        # you may add more attributes if you need
        self.puzzle = puzzle # self.puzzle is a list of lists
        self.ans = copy.deepcopy(puzzle) # self.ans is a list of lists

    def solve(self):
        # TODO: Write your code here
        state = self.puzzle
        domains = [[[1,2,3,4,5,6,7,8,9] for i in range(9)] for j in range(9)]
        self.ans = self.backtrack(domains, state)
        
        print("ans is " + str(self.ans))
        # self.ans is a list of lists
        return self.ans

    # `assignment` is the same as state, as it is represented as a 9x9 2D matrix
    # `domains` is a 9x9 2D matrix, where each cell stores an array of allowable values
    def backtrack(self, domains, state):
        if self.is_assignment_complete(state):
            return state

        variable = self.select_unassigned_variable(state) # variable is a tuple of (row, col)
        row = variable[0]
        col = variable[1]

        for value in self.order_domain_values(variable, domains, state):
            if self.is_value_consistent(value, variable, state):
                new_state = copy.deepcopy(state)
                new_state[row][col] = value
                new_domains = copy.deepcopy(domains)
                new_domains[row][col] = [value]
                
                # `inferences` are reduced domains of variables
                inferences = self.inference(new_domains, variable, value)
                if inferences != []: # not failure
                    new_domains = inferences
                    result = self.backtrack(new_domains, new_state)
                    # successful result is a complete assignment
                    # failure is an empty list
                    if result != []: # not failure
                        return result
            # removing assignment {var = value} and inferences from assignment 
            # is not needed because of `deepcopy`
        return [] # failure           

    def is_assignment_complete(self, assignment):
        is_complete = True
        for row in range(0, 9):
            for col in range(0, 9):
                if assignment[row][col] == 0:
                    is_complete = False

        return is_complete

    # returns the coordinate of the unassigned variable
    def select_unassigned_variable(self, state):
        # for now, just find any 0 cell
        for row in range(0, 9):
            for col in range(0, 9):
                if state[row][col] == 0:
                    return (row, col)

    # returns a list of allowable values for the specified variable in the current state
    def order_domain_values(self, variable, domains, state):
        # for now, just return its domain
        row = variable[0]
        col = variable[1]
        return domains[row][col]

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

    def inference(self, domains, variable, value):
        # Forward Checking for now
        # can try AC3 in the future
        return self.forward_checking(domains, variable, value)

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

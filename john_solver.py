import numpy as np
import copy
def ones_counter():
    """Generates a lookup list to know how many 1s are present in a binary representation of a number up to 9 bits (511)
        As possible values of sudoku cells are encoded as bits, this is useful for understanding how many possible
        possible values remain for a cell. It is a very fast way to tell if a value is a final value as it will have
        only 1 possible value if it is final. It is also used in identifying naked pairs as it allows us to tell that
        two cells both have only 2 possible values."""

    # Using a list, when we look up a number by referencing its value as the index, it returns the number of 1s in the
    # binary equivalent of that number
    lookup_list = []
    for number in range(0, 512):
        binary_num = bin(number)
        count = 0
        # We ignore the first two cars of a binary representation as they are not part of the binary number
        for char in range(2, len(binary_num)):
            if binary_num[char] == '1':
                count += 1
        lookup_list.append(count)
    return lookup_list


# Generate the lookup list once at the beginning of the program
ones_lookup = ones_counter()


def decode(value):
    """Given a binary encoding (an integer which has the value representing a sudoku value) returns the integer
       which that encoding represents. E.g. the binary number 1000 is the same as the integer 8, this is used to
       encode the value 4 because there is a 1 in the 4th position from the right"""

    if value == 0:
        return 0
    elif value == 1:
        return 1
    elif value == 2:
        return 2
    elif value == 4:
        return 3
    elif value == 8:
        return 4
    elif value == 16:
        return 5
    elif value == 32:
        return 6
    elif value == 64:
        return 7
    elif value == 128:
        return 8
    elif value == 256:
        return 9
    else:
        return 0


class SudokuState:

    def __init__(self, initial_values):
        # Tracks the number of unsolved cells remaining
        self.unsolved_cells = 81
        # Represents the start state of the sudoku board, not encoded
        self.initial_values = initial_values
        # We want each cell to represent 9 possible values as bits, so we need to use int16 as the provided
        # sudokus use int8, which only have 8 bits and not enough for this encoding.
        self.final_values = np.ndarray(shape=(9, 9), dtype=np.int16)

        # These are the only 'valid' values a cell can have once it has been solved, but before it is decoded
        self.final_possible_values = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256])

        # This is a lookup table to encode an integer as a binary representation of its possible values
        # 511 is used as it is the binary number 111111111 which represents all 9 values as being possible
        self.encoding = np.array([511, 1, 2, 4, 8, 16, 32, 64, 128, 256])

        # This is used for marking which cells have been finally set, opposed to just have only 1 possible value
        self.solved_values = np.full((9, 9), False)
        
        # Encode the final values into binary representations
        self.encode_sudoku()
        # Set final values when there is a single possible value
        self.set_final_values()

    def encode_sudoku(self):
        """ Transforms the object's final_values from integers to bit representations of its possible values """
        for row in range(0, 9):
            for col in range(0, 9):
                self.final_values[row, col] = self.encoding[self.initial_values[row, col]]

    def decode_sudoku(self):
        """ Transforms the object's final_values from bit representations of its possible values to integers"""
        for row in range(0, 9):
            for col in range(0, 9):
                self.final_values[row, col] = decode(self.final_values[row, col])

    def set_value(self, row, col):
        """ Given a cell, removes the value of this cell from the possible values of other cells
        in the same row, column and block."""

        # Only set the value if it hasn't been set before
        if self.solved_values[row, col]:
            return

        self.solved_values[row, col] = True
        self.unsolved_cells -= 1

        # Update cells in the same row
        for update_col in range(0, 9):
            # ignore target cell
            if update_col == col:
                continue
            # if the value is not a possible value of the cell, then an AND will yield 0, and we can ignore it
            # This is necessary because if we XOR a value which doesn't contain this, it will not add it to the
            # the cells possible values.
            if self.final_values[row, update_col] & self.final_values[row, col] == 0:
                continue
            # otherwise, the value is in it and can be removed with a bitwise XOR
            # Note: this is the key benefit of using a bit representation for possible values as it is much
            # faster to perform a bitwise operation than to loop and check a list of possible values for a cell
            self.final_values[row, update_col] = self.final_values[row, update_col] ^ self.final_values[row, col]

        # Update cells in same column
        for update_row in range(0, 9):
            # ignore starting cell
            if update_row == row:
                continue
            # if the value is not a possible value of the cell, then an AND will yield 0, and we can ignore it
            if self.final_values[update_row, col] & self.final_values[row, col] == 0:
                continue
            # remove value with a bitwise XOR
            self.final_values[update_row, col] = self.final_values[update_row, col] ^ self.final_values[row, col]

        # now update cells in the same 9 x 9 block
        starting_cell_row = (row // 3) * 3
        starting_cell_col = (col // 3) * 3
        for block_row in range(starting_cell_row, starting_cell_row + 3):
            for block_col in range(starting_cell_col, starting_cell_col + 3):
                # Ignore the updated cell
                if block_row == row and block_col == col:
                    continue

                # if the value is not a possible value of the cell, then an AND will yield 0, and we can ignore it
                if self.final_values[block_row, block_col] & self.final_values[row, col] == 0:
                    continue
                # remove value with a bitwise XOR
                self.final_values[block_row, block_col] = self.final_values[block_row, block_col] ^ \
                                                          self.final_values[row, col]

    def set_final_values(self):
        """ Sets any value that may be final. This is used after applying rules and removing possible values."""
        for row in range(0, 9):
            for col in range(0, 9):
                if ones_lookup[self.final_values[row, col]] == 1:
                    self.set_value(row, col)

    def is_only_possibility_in_row(self, row):
        """Sets possible value if it is the only instance of that possible value in a whole row"""

        for col in range(0, 9):
            # If this cell is already a final value, skip
            if ones_lookup[self.final_values[row, col]] == 1:
                continue
            for value in self.final_possible_values:
                # If not a possible value for this cell, move on to next possible value
                if self.final_values[row, col] & value == 0:
                    continue

                # Use a boolean flag to remember if any other cell contains this value
                is_only_possible_value = True

                # Check against all other values
                for other_col in range(0, 9):
                    # don't check against self
                    if col == other_col:
                        continue
                    # If the value is possible for another cell, then it isn't the only possible value
                    if self.final_values[row, other_col] & value != 0:
                        is_only_possible_value = False
                        break

                if is_only_possible_value:
                    # set the value
                    self.final_values[row, col] = value
                    self.set_value(row, col)
                    # break out of loop
                    break

    def is_only_possibility_in_col(self, col):
        """Sets possible value if unique among a column"""

        for row in range(0, 9):

            # If this is already a final value, skip
            if ones_lookup[self.final_values[row, col]] == 1:
                continue
            for value in self.final_possible_values:

                # If not a possible value for this cell, move on to next possible value
                if self.final_values[row, col] & value == 0:
                    continue

                # Use a boolean flag to remember if any other cell contains this value
                is_only_possible_value = True
                for other_row in range(0, 9):
                    # don't check against self
                    if row == other_row:
                        continue
                    # If the value is possible for another cell, then it isn't the only possible value
                    if self.final_values[other_row, col] & value != 0:
                        is_only_possible_value = False
                        break

                if is_only_possible_value:
                    # set the value
                    self.final_values[row, col] = value
                    self.set_value(row, col)
                    # break out of loop
                    break

    def is_only_possibility_in_block(self, starting_cell_row, starting_cell_col):
        """Checks if a possible value is unique in a 9x9 block"""

        for block_row in range(starting_cell_row, starting_cell_row + 3):
            for block_col in range(starting_cell_col, starting_cell_col + 3):
                # If this is already a final value, skip
                if ones_lookup[self.final_values[block_row, block_col]] == 1:
                    continue
                for value in self.final_possible_values:

                    # Use a boolean flag to remember if any other cell contains this value
                    is_only_possible_value = True
                    # If not a possible value for this cell, move on to next possible value
                    if self.final_values[block_row, block_col] & value == 0:
                        continue

                    for other_row in range(starting_cell_row, starting_cell_row + 3):
                        for other_col in range(starting_cell_col, starting_cell_col + 3):
                            # don't check against self
                            if block_row == other_row and block_col == other_col:
                                continue
                            # If the value is possible for another cell, then it isn't the only possible value
                            if self.final_values[other_row, other_col] & value != 0:
                                is_only_possible_value = False
                                break
                        else:
                            continue
                        break

                    if is_only_possible_value:
                        # set the value
                        self.final_values[block_row, block_col] = value
                        self.set_value(block_row, block_col)
                        # break out of loop
                        break

    def resolve_naked_pairs(self):
        """Examines cells in rows, columns and blocks for naked pairs. If a naked pair is found, removes the
        values of the naked pair from the domains of relevant cells"""
        # Rows first
        for row in range(0, 9):
            for col in range(0, 9):
                # Ignore solved cells and cells with more than 2 values
                if ones_lookup[self.final_values[row, col]] == 1 or \
                        ones_lookup[self.final_values[row, col]] != 2:
                    continue
                for next_col in range(col + 1, 9):
                    # Ignore solved cells and cells with more than x values
                    if ones_lookup[self.final_values[row, next_col]] == 1 or \
                            ones_lookup[self.final_values[row, next_col]] != 2:
                        continue
                    if self.final_values[row, col] == self.final_values[row, next_col]:
                        for change_col in range(0, 9):
                            # Ignore any cells which have the same values
                            if self.final_values[row, col] == self.final_values[row, change_col]:
                                continue
                            # Remove the values from all other cells if they are there
                            if self.final_values[row, col] & self.final_values[row, change_col] == \
                                    self.final_values[row, col]:
                                self.final_values[row, change_col] = self.final_values[row, col] ^ \
                                                                     self.final_values[row, change_col]

        # Then columns
        for col in range(0, 9):
            for row in range(0, 9):
                # Ignore solved cells and cells with more than 2 values
                if ones_lookup[self.final_values[row, col]] == 1 or ones_lookup[self.final_values[row, col]] != 2:
                    continue
                for next_row in range(row + 1, 9):
                    # Ignore solved cells and cells with more than x values
                    if ones_lookup[self.final_values[next_row, col]] == 1 or \
                            ones_lookup[self.final_values[next_row, col]] != 2:
                        continue
                    if self.final_values[row, col] == self.final_values[next_row, col]:
                        for change_row in range(0, 9):
                            # Ignore any cells which have the same values
                            if self.final_values[row, col] == self.final_values[change_row, col]:
                                continue
                            # Remove the values from all other cells if they are there
                            if self.final_values[row, col] & self.final_values[change_row, col] == \
                                    self.final_values[row, col]:
                                self.final_values[change_row, col] = self.final_values[row, col] ^ \
                                                                     self.final_values[change_row, col]

        # Then Blocks
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                for cell_row in range(row, row + 3):
                    for cell_col in range(col, col + 3):
                        if ones_lookup[self.final_values[cell_row, cell_col]] == 1 or ones_lookup[
                            self.final_values[cell_row, cell_col]] != 2:
                            continue
                        for next_row in range(row, row + 3):
                            for next_col in range(col, col + 3):
                                # Ignore solved cells and cells that have too many possible values
                                if ones_lookup[self.final_values[next_row, col]] == 1 or ones_lookup[
                                    self.final_values[cell_row, cell_col]] != 2:
                                    continue
                                # Ignore the cell we are comparing
                                if cell_row == next_row and cell_col == next_col:
                                    continue

                                if self.final_values[cell_row, cell_col] == self.final_values[next_row, next_col]:
                                    for change_row in range(row, row + 3):
                                        for change_col in range(col, col + 3):
                                            # Ignore the pairs
                                            if (change_row == cell_row and change_col == cell_col) or (
                                                    change_row == next_row and change_col == next_col):
                                                continue
                                            # Otherwise, remove those possible values from cells if they are there
                                            if self.final_values[cell_row, cell_col] & self.final_values[change_row,
                                                                                                         change_col] == \
                                                    self.final_values[cell_row, cell_col]:
                                                self.final_values[change_row, change_col] = self.final_values[cell_row,
                                                                                                              cell_col] ^ \
                                                                                            self.final_values[
                                                                                                change_row, change_col]

    def apply_constraints(self):
        """Sequentially apply all constraints to the grid and then set any cells that have only one possible value"""

        for row in range(0, 9):
            self.is_only_possibility_in_row(row)
        for col in range(0, 9):
            self.is_only_possibility_in_col(col)
        for starting_row in range(0, 9, 3):
            for starting_col in range(0, 9, 3):
                self.is_only_possibility_in_block(starting_row, starting_col)

        self.resolve_naked_pairs()
        self.set_final_values()

    def is_goal(self):
        """ Returns True if the board's final values represent a solved sudoku board, false otherwise """
        # The board is solved when all solved values are True
        return np.array_equal(self.solved_values, np.full((9, 9), True))

    def is_invalid(self):
        """ Returns True if the board is unsolveable or False otherwise """
        # This state is invalid if any cell on the board has no possible values
        for row in range(0, 9):
            for col in range(0, 9):
                if self.final_values[row, col] == 0:
                    return True
        return False

    def is_malformed(self):
        """ Returns true if the board has the same final value in any row, column or block
            This is the implementation of the alldiff constraint"""
        # Check rows
        for row in range(0, 9):
            for col in range(0, 9):
                if ones_lookup[self.final_values[row, col]] != 1:
                    continue
                for next_col in range(0, 9):
                    if col == next_col:
                        continue
                    if self.final_values[row, col] == self.final_values[row, next_col]:
                        return True

        # Check cols
        for col in range(0, 9):
            for row in range(0, 9):
                if ones_lookup[self.final_values[row, col]] != 1:
                    continue
                for next_row in range(0, 9):
                    if row == next_row:
                        continue
                    if self.final_values[row, col] == self.final_values[next_row, col]:
                        return True

        # Check blocks
        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                for cell_row in range(row, row + 3):
                    for cell_col in range(col, col + 3):
                        if ones_lookup[self.final_values[cell_row, cell_col]] != 1:
                            continue
                        for next_row in range(row, row + 3):
                            for next_col in range(col, col + 3):
                                # Ignore the cell we are comparing
                                if cell_row == next_row and cell_col == next_col:
                                    continue
                                if self.final_values[cell_row, cell_col] == self.final_values[next_row, next_col]:
                                    return True
        return False

    def pick_next_cell(self):
        """ Returns a tuple with a row and column representing the cell with the least number of possible values """

        # Find an empty cell with the least number of possible values and return it
        least_options_cell = (0, 0)
        min_options = 10
        for row in range(0, 9):
            for col in range(0, 9):
                # Ignore solved cells
                num_options = ones_lookup[self.final_values[row, col]]
                if num_options == 1:
                    continue
                if num_options < min_options:
                    min_options = num_options
                    least_options_cell = (row, col)

        return least_options_cell


def depth_first_search(partial_state):
    """ Applies a depth-first backtracking search on a partially solved sudoku grid. First it applies
        rules to the grid to resolve any values that can be solved by applying constraints"""
    # First apply all rules to the given state until the same output is yielded

    start_state = copy.deepcopy(partial_state)
    next_state = copy.deepcopy(partial_state)

    next_state.apply_constraints()

    # Apply a heuristic to only try applying rules if there are more than 50 unsolved cells
    while next_state.unsolved_cells > 50 and not np.array_equal(next_state.final_values, start_state.final_values):
        start_state = copy.deepcopy(next_state)
        next_state.apply_constraints()

    # Check if applying the rules yielded the goal
    if next_state.is_goal():
        return next_state

    # Otherwise, prepare for the next level of the depth search by choosing a cell to try
    cell = next_state.pick_next_cell()
    row = cell[0]
    col = cell[1]

    # Attempt a depth-first search on all possible values for that cell
    for value in next_state.final_possible_values:
        if next_state.final_values[row, col] & value == 0:
            continue
        #  Next step
        attempt_state = copy.deepcopy(next_state)
        attempt_state.final_values[row, col] = value
        attempt_state.set_value(row, col)
        if attempt_state.is_goal():
            return attempt_state

        if not attempt_state.is_invalid() and not attempt_state.is_malformed():
            deep_state = depth_first_search(attempt_state)
            if deep_state is not None and deep_state.is_goal():
                return deep_state

    return None


def sudoku_solver(sudoku):
    """
    Solves a Sudoku puzzle and returns its unique solution.

    Input
        sudoku : 9x9 numpy array
            Empty cells are designated by 0.

    Output
        9x9 numpy array of integers
            It contains the solution, if there is one. If there is no solution, all array entries should be -1.
    """

    # First transform the grid into a SudokuState object
    partial_state = SudokuState(sudoku)

    # Check that the grid wasn't an invalid grid from the beginning
    if partial_state.is_malformed():
        return np.full((9, 9), -1)

    # Check that the grid is not already solved
    if partial_state.is_goal():
        partial_state.decode_sudoku()
        return partial_state.final_values

    # Perform the searching algorithm
    solution = depth_first_search(partial_state)
    # If no solution is possible, return a grid of -1s
    if solution is None:
        return np.full((9, 9), -1)
    # Otherwise return the decoded grid
    solution.decode_sudoku()

    return solution.final_values


def main():
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard', 'extreme']
    master = time.process_time()
    for difficulty in difficulties:
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        main_start_time = time.process_time()
        print(difficulty)
        #for i in range(len(sudokus)):
        for i in [10]:
            sudoku = sudokus[i].copy()
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            if np.array_equal(your_solution, solutions[i]):
                print(f"[OK] Test {difficulty}", i, "This sudoku took", end_time - start_time, "seconds.")
                # print(end_time - start_time)
                count += 1
            else:
                print(f"[[NG]] Test {difficulty}", i, "This sudoku took", end_time - start_time)
                print(your_solution)
                print(solutions[i])
        main_end_time = time.process_time()
        print("total run time :", main_end_time - main_start_time)
        print()
    print(time.process_time() - master)

main()
import numpy as np
# will be re-imported just in case


# a way of checking if we completed the grid (assuming all rules followed)
def is_solved(sudoku):
    if np.sum(sudoku) == 405:
        return True
    return False


# generate index of cells with zeros
def get_zeros(sudoku):
    zeros_index = [(y, x) for y in range(9) for x in range(9) if sudoku[y][x] == 0]
    return zeros_index


# generate index of cells with zeros
def clues(sudoku):
    val = (81 - len(get_zeros(sudoku)))
    return val


# generate an optimised start sequence for backtracking
def get_zeros_backtrack(sudoku):
    # all code only sequences the cells in row-sequence and col-sequence
    # for some reason using col-sequence slowed down those cases slightly
    # could be due to the way numpy-arrays are addressed
    # or the slow down from generating the index itself.
    if clues(sudoku) > 26:  # it is a fudge value - 26 and it almost doesn't matter
        row_list = [0] * 9
        for row_n, row in enumerate(sudoku):
            for cell in row:
                if cell != 0:
                    row_list[row_n] += 1

        max_value_r = max(row_list)
        max_index1 = row_list.index(max_value_r)

        zeros_index1 = [(y, x) for y in range(max_index1, 9) for x in range(9) if sudoku[y][x] == 0]
        zeros_index2 = [(y, x) for y in range(max_index1) for x in range(9) if sudoku[y][x] == 0]

        zero_index = zeros_index1 + zeros_index2

    else:
        zero_index = get_zeros(sudoku)
    return zero_index


# solve the most obvious cells
def solve_for_options(options, sudoku):
    for k in options:
        if len(options[k]) == 1:
            sudoku[k] = options[k][0]
    return sudoku


# List1 - remove (to avoid set conversion)
def naked_helper(list1, remove):
    result = [value for value in list1 if value not in remove]
    return result


# Hidden singles
def hidden_singles(sudoku):
    zeros = get_zeros(sudoku)
    options = get_options(sudoku)
    for (y_pos, x_pos) in zeros:
        option = options[(y_pos, x_pos)]
        for col in [r for r in range(9) if r != x_pos]:
            if (y_pos, col) in options:
                d = options[(y_pos, col)]
                option = naked_helper(option, d)
            if len(option) < 1:
                break
        if len(option) == 1:
            # it could be this value will violates other cells (like hard 15)
            if is_move_valid(sudoku, y_pos, x_pos, option[0]):
                sudoku[(y_pos, x_pos)] = option[0]
            else:
                return -1 * np.ones_like(sudoku)

    zeros = get_zeros(sudoku)
    for (y_pos, x_pos) in zeros:
        option = options[(y_pos, x_pos)]
        for row in [r for r in range(9) if r != y_pos]:
            if (row, x_pos) in options:
                d = options[(row, x_pos)]
                option = naked_helper(option, d)
        if len(option) == 1:
            # it could be this value will violates other cells (like hard 15)
            if is_move_valid(sudoku, y_pos, x_pos, option[0]):
                sudoku[(y_pos, x_pos)] = option[0]
            else:
                return -1 * np.ones_like(sudoku)

    zeros = get_zeros(sudoku)
    for (y_pos, x_pos) in zeros:
        option = options[(y_pos, x_pos)]
        sub_cell_y = (y_pos // 3) * 3
        sub_cell_x = (x_pos // 3) * 3
        for y in range(sub_cell_y, sub_cell_y + 3):
            for x in range(sub_cell_x, sub_cell_x + 3):
                if x == x_pos and y == y_pos:
                    continue
                elif (y, x) in options:
                    d = options[(y, x)]
                    option = naked_helper(option, d)
        if len(option) == 1:
            # it could be this value will violates other cells (like hard 15)
            if is_move_valid(sudoku, y_pos, x_pos, option[0]):
                sudoku[(y_pos, x_pos)] = option[0]
            else:
                return -1 * np.ones_like(sudoku)
    return sudoku


# an options dict of each cell (for validation check of the board validity - as solvable)
def get_options_full(sudoku):
    options = hidden_pairs(sudoku)  # this is the most robust way of detecting a defective game
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] != 0:
                options[(y, x)] = []
    return options


# an options dict of each 0 cell
def get_options(sudoku):
    zeros = get_zeros(sudoku)
    options = {}
    for (y, x) in zeros:
        options[(y, x)] = [opt for opt in range(1, 10) if is_move_valid(sudoku, y, x, opt)]
    return options


# search and remove based on naked pairs (in rows, cols, boxes)
def get_options_nkd_pairs(sudoku):
    options = get_options(sudoku)
    # converted to set equations (mostly) - no major speed difference, probably due to the mix of lists and sets
    sub_sets = [{1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 6}, {1, 7}, {1, 8}, {1, 9},
                {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {2, 8}, {2, 9}, {3, 4}, {3, 5}, {3, 6}, {3, 7}, {3, 8}, {3, 9},
                {4, 5}, {4, 6}, {4, 7}, {4, 8}, {4, 9}, {5, 6}, {5, 7}, {5, 8}, {5, 9}, {6, 7}, {6, 8}, {6, 9}, {7, 8},
                {7, 9}, {8, 9}]
    
    for sub_set in sub_sets:
        for row in range(9):
            location = []    
            for col in range(9):
                if (row, col) in options:
                    if set(options[(row, col)]) == sub_set:
                        location.append((row, col))
                if len(location) == 2:
                    for col2 in range(9):
                        if (row, col2) in options and (row, col2) not in location:
                            options[(row, col2)] = naked_helper(options[(row, col2)], list(sub_set))

    for sub_set in sub_sets:
        for col in range(9):
            location = []    
            for row in range(9):
                if (row, col) in options:
                    if set(options[(row, col)]) == sub_set:
                        location.append((row, col))
                if len(location) == 2:
                    for row2 in range(9):
                        if (row2, col) in options and (row2, col) not in location:
                            options[(row2, col)] = naked_helper(options[(row2, col)], list(sub_set))

    # still old for-loop based value comparison
    for sub_set in sub_sets:
        for row in [0, 3, 6]:
            for col in [0, 3, 6]:
                location = []
                for y in range(row, row + 3):
                    for x in range(col, col + 3):
                        if (y, x) in options:
                            if set(options[(y, x)]) == sub_set:
                                location.append((y, x))
                        if len(location) == 2:
                            for y2 in range(row, row + 3):
                                for x2 in range(col, col + 3):
                                    if (y2, x2) in options and (y2, x2) not in location:
                                        options[(y2, x2)] = naked_helper(options[(y2, x2)], list(sub_set))
    return options


def hidden_pairs(sudoku):
    options = get_options_nkd_pairs(sudoku)
    sub_sets = [{1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 6}, {1, 7}, {1, 8}, {1, 9},
                {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {2, 8}, {2, 9}, {3, 4}, {3, 5}, {3, 6}, {3, 7}, {3, 8}, {3, 9},
                {4, 5}, {4, 6}, {4, 7}, {4, 8}, {4, 9}, {5, 6}, {5, 7}, {5, 8}, {5, 9}, {6, 7}, {6, 8}, {6, 9}, {7, 8},
                {7, 9}, {8, 9}]

    # hidden pairs for row
    for y in range(9):
        location = []
        for sub_set in sub_sets:
            count = 0
            tmp = []
            for x in range(9):
                if (y, x) not in options:
                    continue
                unit = options[(y, x)]
                if sub_set.issubset(unit):
                    count += 1
                    tmp.append((y, x))
            if count == 2:
                location.append((sub_set, tmp[0], tmp[1]))
                tmp.clear()

        for (digits, loc1, loc2) in location:
            found_first = 0
            for digit_number in (list(digits)):
                count2 = 0
                single_digit = {digit_number}
                for x in range(9):
                    if (y, x) not in options:
                        continue
                    unit2 = options[(y, x)]
                    if single_digit.issubset(unit2):
                        if (y, x) != loc1 and (y, x) != loc2:
                            count2 = 0
                            found_first = 0
                            break
                        else:
                            count2 += 1
                if count2 == 2 and found_first != 1:
                    found_first += 1
                elif count2 == 2 and found_first == 1:
                    options[loc1] = list(digits)
                    options[loc2] = list(digits)


# hidden pairs for columns
    for x in range(9):
        location2 = []
        for sub_set in sub_sets:
            count = 0
            tmp = []
            for y in range(9):
                if (y, x) not in options:
                    continue
                unit = options[(y, x)]
                if sub_set.issubset(unit):
                    count += 1
                    tmp.append((y, x))
            if count == 2:
                location2.append((sub_set, tmp[0], tmp[1]))
                tmp.clear()

        for (digits, loc1, loc2) in location2:
            found_first = 0
            for digit_number in (list(digits)):
                count2 = 0
                single_digit = {digit_number}
                for y in range(9):
                    if (y, x) not in options:
                        continue
                    unit2 = options[(y, x)]
                    if single_digit.issubset(unit2):
                        if (y, x) != loc1 and (y, x) != loc2:
                            count2 = 0
                            found_first = 0
                            break
                        else:
                            count2 += 1
                if count2 == 2 and found_first != 1:
                    found_first += 1
                elif count2 == 2 and found_first == 1:
                    options[loc1] = list(digits)
                    options[loc2] = list(digits)
    
    # hidden pairs for boxes
    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            location3 = []
            for sub_set in sub_sets:
                count = 0
                tmp = []
                for y in range(row, row + 3):
                    for x in range(col, col + 3):
                        if (y, x) in options:
                            unit = options[(y, x)]
                            if sub_set.issubset(unit):
                                count += 1
                                tmp.append((y, x))
                if count == 2:
                    location3.append((sub_set, tmp[0], tmp[1]))        
                    tmp.clear()
                        
            for (digits, loc1, loc2) in location3:
                found_first = 0
                for digit_number in (list(digits)):
                    count2 = 0
                    single_digit = {digit_number}
                    skip = 0
                    for y in range(row, row + 3):
                        for x in range(col, col + 3):
                            if (y, x) in options and skip == 0:
                                unit2 = options[(y, x)]
                                if single_digit.issubset(unit2):
                                    if (y, x) != loc1 and (y, x) != loc2:
                                        count2 = 0
                                        found_first = 0
                                        skip = 1
                                    else:
                                        count2 += 1
                    if count2 == 2 and found_first != 1:
                        found_first += 1
                    elif count2 == 2 and found_first == 1:
                        options[loc1] = list(digits)
                        options[loc2] = list(digits)
    
    return options


def check_valid_state(sudoku):
    options = get_options_full(sudoku)

    # element_row
    rows_set = []
    for y in range(9):
        tmp_index = [(y, x) for x in range(9)]
        rows_set.append(tmp_index)

    # element_col
    cols_set = []
    for x in range(9):
        tmp_index = [(y, x) for y in range(9)]
        cols_set.append(tmp_index)

    # check rows and columns
    for row_col_set in [rows_set, cols_set]:
        for index in row_col_set:
            check_list = [sudoku[y][x] for y, x in index]

            # check that they are all containing at max a single entry of each value
            if not all_single_qty(check_list):
                return False

            # check that within the compliant options, it possible to generate a valid result
            range_cells = (index[0], index[len(index) - 1])
            check_list += list(scan_options(options, range_cells))
            possible = all_available(check_list)
            if not possible:
                return False

    # check boxes
    for y0 in [0, 3, 6]:
        for x0 in [0, 3, 6]:
            sub_box = []
            for y in range(y0, y0 + 3):
                for x in range(x0, x0 + 3):
                    sub_box.append(sudoku[y, x])
                    # all the values of a sub-box
            if not all_single_qty(sub_box):
                return False

            for y in range(y0, y0 + 3):
                for x in range(x0, x0 + 3):
                    full_opt = set(options[y, x])
                    sub_box += full_opt
                    # sum sudoku values and options
            possible = all_available(sub_box)
            if not possible:
                return False
    return True


# uses the get_options to check all options ina  given row/col/box
def scan_options(options, range_cells):
    # modified to not use sudoku but directly take the options list
    # using sets to easily get the set union
    # and performs the union with each cell in an rcb
    first_cell, last_cell = range_cells
    scanned = set()
    
    for y in range(first_cell[0], last_cell[0] + 1):
        for x in range(first_cell[1], last_cell[1] + 1):
            sub_opt = set(options[y, x])
            scanned = scanned | sub_opt
    return scanned


# confirm only 1 input per value in rcb (row/col/box)
def all_single_qty(rcb):
    qty = count_hits(rcb)
    for max_n in qty:  # exclude 0:
        if max_n > 1:
            return False  # more than 1 of value
    return True


# confirm all values are available in rcb (row/col/box)
def all_available(rcb):
    qty = count_hits(rcb)
    for min_n in qty:  # exclude 0:
        if min_n == 0:
            return False
    return True


# used by all_available() and all_single_qty()
def count_hits(rcb):
    qty = [0] * 9
    for value in rcb:
        if value > 0:  # no need to check for 0
            qty[value - 1] += 1  # if we see 1, save in pos 0, if we see 9, save in pos 8
    return qty


# most basic algo - used to generate zeros - initially used to validate back-tracking guess
def is_move_valid(sudoku, y, x, possible):
    for index in range(9):
        if (sudoku[y][index] == possible) or (sudoku[index][x] == possible):
            return False
    sub_cell_y = (y // 3) * 3
    sub_cell_x = (x // 3) * 3
    for y in range(sub_cell_y, sub_cell_y + 3):
        for x in range(sub_cell_x, sub_cell_x + 3):
            if sudoku[y][x] == possible:
                return False
    return True


def back_tracker(valid_options, zeros, sudoku):
    for (y_pos, x_pos) in zeros:
        valid_values = valid_options[(y_pos, x_pos)]
        if len(valid_values) < 1:  # invalid grid if there is no option (not necessary probably)
            return sudoku
        for possible in valid_values:
            # theoretically we can delete some options, but it is slow to re-build the options list
            if is_move_valid(sudoku, y_pos, x_pos, possible):
                sudoku[y_pos, x_pos] = possible
                dump, *new_zeros = zeros
                sudoku = back_tracker(valid_options, new_zeros, sudoku)
                if not is_solved(sudoku):
                    sudoku[y_pos, x_pos] = 0
                else:
                    break
        break
    return sudoku


# main wrapper function
def sudoku_solver(sudoku):
    # same like -1 * np.ones_like(sudoku)
    failed = np.array([
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1],
                    [-1, -1, -1, -1, -1, -1, -1, -1, -1]
                    ])

    sudoku = hidden_singles(sudoku)
    loop_flag = True
    while loop_flag:
        start = sudoku.copy()
        sudoku = hidden_singles(sudoku)
        options = get_options_nkd_pairs(sudoku)
        sudoku = solve_for_options(options, sudoku)
        finish = sudoku.copy()
        if np.array_equal(start, finish): # check if it is worth to loop again (may cause 1 extra redundant loop)
            loop_flag = False
    if not check_valid_state(sudoku):  # check if it is simply not solvable
        return failed
    elif is_solved(sudoku):
        return sudoku
    options = hidden_pairs(sudoku)  # use the least options for back-tracking

    sudoku = solve_for_options(options, sudoku)
    zeros = get_zeros_backtrack(sudoku)  # use the least options for back-tracking
    sudoku = back_tracker(options, zeros, sudoku)
    if not is_solved(sudoku):
        return failed
    return sudoku


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
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            if np.array_equal(your_solution, solutions[i]):
                print(f"[OK] Test {difficulty}", i, "This sudoku took", end_time - start_time, "seconds.")
                print(end_time - start_time)
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

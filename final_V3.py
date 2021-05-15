import numpy as np  # will be re-imported just in case


# a way of checking if we completed the grid (assuming all rules followed)
def is_solved(sudoku):
    if np.sum(sudoku) == 405:
        return True
    return False


def get_zeros(sudoku):
    zeros_index = [(y, x) for y in range(9) for x in range(9) if sudoku[y][x] == 0]
    return zeros_index


def solve_singles(options, sudoku):
    for k in options:
        if len(options[k]) == 1:
            sudoku[k] = options[k][0]
    return sudoku


def naked_helper(list1, remove):
    result = [value for value in list1 if value not in remove]
    return result


def hidden_singles(sudoku):
    zeros = get_zeros(sudoku)
    options = get_options(sudoku)  # using get_options_nkd_paris is even faster on some
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

def no_duplicates(sudoku, rcb):
    count = [0] * (10)
    for x in rcb:
        count[x] += 1

    for c in count[1:]:  # exclude 0:
        if c > 1:
            return False  # more than 1 of value
    return True

def all_exist(rcb):
    """ verify that there is at least one of each number present """
    count = [0] * 10
    for x in rcb:
        count[x] += 1
    for c in count[1:]:  # exclude 0:
        print(c)
        if c == 0:
            return False
    return True

def get_options_full(sudoku):
    options = {}
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                options[(y, x)] = set()
            else:
                options[(y, x)] = [opt for opt in range(1, 10) if is_move_valid(sudoku, y, x, opt)]
    return options

def get_options(sudoku):
    zeros = get_zeros(sudoku)
    options = {}
    for (y, x) in zeros:
        options[(y, x)] = [opt for opt in range(1, 10) if is_move_valid(sudoku, y, x, opt)]
    return options

def get_options_nkd_pairs(sudoku):
    options = get_options(sudoku)
    for row in range(9):
        for col in range(9):
            if (row, col) in options:
                val = options[row, col]
                if len(val) == 2:
                    for col1 in range(9):
                        if (row, col1) in options:
                            val1 = options[row, col1]
                            if col1 != col and len(val1) == 2 and val == val1:
                                for col2 in range(9):
                                    if (row, col2) in options:
                                        if col2 != col and col2 != col1:
                                            val2 = options[(row, col2)]
                                            options[(row, col2)] = naked_helper(val2, val)

# faster to start over since options will be how been reduced
    for col in range(9):
        for row in range(9):
            if (row, col) in options:
                val = options[row, col]
                if len(val) == 2:
                    for row1 in range(9):
                        if (row1, col) in options:
                            val1 = options[row1, col]
                            if row1 != row and len(val1) == 2 and val == val1:
                                for row2 in range(9):
                                    if (row2, col) in options:
                                        if row2 != row and row2 != row1:
                                            val2 = options[(row2, col)]
                                            options[(row2, col)] = naked_helper(val2, val)

    for row in [0, 3, 6]:
        for col in [0, 3, 6]:
            suby = (row // 3) * 3
            subx = (col // 3) * 3
            for y in range(suby, suby + 3):
                for x in range(subx, subx + 3):
                    if (y, x) in options:
                        val = options[y, x]
                        if len(val) == 2:
                            for y1 in range(suby, suby + 3):
                                for x1 in range(subx, subx + 3):
                                    if (y1, x1) in options:
                                        val1 = options[y1, x1]
                                        if (y1, x1) != (y, x) and len(val1) == 2 and val == val1:
                                            for y2 in range(suby, suby + 3):
                                                for x2 in range(subx, subx + 3):
                                                    if (y2, x2) in options:
                                                        if (y2, x2) != (y, x) and (y2, x2) != (y1, x1):
                                                            val2 = options[(y2, x2)]
                                                            options[(y2, x2)] = naked_helper(val2, val)
    return options


def get_options_nkd_trpl(sudoku):
    # this algo only checks rows and columns
    options = get_options_nkd_pairs(sudoku)  # faster on 1 puzzle I tested
    for row in range(9):
        for col in range(9):
            if (row, col) in options:
                val = options[row, col]
                if len(val) == 3:
                    for col1 in range(9):
                        if (row, col1) in options:
                            val1 = options[row, col1]
                            if col1 != col and len(val1) == 3 and val1 == val:
                                for col2 in range(9):
                                    if (row, col2) in options:
                                        val2 = options[row, col2]
                                        if col2 != col and col2 != col1 and len(val1) == 3 and val2 == val1:
                                            for col3 in range(9):
                                                if (row, col3) in options:
                                                    if col3 != col2 and col3 != col1 and col3 != col:
                                                        val3 = options[(row, col3)]
                                                        options[(row, col3)] = naked_helper(val3, val)
    # faster to start over since options will be how been reduced
    for row in range(9):
        for col in range(9):
            if (row, col) in options:
                val = options[row, col]
                if len(val) == 3:
                    for row1 in range(9):
                        if (row1, col) in options:
                            val1 = options[row1, col]
                            if row1 != row and len(val1) == 3 and val1 == val:
                                for row2 in range(9):
                                    if (row2, col) in options:
                                        val2 = options[row2, col]
                                        if row2 != row and row2 != row1 and len(val1) == 3 and val2 == val1:
                                            for row3 in range(9):
                                                if (row3, col) in options:
                                                    if row3 != row2 and row3 != row1 and row3 != row:
                                                        val3 = options[(row3, col)]
                                                        options[(row3, col)] = naked_helper(val3, val)

    return options


def back_tracker(valid_options, zeros, current_state):
    for (y_pos, x_pos) in zeros:
        valid_values = valid_options[(y_pos, x_pos)]
        if len(valid_values) < 1:  # invalid grid if there is no option...
            return current_state
        for possible in valid_values:
            if is_move_valid(current_state, y_pos, x_pos, possible):
                current_state[y_pos, x_pos] = possible
                dump, *new_zeros = zeros
                current_state = back_tracker(valid_options, new_zeros, current_state)
                if not is_solved(current_state):
                    current_state[y_pos, x_pos] = 0
                else:
                    break
        break
    return current_state

def check_possible(sudoku):
        """ check if each row/column/box can have all unique elements"""
        #get rows
        rows_set = []
        for i in range(9):
            inds = [(i, j) for j in range(9)]
            rows_set.append(inds)
        # get columns
        cols_set = []
        for j in range(9):
            inds = [(i, j) for i in range(9)]
            cols_set.append(inds)
        # # check rows and columns
        type_ = ['row', 'col']
        for t, inds_set in enumerate([rows_set, cols_set]):
            for k, inds in enumerate(inds_set):
                arr = [sudoku[i][j] for i, j in inds]
                if not no_duplicates(arr):
                    print("duplicate1")
                    return False
                arr += list(get_candidates(sudoku, inds[0], inds[-1]))
                print(arr)
                possible = all_exist(arr)
                if not possible:
                    print("not possible1")
                    return False
        # check boxes
        for i0 in [0,3,6]:
            for j0 in [0,3,6]:
                suby = (i0 // 3) * 3
                subx = (j0 // 3) * 3
                sub_box = []
                for y in range(suby, suby + 3):
                    for x in range(subx, subx + 3):\
                        sub_box.append(sudoku[y,x])

                if not no_duplicates(sub_box):
                    print("duplicate1")
                    return 
                
                full_options = get_options_full(sudoku)             
                for i in range(i0, i0 + 3):
                    for j in range(j0, j0 + 3):
                        full_opt = set(full_options[i,j])
                        sub_box += full_opt
                        print(sub_box)
                possible = all_exist(sub_box)
                print(possible)
                if not possible:
                    print("not possible1")
                    return False
        return True


def get_candidates(sudoku, start, end):
    " get candidates within two corners of a rectangle/column/row"
    candidates = set()  #null set
    full_options = get_options_full(sudoku)
    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            full_opt = set(full_options[i,j])
            #print()
            #print("First", i,j, candidates, full_opt)
            candidates = candidates | full_opt # grow the list with all that we've seen
            #print(candidates)        
    return candidates


#rcb
def no_duplicates(rcb):
    count = [0] * (10)
    for x in rcb:
        count[x] += 1

    for c in count[1:]:  # exclude 0:
        if c > 1:
            return False  # more than 1 of value
    return True

def all_exist(rcb):
    """ verify that there is at least one of each number present """
    count = [0] * 10
    for x in rcb:
        count[x] += 1
    for c in count[1:]:  # exclude 0:
        #print(c)
        if c == 0:
            return False
    return True


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


def sudoku_solver(sudoku):
    loop_flag = True
    check_possible(sudoku)
    while loop_flag:
        start = sudoku.copy()
        sudoku = hidden_singles(sudoku)
        options = get_options_nkd_trpl(sudoku)
        sudoku = solve_singles(options, sudoku)
        
        # maybe we solved it
        if np.sum(sudoku) < 0 or is_solved(sudoku):
            return sudoku
        finish = sudoku.copy()
        
        # maybe we cannot do more...
        if np.array_equal(start, finish):
            loop_flag = False
            
    # if not, got to try brute-force but... (may take long)
    options = get_options_nkd_trpl(sudoku)
    zeros = get_zeros(sudoku)
    sudoku = back_tracker(options, zeros, sudoku)
    if not is_solved(sudoku):
        return -1 * np.ones_like(sudoku)
    return sudoku


def main():
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard', 'extreme']
    difficulties = ['medium']

    for difficulty in difficulties:
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        main_start_time = time.process_time()
        #for i in range(len(sudokus)):
        for i in [5]:
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

        main_end_time = time.process_time()
        print("total run time :", main_end_time-main_start_time)


main()

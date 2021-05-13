import numpy as np

# a way of checking if we completed the grid (assuming all rules followed)
def sudoku_sovled(sudoku):
    if np.sum(sudoku) == 405 and len(sudoku_zeros(sudoku))==0:
        return True
    else:
        return False


# find all zeros
def sudoku_zeros(sudoku):
    zeros_index = []
    for y_pos in range(9):
        for x_pos in range(9):
            if sudoku[y_pos][x_pos] == 0:
                zeros_index.append((y_pos, x_pos))
    return zeros_index

def sort_by_values_len(d):
    z = d
    return z

def naked_singles(sudoku):
    valid_options = possibilities(sudoku)
    for k in valid_options:
        if len(valid_options[k]) == 1:
            sudoku[k] = valid_options[k][0]
    return sudoku


def naked_helper(a,b):
    for value in b:
        if value in a:
            a.remove(value)


def hidden_singles(sudoku):
    zeros = sudoku_zeros(sudoku)
    valid_options = possibilities(sudoku)
    for (y_pos, x_pos) in zeros:
        option = valid_options[(y_pos, x_pos)].copy()
        for col in range(9):
            if col == x_pos:
                continue
            elif (y_pos, col) in valid_options:
                d = valid_options[(y_pos, col)]
                naked_helper(option, d)
            if len(option) < 1:
                break
        if len(option) == 1:
            if check_move(sudoku, y_pos, x_pos, option[0]):
                sudoku[(y_pos, x_pos)] = option[0]
            else:
                return -1 * np.ones_like(sudoku)

    zeros = sudoku_zeros(sudoku)
    valid_options = possibilities(sudoku)
    for (y_pos, x_pos) in zeros:
        option = valid_options[(y_pos, x_pos)].copy()
        for row in range(9):
            if row == y_pos:
                continue
            elif (row, x_pos) in valid_options:
                d = valid_options[(row, x_pos)]
                naked_helper(option, d)
        if len(option) == 1:
            if check_move(sudoku, y_pos, x_pos, option[0]):
                sudoku[(y_pos, x_pos)] = option[0]
            else:
                return -1 * np.ones_like(sudoku)

    zeros = sudoku_zeros(sudoku)
    valid_options = possibilities(sudoku)
    for (y_pos, x_pos) in zeros:
        option = valid_options[(y_pos, x_pos)].copy()
        sub_cell_y = (y_pos // 3) * 3
        sub_cell_x = (x_pos // 3) * 3
        for y in range(sub_cell_y, sub_cell_y + 3):
            for x in range(sub_cell_x, sub_cell_x + 3):
                if x == x_pos and y == y_pos:
                    continue
                elif (y, x) in valid_options:
                    d = valid_options[(y, x)]
                    naked_helper(option, d)
        if len(option) == 1:
            if check_move(sudoku, y_pos, x_pos, option[0]):
                sudoku[(y_pos, x_pos)] = option[0]
            else:
                return -1 * np.ones_like(sudoku)
    return sudoku


def possibilities(sudoku):
    zeros = sudoku_zeros(sudoku)
    valid_options = {}
    for (y_pos, x_pos) in zeros:
            tmp = []
            for possible in range(1, 10):
                if check_move(sudoku, y_pos, x_pos, possible):
                    tmp.append(possible)
            valid_options[(y_pos, x_pos)] = tmp
    valid_options = sort_by_values_len(valid_options)
    return valid_options



def sudoku_solver(sudoku):
    f = True
    i = 0
    while f:
        i = i + 1
        start_sudoku = sudoku.copy()
        sudoku = naked_singles(sudoku)
        sudoku = hidden_singles(sudoku)
        if np.array_equal(start_sudoku, sudoku):
            f = False
    if np.sum(sudoku) < 0:
        return sudoku
    zeros = sudoku_zeros(sudoku)
    valid_options = possibilities(sudoku)
    sudoku = sudoku_solve(valid_options, zeros, sudoku)
    if not sudoku_sovled(sudoku):
        return -1 * np.ones_like(sudoku)
    else:
        return sudoku


def sudoku_solve(valid_options, zeros, current_state):
    for (y_pos, x_pos)in zeros:
        valid_values = valid_options[(y_pos, x_pos)]
        for possible in valid_values:
            if check_move(current_state, y_pos, x_pos, possible):
                current_state[y_pos, x_pos] = possible
                dump, *new_zeros = zeros
                #new_valid_options = possibilities(new_zeros, current_state) #no major speed gain (+/- same)
                current_state = sudoku_solve(valid_options, new_zeros, current_state)
                if not sudoku_sovled(current_state):
                    current_state[y_pos, x_pos] = 0
                else:
                    break
        break
    return current_state


def check_move(temp_state, y_pos, x_pos, possible):
    for index in range(9):
        if (temp_state[y_pos][index] == possible) or (temp_state[index][x_pos] == possible):
            return False
    sub_cell_y = (y_pos // 3) * 3
    sub_cell_x = (x_pos // 3) * 3
    for y in range(sub_cell_y, sub_cell_y + 3):
        for x in range(sub_cell_x, sub_cell_x + 3):
            if temp_state[y][x] == possible:
                return False
    return True


SKIP_TESTS = False


def main():
    import time
    difficulties = ['very_easy', 'easy', 'medium', 'hard']
    #difficulties = ['hard']

    for difficulty in difficulties:
        #print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        main_start_time = time.process_time()
        for i in range(len(sudokus)):
        #for i in [14]:

            for j in range(1):
                sudoku = sudokus[i].copy()
                #print(sudoku)
                start_time = time.process_time()
                your_solution = sudoku_solver(sudoku)
                end_time = time.process_time()


                if np.array_equal(your_solution, solutions[i]):
                    print(f"[OK] Test {difficulty} sudoku number", i,j, "This sudoku took", end_time - start_time, "seconds to solve.")
                    count += 1
                else:
                    print(f"[[NG]] Test {difficulty} sudoku number", i,j, "This sudoku took", end_time - start_time,
                          "seconds to solve.")


        if count != len(sudokus):
            print("SHIIIIIIIIIIIIIIIIIIIIIIIIIIIIITTTTTTTTT")
            # if count < len(sudokus):
            #    break
        main_end_time = time.process_time()
        print("total run time :", main_end_time-main_start_time)
main()

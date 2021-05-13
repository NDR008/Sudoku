import numpy as np
import random

#some online tests i found, not used for now.
a = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 3, 6, 0, 0, 0, 0, 0],
     [0, 7, 0, 0, 9, 0, 2, 0, 0],
     [0, 5, 0, 0, 0, 7, 0, 0, 0],
     [0, 0, 0, 0, 4, 5, 7, 0, 0],
     [0, 0, 0, 1, 0, 0, 0, 3, 0],
     [0, 0, 1, 0, 0, 0, 0, 6, 8],
     [0, 0, 8, 5, 0, 0, 0, 1, 0],
     [0, 9, 0, 0, 0, 0, 4, 0, 0]]
extra1 = np.array(a)

b = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 1, 2, 0, 0, 0, 0],
     [0, 0, 0, 3, 4, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 5, 0, 0],
     [0, 0, 0, 0, 0, 5, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0, 0, 0, 0, 0]]
extra2 = np.array(b)

c = [[0, 0, 0, 0, 0, 5, 0, 8, 0],
     [0, 0, 0, 6, 0, 1, 0, 4, 3],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 1, 0, 5, 0, 0, 0, 0, 0],
     [0, 0, 0, 2, 0, 6, 0, 0, 0],
     [3, 0, 0, 0, 0, 0, 0, 0, 5],
     [5, 3, 0, 0, 0, 0, 0, 6, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 4],
     [0, 0, 0, 0, 0, 0, 0, 0, 0]]
extra3 = np.array(c)

extra = [extra1, extra2, extra3]

# a way of checking if we completed the grid (assuming all rules followed)
def sudoku_sovled(sudoku):
    if np.sum(sudoku) == 405:
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

def sudoku_options(sudoku):
    options = [0] * 10
    for y_pos in range(9):
        for x_pos in range(9):
            options[sudoku[y_pos][x_pos]] = options[sudoku[y_pos][x_pos]] + 1
    _, *options = options
    return options


def sort_by_values_len(d):
    z = {}
    for k in sorted(d, key=lambda k: len(d[k])):
        z[k] = d[k]
    return z


def initial_pass(sudoku):
    zeros = sudoku_zeros(sudoku)
    valid_options = possibilities(zeros, sudoku)
    # for zero_index in zeros:
    #     y_pos, x_pos = zero_index
    #     valid_option = valid_options[zero_index]
    #     if len(valid_option) == 1:
    #         sudoku[y_pos, x_pos] = valid_option[0]
    #     else:
    #         return sudoku
    for k in valid_options:
        if len(valid_options[k])==1:
            sudoku[k]=valid_options[k][0]
        elif len(valid_options[k])>1:
            return sudoku
    return sudoku


def naked_helper(a,b):
    z = a.copy()
    for value in b:
        if value in z:
            z.remove(value)
    return z


def naked(sudoku):
    zeros = sudoku_zeros(sudoku)
    valid_options = possibilities(zeros, sudoku)
    for (y_pos, x_pos) in zeros:
        c = valid_options[(y_pos, x_pos)]
        for col in range(9):
            if col == x_pos:
                continue
            elif (y_pos, col) in valid_options:
                d = valid_options[(y_pos, col)]
                c = naked_helper(c, d)
        c = naked_helper(c, [0])
        if len(c) == 1:
            sudoku[(y_pos, x_pos)] = c[0]
        else:
            #valid_options = possibilities(zeros, sudoku)
            for row in range(9):
                if row == y_pos:
                    continue
                elif (row, x_pos) in valid_options:
                    d = valid_options[(row, x_pos)]
                    c = naked_helper(c, d)
            c = naked_helper(c, [0])
            if len(c) == 1:
                sudoku[(y_pos, x_pos)] = c[0]

            else:
                #valid_options = possibilities(zeros, sudoku)
                sub_cell_y = (y_pos // 3) * 3
                sub_cell_x = (x_pos // 3) * 3
                for y in range(sub_cell_y, sub_cell_y + 3):
                    for x in range(sub_cell_x, sub_cell_x + 3):
                        if x == x_pos and y == y_pos:
                            continue
                        elif (y, x) in valid_options:
                            d = valid_options[(y, x)]
                            c = naked_helper(c, d)
                c = naked_helper(c, [0])
                if len(c) == 1:
                    sudoku[(y_pos, x_pos)] = c[0]
    return sudoku


def possibilities(zeros, sudoku):
    valid_options = {}
    for (y_pos, x_pos) in zeros:
            tmp = []
            for possible in range(1, 10):
                if check_move(sudoku, y_pos, x_pos, possible):
                    tmp.append(possible)
            #if len(tmp) > 555:
                #random.shuffle(tmp) #no major gain... but hard 4 went from 5.5s to 0.06s but hard 5 went from 26 to 40
            valid_options[(y_pos, x_pos)] = tmp
    valid_options = sort_by_values_len(valid_options)
    #print(valid_options)
    return valid_options


def sudoku_solver(sudoku):
    f = True
    i = 0
    while f:
        i = i + 1
        start_sudoku = sudoku.copy()
        sudoku = initial_pass(sudoku)
        sudoku = naked(sudoku)
        if np.array_equal(start_sudoku, sudoku):
            f = False

    zeros = sudoku_zeros(sudoku)
    valid_options = possibilities(zeros, sudoku)
    options = sudoku_options(sudoku)
    sol = sudoku_solve(valid_options, zeros, options, sudoku)
    if not sudoku_sovled(sol):
        return -1 * np.ones_like(sol)
    else:
        return sol

def sudoku_solve(valid_options, zeros, options, current_state):
    for (y_pos, x_pos)in zeros:
        valid_values = valid_options[(y_pos, x_pos)]
        for possible in valid_values:
            if check_move(current_state, y_pos, x_pos, possible):
                options[possible-1] += 1
                current_state[y_pos, x_pos] = possible
                dump, *new_zeros = zeros
                #new_valid_options = possibilities(new_zeros, current_state) #no major speed gain (+/- same)
                current_state = sudoku_solve(valid_options, new_zeros, options, current_state)
                if not sudoku_sovled(current_state):
                    current_state[y_pos, x_pos] = 0
                    options[possible - 1] -= 1
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
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        main_start_time = time.process_time()
        for i in range(len(sudokus)):
        #for i in [10]:

            for j in range(1):
                sudoku = sudokus[i].copy()
                #print(sudoku)
                #print(solutions[i])
                start_time = time.process_time()
                your_solution = sudoku_solver(sudoku)
                end_time = time.process_time()
                #print(your_solution)

                if np.array_equal(your_solution, solutions[i]):
                    print(f"[OK] Test {difficulty} sudoku number", i,j, "This sudoku took", end_time - start_time,
                          "seconds to solve.")
                    count += 1
                else:
                    print(f"[NG] Test {difficulty} sudoku number", i,j, "This sudoku took", end_time - start_time,
                          "seconds to solve.")

            #print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
            # if count < len(sudokus):
            #    break
        main_end_time = time.process_time()
        print("total run time :", main_end_time-main_start_time)
main()

import numpy as np

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


def hidden_singles(sudoku):
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
            valid_options[(y_pos, x_pos)] = tmp
    valid_options = sort_by_values_len(valid_options)
    return valid_options


def sudoku_solver(sudoku):
    f = True
    i = 0
    while f:
        i = i + 1
        start_sudoku = sudoku.copy()
        #sudoku = initial_pass(sudoku)
        sudoku = hidden_singles(sudoku)
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
    difficulties = ['very_easy', 'easy', 'medium', 'hard', 'extreme']
    difficulties = ['hard', 'extreme']
    master = time.process_time()
    for difficulty in difficulties:
        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        main_start_time = time.process_time()
        print(difficulty)
        for i in range(len(sudokus)):
            # for i in [8]:
            sudoku = sudokus[i].copy()
            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            if np.array_equal(your_solution, solutions[i]):
                # print(f"[OK] Test {difficulty}", i, "This sudoku took", end_time - start_time, "seconds.")
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

import numpy as np

def sudoku_sovled(sudoku):
    if np.sum(sudoku) == 405:
        return True
    else:
        return False


def sudoku_zeros(sudoku):
    zeros_index = []
    for y_pos in range(9):
        for x_pos in range(9):
            if sudoku[y_pos][x_pos] == 0:
                zeros_index.append((y_pos, x_pos))
    return zeros_index


def sudoku_solver(sudoku):
    zeros = sudoku_zeros(sudoku)
    sol = sudoku_solve(zeros, sudoku)
    if not sudoku_sovled(sol):
        return (-1 * np.ones_like(sol))
    else:
        return sol


def sudoku_solve(zeros, current_state):
    for (y_pos, x_pos) in zeros:
        for possible in range(1, 10):
            if check_move(current_state, y_pos, x_pos, possible):
                current_state[y_pos, x_pos] = possible
                dump, *new_zeros = zeros
                current_state = sudoku_solve(new_zeros, current_state)
                if not sudoku_sovled(current_state):
                    current_state[y_pos, x_pos] = 0
                else:
                    return current_state
        return current_state
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

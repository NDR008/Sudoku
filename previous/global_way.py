import numpy as np

# Load sudokus
sudoku = np.load("data/very_easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

# Load solutions for demonstration
solutions = np.load("data/very_easy_solution.npy")
print()


def solve():
    for y_pos in range(9):
        for x_pos in range(9):
            if grid[y_pos][x_pos] == 0:
                for possible in range(1, 10):
                    if check_move(grid, y_pos, x_pos, possible):
                        grid[y_pos, x_pos] = possible
                        if solve():
                            return True
                        else:
                            grid[y_pos, x_pos] = 0
    # there are no empty cells which means a solution is found
    print("Yes2")
    print(grid)
    return False


def sudoku_solver(sudoku):
    global grid
    grid = sudoku
    solve()
    return grid


def check_move(temp_state, y_pos, x_pos, possible):
    # check rows and cols
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


def tests():
    import time
    # difficulties = ['very_easy', 'easy', 'medium', 'hard']
    difficulties = ['very_easy']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        # for i in range(len(sudokus)):
        for i in range(1):
            sudoku = sudokus[i].copy()

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

        if count < len(sudokus):
            break


if not SKIP_TESTS:
    tests()

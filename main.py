import numpy as np

# Load sudokus
sudoku = np.load("data/very_easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

# Load solutions for demonstration
solutions = np.load("data/very_easy_solution.npy")
print()

# Print the first 9x9 sudoku...
print("First sudoku:")
print(sudoku[0], "\n")

# ...and its solution
print("Solution of first sudoku:")
print(solutions[0])


def sudoku_solver(sudoku):
    solved = []
    current_state = sudoku
    for y_pos in range(9):
        for x_pos in range(9):
            if current_state[y_pos][x_pos] == 0:
                for possible in range(1, 10):
                    print(y_pos, x_pos, possible)
                    if check_move(current_state, y_pos, x_pos, possible):
                        # make that move
                        current_state[y_pos, x_pos] = possible
                        # solve the new grid
                        sudoku_solver(current_state)
                        # if we reached here that means our prior move was a bad one
                        current_state[y_pos, x_pos] = 0
                        print("back track!")
                # return to calling with prior state
                print("aaa ")
                print(current_state)
                return current_state
    # there are no empty cells which means a solution is found
    return current_state


def check_move(temp_state, y_pos, x_pos, possible):
    # check rows and cols
    for index in range(9):
        if (temp_state[y_pos][index] == possible) or (temp_state[index][x_pos] == possible):
                return False

    sub_cell_y = (y_pos // 3) * 3
    sub_cell_x = (x_pos // 3) * 3
    for y in range (sub_cell_y, sub_cell_y+3):
        for x in range(sub_cell_x, sub_cell_x + 3):
            if temp_state[y][x] == possible:
                return False
    print("Yes we can place in", y_pos, x_pos, possible)
    return True


# YOUR CODE HERE
# raise NotImplementedError()

SKIP_TESTS = False


def tests():
    import time
    #difficulties = ['very_easy', 'easy', 'medium', 'hard']
    difficulties = ['very_easy']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        #for i in range(len(sudokus)):
        for i in range(1):
            sudoku = sudokus[i].copy()
            print(f"This is {difficulty} sudoku number", i)
            print(sudoku)

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            print(f"This is your solution for {difficulty} sudoku number", i)
            print(your_solution)

            print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                print("Yes! Correct solution.")
                count += 1
            else:
                print("No, the correct solution is:")
                print(solutions[i])
                print(your_solution - solutions[i])
                print("This sudoku took", end_time - start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break


if not SKIP_TESTS:
    tests()

import numpy as np

# Load sudokus
sudoku = np.load("data/very_easy_puzzle.npy")
print("very_easy_puzzle.npy has been loaded into the variable sudoku")
print(f"sudoku.shape: {sudoku.shape}, sudoku[0].shape: {sudoku[0].shape}, sudoku.dtype: {sudoku.dtype}")

# Load solutions for demonstration
solutions = np.load("data/very_easy_solution.npy")
print()


def sudoku_sovled(game):
    if np.sum(game) == 405:
        return True
    else:
        return False

def find_zeros(sudoku):
    zeros_index=[]
    for y_pos in range(9):
        for x_pos in range(9):
            if sudoku[y_pos][x_pos] == 0:
                zeros_index.append((y_pos, x_pos))
    return zeros_index

def find_nonZeros(sudoku):
    a=[0]*10
    for y_pos in range(9):
        for x_pos in range(9):
            if sudoku[y_pos][x_pos] == 0: a[0] = a[0] + 1
            elif sudoku[y_pos][x_pos] == 1: a[1] = a[1] + 1
            elif sudoku[y_pos][x_pos] == 2: a[2] = a[2] + 1
            elif sudoku[y_pos][x_pos] == 3: a[3] = a[3] + 1
            elif sudoku[y_pos][x_pos] == 4: a[4] = a[4] + 1
            elif sudoku[y_pos][x_pos] == 5: a[5] = a[5] + 1
            elif sudoku[y_pos][x_pos] == 6: a[6] = a[6] + 1
            elif sudoku[y_pos][x_pos] == 7: a[7] = a[7] + 1
            elif sudoku[y_pos][x_pos] == 8: a[8] = a[8] + 1
            elif sudoku[y_pos][x_pos] == 9: a[9] = a[9] + 1
            head, *b = a
    return b

def sudoku_solver(sudoku):
    backup = sudoku
    list = find_zeros(sudoku)
    b = find_nonZeros(sudoku)
    sol = sudoku_solve(list, b, sudoku)

    if np.array_equal(backup, sol) and not sudoku_sovled(sol):
        blank = -1*np.ones_like(sudoku)
        return blank
    else:
        return sol


def sudoku_solve(list, b, sudoku):
    current_state = sudoku
    for (y_pos, x_pos) in list:
        if current_state[y_pos][x_pos] == 0:
            for value in range(0, 9):
                qty = b[value]
                possible = value +1
                if qty >0 and check_move(current_state, y_pos, x_pos, possible):
                    current_state[y_pos, x_pos] = possible
                    _, *tail = list
                    backup_list = list
                    b[value] = b[value] - 1
                    current_state = sudoku_solve(tail, b, current_state)
                    if not sudoku_sovled(current_state):
                        current_state[y_pos, x_pos] = 0
                        b[value] = b[value] + 1
                    else:
                        return current_state
            return current_state
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
    return True


# YOUR CODE HERE
# raise NotImplementedError()

SKIP_TESTS = False


def main2():
    import time
    #difficulties = ['very_easy', 'easy', 'medium', 'hard']
    #difficulties = ['very_easy', 'easy', 'medium']
    difficulties = ['medium']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        #for i in range(len(sudokus)):
        for i in [10]:
            sudoku = sudokus[i].copy()

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            #print(f"This is your solution for {difficulty} sudoku number", i)
            #print(your_solution)

            #print("Is your solution correct?")
            if np.array_equal(your_solution, solutions[i]):
                #print(f"Correct solution for {difficulty} sudoku number", i)
                count += 1
            else:
                print(f"This is {difficulty} sudoku number", i)
                print(sudoku)
                print(solutions[i])
                print("This sudoku took", end_time - start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break


#if not SKIP_TESTS:
#    tests()

main2()
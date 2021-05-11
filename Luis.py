import numpy as np

# Program to solve Sudokus using backtracking algorithm

# List that draw the board
prev = [
    [0, 0, 0, 0, 0, 0, 0, 0, 3],
    [0, 5, 6, 9, 0, 0, 0, 0, 0],
    [0, 9, 0, 0, 3, 4, 0, 0, 0],
    [0, 6, 0, 0, 8, 9, 5, 0, 0],
    [0, 0, 4, 6, 0, 2, 8, 0, 0],
    [0, 0, 8, 4, 5, 0, 0, 1, 0],
    [0, 0, 0, 3, 9, 0, 0, 7, 0],
    [0, 0, 0, 0, 0, 1, 2, 5, 0],
    [8, 0, 0, 0, 0, 0, 0, 0, 0]
]

board_med = [[3, 4, 6, 7, 2, 5, 9, 8, 1],
     [0, 2, 7, 9, 4, 8, 5, 0, 6],
     [9, 5, 0, 0, 1, 6, 7, 0, 2],
     [0, 7, 4, 1, 5, 0, 3, 6, 8],
     [8, 0, 0, 0, 3, 7, 1, 5, 4],
     [5, 3, 1, 0, 6, 4, 2, 7, 9],
     [6, 9, 0, 4, 7, 1, 8, 0, 5],
     [0, 0, 0, 5, 0, 3, 6, 1, 7],
     [0, 0, 5, 6, 8, 0, 4, 9, 3]]

board =    [[0, 2, 0, 0, 0, 6, 9, 0, 0],
       [0, 0, 0, 0, 5, 0, 0, 2, 0],
       [6, 0, 0, 3, 0, 0, 0, 0, 0],
       [9, 4, 0, 0, 0, 7, 0, 0, 0],
       [0, 0, 0, 4, 0, 0, 7, 0, 0],
       [0, 3, 0, 2, 0, 0, 0, 8, 0],
       [0, 0, 9, 0, 4, 0, 0, 0, 0],
       [3, 0, 0, 9, 0, 2, 0, 1, 7],
       [0, 0, 8, 0, 0, 0, 0, 0, 2]]

# Function to solve the Sudoku using the algorithm backtracking\
def sudoku_solver(bo):
    if solve(bo):
        return bo
    else:
        return(-1 * np.ones_like(bo))
    
def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


# Function to check the row, col and squares
def valid(bo, num, pos):
    # Check the row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False
    # Check the columns
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check the square
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


# Function to print the board
def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")

            # Function to find the empty squares


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col
    return None

def main():
    import time
    #difficulties = ['very_easy', 'easy', 'medium', 'hard']
    difficulties = ['medium', 'hard']

    for difficulty in difficulties:
        print(f"Testing {difficulty} sudokus")

        sudokus = np.load(f"data/{difficulty}_puzzle.npy")
        solutions = np.load(f"data/{difficulty}_solution.npy")

        count = 0
        for i in range(len(sudokus)):
            sudoku = sudokus[i].copy()

            start_time = time.process_time()
            your_solution = sudoku_solver(sudoku)
            end_time = time.process_time()

            print(f"This is your solution for {difficulty} sudoku number", i)
            if np.array_equal(your_solution, solutions[i]):
                #print(f"This is your solution for {difficulty} sudoku number", i)
                #print ("correct")
                count += 1
                #print("This sudoku took", end_time - start_time, "seconds to solve.\n")
            else:
                #print(f"This is your solution for {difficulty} sudoku number", i)
                print ("wrong")
                print("This sudoku took", end_time - start_time, "seconds to solve.\n")

        print(f"{count}/{len(sudokus)} {difficulty} sudokus correct")
        if count < len(sudokus):
            break


main()
print("__________________")
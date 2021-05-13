import numpy as np

a = [[3, 4, 6, 7, 2, 5, 9, 8, 1],
     [0, 2, 7, 9, 4, 8, 5, 0, 6],
     [9, 5, 0, 0, 1, 6, 7, 0, 2],
     [0, 7, 4, 1, 5, 0, 3, 6, 8],
     [8, 0, 0, 0, 3, 7, 1, 5, 4],
     [5, 3, 1, 0, 6, 4, 2, 7, 9],
     [6, 9, 0, 4, 7, 1, 8, 0, 5],
     [0, 0, 0, 5, 0, 3, 6, 1, 7],
     [0, 0, 5, 6, 8, 0, 4, 9, 3]]

puzzle = np.array(a)


def sudoku_sovled(game):
    if np.sum(game) == 405:
        return True
    else:
        return False


def illegal(game):
    if np.sum(game) > 405:
        return True
    else:
        return False


def find_zeros(sudoku):
    zeros_index = []
    zeros_qty = 0
    for y_pos in range(9):
        for x_pos in range(9):
            if sudoku[y_pos][x_pos] == 0:
                zeros_index.append((y_pos, x_pos))
                zeros_qty = zeros_qty + 1
    return zeros_qty, zeros_index


def find_non_zeros(sudoku):
    popularity = [0] * 9
    for y_pos in range(9):
        for x_pos in range(9):
            if sudoku[y_pos][x_pos] == 1:
                popularity[0] = popularity[0] + 1
            elif sudoku[y_pos][x_pos] == 2:
                popularity[1] = popularity[1] + 1
            elif sudoku[y_pos][x_pos] == 3:
                popularity[2] = popularity[2] + 1
            elif sudoku[y_pos][x_pos] == 4:
                popularity[3] = popularity[3] + 1
            elif sudoku[y_pos][x_pos] == 5:
                popularity[4] = popularity[4] + 1
            elif sudoku[y_pos][x_pos] == 6:
                popularity[5] = popularity[5] + 1
            elif sudoku[y_pos][x_pos] == 7:
                popularity[6] = popularity[6] + 1
            elif sudoku[y_pos][x_pos] == 8:
                popularity[7] = popularity[7] + 1
            elif sudoku[y_pos][x_pos] == 9:
                popularity[8] = popularity[8] + 1
    return popularity


def sudoku_solver(sudoku):
    backup = sudoku
    zeros_qty, zeros_index = find_zeros(sudoku)
    popularity = find_non_zeros(sudoku)
    sol = sudoku_solve(zeros_index, popularity, sudoku)

    if np.array_equal(backup, sol) and not sudoku_sovled(sol):
        blank = -1 * np.ones_like(sudoku)
        return blank
    else:
        return sol


def check_move(temp_state, y_pos, x_pos, possible):
    if illegal(temp_state):
        return False
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


def sudoku_solve(zeros_index, popularity, sudoku):
    for (y_pos, x_pos) in zeros_index:
        for ind_pos in range(len(popularity)):
            if popularity[ind_pos] >= 9:
                continue
            possible = ind_pos + 1
            if check_move(sudoku, y_pos, x_pos, possible):
                print(popularity)
                sudoku[y_pos, x_pos] = possible
                _, *trimmed_list = zeros_index
                popularity[ind_pos] = popularity[ind_pos] + 1
                sudoku = sudoku_solve(trimmed_list, popularity, sudoku)
                if not sudoku_sovled(sudoku):
                    sudoku[y_pos, x_pos] = 0
                    popularity[ind_pos] = popularity[ind_pos] - 1
                else:
                    return sudoku
                return sudoku
    return sudoku

result = sudoku_solver(puzzle)
print(result)
import numpy as np

grid = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 0]]

grid2 = [[0, 0, 4, 6, 7, 8, 9, 1, 2],
         [6, 7, 2, 1, 9, 5, 3, 4, 8],
         [1, 9, 8, 3, 4, 2, 5, 6, 7],
         [8, 5, 9, 7, 6, 1, 4, 2, 3],
         [4, 2, 6, 8, 5, 3, 7, 9, 1],
         [7, 1, 3, 9, 2, 4, 8, 5, 6],
         [9, 6, 1, 5, 3, 7, 2, 8, 4],
         [2, 8, 7, 4, 1, 9, 6, 3, 5],
         [3, 4, 5, 2, 8, 6, 1, 7, 9]]


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
    # print("Yes we can place in", y_pos, x_pos, possible)
    return True


def sudoku_sovled(game):
    if np.sum(game) == 405:
        return True
    else:
        return False


def sudoku_solver(game):
    for y_pos in range(2):
        for x_pos in range(2):
            if game[y_pos][x_pos] == 0:
                for possible in range(2, 6):
                    if check_move(game, y_pos, x_pos, possible):
                        game[y_pos, x_pos] = possible
                        if not sudoku_sovled(game):
                            game = sudoku_solver(game)
                        if not sudoku_sovled(game):
                            game[y_pos, x_pos] = 0
                # return to calling with
                return game
    return game
    # there are no empty cells which means a solution is found


game2 = np.array(grid2)
print("try to solve:")
print(game2)
game_result = sudoku_solver(game2)
print(game_result)

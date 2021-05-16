import numpy as np
from itertools import combinations

def as_string(sudoku):
    str_sudoku = ""
    for i in range(9):
        for j in range(9):
            a = sudoku[i][j]
            str_sudoku = str_sudoku + str(a)
    return str_sudoku

def main():
    difficulties = ['very_easy', 'easy', 'medium', 'hard', 'extreme']
    diff = 1
    puzzle = 5
    difficulty = difficulties[diff]

    sudokus = np.load(f"data/{difficulty}_puzzle.npy")
    solutions = np.load(f"data/{difficulty}_solution.npy")

    sudoku = sudokus[puzzle].copy()
    solution = solutions[puzzle].copy()

    #print("Sudoku Puzzle")
    print(sudoku)
    #print()
    options = get_options(sudoku)
    row_vals = val_can_go_row(sudoku)
    col_vals = val_can_go_col(sudoku)
    cross = [row_vals, col_vals]
    for each in cross:
        for individual in each:
            uniques = []  # final set of unique candidates to return
            uniques_temp = {2: [], 3: []}  # potential unique candidates
            for num, group_inds in enumerate(individual):
                c = len(group_inds)
                if c == 1:
                    uniques.append((group_inds, [num]))
                if c == 2:
                    uniques_temp[2].append(num)
                if c == 3:
                    uniques_temp[3].append(num)
            uniques_temp[3] += uniques_temp[2]
            for c in [2]:
                # make every possible combination
                for combo in list(combinations(uniques_temp[c], c)):
                    group_inds = set(individual[combo[0]])
                    for k in range(1, c):
                        # if positions are shared, this will not change the length
                        group_inds = group_inds | set(individual[combo[k]])
                    if len(group_inds) == c:
                        # unique combo (pair or triple) found
                        uniques.append((list(group_inds), combo))
            print(uniques)
            for each in uniques:
                print("at ", each[0], "put", each[1])
                sudoku[each[0][0]] = each[1][0]
            #for inds_combo, combo in uniques:
            #return uniques
    print(sudoku)
    print()
    print("As 1 line")
    print(as_string(sudoku))
    print(81-as_string(sudoku).count('0'))
    print()
    print("Sudoku Solution")
    print(solution)
    print(check_possible(sudoku))


def check_possible(sudoku):
        """ check if each row/column/box can have all unique elements"""
        #get rows
        rows_set = []
        for i in range(9):
            inds = [(i, j) for j in range(9)]
            rows_set.append(inds)
        # get columns
        cols_set = []
        for j in range(9):
            inds = [(i, j) for i in range(9)]
            cols_set.append(inds)
            
        # # check rows and columns
        for t, inds_set in enumerate([rows_set, cols_set]):
            for k, inds in enumerate(inds_set):
                arr = [sudoku[i][j] for i, j in inds]
                if not no_duplicates(arr):
                    print("duplicate1")
                    return 
                arr += list(get_candidates(sudoku, inds[0], inds[-1]))
                possible = all_exist(arr)
                if not possible:
                    print("not possible1")
                    return False
        # check boxes
        for i0 in [0,3,6]:
            for j0 in [0,3,6]:
                suby = (i0 // 3) * 3
                subx = (j0 // 3) * 3
                sub_box = []
                for y in range(suby, suby + 3):
                    for x in range(subx, subx + 3):\
                        sub_box.append(sudoku[y,x])

                if not no_duplicates(sub_box):
                    print("duplicate2")
                    return 
                
                full_options = get_options_full(sudoku)             
                for i in range(i0, i0 + 3):
                    for j in range(j0, j0 + 3):
                        full_opt = set(full_options[i,j])
                        sub_box += full_opt
                possible = all_exist(sub_box)
                if not possible:
                    print("not possible2")
                    return False
        return True


def get_candidates(sudoku, start, end):
    " get candidates within two corners of a rectangle/column/row"
    candidates = set()  #null set
    full_options = get_options_full(sudoku)
    for i in range(start[0], end[0] + 1):
        for j in range(start[1], end[1] + 1):
            full_opt = set(full_options[i,j])
            #print()
            #print("First", i,j, candidates, full_opt)
            candidates = candidates | full_opt # grow the list with all that we've seen
            #print(candidates)        
    return candidates


#rcb
def no_duplicates(rcb):
    count = [0] * (10)
    for x in rcb:
        count[x] += 1

    for c in count[1:]:  # exclude 0:
        if c > 1:
            return False  # more than 1 of value
    return True

def all_exist(rcb):
    """ verify that there is at least one of each number present """
    count = [0] * 10
    for x in rcb:
        count[x] += 1
    for c in count[1:]:  # exclude 0:
        #print(c)
        if c == 0:
            return False
    return True

## copied stuff from my code 
def get_options_full(sudoku):
    options = {}
    for y in range(9):
        for x in range(9):
            if sudoku[y][x] == 0:
                options[(y, x)] = [opt for opt in range(1, 10) if is_move_valid(sudoku, y, x, opt)]
            else:
                options[(y, x)] = []
    return options		


def get_options(sudoku):
    zeros = get_zeros(sudoku)
    options = {}
    for (y, x) in zeros:
        options[(y, x)] = [opt for opt in range(1, 10) if is_move_valid(sudoku, y, x, opt)]
    return options


def get_zeros(sudoku):
    zeros_index = [(y, x) for y in range(9) for x in range(9) if sudoku[y][x] == 0]
    return zeros_index

def val_can_go_row(sudoku):
    val_by_row = []
    options = get_options_full(sudoku)
    for row in range(9):
        count = [[] for _ in range(10)] # for 9 cells and a value
        for col in range (9):
            for num in options[(row,col)]:
                count[num].append((row,col))
        val_by_row.append(count)
    return val_by_row

def val_can_go_col(sudoku):
    val_by_col = []
    options = get_options_full(sudoku)
    for col in range(9):
        count = [[] for _ in range(10)] # for 9 cells and a value
        for row in range (9):
            for num in options[(row,col)]:
                count[num].append((row,col))
        val_by_col.append(count)
    return val_by_col

def is_move_valid(sudoku, y, x, possible):
    for index in range(9):
        if (sudoku[y][index] == possible) or (sudoku[index][x] == possible):
            return False
    sub_cell_y = (y // 3) * 3
    sub_cell_x = (x // 3) * 3
    for y in range(sub_cell_y, sub_cell_y + 3):
        for x in range(sub_cell_x, sub_cell_x + 3):
            if sudoku[y][x] == possible:
                return False
    return True

main()
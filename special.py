import numpy as np
sudokus = np.load(f"data/extreme_puzzle.npy")
sudoku = sudokus[10]


def get_zeros(sudoku):
    zeros_index = [(y, x) for y in range(9) for x in range(9) if sudoku[y][x] == 0]
    return zeros_index


def get_options(sudoku):
    zeros = get_zeros(sudoku)
    options = {}
    for (y, x) in zeros:
        options[(y, x)] = [opt for opt in range(1, 10) if is_move_valid(sudoku, y, x, opt)]
    return options


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


options = get_options(sudoku)

# hard coded set (in the future I would adapt this code for naked_pairs
sub_sets = [{1, 2}, {1, 3}, {1, 4}, {1, 5}, {1, 6}, {1, 7}, {1, 8}, {1, 9},
            {2, 3}, {2, 4}, {2, 5}, {2, 6}, {2, 7}, {2, 8}, {2, 9}, {3, 4}, {3, 5}, {3, 6}, {3, 7}, {3, 8}, {3, 9},
            {4, 5}, {4, 6}, {4, 7}, {4, 8}, {4, 9}, {5, 6}, {5, 7}, {5, 8}, {5, 9}, {6, 7}, {6, 8}, {6, 9}, {7, 8},
            {7, 9}, {8, 9}]
tmp = []
for x in range(4,5):
    unit = []
    for y in range(9):
        k = (y, x)
        unit.append(options.get(k))
        count = 0
        location = []
        for s_found, sub_set in enumerate(sub_sets):
            #for r_found, row_content in enumerate(unit):
            if (y, x) in options:
                opt = options[y, x]
                if opt is None:
                    count = 0
                    continue
                elif sub_set.issubset(opt):
                    print("for", (y,x), sub_set, "in", opt)
                    count += 1
                    tmp.append((y, x))
            if y == 8 and count == 2:
                location.append((sub_set, tmp[0], tmp[1]))
                print("boom")
                tmp.clear()
                count = 0
            elif y == 8:
                print("poof")
                tmp.clear()
                count = 0

for x in range(4, 5):
    for y in range(9):
        location2 = []
        for (digits, loc1, loc2) in location:
            found_first = 0
            for qty, digit_number in enumerate(list(digits)):
                tmp2 = []
                count2 = 0
                single_digit = {digit_number}
                for r_found2, row_content2 in enumerate(unit):
                    if row_content2 is None:
                        continue
                    elif single_digit.issubset(row_content2):
                        if (r_found2, x) != loc1 and (r_found2, x) != loc2:
                            count2 = 0
                            found_first = 0
                            break
                        else:
                            count2 += 1
                if count2 == 2 and found_first != 1:
                    found_first += 1
                elif count2 == 2 and found_first == 1:
                    location2.append((list(digits), loc1, loc2))

        for (values, loc1, loc2) in location2:
            options[loc1] = list(values)
            options[loc2] = list(values)
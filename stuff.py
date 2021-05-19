for y0 in [0, 3, 6]:
    for x0 in [0, 3, 6]:
        for y in range(y0, y0 + 3):
            for x in range(x0, x0 + 3):

                for sub_set in (sub_sets):
                    count = 0
                    tmp = []
                    for y in range(y0, y0 + 3):
                        for x in range(x0, x0 + 3):
                            if (y, x) not in options:
                                continue
                            unit = options[(y, x)]
                            if sub_set.issubset(unit):
                                count += 1
                                tmp.append((y, x))
                        if count == 2:
                            location.append((sub_set, tmp[0], tmp[1]))
                            tmp.clear()

                for (digits, loc, loc2) in location:
                    found_first = 0
                    for digit_number in (list(digits)):
                        count2 = 0
                        single_digit = {digit_number}
                        for y in range(y0, y0 + 3):
                            for x in range(x0, x0 + 3):
                                if (y, x) not in options:
                                    continue
                                unit2 = options[(y, x)]
                                if single_digit.issubset(unit2):
                                    if (y, x) != loc1 and (y, x) != loc2:
                                        count2 = 0
                                        found_first = 0
                                        break
                                    else:
                                        count2 += 1
                            if count2 == 2 and found_first != 1:
                                found_first += 1
                            elif count2 == 2 and found_first == 1:
                                options[loc1] = list(digits)
                                options[loc2] = list(digits)
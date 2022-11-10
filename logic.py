# https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python


from sudokus import evil_sudoku, normal_sudoku, empty_sudoku

side_of_unit = 3
counter = 0
solutions = []
MAX_TOTAL_CYCLES = 200


def check_valid_move(sudoku, x, y, number):
    if sudoku[y][x] != 0:
        return False
    for value in range(side_of_unit**2):
        if sudoku[y][value] == number:
            return False
    for value in range(side_of_unit**2):
        if sudoku[value][x] == number:
            return False
    for x_value in range(
        int(x / side_of_unit) * side_of_unit, (int(x / side_of_unit) + 1) * side_of_unit
    ):
        for y_value in range(
            int(y / side_of_unit) * side_of_unit,
            (int(y / side_of_unit) + 1) * side_of_unit,
        ):
            if sudoku[y_value][x_value] == number:
                return False
    return True


def check_solution(sudoku):
    flat = [item for items in sudoku for item in items]
    try:
        flat.index(0)
        return False
    except ValueError:
        pass

    if not all(sum(row) == sum(set(row)) for row in sudoku):
        return False
    transposed_sudoku = list(zip(*sudoku))

    if not all(sum(row) == sum(set(row)) for row in transposed_sudoku):
        return False

    numbers = [x + 1 for x in range(side_of_unit**2)]
    for vertical_step in range(side_of_unit):
        for horizontal_step in range(side_of_unit):
            grid = []
            for x in range(side_of_unit):
                for y in range(side_of_unit):
                    grid.append(
                        sudoku[(side_of_unit * vertical_step) + y][
                            (side_of_unit * horizontal_step) + x
                        ]
                    )
            grid.sort()
            if grid != numbers:
                return False
    return True


def solve_sudoku(sudoku):
    global counter
    while counter < MAX_TOTAL_CYCLES:
        for x in range(side_of_unit**2):
            for y in range(side_of_unit**2):
                if sudoku[y][x] == 0:
                    for number in range(1, (side_of_unit**2) + 1):
                        if check_valid_move(sudoku, x=x, y=y, number=number):
                            sudoku[y][x] = number
                            if check_solution(sudoku):
                                counter += 1
                                solutions.append(sudoku)
                                return
                            solve_sudoku(sudoku)
                            sudoku[y][x] = 0
                    return


if __name__ == "__main__":

    test = empty_sudoku
    solve_sudoku(test)
    if counter == 1:
        print(f"the sudoku has one solution")

    elif counter == MAX_TOTAL_CYCLES:
        print(f"the sudoku has at least {MAX_TOTAL_CYCLES} solutions")
    elif counter > 1:
        print(f"the sudoku has {counter} solutions")
    elif counter == 0:
        print(f"the sudoku has no solution")
    else:
        print("check other options")

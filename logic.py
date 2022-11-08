# https://stackoverflow.com/questions/45471152/how-to-create-a-sudoku-puzzle-in-python


normal_sudoku = [
    [8, 0, 0, 4, 0, 6, 0, 0, 7],
    [0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 1, 0, 0, 0, 0, 6, 5, 0],
    [5, 0, 9, 0, 3, 0, 7, 8, 0],
    [0, 0, 0, 0, 7, 0, 0, 0, 0],
    [0, 4, 8, 0, 2, 0, 1, 0, 3],
    [0, 5, 2, 0, 0, 0, 0, 9, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [3, 0, 0, 9, 0, 2, 0, 0, 5],
]

# evil
evil_sudoku = [
    [0, 7, 0, 5, 3, 0, 1, 0, 6],
    [0, 0, 2, 0, 0, 0, 0, 0, 7],
    [0, 0, 0, 0, 8, 0, 0, 0, 0],
    [0, 5, 0, 0, 0, 8, 0, 0, 0],
    [0, 0, 4, 6, 5, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 2, 6, 0, 0],
    [0, 0, 0, 0, 0, 6, 0, 0, 0],
    [9, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 2, 0, 1, 7, 0, 3, 0, 0],
]

side_of_unit = 3
counter = 0
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
    pass


def solve_sudoku(sudoku):
    global counter
    while counter < MAX_TOTAL_CYCLES:
        for x in range(side_of_unit**2):
            for y in range(side_of_unit**2):
                if sudoku[y][x] == 0:
                    for number in range(1, (side_of_unit**2) + 1):
                        if check_valid_move(sudoku, x=x, y=y, number=number):
                            sudoku[y][x] = number
                            solve_sudoku(sudoku)
                            sudoku[y][x] = 0
                    return
        counter += 1
        return sudoku


if __name__ == "__main__":

    sudoku = normal_sudoku
    solution = solve_sudoku(sudoku)
    if counter == 1:
        print(f"the sudoku has one solution")
        for row in solution:
            print(row)
    elif counter == MAX_TOTAL_CYCLES:
        print(f"the sudoku has at least {MAX_TOTAL_CYCLES} solutions")
    elif counter > 1:
        print(f"the sudoku has {counter} solutions")

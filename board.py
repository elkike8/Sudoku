import tkinter as tk
from itertools import cycle
import random
from sudokus import *

random.seed(13)
MAX_TOTAL_CYCLES = 200
colors = ("#CBEBF4", "#CBD7F5")
height = 2
width = 4
title_font = ("Arial", 18, "bold")
button_font = ("Arial", 10, "bold")
user_button_color = "red"
system_button_color = "black"


def is_even(number: int):
    if number % 2 == 0:
        return True
    else:
        return False


class SudokuBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.original_sudoku = normal_sudoku
        self.working_sudoku = self.original_sudoku.copy()
        self.size_of_unit = 3
        self.spaces = {}
        self.counter = 0
        self.found_solutions = 0
        self.unique_solution = [
            [0 for x in range(self.size_of_unit**2)]
            for x in range(self.size_of_unit**2)
        ]

        self.create_hud()
        self.create_blank_board()
        self.reset_board()

    def create_hud(self):
        hud = tk.Frame(self)
        message = tk.Label(hud, font=title_font, text=f"Let's play some Sudoku")
        message.grid(row=0, columnspan=3)

        button_check_solution = tk.Button(
            master=hud,
            text="check solution",
            command=self.is_it_solved,
        )
        button_check_solution.grid(row=1, column=0)

        button_give_solution = tk.Button(
            master=hud,
            text="show no. solutions",
            command=self.solution_message,
        )
        button_give_solution.grid(row=1, column=1)

        button_create_solution = tk.Button(
            master=hud,
            text="give solution",
            command=self.print_solution,
        )
        button_create_solution.grid(row=1, column=2)

        button_reset = tk.Button(
            master=hud,
            text="reset",
            command=self.reset_board,
        )
        button_reset.grid(row=2, column=0)

        button_create_sudoku = tk.Button(
            master=hud,
            text="create sudoku",
            command=self.create_sudoku,
        )
        button_create_sudoku.grid(row=2, column=1)

        button_unique_sudoku = tk.Button(
            master=hud,
            text="unique sudoku",
            command=self.unique_sudoku,
        )
        button_unique_sudoku.grid(row=2, column=2)

        hud.pack(fill=tk.X)

    def reset_board(self):
        self.working_sudoku = [
            [0 for x in range(self.size_of_unit**2)]
            for x in range(self.size_of_unit**2)
        ]
        self.counter = 0
        self.found_solutions = 0
        for k, v in self.spaces.items():
            x, y = v
            self.update_board(k, "")
            self.unique_solution[x][y] = self.working_sudoku[x][y]

    def create_blank_board(self):
        self.working_sudoku = [
            [0 for x in range(self.size_of_unit**2)]
            for x in range(self.size_of_unit**2)
        ]
        board = tk.Frame(self)
        board.pack()
        self.color = cycle(colors)

        for row in range(self.size_of_unit**2):
            if is_even(self.size_of_unit) and int(row % self.size_of_unit) == 0:
                bg_color = next(self.color)
            elif not is_even(self.size_of_unit) and int(row % self.size_of_unit) != 0:
                bg_color = next(self.color)

            for col in range(self.size_of_unit**2):
                if int(col % self.size_of_unit) == 0:
                    bg_color = next(self.color)
                button = tk.Button(
                    master=board,
                    text="",
                    font=button_font,
                    bg=bg_color,
                    fg=user_button_color,
                    height=height,
                    width=width,
                )
                button.bind("<ButtonPress>", self.create_entry_pad)
                self.spaces[button] = (row, col)
                button.grid(row=row, column=col)

    def create_premade_board(self, size: int = 3):
        board = tk.Frame(self)
        board.pack()
        self.color = cycle(colors)

        for row in range(size**2):
            if is_even(self.size_of_unit) and int(row % size) == 0:
                bg_color = next(self.color)
            elif not is_even(self.size_of_unit) and int(row % size) != 0:
                bg_color = next(self.color)
            for col in range(size**2):
                if int(col % size) == 0:
                    bg_color = next(self.color)
                if self.original_sudoku[row][col] == 0:
                    button = tk.Button(
                        master=board,
                        text="",
                        font=button_font,
                        bg=bg_color,
                        fg=user_button_color,
                        height=height,
                        width=width,
                    )

                    button.bind("<ButtonPress-1>", self.create_entry_pad)
                    self.spaces[button] = (row, col)
                    button.grid(row=row, column=col)

                else:
                    button = tk.Button(
                        master=board,
                        text=self.original_sudoku[row][col],
                        font=button_font,
                        bg=bg_color,
                        height=height,
                        width=width,
                        state="disabled",
                        disabledforeground=system_button_color,
                    )
                    self.spaces[button] = (row, col)
                    button.grid(row=row, column=col)

    def create_entry_pad(self, event):
        self.pad_buttons = {}
        selected_space = event.widget
        x_pos, y_pos = self.spaces[selected_space]

        def get_number(pad_event):
            number = pad_event.widget
            number = self.pad_buttons[number]
            self.update_board(selected_space, number)
            self.working_sudoku[x_pos][y_pos] = number
            window.destroy()

        window = tk.Toplevel(self)

        pad = tk.Frame(window)
        pad.pack()
        i = 1

        for row in range(self.size_of_unit):
            self.rowconfigure(row, weight=1)
            self.columnconfigure(row, weight=1)
            for col in range(self.size_of_unit):
                button = tk.Button(
                    master=pad,
                    text=i,
                    height=2,
                    width=4,
                    relief="raised",
                )
                self.pad_buttons[button] = i
                i += 1
                button.bind("<ButtonPress>", get_number)
                button.grid(row=row, column=col, sticky="nsew")

    def update_board(self, selected_space, number):
        selected_space.config(text=number)

    def is_it_solved(self):
        if self.check_for_solution():
            self.display_message("congratulations, you solved the sudoku!")
        else:
            self.display_message("the answer isn't correct")

    def check_for_solution(self):
        flat = [item for items in self.working_sudoku for item in items]
        try:
            flat.index(0)
            return False
        except ValueError:
            pass

        if not all(sum(row) == sum(set(row)) for row in self.working_sudoku):
            return False
        self.transposed_sudoku = list(zip(*self.working_sudoku))

        if not all(sum(row) == sum(set(row)) for row in self.transposed_sudoku):
            return False

        numbers = [x + 1 for x in range(self.size_of_unit**2)]
        for vertical_step in range(self.size_of_unit):
            for horizontal_step in range(self.size_of_unit):
                self.grid = []
                for x in range(self.size_of_unit):
                    for y in range(self.size_of_unit):
                        self.grid.append(
                            self.working_sudoku[
                                (self.size_of_unit * vertical_step) + y
                            ][(self.size_of_unit * horizontal_step) + x]
                        )
                self.grid.sort()
                if self.grid != numbers:
                    return False
        return True

    def check_valid_move(self, sudoku, x, y, number):
        if sudoku[y][x] != 0:
            return False
        for value in range(self.size_of_unit**2):
            if sudoku[y][value] == number:
                return False
        for value in range(self.size_of_unit**2):
            if sudoku[value][x] == number:
                return False
        for x_value in range(
            int(x / self.size_of_unit) * self.size_of_unit,
            (int(x / self.size_of_unit) + 1) * self.size_of_unit,
        ):
            for y_value in range(
                int(y / self.size_of_unit) * self.size_of_unit,
                (int(y / self.size_of_unit) + 1) * self.size_of_unit,
            ):
                if sudoku[y_value][x_value] == number:
                    return False
        return True

    def give_solutions(self):

        solved = self.check_for_solution()

        while self.counter < MAX_TOTAL_CYCLES:
            if solved:
                self.counter += 1
                self.found_solutions += 1
                return
            else:
                for y in range(self.size_of_unit**2):
                    for x in range(self.size_of_unit**2):
                        if self.working_sudoku[y][x] == 0:
                            for number in range(1, (self.size_of_unit**2) + 1):
                                if self.check_valid_move(
                                    self.working_sudoku, x, y, number
                                ):
                                    self.working_sudoku[y][x] = number
                                    self.give_solutions()
                                    self.working_sudoku[y][x] = 0
                            return

    def solve_sudoku(self):

        solved = self.check_for_solution()

        while self.counter < MAX_TOTAL_CYCLES:
            if solved:
                self.counter += 1
                self.found_solutions += 1
                if self.found_solutions == 1:
                    for k, v in self.spaces.items():
                        x, y = v
                        self.update_board(k, self.working_sudoku[x][y])
                        self.unique_solution[x][y] = self.working_sudoku[x][y]
                self.counter += 1
                return
            else:
                for y in range(self.size_of_unit**2):
                    for x in range(self.size_of_unit**2):
                        if self.working_sudoku[y][x] == 0:
                            for number in range(1, (self.size_of_unit**2) + 1):
                                if self.check_valid_move(
                                    self.working_sudoku, x, y, number
                                ):
                                    self.working_sudoku[y][x] = number
                                    self.solve_sudoku()
                                    self.working_sudoku[y][x] = 0
                            return

    def print_solution(self):
        self.solve_sudoku()
        self.working_sudoku = self.unique_solution

    def create_sudoku(self):
        self.counter = 0
        self.found_solutions = 0

        self.working_sudoku = [
            [0 for x in range(self.size_of_unit**2)]
            for x in range(self.size_of_unit**2)
        ]
        rand_number = random.randint(1, (self.size_of_unit**2) + 1)
        rand_x_coordinate = random.randint(1, (self.size_of_unit**2) + 1)
        rand_y_coordinate = random.randint(1, (self.size_of_unit**2) + 1)
        self.working_sudoku[rand_x_coordinate][rand_y_coordinate] = rand_number
        self.solve_sudoku()
        self.working_sudoku = self.unique_solution

        self.counter = 0
        self.found_solutions = 0

    def unique_sudoku(self):
        self.counter = 0
        self.found_solutions = 0
        self.give_solutions()
        for _ in range(int((self.size_of_unit**3) / 4)):
            rand_x_coordinate = random.randint(1, (self.size_of_unit**2) + 1)
            rand_y_coordinate = random.randint(1, (self.size_of_unit**2) + 1)
            self.working_sudoku[rand_x_coordinate][rand_y_coordinate] = 0
        self.give_solutions()

        if self.found_solutions > 1:
            rand_x_coordinate = random.randint(1, (self.size_of_unit**2) + 1)
            rand_y_coordinate = random.randint(1, (self.size_of_unit**2) + 1)
            self.working_sudoku[rand_x_coordinate][rand_y_coordinate] = 0
            for row in self.working_sudoku:
                print(row)
            self.unique_sudoku()
            return

    def display_message(self, message: str = ""):
        window = tk.Toplevel(self)
        # window.geometry("500x50")
        label = tk.Label(master=window, text=message, font=title_font)
        label.pack()

    def solution_message(self):
        self.working_sudoku = self.unique_solution
        self.give_solutions()
        if self.check_for_solution():
            self.display_message(f"the sudoku is already solved")

        elif self.found_solutions == 1:
            self.display_message(f"the sudoku has a unique solution")
            self.counter = 0
            self.found_solutions = 0

        elif self.counter == MAX_TOTAL_CYCLES:
            self.display_message(
                f"the sudoku has at least {MAX_TOTAL_CYCLES} ways to be solved"
            )
            self.counter = 0
            self.found_solutions = 0

        elif self.counter > 1:
            self.display_message(
                f"the sudoku has {self.found_solutions} ways to be solved"
            )
            self.counter = 0
            self.found_solutions = 0

        elif self.counter == 0:
            self.display_message(f"the sudoku has no solution")
            self.counter = 0
            self.found_solutions = 0

        else:
            self.display_message("check other options")


if __name__ == "__main__":
    game = SudokuBoard()
    game.mainloop()

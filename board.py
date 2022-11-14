import tkinter as tk
from itertools import cycle
from sudokus import *


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
        self.size_of_unit = 2
        self.empty_sudoku = [0 for x in range(self.size_of_unit)]
        self.spaces = {}
        self.counter = 0
        self.found_solutions = 0
        self.solutions = []
        self.unique_solution = [
            [0 for x in range(self.size_of_unit**2)]
            for x in range(self.size_of_unit**2)
        ]

        self.create_hud()
        self.create_blank_board(self.size_of_unit)

    def create_hud(self):
        hud = tk.Frame(self)
        message = tk.Label(hud, font=title_font, text=f"Let's play some Sudoku")
        message.pack(fill=tk.X)
        button_check_solution = tk.Button(
            master=hud,
            text="check solution",
            command=self.is_it_solved,
        )
        button_check_solution.pack()
        button_give_solution = tk.Button(
            master=hud,
            text="give solution",
            command=self.solve_sudoku,
        )
        button_give_solution.pack()
        hud.pack(fill=tk.X)

    def create_blank_board(self, size):
        self.working_sudoku = [[0 for x in range(size**2)] for x in range(size**2)]
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
            window = tk.Toplevel(self)
            label = tk.Label(
                master=window, text="congratulations, you solved the sudoku!"
            )
            label.pack()
        else:
            window = tk.Toplevel(self)
            label = tk.Label(master=window, text="the answer isn't correct")
            label.pack()

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

    def solve_sudoku(self):

        solved = self.check_for_solution()

        while self.counter < MAX_TOTAL_CYCLES:
            if solved:
                self.counter += 1
                if self.counter == 0:
                    print("the sudoku entered is solved")
                    return
                else:
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


if __name__ == "__main__":
    a = SudokuBoard()
    a.mainloop()

import tkinter as tk
from itertools import cycle
from sudokus import *


colors = ("#6f7cf7", "#6ff7e9")


def is_even(number):
    if number % 2 == 0:
        return True
    else:
        return False


class SudokuBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.original_sudoku = evil_sudoku
        self.working_sudoku = self.original_sudoku.copy()
        self.size_of_unit = 3
        self.empty_sudoku = [0 for x in range(self.size_of_unit)]
        self.spaces = {}
        self.create_premade_board(self.size_of_unit)

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
                    master=board, text="", bg=bg_color, height=2, width=4
                )
                button.bind("<ButtonPress-1>", self.create_entry_pad)
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
                        bg=bg_color,
                        height=2,
                        width=4,
                    )

                    button.bind("<ButtonPress-1>", self.create_entry_pad)
                    self.spaces[button] = (row, col)
                    button.grid(row=row, column=col)

                else:
                    button = tk.Button(
                        master=board,
                        text=self.original_sudoku[row][col],
                        bg=bg_color,
                        height=2,
                        width=4,
                    )
                    self.spaces[button] = (row, col)
                    button.grid(row=row, column=col)

    def create_entry_pad(self, event):
        self.pad_buttons = {}
        selected_space = event.widget
        x_pos, y_pos = self.spaces[selected_space]
        print(x_pos, y_pos)

        def get_number(pad_event):
            number = pad_event.widget
            number = self.pad_buttons[number]
            self.update_board(selected_space, number)
            self.working_sudoku[x_pos][y_pos] = number
            for row in self.working_sudoku:
                print(row)
            window.destroy()

        size = self.size_of_unit

        window = tk.Toplevel(self)

        pad = tk.Frame(window)
        pad.pack()
        i = 1

        for row in range(size):
            self.rowconfigure(row, weight=1)
            self.columnconfigure(row, weight=1)
            for col in range(size):
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


a = SudokuBoard()
a.mainloop()

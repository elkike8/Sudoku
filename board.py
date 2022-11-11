import tkinter as tk
from sudokus import *


class SudokuBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.original_sudoku = evil_sudoku
        self.working_sudoku = self.original_sudoku.copy()
        self.size_of_unit = 2
        self.spaces = {}
        self.create_board(size=self.size_of_unit)

    def create_board(self, size: int = 3):
        board = tk.Frame(self)
        board.pack()

        for row in range(size**2):
            self.rowconfigure(row, weight=1)
            self.columnconfigure(row, weight=1)
            for col in range(size**2):
                if self.original_sudoku[row][col] == 0:
                    button = tk.Button(
                        master=board,
                        text="",
                        bg="black",
                        height=2,
                        width=4,
                        relief="flat",
                    )

                    button.bind("<ButtonPress-1>", self.create_entry_pad)
                    self.spaces[button] = (row, col)
                    button.grid(row=row, column=col)

                else:
                    button = tk.Button(
                        master=board,
                        text=self.original_sudoku[row][col],
                        bg="white",
                        height=2,
                        width=4,
                        relief="flat",
                    )
                    self.spaces[button] = (row, col)
                    button.grid(row=row, column=col)

    def create_entry_pad(self, event):
        self.pad_buttons = {}
        selected_space = event.widget

        def get_number(pad_event):
            number = pad_event.widget
            print(self.pad_buttons[number])
            self.update_board(selected_space, self.pad_buttons[number])
            window.destroy()

        size = self.size_of_unit

        window = tk.Toplevel(self)

        pad = tk.Frame(window)
        pad.pack()
        i = 1
        print(self.spaces[selected_space])

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

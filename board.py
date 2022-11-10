import tkinter as tk
from sudokus import *


class SudokuBoard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.create_board()

    def create_board(self, size: int = 3):
        board = tk.Frame(self)
        board.pack()

        for row in range(size**2):
            self.rowconfigure(row, weight=1)
            self.columnconfigure(row, weight=1)
            for col in range(size**2):
                button = tk.Button(
                    master=board,
                    text=evil_sudoku[col][row],
                    bg="SystemButtonFace",
                    height=2,
                    width=4,
                    relief="raised",
                )
                button.grid(row=row, column=col, sticky="nsew")


a = SudokuBoard()
a.mainloop()

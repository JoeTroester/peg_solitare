# gui.py
# The tkinter window. This class only handles drawing and clicks.
# All the rules are in the Game and Board classes.

import tkinter as tk
from tkinter import messagebox

from game.board import BOARD_TYPES, INVALID, PEG
from game.game import Game

CELL = 50  # size of each hole in pixels
RADIUS = 18


class PegSolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.game = Game()
        self.selected = None  # (row, col) of the peg the player clicked

        # settings on the left side
        settings = tk.Frame(root)
        settings.pack(side=tk.LEFT, padx=10, pady=10, anchor="n")

        tk.Label(settings, text="Board Type").pack(anchor="w")
        self.type_choice = tk.StringVar(value="English")
        for name in BOARD_TYPES:
            tk.Radiobutton(settings, text=name, variable=self.type_choice,
                           value=name).pack(anchor="w")

        tk.Label(settings, text="Board Size").pack(anchor="w")
        self.size_choice = tk.StringVar(value="7")
        tk.Spinbox(settings, from_=5, to=9, increment=2, width=5,
                   textvariable=self.size_choice).pack(anchor="w")

        tk.Button(settings, text="New Game", command=self.new_game).pack(anchor="w", pady=10)

        # board on the right side
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

    def new_game(self):
        try:
            size = int(self.size_choice.get())
            self.game.new_game(self.type_choice.get(), size)
        except ValueError:
            messagebox.showerror("Error", "Board size must be an odd number from 5 to 9")
            return
        self.selected = None
        self.draw_board()

    def get_xy(self, row, col):
        # center of a hole in pixels
        offset = self.game.board.get_row_offset(row)
        x = (col + offset) * CELL + CELL
        y = row * CELL + CELL
        return x, y

    def find_cell(self, x, y):
        # figure out which hole was clicked
        board = self.game.board
        for row in range(board.size):
            for col in range(board.size):
                if board.get_cell(row, col) != INVALID:
                    cx, cy = self.get_xy(row, col)
                    if abs(x - cx) < RADIUS and abs(y - cy) < RADIUS:
                        return row, col
        return None

    def on_click(self, event):
        cell = self.find_cell(event.x, event.y)
        if cell is None or self.game.is_game_over():
            return
        row, col = cell

        if self.game.board.get_cell(row, col) == PEG:
            # clicked a peg, so remember it
            self.selected = (row, col)
        elif self.selected is not None:
            # clicked an empty hole, so try to jump there
            from_row, from_col = self.selected
            if self.game.make_move(from_row, from_col, row, col):
                self.selected = None
                self.draw_board()

        if self.game.is_game_over():
            messagebox.showinfo("Game Over", self.game.get_result())

    def draw_board(self):
        board = self.game.board
        self.canvas.delete("all")
        self.canvas.config(width=(board.size + 1) * CELL, height=(board.size + 1) * CELL)

        for row in range(board.size):
            for col in range(board.size):
                cell = board.get_cell(row, col)
                if cell == INVALID:
                    continue
                x, y = self.get_xy(row, col)
                if cell == PEG:
                    self.canvas.create_oval(x - RADIUS, y - RADIUS, x + RADIUS, y + RADIUS,
                                            fill="blue")
                else:
                    self.canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill="gray")

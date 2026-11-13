# gui.py
# The tkinter window. This class only handles drawing, clicks, and the
# timer for the computer's moves. All the rules are in the Game and Board classes.

import tkinter as tk
from tkinter import messagebox

from game.board import BOARD_TYPES, INVALID, PEG
from game.game import GAME_MODES, AutomatedGame, ManualGame

CELL = 50  # size of each hole in pixels
RADIUS = 18
AUTO_DELAY = 500  # milliseconds between computer moves so you can watch them


class PegSolitaireGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Peg Solitaire")
        self.game = ManualGame()
        self.selected = None  # (row, col) of the peg the player clicked
        self.auto_job = None  # timer for the next computer move

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

        tk.Label(settings, text="Game Mode").pack(anchor="w")
        self.mode_choice = tk.StringVar(value="Manual")
        for name in GAME_MODES:
            tk.Radiobutton(settings, text=name, variable=self.mode_choice,
                           value=name).pack(anchor="w")

        tk.Button(settings, text="New Game", command=self.new_game).pack(anchor="w", pady=10)
        self.randomize_button = tk.Button(settings, text="Randomize", command=self.randomize)
        self.randomize_button.pack(anchor="w")

        # board on the right side
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)

        self.draw_board()

    def new_game(self):
        self.stop_autoplay()
        try:
            size = int(self.size_choice.get())
            game_class = GAME_MODES[self.mode_choice.get()]
            # make the new game first, so if the size is bad the old game stays
            self.game = game_class(self.type_choice.get(), size)
        except ValueError:
            messagebox.showerror("Error", "Board size must be an odd number from 5 to 9")
            return
        self.selected = None
        self.draw_board()

        # randomize is only for manual games
        if isinstance(self.game, ManualGame):
            self.randomize_button.config(state=tk.NORMAL)
        else:
            self.randomize_button.config(state=tk.DISABLED)

        # in an automated game the computer starts playing right away
        if isinstance(self.game, AutomatedGame):
            self.auto_job = self.root.after(AUTO_DELAY, self.auto_step)

    def auto_step(self):
        # the computer makes one move, then sets a timer for the next one
        self.auto_job = None
        if self.game.make_auto_move() is not None:
            self.draw_board()
        if self.game.is_game_over():
            messagebox.showinfo("Game Over", self.game.get_result())
        else:
            self.auto_job = self.root.after(AUTO_DELAY, self.auto_step)

    def stop_autoplay(self):
        # cancel the computer's next move (used when a new game starts)
        if self.auto_job is not None:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None

    def randomize(self):
        if not isinstance(self.game, ManualGame):
            return
        if self.game.randomize():
            self.selected = None
            self.draw_board()
            # the new layout might not have any moves left
            if self.game.is_game_over():
                messagebox.showinfo("Game Over", self.game.get_result())

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
        # clicks only do something in a manual game
        if not isinstance(self.game, ManualGame):
            return
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

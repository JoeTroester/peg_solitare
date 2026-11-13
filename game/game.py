# game.py
# Game is the parent class. It has everything a manual game and an
# automated game have in common: the board, the move count, the rules for
# a move, and checking if the game is over.
# ManualGame and AutomatedGame are the child classes. They only add the
# things that are different for each mode. No GUI code in this file.

import random

from game.board import BOARD_TYPES


class Game:
    def __init__(self, board_type="English", size=7, rng=None):
        # rng lets the tests pass in a seeded random so the results repeat
        self.rng = rng if rng is not None else random.Random()
        self.new_game(board_type, size)

    def new_game(self, board_type, size):
        if board_type not in BOARD_TYPES:
            raise ValueError("Unknown board type")
        # make the board first, so if the size is bad the old game stays
        board_class = BOARD_TYPES[board_type]
        self.board = board_class(size)
        self.board_type = board_type
        self.size = size
        self.moves = 0

    def make_move(self, from_row, from_col, to_row, to_col):
        if self.is_game_over():
            return False
        if self.board.make_move(from_row, from_col, to_row, to_col):
            self.moves += 1
            return True
        return False

    def is_game_over(self):
        return not self.board.has_moves_left()

    def is_won(self):
        return self.is_game_over() and self.board.count_pegs() == 1

    def get_result(self):
        pegs = self.board.count_pegs()
        if pegs == 1:
            return "You won! Only 1 peg left."
        return "Game over! No moves left. Pegs left: " + str(pegs)


class ManualGame(Game):
    # The player makes every move by clicking. The extra thing a manual
    # game can do is mix up the board in the middle of the game.

    def randomize(self):
        # can't randomize a game that is already over
        if self.is_game_over():
            return False
        self.board.randomize_pegs(self.rng)
        return True


class AutomatedGame(Game):
    # The computer makes every move. It picks a random legal jump each turn
    # until there are no moves left.

    def choose_move(self):
        moves = self.board.get_all_moves()
        if len(moves) == 0:
            return None
        return self.rng.choice(moves)

    def make_auto_move(self):
        # makes one computer move and returns it, or None if the game is over
        move = self.choose_move()
        if move is None:
            return None
        self.make_move(*move)
        return move

    def play_to_end(self):
        # keep moving until the game is over (the GUI does one move at a
        # time instead so you can watch it, but this is handy for tests)
        while self.make_auto_move() is not None:
            pass

    def get_result(self):
        pegs = self.board.count_pegs()
        if pegs == 1:
            return "The computer won! Only 1 peg left."
        return "Game over! The computer has no moves left. Pegs left: " + str(pegs)


# To add a new game mode, make a new class above and add it here.
GAME_MODES = {
    "Manual": ManualGame,
    "Automated": AutomatedGame,
}

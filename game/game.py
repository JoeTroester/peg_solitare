# game.py
# The Game class keeps track of one game: the board, the move count,
# and whether the game is over. It has no GUI code in it.

from game.board import BOARD_TYPES


class Game:
    def __init__(self, board_type="English", size=7):
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

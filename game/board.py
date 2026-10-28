# board.py
# Board classes for Peg Solitaire.
# Board is the parent class and has the code that every board shares.
# Each board type is a child class that only changes which spots are on
# the board and which directions a peg can jump.

PEG = "O"
EMPTY = "."
INVALID = " "  # spot that is not part of the board


class Board:
    def __init__(self, size):
        if size < 5 or size > 9 or size % 2 == 0:
            raise ValueError("Board size must be an odd number from 5 to 9")
        self.size = size

        # fill every spot on the board with a peg
        self.grid = []
        for row in range(size):
            new_row = []
            for col in range(size):
                if self.is_on_board(row, col):
                    new_row.append(PEG)
                else:
                    new_row.append(INVALID)
            self.grid.append(new_row)

        # the middle hole starts empty
        middle = size // 2
        self.grid[middle][middle] = EMPTY

    # The child classes override these methods
    def is_on_board(self, row, col):
        return True

    def get_directions(self):
        # up, down, left, right
        return [(-1, 0), (1, 0), (0, -1), (0, 1)]

    def get_row_offset(self, row):
        # how far to shift a row when drawing it (only the hexagon uses this)
        return 0

    def get_cell(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return INVALID
        return self.grid[row][col]

    def set_cell(self, row, col, value):
        self.grid[row][col] = value

    def is_valid_move(self, from_row, from_col, to_row, to_col):
        # the peg has to move exactly 2 spaces in an allowed direction
        good_direction = False
        for dr, dc in self.get_directions():
            if to_row - from_row == dr * 2 and to_col - from_col == dc * 2:
                good_direction = True
        if not good_direction:
            return False

        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2

        # need a peg to move, a peg to jump over, and an empty hole to land in
        if self.get_cell(from_row, from_col) != PEG:
            return False
        if self.get_cell(mid_row, mid_col) != PEG:
            return False
        if self.get_cell(to_row, to_col) != EMPTY:
            return False
        return True

    def make_move(self, from_row, from_col, to_row, to_col):
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False
        mid_row = (from_row + to_row) // 2
        mid_col = (from_col + to_col) // 2
        self.grid[from_row][from_col] = EMPTY
        self.grid[mid_row][mid_col] = EMPTY  # jumped peg gets removed
        self.grid[to_row][to_col] = PEG
        return True

    def get_moves_from(self, row, col):
        # list of every spot the peg at (row, col) can jump to
        moves = []
        for dr, dc in self.get_directions():
            to_row = row + dr * 2
            to_col = col + dc * 2
            if self.is_valid_move(row, col, to_row, to_col):
                moves.append((to_row, to_col))
        return moves

    def has_moves_left(self):
        for row in range(self.size):
            for col in range(self.size):
                if len(self.get_moves_from(row, col)) > 0:
                    return True
        return False

    def count_pegs(self):
        count = 0
        for row in self.grid:
            count += row.count(PEG)
        return count

    def count_holes(self):
        # number of spots that are part of the board
        count = 0
        for row in self.grid:
            for cell in row:
                if cell != INVALID:
                    count += 1
        return count


class EnglishBoard(Board):
    # plus sign shape, the corners are cut off
    def is_on_board(self, row, col):
        corner = (self.size - 3) // 2
        if row < corner or row >= self.size - corner:
            if col < corner or col >= self.size - corner:
                return False
        return True


class DiamondBoard(Board):
    # diamond shape, every spot close enough to the middle
    def is_on_board(self, row, col):
        middle = self.size // 2
        return abs(row - middle) + abs(col - middle) <= middle


class HexagonBoard(Board):
    # Hexagon shape. Each row is drawn shifted half a hole over, so pegs
    # can jump in 6 directions instead of 4.
    def is_on_board(self, row, col):
        middle = self.size // 2
        x = col - middle
        y = row - middle
        return abs(x) <= middle and abs(y) <= middle and abs(x + y) <= middle

    def get_directions(self):
        return [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, -1)]

    def get_row_offset(self, row):
        return (row - self.size // 2) / 2


# To add a new board type, make a new class above and add it here.
BOARD_TYPES = {
    "English": EnglishBoard,
    "Hexagon": HexagonBoard,
    "Diamond": DiamondBoard,
}

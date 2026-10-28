# test_board.py
# Tests for the Board classes.

import pytest

from game.board import EMPTY, INVALID, PEG, DiamondBoard, EnglishBoard, HexagonBoard


# User Story 1: Choose board size and type
class TestBoardSize:
    def test_valid_board_sizes(self):
        assert EnglishBoard(5).size == 5
        assert EnglishBoard(7).size == 7
        assert EnglishBoard(9).size == 9

    def test_even_size_not_allowed(self):
        with pytest.raises(ValueError):
            EnglishBoard(6)

    def test_size_too_small_or_too_big(self):
        with pytest.raises(ValueError):
            EnglishBoard(3)
        with pytest.raises(ValueError):
            EnglishBoard(11)


class TestBoardType:
    def test_english_board_has_33_holes(self):
        board = EnglishBoard(7)
        assert board.count_holes() == 33
        assert board.get_cell(0, 0) == INVALID  # corner is cut off

    def test_diamond_board_has_25_holes(self):
        board = DiamondBoard(7)
        assert board.count_holes() == 25
        assert board.get_cell(0, 0) == INVALID

    def test_hexagon_board_has_37_holes(self):
        board = HexagonBoard(7)
        assert board.count_holes() == 37


# User Story 2: Start a new game
class TestStartingBoard:
    def test_middle_starts_empty(self):
        for board in [EnglishBoard(7), DiamondBoard(7), HexagonBoard(7)]:
            assert board.get_cell(3, 3) == EMPTY
            assert board.count_pegs() == board.count_holes() - 1


# User Story 3: Making a move
class TestBoardMoves:
    def test_valid_move(self):
        board = EnglishBoard(7)
        assert board.make_move(1, 3, 3, 3) is True
        assert board.get_cell(1, 3) == EMPTY  # where the peg was
        assert board.get_cell(2, 3) == EMPTY  # peg that got jumped
        assert board.get_cell(3, 3) == PEG    # where the peg landed
        assert board.count_pegs() == 31

    def test_hexagon_can_jump_diagonal(self):
        board = HexagonBoard(7)
        assert board.make_move(5, 1, 3, 3) is True

    def test_get_moves_from(self):
        board = EnglishBoard(7)
        assert board.get_moves_from(1, 3) == [(3, 3)]
        assert board.get_moves_from(0, 3) == []

    def test_cant_jump_into_a_peg(self):
        board = EnglishBoard(7)
        assert board.make_move(0, 3, 2, 3) is False

    def test_cant_move_from_empty_hole(self):
        board = EnglishBoard(7)
        assert board.make_move(3, 3, 1, 3) is False

    def test_cant_jump_over_empty_hole(self):
        board = EnglishBoard(7)
        board.make_move(1, 3, 3, 3)
        board.set_cell(0, 3, PEG)
        assert board.make_move(0, 3, 2, 3) is False  # (1, 3) is empty now

    def test_cant_move_one_space(self):
        board = EnglishBoard(7)
        assert board.make_move(2, 3, 3, 3) is False

    def test_no_diagonal_jump_on_english_board(self):
        board = EnglishBoard(7)
        board.set_cell(4, 4, EMPTY)
        assert board.make_move(2, 2, 4, 4) is False

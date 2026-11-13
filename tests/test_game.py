# test_game.py
# Tests for the Game parent class. These are the rules that the manual
# game and the automated game both share.

import pytest

from game.board import EMPTY, PEG, HexagonBoard
from game.game import Game


def empty_the_board(game):
    # take every peg off so a test can set up its own pegs
    for row in range(game.size):
        for col in range(game.size):
            if game.board.get_cell(row, col) == PEG:
                game.board.set_cell(row, col, EMPTY)


# User Story 1 and 3: Choose board size and type, start a new game
class TestNewGame:
    def test_default_game_is_english_7(self):
        game = Game()
        assert game.board_type == "English"
        assert game.size == 7
        assert game.moves == 0

    def test_new_game_with_chosen_type_and_size(self):
        game = Game()
        game.new_game("Hexagon", 5)
        assert game.board_type == "Hexagon"
        assert game.size == 5
        assert isinstance(game.board, HexagonBoard)

    def test_new_game_resets_everything(self):
        game = Game()
        game.make_move(1, 3, 3, 3)
        game.new_game("English", 7)
        assert game.moves == 0
        assert game.board.count_pegs() == 32

    def test_unknown_board_type(self):
        game = Game()
        with pytest.raises(ValueError):
            game.new_game("Triangle", 7)

    def test_bad_size_keeps_old_game(self):
        game = Game("Diamond", 5)
        with pytest.raises(ValueError):
            game.new_game("English", 4)
        assert game.board_type == "Diamond"
        assert game.size == 5


# User Story 4 and 6: Making a move (same rules for both modes)
class TestGameMoves:
    def test_move_adds_to_move_count(self):
        game = Game()
        assert game.make_move(1, 3, 3, 3) is True
        assert game.moves == 1

    def test_bad_move_does_not_count(self):
        game = Game()
        assert game.make_move(0, 3, 2, 3) is False
        assert game.moves == 0


# User Story 5 and 7: Checking the end of the game
class TestEndOfGame:
    def test_game_not_over_at_start(self):
        assert Game().is_game_over() is False

    def test_win_with_one_peg_left(self):
        game = Game()
        empty_the_board(game)
        game.board.set_cell(3, 2, PEG)
        game.board.set_cell(3, 3, PEG)
        game.make_move(3, 2, 3, 4)
        assert game.is_game_over() is True
        assert game.is_won() is True
        assert "won" in game.get_result()

    def test_game_over_with_pegs_stuck(self):
        game = Game()
        empty_the_board(game)
        game.board.set_cell(0, 3, PEG)
        game.board.set_cell(6, 3, PEG)
        assert game.is_game_over() is True
        assert game.is_won() is False
        assert "Pegs left: 2" in game.get_result()

    def test_no_moves_after_game_over(self):
        game = Game()
        empty_the_board(game)
        game.board.set_cell(0, 3, PEG)
        game.board.set_cell(6, 3, PEG)
        assert game.make_move(0, 3, 2, 3) is False

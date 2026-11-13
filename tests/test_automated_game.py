# test_automated_game.py
# Tests for the automated game mode (the computer makes the moves).
# Most tests pass in a seeded random so the computer's picks are the same
# every time the tests run.

import random

import pytest

from game.board import EMPTY, PEG
from game.game import GAME_MODES, AutomatedGame


def empty_the_board(game):
    for row in range(game.size):
        for col in range(game.size):
            if game.board.get_cell(row, col) == PEG:
                game.board.set_cell(row, col, EMPTY)


# User Story 2: Choose the game mode
class TestChooseAutomatedMode:
    def test_automated_mode_makes_an_automated_game(self):
        game = GAME_MODES["Automated"]("Diamond", 5)
        assert isinstance(game, AutomatedGame)
        assert game.board_type == "Diamond"
        assert game.size == 5


# User Story 6: Make a move in an automated game
class TestAutomatedMove:
    def test_computer_makes_a_legal_move(self):
        game = AutomatedGame("English", 7, rng=random.Random(3))
        legal_moves = game.board.get_all_moves()
        move = game.make_auto_move()
        assert move in legal_moves
        assert game.moves == 1
        assert game.board.count_pegs() == 31

    def test_computer_picks_the_only_move(self):
        game = AutomatedGame("English", 7)
        empty_the_board(game)
        # two pegs on the left edge, only (3, 0) can jump (over (3, 1) into (3, 2))
        game.board.set_cell(3, 0, PEG)
        game.board.set_cell(3, 1, PEG)
        assert game.choose_move() == (3, 0, 3, 2)


# User Story 7: An automated game is over
class TestAutomatedGameOver:
    @pytest.mark.parametrize("board_type", ["English", "Hexagon", "Diamond"])
    def test_computer_plays_until_no_moves_left(self, board_type):
        game = AutomatedGame(board_type, 7, rng=random.Random(1))
        start_pegs = game.board.count_pegs()
        game.play_to_end()
        assert game.is_game_over() is True
        # every move takes away exactly one peg
        assert game.moves == start_pegs - game.board.count_pegs()

    def test_no_more_moves_after_game_over(self):
        game = AutomatedGame("English", 7, rng=random.Random(1))
        game.play_to_end()
        moves = game.moves
        assert game.make_auto_move() is None
        assert game.moves == moves

    def test_computer_win_message(self):
        game = AutomatedGame("English", 7)
        empty_the_board(game)
        game.board.set_cell(3, 2, PEG)
        game.board.set_cell(3, 3, PEG)
        game.play_to_end()
        assert game.is_won() is True
        assert game.get_result() == "The computer won! Only 1 peg left."

    def test_computer_stuck_message(self):
        game = AutomatedGame("English", 7)
        empty_the_board(game)
        game.board.set_cell(0, 3, PEG)
        game.board.set_cell(6, 3, PEG)
        assert game.is_game_over() is True
        assert "Pegs left: 2" in game.get_result()

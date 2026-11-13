# test_manual_game.py
# Tests for the manual game mode (the player makes the moves).

import random

from game.board import EMPTY, PEG, INVALID
from game.game import GAME_MODES, ManualGame


def empty_the_board(game):
    # take every peg off so a test can set up its own pegs
    for row in range(game.size):
        for col in range(game.size):
            if game.board.get_cell(row, col) == PEG:
                game.board.set_cell(row, col, EMPTY)


# User Story 2: Choose the game mode
class TestChooseManualMode:
    def test_manual_mode_makes_a_manual_game(self):
        game = GAME_MODES["Manual"]("Hexagon", 7)
        assert isinstance(game, ManualGame)
        assert game.board_type == "Hexagon"
        assert game.size == 7


# User Story 4: Make a move in a manual game
class TestManualMove:
    def test_player_makes_a_valid_move(self):
        game = ManualGame("English", 7)
        assert game.make_move(1, 3, 3, 3) is True
        assert game.board.get_cell(2, 3) == EMPTY  # jumped peg is gone
        assert game.board.get_cell(3, 3) == PEG
        assert game.moves == 1

    def test_player_makes_an_invalid_move(self):
        game = ManualGame("English", 7)
        assert game.make_move(0, 3, 2, 3) is False  # landing spot has a peg
        assert game.moves == 0
        assert game.board.count_pegs() == 32


# User Story 5: A manual game is over
class TestManualGameOver:
    def test_manual_win(self):
        game = ManualGame("English", 7)
        empty_the_board(game)
        game.board.set_cell(3, 2, PEG)
        game.board.set_cell(3, 3, PEG)
        game.make_move(3, 2, 3, 4)
        assert game.is_game_over() is True
        assert game.get_result() == "You won! Only 1 peg left."

    def test_manual_game_over_with_pegs_left(self):
        game = ManualGame("English", 7)
        empty_the_board(game)
        game.board.set_cell(0, 3, PEG)
        game.board.set_cell(6, 3, PEG)
        assert game.is_game_over() is True
        assert "Pegs left: 2" in game.get_result()


# User Story 8: Randomize the state of the board during a manual game
class TestRandomize:
    def test_randomize_keeps_pegs_and_moves(self):
        game = ManualGame("English", 7, rng=random.Random(5))
        game.make_move(1, 3, 3, 3)
        before = [row[:] for row in game.board.grid]
        assert game.randomize() is True
        assert game.board.grid != before
        assert game.board.count_pegs() == 31  # same number of pegs
        assert game.moves == 1  # randomizing is not a move

    def test_pegs_only_land_in_real_holes(self):
        game = ManualGame("English", 7, rng=random.Random(5))
        game.randomize()
        for row in range(7):
            for col in range(7):
                if not game.board.is_on_board(row, col):
                    assert game.board.get_cell(row, col) == INVALID

    def test_can_keep_playing_after_randomize(self):
        game = ManualGame("English", 7, rng=random.Random(5))
        game.randomize()
        assert game.is_game_over() is False
        move = game.board.get_all_moves()[0]
        assert game.make_move(*move) is True
        assert game.moves == 1

    def test_cant_randomize_after_game_over(self):
        game = ManualGame("English", 7)
        empty_the_board(game)
        game.board.set_cell(0, 3, PEG)
        game.board.set_cell(6, 3, PEG)
        before = [row[:] for row in game.board.grid]
        assert game.randomize() is False
        assert game.board.grid == before

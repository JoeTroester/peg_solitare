# Peg Solitaire (CS 449) - Sprint 3

## How to run
```
python main.py
```
Pick a board type, an odd size (5, 7 or 9) and a game mode, then click **New Game**.

- **Manual** - click a peg, then click the hole you want it to jump into.
  Click **Randomize** any time during the game to mix up where the pegs are.
- **Automated** - the computer starts playing as soon as you click New Game and
  makes one move every half second until it runs out of moves.

A popup shows up when there are no moves left.

## How to run the tests
```
pip install pytest
python -m pytest
```

## Folder layout
- `game/` - all the rules (boards, game modes, end of game). No tkinter in here.
  - `board.py` - `Board` parent class with `EnglishBoard`, `HexagonBoard`, `DiamondBoard`
  - `game.py` - `Game` parent class with `ManualGame` and `AutomatedGame`
- `ui/` - the tkinter window (`gui.py`).
- `tests/` - pytest unit tests.

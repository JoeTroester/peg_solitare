# Peg Solitaire (CS 449) - Sprint 2

## How to run
```
python main.py
```
Pick a board type and an odd size (5, 7 or 9), click **New Game**, then click a
peg and click the hole you want it to jump into. Green rings show where the
selected peg can go. A popup shows up when there are no moves left.

## How to run the tests
```
pip install pytest
python -m pytest
```

## Folder layout
- `game/` - all the rules (boards, game state, end of game). No tkinter in here.
- `ui/` - the tkinter window (`gui.py`).
- `tests/` - pytest unit tests.

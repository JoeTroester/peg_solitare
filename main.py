# main.py
# Run this file to start the game.

import tkinter as tk

from ui.gui import PegSolitaireGUI

root = tk.Tk()
app = PegSolitaireGUI(root)
root.mainloop()

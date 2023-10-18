import tkinter as tk
from src.gui import IsolationGui

def run_game():
    root = tk.Tk()
    game = IsolationGui(root)
    root.mainloop()

if __name__ == "__main__":
    run_game()

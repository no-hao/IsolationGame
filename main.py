import tkinter as tk
from src.gui import IsolationGUI

def main():
    root = tk.Tk()
    game = IsolationGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk
from .isolation import Isolation
from .player import Player, HumanPlayer

class IsolationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Isolation Game")

        # Create the game board
        self.cells = []
        for i in range(8):
            row = []
            for j in range(6):
                cell = tk.Label(master, width=10, height=4, bg="white", relief="ridge")
                cell.grid(row=i, column=j)
                cell.bind("<Button-1>", self.handle_cell_click)
                row.append(cell)
            self.cells.append(row)

        # Frame for player selection dropdowns
        self.selection_frame = tk.Frame(master)
        self.selection_frame.grid(row=8, column=0, columnspan=6)

        # Player 1 selection in the frame
        self.player1_label = tk.Label(self.selection_frame, text="Player 1:")
        self.player1_label.pack(side=tk.LEFT, padx=10)
        self.player1_var = tk.StringVar(master)
        self.player1_var.set("Human")  # default value
        self.player1_dropdown = ttk.Combobox(self.selection_frame, textvariable=self.player1_var, values=["Human", "Computer"])
        self.player1_dropdown.pack(side=tk.LEFT, padx=10)

        # Player 2 selection in the frame
        self.player2_label = tk.Label(self.selection_frame, text="Player 2:")
        self.player2_label.pack(side=tk.LEFT, padx=10)
        self.player2_var = tk.StringVar(master)
        self.player2_var.set("Human")  # default value
        self.player2_dropdown = ttk.Combobox(self.selection_frame, textvariable=self.player2_var, values=["Human", "Computer"])
        self.player2_dropdown.pack(side=tk.LEFT, padx=10)

        # Start button below the frame
        self.start_button = tk.Button(master, text="Start", command=self.start_game)
        self.start_button.grid(row=9, column=0, columnspan=6)

    def refresh_board(self):
        for i in range(8):
            for j in range(6):
                cell_value = self.game.board[i][j]
                if cell_value == 0:
                    self.cells[i][j].config(bg="white")  # Empty cell
                elif cell_value == -1:
                    self.cells[i][j].config(bg="grey")   # Removed token
                elif isinstance(cell_value, Player):
                    if cell_value == self.game.players[0]:
                        self.cells[i][j].config(bg="blue")   # Player 1
                    else:
                        self.cells[i][j].config(bg="red")    # Player 2

    def handle_cell_click(self, event):
        row, col = event.widget.grid_info()["row"], event.widget.grid_info()["column"]
        current_player = self.game.players[self.game.current_player_index]

        # If a move is valid, switch to the next player
        if self.game.make_move(current_player, row, col):
            self.game.current_player_index ^= 1  # Toggle between 0 and 1

        self.refresh_board()

    def start_game(self):
        # Initialize the game with the selected players
        player1_class = HumanPlayer if self.player1_var.get() == "Human" else ComputerPlayer
        player2_class = HumanPlayer if self.player2_var.get() == "Human" else ComputerPlayer

        self.game = Isolation(player1_class("Player 1"), player2_class("Player 2"))

        # Display the players on the board
        self.refresh_board()

        # Disabling the dropdowns once the game starts
        self.player1_dropdown.config(state="disabled")
        self.player2_dropdown.config(state="disabled")
        self.start_button.config(state="disabled")

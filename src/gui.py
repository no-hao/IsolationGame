import random
import logging
import tkinter as tk
from tkinter import ttk, messagebox, Canvas
from .isolation import Isolation
from .player import Player, HumanPlayer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)
logger.handlers = []  # Clear existing handlers

class ListboxHandler(logging.Handler):
    def __init__(self, listbox):
        super().__init__()
        self.listbox = listbox

    def emit(self, record):
        log_entry = self.format(record)
        self.listbox.insert(tk.END, log_entry)
        # Ensure the latest log is visible in the Listbox
        self.listbox.yview(tk.END)

class IsolationGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Isolation Game")

        # Player 1 Selection Frame
        self.player1_selection_frame = tk.Frame(master)
        self.player1_selection_frame.grid(row=0, column=0, columnspan=6, pady=(20, 10))

        # Player 1 light indicator
        self.player1_light = Canvas(self.player1_selection_frame, width=10, height=10, bg="#a4a6a0", relief="ridge")
        self.player1_light.pack(side=tk.LEFT, padx=5)

        # Player 1 selection in the frame
        self.player1_label = tk.Label(self.player1_selection_frame, text="Player 1:")
        self.player1_label.pack(side=tk.LEFT, padx=10)
        self.player1_var = tk.StringVar(master)
        self.player1_var.set("Human")  # default value
        self.player1_dropdown = ttk.Combobox(self.player1_selection_frame, textvariable=self.player1_var, values=["Human", "Computer"])
        self.player1_dropdown.pack(side=tk.LEFT, padx=10)

        # Create the game board
        self.cells = []
        for i in range(8):
            row = []
            for j in range(6):
                cell = tk.Label(master, width=10, height=4, bg="white", relief="ridge")
                cell.grid(row=i+1, column=j)  # Offset by 1 to account for Player 1 dropdown
                cell.bind("<Button-1>", self.handle_cell_click)
                row.append(cell)
            self.cells.append(row)

        # Player 2 Selection Frame
        self.player2_selection_frame = tk.Frame(master)
        self.player2_selection_frame.grid(row=9, column=0, columnspan=6, pady=(10, 20))

        # Player 2 light indicator
        self.player2_light = Canvas(self.player2_selection_frame, width=10, height=10, bg="#a4a6a0", relief="ridge")
        self.player2_light.pack(side=tk.LEFT, padx=5)

        # Player 2 selection in the frame
        self.player2_label = tk.Label(self.player2_selection_frame, text="Player 2:")
        self.player2_label.pack(side=tk.LEFT, padx=10)
        self.player2_var = tk.StringVar(master)
        self.player2_var.set("Human")  # default value
        self.player2_dropdown = ttk.Combobox(self.player2_selection_frame, textvariable=self.player2_var, values=["Human", "Computer"])
        self.player2_dropdown.pack(side=tk.LEFT, padx=10)

        # Start and Restart buttons
        self.start_button = tk.Button(master, text="Start", command=self.start_game)
        self.start_button.grid(row=11, column=0, columnspan=3)
        self.restart_button = tk.Button(master, text="Restart", command=self.restart_game, state="disabled")
        self.restart_button.grid(row=11, column=3, columnspan=3)

        # Legend and Action Log to the right of the board
        self.side_frame = tk.Frame(master)
        self.side_frame.grid(row=0, column=6, rowspan=12, sticky="ns", pady=(50, 0))  # Added padding at the top to move legend down
        legend_items = [("blue", "Player 1"), ("red", "Player 2"), ("#44463e", "Removed Token"), ("white", "Available Cell")]
        for color, text in legend_items:
            item_frame = tk.Frame(self.side_frame)
            item_frame.pack(pady=5, fill=tk.X, anchor="e")
            color_label = tk.Label(item_frame, width=5, height=2, bg=color, relief="ridge")
            color_label.pack(side=tk.LEFT, padx=5)
            text_label = tk.Label(item_frame, text=text, width=15)  # Set a consistent width
            text_label.pack(side=tk.LEFT, padx=5)

        # Action Log
        self.action_log = tk.Listbox(self.side_frame, height=15, width=25)
        self.action_log.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Set up the logger to display logs in the action_log Listbox
        handler = ListboxHandler(self.action_log)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    # When updating the turn, we should also update the light indicators:
    def update_turn_indicator(self):
        # If player 1's turn
        if self.game.current_player_index == 0:
            self.player1_light.config(bg="#27c840") # green
            self.player2_light.config(bg="#febc2f") # orange
        # If player 2's turn
        else:
            self.player1_light.config(bg="#febc2f")
            self.player2_light.config(bg="#27c840")

    def refresh_board(self):
        for i in range(8):
            for j in range(6):
                cell_value = self.game.board[i][j]
                if cell_value == 0:
                    self.cells[i][j].config(bg="white")  # Empty cell
                elif cell_value == -1:
                    self.cells[i][j].config(bg="#44463e")   # Removed token
                elif isinstance(cell_value, Player):
                    if cell_value == self.game.players[0]:
                        self.cells[i][j].config(bg="blue")   # Player 1
                    else:
                        self.cells[i][j].config(bg="red")    # Player 2

    def handle_cell_click(self, event):
        row, col = event.widget.grid_info()["row"] - 1, event.widget.grid_info()["column"]  # Offset row by 1
        current_player = self.game.players[self.game.current_player_index]

        if not self.game.awaiting_token_removal:
            # Process a move
            if self.game.is_valid_move(current_player, row, col):
                self.game.make_move(current_player, row, col)
                self.refresh_board()
                self.update_turn_indicator()
            else:
                self.shake_window()  # Provide feedback for invalid move
        else:
            # Process a token removal
            if self.game.is_valid_token_removal(row, col):
                self.game.remove_token(row, col)
                self.game.current_player_index ^= 1  # Toggle between 0 and 1
                self.refresh_board()
                self.update_turn_indicator()
            else:
                self.shake_window()  # Provide feedback for invalid token removal

        if self.game.is_game_over():
            self.display_game_over_message()

    def shake_window(self):
        # Shake the window as feedback for invalid action
        x, y = self.master.winfo_x(), self.master.winfo_y()
        offset = 5  # Number of pixels to move the window
        
        for _ in range(2):  # Shake back and forth, therefore 2 iterations
            for (dx, dy) in [(offset, 0), (-offset, 0), (-offset, 0), (offset, 0), (0, offset), (0, -offset), (0, -offset), (0, offset)]:
                self.master.geometry(f"+{x+dx}+{y+dy}")
                self.master.update_idletasks()  # Force update the display
                self.master.after(3)  # Pause for 3 milliseconds

        self.master.geometry(f"+{x}+{y}")  # Return the window to its original location

    def start_game(self):
        # Initialize the game with the selected players
        player1_class = HumanPlayer if self.player1_var.get() == "Human" else ComputerPlayer
        player2_class = HumanPlayer if self.player2_var.get() == "Human" else ComputerPlayer

        self.game = Isolation(player1_class("Player 1"), player2_class("Player 2"))

        # Randomize the starting player
        self.game.current_player_index = random.choice([0, 1])
        
        # Update light indicator for the starting player
        self.update_turn_indicator()

        # Display the players on the board
        self.refresh_board()

        # Disabling the dropdowns and start button once the game starts
        self.player1_dropdown.config(state="disabled")
        self.player2_dropdown.config(state="disabled")
        self.start_button.config(state="disabled")
        self.restart_button.config(state="normal")  # Enable the restart button

        # logging message
        logger.info(f"Game started. {self.game.players[self.game.current_player_index].name} goes first.")


    def restart_game(self):
        # Reset the board and game-related variables
        self.game = None
        for i in range(8):
            for j in range(6):
                self.cells[i][j].config(bg="white")
        self.player1_dropdown.config(state="normal")
        self.player2_dropdown.config(state="normal")
        self.start_button.config(state="normal")
        self.restart_button.config(state="disabled")
        # Remove the reference to self.turn_prompt as it's not defined in the current class
        self.action_log.delete(0, tk.END)  # Clear the action log

        # logging message
        logger.info("Game restarted.")


    def display_game_over_message(self):
        # Display a game over message
        winning_player_index = 1 - self.game.current_player_index  # Toggle between 0 and 1
        winning_player_name = self.game.players[winning_player_index].name
        tk.messagebox.showinfo("Game Over", f"{winning_player_name} Wins!")

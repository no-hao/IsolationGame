import time
import random
import logging
import tkinter as tk
from tkinter import ttk, messagebox, Canvas
from .isolation import Isolation
from .player import Player, HumanPlayer, ComputerPlayer

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger("IsolationGameLogger")
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
    # Define the class-level constant here
    COMPUTER_TURN_DELAY = 250  # .1 second delay

    def __init__(self, master):
        self.master = master
        self.master.title("Isolation Game")

        self.setup_bindings()
        self.setup_player_selection()
        self.setup_board()
        self.setup_buttons()
        self.setup_side_panel()
        self.setup_logger()

    def setup_player_selection(self):
        # Player 1 Selection Frame
        self.player1_selection_frame = tk.Frame(self.master)
        self.player1_selection_frame.grid(row=0, column=0, columnspan=6, pady=(20, 10))

        # Player 1 light indicator
        self.player1_light = Canvas(self.player1_selection_frame, width=10, height=10, bg="#a4a6a0", relief="ridge")
        self.player1_light.pack(side=tk.LEFT, padx=5)

        # Player 1 selection in the frame
        self.player1_label = tk.Label(self.player1_selection_frame, text="Player 1:")
        self.player1_label.pack(side=tk.LEFT, padx=10)
        self.player1_var = tk.StringVar(self.master)
        self.player1_var.set("Human")  # default value
        self.player1_dropdown = ttk.Combobox(self.player1_selection_frame, textvariable=self.player1_var, values=["Human", "Computer"], state="readonly")
        self.player1_dropdown.pack(side=tk.LEFT, padx=10)

        # Player 2 Selection Frame
        self.player2_selection_frame = tk.Frame(self.master)
        self.player2_selection_frame.grid(row=9, column=0, columnspan=6, pady=(10, 20))

        # Player 2 light indicator
        self.player2_light = Canvas(self.player2_selection_frame, width=10, height=10, bg="#a4a6a0", relief="ridge")
        self.player2_light.pack(side=tk.LEFT, padx=5)

        # Player 2 selection in the frame
        self.player2_label = tk.Label(self.player2_selection_frame, text="Player 2:")
        self.player2_label.pack(side=tk.LEFT, padx=10)
        self.player2_var = tk.StringVar(self.master)
        self.player2_var.set("Human")  # default value
        self.player2_dropdown = ttk.Combobox(self.player2_selection_frame, textvariable=self.player2_var, values=["Human", "Computer"], state="readonly")
        self.player2_dropdown.pack(side=tk.LEFT, padx=10)

    def setup_side_panel(self):
        # Legend and Action Log to the right of the board
        self.side_frame = tk.Frame(self.master)
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
        self.action_log = tk.Listbox(self.side_frame, height=15, width=35)
        self.action_log.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def setup_board(self):
        # Create the game board
        self.cells = []
        for i in range(8):
            row = []
            for j in range(6):
                cell = tk.Label(self.master, width=10, height=4, bg="white", relief="ridge")
                cell.grid(row=i+1, column=j)  # Offset by 1 to account for Player 1 dropdown
                cell.bind("<Button-1>", self.handle_cell_click)
                row.append(cell)
            self.cells.append(row)

    def setup_buttons(self):
        # Start and Restart buttons
        self.start_button = tk.Button(self.master, text="Start", command=self.start_game)
        self.start_button.grid(row=11, column=0, columnspan=3)
        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game, state="disabled")
        self.restart_button.grid(row=11, column=3, columnspan=3)

    def setup_logger(self):
        handler = ListboxHandler(self.action_log)
        formatter = logging.Formatter('%(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def setup_bindings(self):
        # Bind the "Escape" key to the close_confetti method
        self.master.bind("<Escape>", self.close_confetti)

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
        logger.info("handle_cell_click invoked")
        if self.game and self.game.is_game_over():
            return  # If the game is over, don't process any clicks
        
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

        next_player = self.game.players[self.game.current_player_index]
        if isinstance(next_player, ComputerPlayer):
            self.master.after(1000, self.execute_computer_turn)  # Start the computer's turn after a 1-second delay

    def execute_computer_turn(self):
        # Check if the game is over
        if self.game.is_game_over():
            self.display_game_over_message()
            return

        # Get the current player
        current_player = self.game.players[self.game.current_player_index]

        # If the current player is a computer
        if isinstance(current_player, ComputerPlayer):
            if not self.game.awaiting_token_removal:
                # Get a move from the computer and make it
                move = current_player.choose_move(self.game)
                if move:
                    row, col = move
                    self.game.make_move(current_player, row, col)
            else:
                # Get a token removal choice from the computer and execute it
                token_removal = current_player.choose_token_to_remove(self.game)
                if token_removal:
                    row, col = token_removal
                    self.game.remove_token(row, col)
                    self.game.current_player_index ^= 1  # Only toggle the player after token removal

            # Refresh the board state in the GUI
            self.refresh_board()
            self.update_turn_indicator()

            # If the next player is also a computer, call this method again after a short delay
            next_player = self.game.players[self.game.current_player_index]
            if isinstance(next_player, ComputerPlayer):
                self.computer_turn_id = self.master.after(IsolationGUI.COMPUTER_TURN_DELAY, self.execute_computer_turn)

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
        self.start_time = time.time()

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

        starting_player = self.game.players[self.game.current_player_index]
        if isinstance(starting_player, ComputerPlayer):
            self.master.after(1000, self.execute_computer_turn)  # Start the computer's turn after a 1-second delay

    def restart_game(self):
        # Reset the board and game-related variables
        self.game = None
        for i in range(8):
            for j in range(6):
                self.cells[i][j].config(bg="white")
        self.player1_dropdown.config(state="readonly")
        self.player2_dropdown.config(state="readonly")
        self.start_button.config(state="normal")
        self.restart_button.config(state="disabled")
        # Remove the reference to self.turn_prompt as it's not defined in the current class
        self.action_log.delete(0, tk.END)  # Clear the action log

        if hasattr(self, 'computer_turn_id'):
            self.master.after_cancel(self.computer_turn_id)

        # logging message
        logger.info("Game restarted.")

    def display_confetti(self):
        # Create a canvas overlaying the entire game board
        self.confetti_canvas = tk.Canvas(self.master, width=self.master.winfo_width(), height=self.master.winfo_height(), bd=0, highlightthickness=0)
        self.confetti_canvas.grid(row=0, column=0, rowspan=12, columnspan=7)

        # Create confetti (small rectangles)
        self.confetti_pieces = []
        for _ in range(100):  # for 100 pieces of confetti
            x = random.randint(0, self.master.winfo_width())
            y = random.randint(-200, -10)  # start off the screen
            confetti_color = random.choice(["red", "blue", "green", "yellow", "purple", "orange"])
            piece = self.confetti_canvas.create_rectangle(x, y, x+10, y+10, fill=confetti_color)
            self.confetti_pieces.append(piece)

        # Start the animation and save the ID
        self.confetti_animation_id = self.master.after(50, self.animate_confetti)

    def animate_confetti(self):
        if not hasattr(self, 'confetti_canvas'):
            return  # Exit the method if there's no confetti canvas
        for piece in self.confetti_pieces:
            self.confetti_canvas.move(piece, 0, 10)  # Move downwards
            if self.confetti_canvas.coords(piece)[1] > self.master.winfo_height():
                # Reset the piece to the top if it falls off the bottom
                self.confetti_canvas.move(piece, 0, -self.master.winfo_height()-20)
        self.master.after(50, self.animate_confetti)  # Repeat every 50 ms

    def close_confetti(self, event=None):
        """Hide the confetti canvas and prepare for a potential game restart."""
        # Stop the confetti animation
        if hasattr(self, 'confetti_animation_id'):
            self.master.after_cancel(self.confetti_animation_id)
            
        if hasattr(self, 'confetti_canvas'):
            self.confetti_canvas.destroy()
            del self.confetti_canvas  # Remove the reference to the canvas
            self.restart_game()  # Prepare for a new game

    def display_game_over_message(self):
        # Create confetti canvas
        self.display_confetti()

        if hasattr(self, 'computer_turn_id'):
            self.master.after_cancel(self.computer_turn_id)

        # Display a game over message
        winning_player_index = 1 - self.game.current_player_index  # Toggle between 0 and 1
        winning_player_name = self.game.players[winning_player_index].name

        # Calculate elapsed time
        elapsed_time = time.time() - self.start_time
        minutes, seconds = divmod(elapsed_time, 60)
        elapsed_time_str = f"Elapsed Time: {int(minutes)} minutes {int(seconds)} seconds"

        # Add the game over message (with elapsed time) to the canvas
        self.confetti_canvas.create_text(self.master.winfo_width() / 2, self.master.winfo_height() / 2 - 70,  # Adjusted position for better spacing
                                        text=f"{winning_player_name} Wins!\n{elapsed_time_str}", 
                                        font=('Arial', 24, 'bold'), fill='black')

        # Add the game statistics below the game over message
        stats_text = (
            f"Moves made by {self.game.players[0].name}: {self.game.moves_by_player[self.game.players[0]]}\n"
            f"Moves made by {self.game.players[1].name}: {self.game.moves_by_player[self.game.players[1]]}\n"
            f"Tokens Removed by {self.game.players[0].name}: {self.game.tokens_removed_by_player[self.game.players[0]]}\n"
            f"Tokens Removed by {self.game.players[1].name}: {self.game.tokens_removed_by_player[self.game.players[1]]}"
        )
        self.confetti_canvas.create_text(self.master.winfo_width() / 2, self.master.winfo_height() / 2 + 30,  # Adjusted position for better spacing
                                        text=stats_text, font=('Arial', 14), fill='black')

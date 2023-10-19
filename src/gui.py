import random
import tkinter as tk
from .isolation import IsolationGameState
from .player import HumanPlayer, ComputerPlayer

class IsolationGui:
    def __init__(self, root):
        self.root = root
        self.root.title("Isolation Game")

        # Parameters
        self.rows = 8
        self.columns = 6
        self.cell_size = 50

        # Colors
        self.removed_cell_color = "#323232"
        self.playerA_color = "#3498db"  # Blue for Player A
        self.playerB_color = "#e74c3c"  # Red for Player B

        # Initialize game state first before setting up the UI components
        self.initialize_game_state()

        # Set up the UI components
        self.setup_ui_components()

        # Finally, initialize the game state using the selected values from the dropdown menus
        self.game_state = IsolationGameState(
            player_A={
                'color': self.playerA_color,
                'player_obj': HumanPlayer() if self.playerA_selection.get() == 'Human' else ComputerPlayer()
            },
            player_B={
                'color': self.playerB_color,
                'player_obj': HumanPlayer() if self.playerB_selection.get() == 'Human' else ComputerPlayer()
            }
        )

        # UI setup
        self.draw_board()
        self.center_window(self.root)

    def setup_ui_components(self):
        """Set up the UI components."""

        # Using a PanedWindow to split the canvas and the legend
        self.paned = tk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.paned.pack(pady=20, fill=tk.BOTH, expand=1)

        # Left Frame (for all the main UI elements)
        self.left_frame = tk.Frame(self.paned)
        self.paned.add(self.left_frame)

        # Player A's Frame (at the top)
        self.frame_A = tk.Frame(self.left_frame)
        self.frame_A.pack(fill=tk.BOTH)

        # Player A's turn label
        self.turn_label_A = tk.Label(self.frame_A, text="", font=("Arial", 16))
        self.turn_label_A.pack()

        # Invalid move message for Player A
        self.invalid_move_label_A = tk.Label(self.frame_A, text="", font=("Arial", 10), fg="#c0392b")
        self.invalid_move_label_A.pack(pady=5)

        self.canvas = tk.Canvas(self.left_frame, width=self.cell_size * self.columns, height=self.cell_size * self.rows)
        self.canvas.pack(pady=20)

        # Player B's Frame (at the bottom)
        self.frame_B = tk.Frame(self.left_frame)
        self.frame_B.pack(fill=tk.BOTH)

        # Player B's turn label
        self.turn_label_B = tk.Label(self.frame_B, text="", font=("Arial", 16))
        self.turn_label_B.pack(side=tk.TOP)

        # Invalid move message for Player B
        self.invalid_move_label_B = tk.Label(self.frame_B, text="", font=("Arial", 10), fg="#c0392b")
        self.invalid_move_label_B.pack(side=tk.TOP, pady=5)

        self.update_turn_labels()

        # Then setup the player selection dropdowns
        self.setup_player_selection()

        # Start/Restart button (moved to bottom of left_frame)
        self.start_button = tk.Button(self.left_frame, text="Start", command=self.start_game, font=("Arial", 20, 'bold'), bg="#323232", fg="black", padx=20, pady=10, relief=tk.GROOVE, bd=3)
        self.start_button.pack(pady=20)

        # Setting up the game legend
        self.setup_legend()

    def setup_legend(self):
        """Set up the game legend."""
        # Right Frame (for the legend)
        self.right_frame = tk.Frame(self.paned, bg=self.root.cget('bg'))
        self.paned.add(self.right_frame)

        # Spacer frame to align the legend with the game board
        spacer_frame = tk.Frame(self.right_frame, bg=self.root.cget('bg'), height=128)  # Adjust height as needed
        spacer_frame.pack(fill=tk.BOTH)

        # Update to access player information from game_state
        player_a_color = self.playerA_color
        player_b_color = self.playerB_color

        legends = [
            ("#bdc3c7", "Available Cell"),
            (player_a_color, "Player A Pawn"),
            (player_b_color, "Player B Pawn"),
            (self.removed_cell_color, "Removed Cell")
        ]

        for color, text in legends:
            legend_item_frame = tk.Frame(self.right_frame, bg=self.root.cget('bg'), padx=10, pady=5)
            legend_item_frame.pack(fill=tk.BOTH, padx=10, pady=5, anchor=tk.N)

            legend_cell_frame = tk.Frame(legend_item_frame, bg=color, width=self.cell_size, height=self.cell_size)
            legend_cell_frame.pack(side=tk.LEFT, padx=5)

            label = tk.Label(legend_item_frame, text=text, bg=self.root.cget('bg'))
            label.pack(side=tk.LEFT, padx=5)

        # After setting up the legend items
        self.log_display = tk.Text(self.right_frame, height=25, width=35, bg="white", wrap=tk.WORD, borderwidth=2, relief=tk.GROOVE)
        self.log_display.pack(pady=10, padx=10)

    def setup_player_selection(self):
        """Set up the player selection dropdowns."""
        self.player_types = ["Human", "Computer"]

        # Player A Selection
        self.playerA_label = tk.Label(self.frame_A, text="Player A:", font=("Arial", 12))
        self.playerA_label.pack(pady=5)

        self.playerA_selection = tk.StringVar(self.frame_A)
        self.playerA_selection.set(self.player_types[0])  # default value
        self.playerA_dropdown = tk.OptionMenu(self.frame_A, self.playerA_selection, *self.player_types)
        self.playerA_dropdown.pack(pady=5)

        # Player B Selection
        self.playerB_label = tk.Label(self.frame_B, text="Player B:", font=("Arial", 12))
        self.playerB_label.pack(pady=5)  # Pack the label first

        self.playerB_selection = tk.StringVar(self.frame_B)
        self.playerB_selection.set(self.player_types[0])  # default value
        self.playerB_dropdown = tk.OptionMenu(self.frame_B, self.playerB_selection, *self.player_types)
        self.playerB_dropdown.pack(pady=5)  # Then pack the dropdown

    def draw_board(self):
        for row in range(self.rows):
            for column in range(self.columns):
                x1, y1, x2, y2 = self.get_coordinates(row, column)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#bdc3c7", tags=f"cell_{row}_{column}", width=2, outline="#9b9b9b")

        # Place initial pawns
        self.place_pawn(self.game_state.players['A']['row'], self.game_state.players['A']['column'], "#3498db", "A")
        self.place_pawn(self.game_state.players['B']['row'], self.game_state.players['B']['column'], "#e74c3c", "B")

    def place_pawn(self, row, column, color, text):
        x1, y1, x2, y2 = self.get_coordinates(row, column)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=f"cell_{row}_{column}")
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, font=("Arial", 16), fill="white")

    def get_coordinates(self, row, column):
        """Calculate and return the x and y coordinates for a given cell."""
        x1 = column * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        return x1, y1, x2, y2

    def canvas_clicked(self, event):
        row = event.y // self.cell_size
        column = event.x // self.cell_size

        if (row, column) not in self.game_state.get_valid_moves_for_current_player():
            print("Invalid move!")  # You can replace this with a more sophisticated warning if desired.
            return

        if isinstance(self.game_state.get_current_player_obj(), HumanPlayer):
            self.cell_clicked(row, column)
            self.canvas.bind("<Button-1>", self.canvas_remove_cell)
        print(f"Canvas clicked at coordinates ({event.x}, {event.y}).")

    def process_next_move(self):
        if self.game_state.is_move_phase:
            if isinstance(self.game_state.get_current_player_obj(), ComputerPlayer):
                move = self.game_state.get_current_player_obj().choose_move(self.game_state)
                if move:
                    self.cell_clicked(*move)
                else:
                    self.display_winner(self.game_state.current_player)
        else:
            if isinstance(self.game_state.get_current_player_obj(), ComputerPlayer):
                cell_to_remove = self.game_state.get_current_player_obj().choose_token_to_remove(self.game_state)
                if cell_to_remove:
                    self.remove_cell(*cell_to_remove)
                else:
                    self.display_winner(self.game_state.current_player)

    def log_message(self, message):
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.see(tk.END)  # Ensure the latest message is visible

    def clear_invalid_move_message(self):
        """Clears the invalid move message after 3 seconds."""
        self.invalid_move_label.config(text="")

    def display_winner(self, winner):
        if not self.game_over:  # Check if the game is already over
            print(f"Player {winner} wins!")  # Print the winner
            self.canvas.unbind("<Button-1>")  # Unbind the canvas click event to prevent further interactions

            # Log the winner
            self.log_message(f"Player {winner} wins!")

            # Create a new popup window
            win_popup = tk.Toplevel(self.root)
            win_popup.title("Game Over")

            label_text = f"Player {winner} wins!"
            win_label = tk.Label(win_popup, text=label_text, font=("Arial", 24), fg="#000000")
            win_label.pack(pady=20)

            close_button = tk.Button(win_popup, text="Close", command=win_popup.destroy)
            close_button.pack(pady=10)

            # Center the popup window relative to the main game window
            self.center_window(win_popup)

            self.game_over = True  # Set the game_over flag to True

    def canvas_clicked(self, event):
        # Convert the canvas coordinates to row and column
        row = event.y // self.cell_size
        column = event.x // self.cell_size

        # Check if the move is valid
        if (row, column) not in self.game_state.get_valid_moves_for_current_player():
            # Handle invalid move (e.g., show a warning or message on the GUI)
            return

        # If it's the human player's turn, process the clicked move
        if isinstance(self.game_state.get_current_player_obj(), HumanPlayer):
            self.cell_clicked(row, column)
            # After the move, bind the next click event to cell removal
            self.canvas.bind("<Button-1>", self.canvas_remove_cell)

    def cell_clicked(self, row, column):
        self.clear_cell(self.game_state.get_player_position(self.game_state.current_player))
        color = self.playerA_color if self.game_state.current_player == "A" else self.playerB_color
        self.place_pawn(row, column, color, self.game_state.current_player)
        self.game_state.apply_move((row, column))

        if self.game_state.check_win_condition():
            self.display_winner(self.game_state.current_player)
        else:
            self.game_state.switch_phase()
            self.update_turn_labels()

    def canvas_remove_cell(self, event):
        row = event.y // self.cell_size
        column = event.x // self.cell_size

        self.remove_cell(row, column)
        print(f"Canvas cell removal clicked at coordinates ({event.x}, {event.y}).")


    def remove_cell(self, row, column):
        if self.game_state.is_valid_removal(row, column):
            x1, y1, x2, y2 = self.get_coordinates(row, column)
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.removed_cell_color, tags=f"cell_{row}_{column}")

            self.game_state.apply_remove_token((row, column))

            if self.game_state.check_win_condition():
                self.display_winner(self.game_state.current_player)
            else:
                self.game_state.switch_player()

    def center_window(self, window):
        """Center the given window on the screen."""
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    def shake(self):
        """
        Shakes the main window to provide visual feedback for an invalid action.
        """
        x, y = self.root.winfo_x(), self.root.winfo_y()
        delta = 4  # Define how much the window will move
        for _ in range(3):  # Define the number of shakes
            for (dx, dy) in [(delta, 0), (-delta, 0), (-delta, 0), (delta, 0)]:
                self.root.geometry(f"+{x+dx}+{y+dy}")
                self.root.update()

    def clear_cell(self, row, column):
        print(f"Clearing cell at ({row}, {column})")
        """Reset the cell to its default state"""
        x1 = column * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        # Remove the pawn from the cell
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#bdc3c7", tags=f"cell_{row}_{column}")

    def update_turn_labels(self):
        instruction_text = "Choose a move" if self.game_state.is_move_phase else "Remove a token"

        if self.game_state.current_player == "A":
            self.turn_label_A.config(text=f"Player A's Turn", fg="#27ae60")
            self.turn_label_B.config(text="")
            self.invalid_move_label_A.config(text=instruction_text, fg="#2c3e50")
        else:
            self.turn_label_A.config(text="")
            self.turn_label_B.config(text=f"Player B's Turn", fg="#27ae60")
            self.invalid_move_label_B.config(text=instruction_text, fg="#2c3e50")

    def start_game(self):
        playerA_type = self.playerA_selection.get()
        playerB_type = self.playerB_selection.get()

        self.playerA_dropdown.config(state=tk.DISABLED)
        self.playerB_dropdown.config(state=tk.DISABLED)
        self.start_button.config(text="Restart", command=self.restart_game)

        self.initialize_game_state(
            player_A={
                'color': self.playerA_color,
                'player_obj': HumanPlayer() if playerA_type == 'Human' else ComputerPlayer()
            },
            player_B={
                'color': self.playerB_color,
                'player_obj': HumanPlayer() if playerB_type == 'Human' else ComputerPlayer()
            }
        )

        self.draw_board()
        self.update_turn_labels()
        self.canvas.bind("<Button-1>", self.canvas_clicked)

        if isinstance(self.game_state.get_current_player_obj(), ComputerPlayer):
            self.trigger_next_move()

        # Add logic here to handle the case when both players are computers.
        # If you decide to implement a game loop for this scenario, add it here.

    def initialize_game_state(self, player_A=None, player_B=None):
        """Initialize or reset the game state."""
        if not hasattr(self, 'game_state'):
            self.game_state = IsolationGameState()

        # Update the game state properties directly
        self.game_state.current_player = random.choice(["A", "B"])
        if player_A and player_B:
            self.game_state.players["A"].update(player_A)
            self.game_state.players["B"].update(player_B)
        else:
            self.game_state.players = {
                "A": {"row": 0, "column": 3, "player_obj": HumanPlayer()},
                "B": {"row": 7, "column": 2, "player_obj": HumanPlayer()}
            }
        self.game_state.removed_tokens = set()
        self.game_state.is_move_phase = True
        self.game_state.game_over = False

    def restart_game(self):
        """Restart the game and re-enable the dropdowns."""
        print("Restarting game...")
        self.canvas.delete("all")

        # Logging the restart
        self.log_message("Game restarted.")

        # Re-enable the dropdowns
        self.playerA_dropdown.config(state=tk.NORMAL)
        self.playerB_dropdown.config(state=tk.NORMAL)

        # Change the button back to "Start"
        self.start_button.config(text="Start", command=self.start_game)

        # Clear any previous invalid move messages
        self.invalid_move_label_A.config(text="")
        self.invalid_move_label_B.config(text="")

        # Unbind the canvas click event to prevent interactions before starting
        self.canvas.unbind("<Button-1>")

        # Initialize the game state and redraw the board
        self.initialize_game_state()
        self.draw_board()

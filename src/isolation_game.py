import random
import tkinter as tk

class IsolationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Isolation Game")

        # Parameters
        self.rows = 8
        self.columns = 6
        self.cell_size = 50

        # Colors
        self.removed_cell_color = "#323232"

        self.initialize_game_state()
        self.setup_ui_components()
        self.draw_board()
        self.center_window(self.root)

    def initialize_game_state(self):
        """Initialize or reset the game state."""
        self.current_player = random.choice(["A", "B"])
        self.players = {
            "A": {"row": 0, "column": 3, "color": "#3498db", "text": "A"},
            "B": {"row": 7, "column": 2, "color": "#e74c3c", "text": "B"}
        }
        self.removed_tokens = set()
        self.is_move_phase = True
        self.game_over = False  # Add this line to track if the game is over

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

        legends = [
            ("#bdc3c7", "Available Cell"),
            (self.players['A']['color'], "Player A Pawn"),
            (self.players['B']['color'], "Player B Pawn"),
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

    def update_turn_labels(self):
        """Update turn labels based on the current player and phase."""
        instruction_text = "Choose a move" if self.is_move_phase else "Remove a token"
        
        if self.current_player == "A":
            self.turn_label_A.config(text=f"Player A's Turn", fg="#27ae60")  # Setting the color to green
            self.turn_label_B.config(text="")
            self.invalid_move_label_A.config(text=instruction_text, fg="#2c3e50")
        else:
            self.turn_label_A.config(text="")
            self.turn_label_B.config(text=f"Player B's Turn", fg="#27ae60")  # Setting the color to green
            self.invalid_move_label_B.config(text=instruction_text, fg="#2c3e50")

    def get_coordinates(self, row, column):
        """Calculate and return the x and y coordinates for a given cell."""
        x1 = column * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        return x1, y1, x2, y2

    def draw_board(self):
        for row in range(self.rows):
            for column in range(self.columns):
                x1, y1, x2, y2 = self.get_coordinates(row, column)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#bdc3c7", tags=f"cell_{row}_{column}", width=2, outline="#9b9b9b")

        self.place_pawn(self.players['A']['row'], self.players['A']['column'], self.players['A']['color'],
                        self.players['A']['text'])
        self.place_pawn(self.players['B']['row'], self.players['B']['column'], self.players['B']['color'],
                        self.players['B']['text'])

    def place_pawn(self, row, column, color, text):
        x1 = column * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, tags=f"cell_{row}_{column}")
        self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=text, font=("Arial", 16), fill="white")

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

    def switch_phase(self):
        """Switch between move and remove phases."""
        self.is_move_phase = not self.is_move_phase
        self.update_turn_labels()

    def switch_player(self):
        """Switch to the other player and start in the move phase."""
        self.current_player = "A" if self.current_player == "B" else "B"
        print(f"Switched to Player {self.current_player}")  # Print the switched player
        self.is_move_phase = True  # Always start the new player's turn in the move phase
        self.update_turn_labels()
        self.trigger_next_move()

    def canvas_clicked(self, event):
        print(f"Canvas clicked at coordinates: {event.x}, {event.y}")
        column = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.is_move_phase:
            self.cell_clicked(row, column)
        else:
            self.remove_cell(row, column)

    def computer_move(self):
        """Generate and apply a random valid move for the computer."""
        valid_moves = self.get_valid_moves(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
        move = random.choice(valid_moves) if valid_moves else None
        if move:
            self.cell_clicked(*move)

            # After making a move, AI should remove a cell
            if not self.is_move_phase:  # Ensure we're in the remove phase
                valid_remove_cells = [
                    (r, c) for r in range(self.rows) for c in range(self.columns)
                    if (r, c) not in self.removed_tokens and
                    (r, c) != (self.players['A']['row'], self.players['A']['column']) and 
                    (r, c) != (self.players['B']['row'], self.players['B']['column'])
                ]
                remove_cell = random.choice(valid_remove_cells) if valid_remove_cells else None
                if remove_cell:
                    self.remove_cell(*remove_cell)
        else:  # If AI has no valid moves, the other player wins
            other_player = 'B' if self.current_player == 'A' else 'A'
            self.display_winner(other_player)

    def trigger_next_move(self):
        print(f"Triggering next move for Player {self.current_player}. Player type: {self.playerA_selection.get() if self.current_player == 'A' else self.playerB_selection.get()}")  # Debug print statement
        if self.playerA_selection.get() == "Computer" and self.current_player == "A":
            print("Scheduling computer move for Player A")  # Debug print statement
            self.root.after(500, self.computer_move)
        elif self.playerB_selection.get() == "Computer" and self.current_player == "B":
            print("Scheduling computer move for Player B")  # Debug print statement
            self.root.after(500, self.computer_move)
        # If both players are computers, continue the game without waiting
        elif self.playerA_selection.get() == "Computer" and self.playerB_selection.get() == "Computer":
            print("Both players are computers. Continuing the game.")  # Debug print statement
            self.root.after(500, self.computer_move)


    def log_message(self, message):
        self.log_display.insert(tk.END, message + "\n")
        self.log_display.see(tk.END)  # Ensure the latest message is visible

    def cell_clicked(self, row, column):
        valid_moves = self.get_valid_moves(self.players[self.current_player]['row'], self.players[self.current_player]['column'])

        if (row, column) in valid_moves:
            self.clear_cell(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
            self.place_pawn(row, column, self.players[self.current_player]['color'], self.players[self.current_player]['text'])
            self.players[self.current_player]['row'] = row
            self.players[self.current_player]['column'] = column
            self.switch_phase()

            # Log the move
            self.log_message(f"Player {self.current_player} moved to ({row}, {column})")
        else:
            self.display_invalid_message("Invalid Move! Try again.")
            self.shake()

    def remove_cell(self, row, column):
        print(f"Starting remove_cell for {row}, {column}")
        if (row, column) not in self.removed_tokens:
            if (row, column) != (self.players['A']['row'], self.players['A']['column']) and \
            (row, column) != (self.players['B']['row'], self.players['B']['column']):
                self.clear_cell(row, column)
                x1, y1, x2, y2 = self.get_coordinates(row, column)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.removed_cell_color, tags=f"cell_{row}_{column}")
                self.removed_tokens.add((row, column))

                # Log the cell removal
                self.log_message(f"Player {self.current_player} removed cell at ({row}, {column})")

                # Switch to the other player
                previous_player = self.current_player  # Remember the player who just finished their turn
                self.switch_player()

                # Check for win condition after switching the player and removing the cell
                valid_moves_for_new_current_player = self.get_valid_moves(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
                if not valid_moves_for_new_current_player:
                    print(f"Player {self.current_player} has no valid moves!")
                    self.display_winner(previous_player)
                else:
                    print(f"Player {self.current_player} has valid moves!")

            else:
                self.display_invalid_message("Cannot remove a cell occupied by a player!")
                self.shake()
        else:
            self.display_invalid_message("Invalid Removal! Try another cell.")
            self.shake()

    def get_valid_moves(self, row, column):
        """Get valid moves for the pawn at the given position."""
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        valid_moves = []
        for dr, dc in directions:
            new_row, new_column = row + dr, column + dc
            if (0 <= new_row < 8 and 
                0 <= new_column < 6 and 
                (new_row, new_column) not in self.removed_tokens and
                (new_row, new_column) != (self.players['A']['row'], self.players['A']['column']) and 
                (new_row, new_column) != (self.players['B']['row'], self.players['B']['column'])):
                    valid_moves.append((new_row, new_column))
        return valid_moves

    def check_win_condition(self):
        """Check if the current player has won the game."""
        # Get the opposing player
        opposing_player = "A" if self.current_player == "B" else "B"

        # Get valid moves for the opposing player
        valid_moves = self.get_valid_moves(self.players[opposing_player]['row'], self.players[opposing_player]['column'])
        print(f"Valid moves for player {opposing_player}: {valid_moves}")  # Debug print statement

        # If the opposing player has no valid moves, the current player wins
        if not valid_moves:
            self.display_winner(self.current_player)
            return True
        return False

    def display_invalid_message(self, message):
        """Display the invalid action message on the respective side of the players."""
        if self.current_player == "A":
            self.invalid_move_label_A.config(text=message, fg="#c0392b")
            self.root.after(3000, self.update_turn_labels)  # Clear the message after 3 seconds and revert to instruction
        else:
            self.invalid_move_label_B.config(text=message, fg="#c0392b")
            self.root.after(3000, self.update_turn_labels)  # Clear the message after 3 seconds and revert to instruction

    def display_winner(self, winner):
        if not self.game_over:  # Check if the game is already over
            print(f"Player {winner} wins!")  # Print the winner
            self.canvas.unbind("<Button-1>")  # Unbind the canvas click event to prevent further interactions
            
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

    def clear_invalid_move_message(self):
        """Clears the invalid move message after 3 seconds."""
        self.invalid_move_label.config(text="")

    def start_game(self):
        """Start or restart the game based on dropdown selections."""
        # Lock the dropdowns to prevent changes during gameplay
        self.playerA_dropdown.config(state=tk.DISABLED)
        self.playerB_dropdown.config(state=tk.DISABLED)

        # Change the "Start" button to "Restart"
        self.start_button.config(text="Restart", command=self.restart_game)

        # Initialize the game based on the dropdown selections
        self.initialize_game_state()
        self.draw_board()
        self.update_turn_labels()
        self.canvas.bind("<Button-1>", self.canvas_clicked)

        # If both players are computers, start the game automatically
        if self.playerA_selection.get() == "Computer" and self.playerB_selection.get() == "Computer":
            self.trigger_next_move()

    def restart_game(self):
        """Restart the game and re-enable the dropdowns."""
        print("Restarting game...")
        self.canvas.delete("all")

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

def run_game():
    root = tk.Tk()
    game = IsolationGame(root)
    root.mainloop()

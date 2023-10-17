from random import choice
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

    def initialize_game_state(self):
        """Initialize or reset the game state."""
        self.current_player = choice(["A", "B"])
        self.players = {
            "A": {"row": 0, "column": 3, "color": "#3498db", "text": "A"},
            "B": {"row": 7, "column": 2, "color": "#e74c3c", "text": "B"}
        }
        self.removed_tokens = set()
        self.is_move_phase = True

    def setup_ui_components(self):
        """Set up the UI components."""

        # Player A's Frame (at the top)
        self.frame_A = tk.Frame(self.root)
        self.frame_A.pack(fill=tk.BOTH)

        # Player A's turn label
        self.turn_label_A = tk.Label(self.frame_A, text="", font=("Arial", 16))
        self.turn_label_A.pack()

        # Invalid move message for Player A
        self.invalid_move_label_A = tk.Label(self.frame_A, text="", font=("Arial", 10), fg="#c0392b")
        self.invalid_move_label_A.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=self.cell_size * self.columns, height=self.cell_size * self.rows)
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.canvas_clicked)

        # Player B's Frame (at the bottom)
        self.frame_B = tk.Frame(self.root)
        self.frame_B.pack(fill=tk.BOTH, side=tk.BOTTOM)

        # Player B's turn label
        self.turn_label_B = tk.Label(self.frame_B, text="", font=("Arial", 16))
        self.turn_label_B.pack(side=tk.BOTTOM)

        # Invalid move message for Player B
        self.invalid_move_label_B = tk.Label(self.frame_B, text="", font=("Arial", 10), fg="#c0392b")
        self.invalid_move_label_B.pack(side=tk.BOTTOM, pady=5)

        self.update_turn_labels()

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.restart_button.pack(pady=20)

    def update_turn_labels(self):
        """Update turn labels based on the current player and phase."""
        instruction_text = "Choose a move" if self.is_move_phase else "Remove a token"
        
        if self.current_player == "A":
            self.turn_label_A.config(text=f"Player A's Turn")
            self.turn_label_B.config(text="")
            self.invalid_move_label_A.config(text=instruction_text, fg="#2c3e50")
        else:
            self.turn_label_A.config(text="")
            self.turn_label_B.config(text=f"Player B's Turn")
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
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#bdc3c7", tags=f"cell_{row}_{column}")

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
        self.is_move_phase = True  # Always start the new player's turn in the move phase
        self.update_turn_labels()

    def canvas_clicked(self, event):
        print(f"Canvas clicked at coordinates: {event.x}, {event.y}")
        column = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.is_move_phase:
            self.cell_clicked(row, column)
        else:
            self.remove_cell(row, column)

    def cell_clicked(self, row, column):
        valid_moves = self.get_valid_moves(self.players[self.current_player]['row'], self.players[self.current_player]['column'])

        if (row, column) in valid_moves:
            self.clear_cell(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
            self.place_pawn(row, column, self.players[self.current_player]['color'], self.players[self.current_player]['text'])
            self.players[self.current_player]['row'] = row
            self.players[self.current_player]['column'] = column
            self.switch_phase()
            
            # Check if the current player has any valid moves left after their move phase
            valid_moves_after_move = self.get_valid_moves(row, column)
            if not valid_moves_after_move:
                self.display_winner(self.current_player)
        else:
            self.display_invalid_message("Invalid Move! Try again.")
            self.shake()

    def remove_cell(self, row, column):
        if (row, column) not in self.removed_tokens:
            if (row, column) != (self.players['A']['row'], self.players['A']['column']) and \
            (row, column) != (self.players['B']['row'], self.players['B']['column']):
                self.clear_cell(row, column)
                x1, y1, x2, y2 = self.get_coordinates(row, column)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.removed_cell_color, tags=f"cell_{row}_{column}")
                self.removed_tokens.add((row, column))
                self.switch_player()

                # Check for win condition after switching the player and removing the cell
                valid_moves_for_opposing_player = self.get_valid_moves(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
                if not valid_moves_for_opposing_player:
                    self.display_winner(self.current_player)

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
        """Display the winner and disable further interactions."""
        if winner == "A":
            self.turn_label_A.config(text=f"Player A wins!")
            self.invalid_move_label_A.config(text="")
        else:
            self.turn_label_B.config(text=f"Player B wins!")
            self.invalid_move_label_B.config(text="")
        self.canvas.unbind("<Button-1>")  # Unbind the canvas click event to prevent further interactions

    def clear_invalid_move_message(self):
        """Clears the invalid move message after 3 seconds."""
        self.invalid_move_label.config(text="")

    def restart_game(self):
        print("Restarting game...")
        self.canvas.delete("all")
        self.initialize_game_state()
        self.draw_board()
        self.update_turn_labels()
        self.invalid_move_label_A.config(text="")
        self.invalid_move_label_B.config(text="")
        self.canvas.bind("<Button-1>", self.canvas_clicked)


def run_game():
    root = tk.Tk()
    game = IsolationGame(root)
    root.mainloop()

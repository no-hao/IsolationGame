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

        # Initialize game state
        self.current_player = "A"
        self.players = {
            "A": {"row": 0, "column": 3, "color": "#3498db", "text": "A"},
            "B": {"row": 7, "column": 2, "color": "#e74c3c", "text": "B"}
        }
        self.removed_tokens = set()
        self.is_move_phase = True

        # UI Components
        self.turn_label = tk.Label(self.root, text=f"Player {self.current_player}'s Turn to Move", font=("Arial", 16))
        self.turn_label.pack()

        self.invalid_move_label = tk.Label(self.root, text="", font=("Arial", 10), fg="#c0392b")
        self.invalid_move_label.pack(pady=5)

        self.canvas = tk.Canvas(self.root, width=self.cell_size*self.columns, height=self.cell_size*self.rows)
        self.canvas.pack(pady=20)
        self.canvas.bind("<Button-1>", self.canvas_clicked)

        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.restart_button.pack(pady=20)

        self.draw_board()

    def draw_board(self):
        print("Drawing the board...")
        for row in range(self.rows):
            for column in range(self.columns):
                x1 = column * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="#bdc3c7", tags=f"cell_{row}_{column}")

        self.place_pawn(self.players['A']['row'], self.players['A']['column'], self.players['A']['color'], self.players['A']['text'])
        self.place_pawn(self.players['B']['row'], self.players['B']['column'], self.players['B']['color'], self.players['B']['text'])

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
        print(f"Switching phase. Is move phase? {not self.is_move_phase}")
        if self.is_move_phase:
            self.is_move_phase = False
            self.turn_label.config(text=f"Player {self.current_player}'s Turn to Remove a Cell")
        else:
            self.switch_player()
            self.is_move_phase = True
            self.turn_label.config(text=f"Player {self.current_player}'s Turn to Move")

    def canvas_clicked(self, event):
        print(f"Canvas clicked at coordinates: {event.x}, {event.y}")
        column = event.x // self.cell_size
        row = event.y // self.cell_size

        if self.is_move_phase:
            self.cell_clicked(row, column)
        else:
            self.remove_cell(row, column)

    def cell_clicked(self, row, column):
        print(f"Cell clicked at ({row}, {column}) during move phase")
        valid_moves = self.get_valid_moves(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
        if (row, column) in valid_moves:
            self.clear_cell(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
            self.place_pawn(row, column, self.players[self.current_player]['color'], self.players[self.current_player]['text'])
            # Update the player's position
            self.players[self.current_player]['row'] = row
            self.players[self.current_player]['column'] = column
            self.switch_phase()
        else:
            self.invalid_move_label.config(text="Invalid Move! Try again.")
            self.shake()

    def remove_cell(self, row, column):
        print(f"Removing cell at ({row}, {column})")
        if (row, column) not in self.removed_tokens:
            if (row, column) != (self.players['A']['row'], self.players['A']['column']) and \
               (row, column) != (self.players['B']['row'], self.players['B']['column']):
                self.clear_cell(row, column)
                x1 = column * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=self.removed_cell_color, tags=f"cell_{row}_{column}")
                self.removed_tokens.add((row, column))
                self.switch_phase()
            else:
                self.invalid_move_label.config(text="Cannot remove a cell occupied by a player!")
                self.shake()
        else:
            self.invalid_move_label.config(text="Cell already has its token removed!")
            self.shake()

    def get_valid_moves(self, row, column):
        print(f"Getting valid moves for pawn at ({row}, {column})")
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        valid_moves = []
        for dr, dc in directions:
            new_row, new_column = row + dr, column + dc
            if (0 <= new_row < self.rows and 
                0 <= new_column < self.columns and 
                (new_row, new_column) not in self.removed_tokens and
                (new_row, new_column) != (self.players['A']['row'], self.players['A']['column']) and 
                (new_row, new_column) != (self.players['B']['row'], self.players['B']['column'])):
                    valid_moves.append((new_row, new_column))
        return valid_moves

    def switch_player(self):
        print(f"Switching player. Current player: {self.current_player}")
        self.current_player = "A" if self.current_player == "B" else "B"

    def restart_game(self):
        print("Restarting game...")
        # Clear the canvas and redraw the board
        self.canvas.delete("all")
        self.draw_board()
        self.current_player = "A"
        self.is_move_phase = True
        self.turn_label.config(text=f"Player {self.current_player}'s Turn to Move")
        self.invalid_move_label.config(text="")

def run_game():
    root = tk.Tk()
    game = IsolationGame(root)
    root.mainloop()

import tkinter as tk
from random import choice

class IsolationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Isolation Game")
        
        # Parameters
        self.rows = 8
        self.columns = 6
        self.cell_size = 50
        
        # Initialize game state
        self.current_player = "A"
        self.players = {
            "A": {"row": 0, "column": 3, "color": "#3498db", "text": "A"},
            "B": {"row": 7, "column": 2, "color": "#e74c3c", "text": "B"}
        }
        self.visited_cells = set()
        
        # UI Components
        self.turn_label = tk.Label(self.root, text=f"Player {self.current_player}'s Turn", font=("Arial", 16))
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
        self.visited_cells.add((row, column))

    def clear_cell(self, row, column):
        """Reset the cell to its default state"""
        x1 = column * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size
        # Remove the pawn from the cell
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#bdc3c7", tags=f"cell_{row}_{column}")

    def canvas_clicked(self, event):
        column = event.x // self.cell_size
        row = event.y // self.cell_size
        self.cell_clicked(row, column)

    def cell_clicked(self, row, column):
        print(f"Cell clicked: ({row}, {column})")
        print(f"Current player's position: ({self.players[self.current_player]['row']}, {self.players[self.current_player]['column']})")
        
        # If clicked cell is the same as the current cell of the player, return
        if (row, column) == (self.players[self.current_player]['row'], self.players[self.current_player]['column']):
            print("Clicked on the same cell as the current pawn. Exiting early.")
            return

        valid_moves = self.get_valid_moves(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
        print(f"Valid moves for current player: {valid_moves}")
        if (row, column) not in valid_moves:
            print("Invalid move attempted. Exiting.")
            self.invalid_move_label.config(text="Invalid Move! Try again.")
            return
        
        print("Clearing current cell of the player...")
        self.clear_cell(self.players[self.current_player]['row'], self.players[self.current_player]['column'])
        
        print("Moving the pawn and updating the visited cells...")
        self.place_pawn(row, column, self.players[self.current_player]['color'], self.players[self.current_player]['text'])
        
        # Update the player's position
        self.players[self.current_player]['row'] = row
        self.players[self.current_player]['column'] = column
        
        self.switch_player()
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")

    def get_valid_moves(self, row, column):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        valid_moves = []
        for dr, dc in directions:
            new_row, new_column = row + dr, column + dc
            if (0 <= new_row < self.rows and 
                0 <= new_column < self.columns and 
                (new_row, new_column) != (self.players['A']['row'], self.players['A']['column']) and 
                (new_row, new_column) != (self.players['B']['row'], self.players['B']['column'])):
                    valid_moves.append((new_row, new_column))
        return valid_moves

    def switch_player(self):
        self.current_player = "A" if self.current_player == "B" else "B"

    def restart_game(self):
        # Clear the canvas and redraw the board
        self.canvas.delete("all")
        self.draw_board()
        self.visited_cells.clear()
        self.current_player = "A"
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")
        self.invalid_move_label.config(text="")

def run_game():
    root = tk.Tk()
    game = IsolationGame(root)
    root.mainloop()

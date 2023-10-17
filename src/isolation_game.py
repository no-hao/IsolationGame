import tkinter as tk
from random import choice

class IsolationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Isolation Game")
        
        # Parameters
        self.rows = 8
        self.columns = 6
        
        # Initialize game state
        self.current_player = "A"
        self.players = {
            "A": {"row": 0, "column": 3, "color": "#3498db", "text": "A"},
            "B": {"row": 7, "column": 2, "color": "#e74c3c", "text": "B"}
        }
        
        # Create the game interface
        self.turn_label = tk.Label(self.root, text=f"Player {self.current_player}'s Turn", font=("Arial", 16))
        self.turn_label.pack()
        
        self.invalid_move_label = tk.Label(self.root, text="", font=("Arial", 10), fg="#c0392b")
        self.invalid_move_label.pack(pady=5)
        
        self.board_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.board_frame.pack(pady=20)
        
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.restart_button.pack(pady=20)
        
        # Draw the board and place the initial pawns
        self.draw_board()

    def draw_board(self):
        self.buttons = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        for row in range(self.rows):
            for column in range(self.columns):
                btn = tk.Button(self.board_frame, text="", width=2, height=1, bg="#ecf0f1",
                                command=lambda r=row, c=column: self.cell_clicked(r, c))
                btn.grid(row=row, column=column, sticky="nsew")
                self.buttons[row][column] = btn
        
        self.place_pawn(self.players['A']['row'], self.players['A']['column'], self.players['A']['color'], self.players['A']['text'])
        self.place_pawn(self.players['B']['row'], self.players['B']['column'], self.players['B']['color'], self.players['B']['text'])

    def place_pawn(self, row, column, color, text):
        self.buttons[row][column].config(bg=color, text=text, fg="white", state=tk.DISABLED)

    def cell_clicked(self, row, column):
        self.invalid_move_label.config(text="")
        
        valid_moves = self.get_valid_moves()
        if (row, column) not in valid_moves:
            self.invalid_move_label.config(text="Invalid Move! Try again.")
            return

        # Move the pawn and mark the previous position as visited
        old_row, old_column = self.players[self.current_player]['row'], self.players[self.current_player]['column']
        self.buttons[old_row][old_column].config(bg="#ecf0f1", text="", state=tk.NORMAL)
        
        self.players[self.current_player]['row'], self.players[self.current_player]['column'] = row, column
        self.place_pawn(row, column, self.players[self.current_player]['color'], self.players[self.current_player]['text'])

        # Switch to the next player
        self.switch_player()
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")

    def get_valid_moves(self):
        row, column = self.players[self.current_player]['row'], self.players[self.current_player]['column']
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        valid_moves = []
        for dr, dc in directions:
            new_row, new_column = row + dr, column + dc
            if 0 <= new_row < self.rows and 0 <= new_column < self.columns and \
               self.buttons[new_row][new_column]['bg'] not in [self.players['A']['color'], self.players['B']['color'], "#95a5a6"]:
                valid_moves.append((new_row, new_column))
        
        return valid_moves

    def switch_player(self):
        self.current_player = "A" if self.current_player == "B" else "B"

    def restart_game(self):
        for btn_row in self.buttons:
            for btn in btn_row:
                btn.config(bg="#ecf0f1", text="", state=tk.NORMAL)
        self.current_player = "A"
        self.players["A"] = {"row": 0, "column": 3, "color": "#3498db", "text": "A"}
        self.players["B"] = {"row": 7, "column": 2, "color": "#e74c3c", "text": "B"}
        self.place_pawn(self.players['A']['row'], self.players['A']['column'], self.players['A']['color'], self.players['A']['text'])
        self.place_pawn(self.players['B']['row'], self.players['B']['column'], self.players['B']['color'], self.players['B']['text'])
        self.invalid_move_label.config(text="")
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")

def run_game():
    root = tk.Tk()
    game = IsolationGame(root)
    root.mainloop()

import tkinter as tk
from tkinter import messagebox

class IsolationGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Improved Isolation Game")
        
        # Parameters
        self.rows = 8
        self.columns = 6
        
        # Initialize game state
        self.current_player = "A"
        self.players = {
            "A": {"row": 0, "column": 3, "color": "blue", "text": "A"},
            "B": {"row": 7, "column": 2, "color": "red", "text": "B"}
        }
        
        # Create GUI
        self.canvas = tk.Canvas(self.root, bg="white", height=400, width=300)
        self.canvas.pack(pady=20)
        
        self.turn_label = tk.Label(self.root, text=f"Player {self.current_player}'s Turn", font=("Arial", 16))
        self.turn_label.pack()
        
        self.restart_button = tk.Button(self.root, text="Restart", command=self.restart_game)
        self.restart_button.pack(pady=20)
        
        self.draw_board()
    
    def draw_board(self):
        self.buttons = [[None for _ in range(self.columns)] for _ in range(self.rows)]
        for row in range(self.rows):
            for column in range(self.columns):
                btn = tk.Button(self.canvas, text="", width=2, height=1, bg="white",
                                command=lambda r=row, c=column: self.cell_clicked(r, c))
                btn.grid(row=row, column=column, sticky="nsew")
                self.buttons[row][column] = btn
        
        # Place initial pawns
        self.place_pawn(self.players['A']['row'], self.players['A']['column'], self.players['A']['color'], self.players['A']['text'])
        self.place_pawn(self.players['B']['row'], self.players['B']['column'], self.players['B']['color'], self.players['B']['text'])
    
    def place_pawn(self, row, column, color, text):
        self.buttons[row][column].config(bg=color, text=text)
    
    def cell_clicked(self, row, column):
        # Ensure move is valid
        valid_moves = self.get_valid_moves()
        if (row, column) not in valid_moves:
            messagebox.showerror("Invalid Move", "You can't move there!")
            return

        # Move player pawn
        old_row, old_column = self.players[self.current_player]['row'], self.players[self.current_player]['column']
        self.players[self.current_player]['row'], self.players[self.current_player]['column'] = row, column

        # Update the buttons
        self.buttons[old_row][old_column].config(bg="white", text="")
        self.place_pawn(row, column, self.players[self.current_player]['color'], self.players[self.current_player]['text'])

        # Check if the game is over
        if self.is_game_over():
            messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
            self.restart_game()
            return

        # Switch to the other player
        self.switch_player()
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")
    
    def get_valid_moves(self):
        row, column = self.players[self.current_player]['row'], self.players[self.current_player]['column']
        
        # All possible directions including diagonals
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        valid_moves = []
        for dr, dc in directions:
            new_row, new_column = row + dr, column + dc
            if 0 <= new_row < self.rows and 0 <= new_column < self.columns and \
               self.buttons[new_row][new_column]['bg'] not in [self.players['A']['color'], self.players['B']['color']]:
                valid_moves.append((new_row, new_column))
        
        return valid_moves
    
    def switch_player(self):
        self.current_player = "A" if self.current_player == "B" else "B"
    
    def is_game_over(self):
        return len(self.get_valid_moves()) == 0
    
    def restart_game(self):
        for btn_row in self.buttons:
            for btn in btn_row:
                btn.config(bg="white")
        self.current_player = "A"
        self.players["A"] = {"row": 0, "column": 3, "color": "blue"}
        self.players["B"] = {"row": 7, "column": 2, "color": "red"}
        self.place_pawn(self.players['A']['row'], self.players['A']['column'], self.players['A']['color'])
        self.place_pawn(self.players['B']['row'], self.players['B']['column'], self.players['B']['color'])
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")

def run_game():
    root = tk.Tk()
    game = IsolationGame(root)
    root.mainloop()

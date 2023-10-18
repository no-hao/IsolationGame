import random

class IsolationGameState:
    def __init__(self, player_A=None, player_B=None):
        # Parameters
        self.rows = 8
        self.columns = 6
        
        # Initialize or reset the game state
        self.current_player = random.choice(["A", "B"])
        
        # Check if specific player information is provided, otherwise use default values
        if player_A and player_B:
            self.players = {
                "A": player_A,
                "B": player_B
            }
        else:
            self.players = {
                "A": {"row": 0, "column": 3},
                "B": {"row": 7, "column": 2}
            }
        
        self.removed_tokens = set()
        self.is_move_phase = True
        self.game_over = False
        print("End of __init__ in IsolationGameState:", self.players)

    def get_player_position(self, player):
        return (self.players[player]['row'], self.players[player]['column'])

    def get_valid_moves_for_current_player(self):
        row, column = self.get_player_position(self.current_player)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        valid_moves = []
        for dr, dc in directions:
            new_row, new_column = row + dr, column + dc
            if (0 <= new_row < 8 and 
                0 <= new_column < 6 and 
                (new_row, new_column) not in self.removed_tokens and
                (new_row, new_column) != self.get_player_position("A") and 
                (new_row, new_column) != self.get_player_position("B")):
                    valid_moves.append((new_row, new_column))
        return valid_moves

    def apply_move(self, move):
        row, column = move
        self.players[self.current_player]['row'] = row
        self.players[self.current_player]['column'] = column

    def apply_cell_removal(self, cell):
        self.removed_tokens.add(cell)

    def switch_phase(self):
        self.is_move_phase = not self.is_move_phase

    def switch_player(self):
        self.current_player = "A" if self.current_player == "B" else "B"
        self.is_move_phase = True

    def check_win_condition(self):
        valid_moves = self.get_valid_moves_for_current_player()
        return not valid_moves

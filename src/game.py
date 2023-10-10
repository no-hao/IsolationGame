import random
from .board import Board


class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]

        # Always assign Player 1 to (0, 3) and Player 2 to (7, 2)
        self.players[0].position = (0, 3)
        self.players[1].position = (7, 2)

        # Randomize which player starts the game
        if random.choice([True, False]):
            self.current_player = self.players[0]
            self.next_player = self.players[1]
        else:
            self.current_player = self.players[1]
            self.next_player = self.players[0]

    def switch_players(self):
        """Switches the turn to the other player."""
        self.current_player, self.next_player = self.next_player, self.current_player

    def is_game_over(self):
            """Checks if the game is over."""
            row, col = self.next_player.position
            # Check all possible moves (up, down, left, right, and diagonally)
            possible_moves = [
                (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                (row, col - 1),                     (row, col + 1),
                (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
            ]
            for move in possible_moves:
                if self.next_player._is_valid_move(*move, self.board):
                    return False  # A valid move exists for the next player
            return True  # No valid moves left

    def play(self):
        print("Starting the game of Isolation!")
        while not self.is_game_over():
            print(self.board.display())
            print(f"{self.current_player.name}'s turn:")
            
            # Make the player move with error handling
            try:
                self.current_player.move(self.board)
                self.current_player.remove_token(self.board)
            except Exception as e:
                print(f"Error: {e}")
                continue
            
            # Switch to the other player
            self.switch_players()

        print("Game over!")
        self.switch_players()  # Switch back to the player who won
        print(f"{self.current_player.name} wins!")

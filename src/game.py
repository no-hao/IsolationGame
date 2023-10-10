import random
from .board import Board


class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]

        # List of starting positions
        starting_positions = [(0, 3), (7, 2)]
        random.shuffle(starting_positions)

        # Assign starting positions to players
        self.players[0].position = starting_positions[0]
        self.players[1].position = starting_positions[1]

        # First player to play is the one at position (0,3)
        if self.players[0].position == (0, 3):
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
        # TODO: Implement the logic to check if the current player has no valid moves left.
        return False

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

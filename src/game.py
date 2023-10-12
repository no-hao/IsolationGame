import random
from .board import Board, CellState
from .player import ComputerPlayer

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.players = [player1, player2]

        # Randomly decide which player starts the game
        starting_player = random.choice(self.players)
        other_player = self.players[1] if starting_player == self.players[0] else self.players[0]

        # Set initial positions and update the board
        self._set_initial_positions_and_board(starting_player, other_player)

        self.current_player = starting_player
        self.next_player = other_player

        # Add both players as observers to the board
        self.board.add_observer(player1)
        self.board.add_observer(player2)

    def other_player(self):
        return self.players[1] if self.current_player == self.players[0] else self.players[0]

    def switch_players(self):
        """Switches the turn to the other player."""
        self.current_player, self.next_player = self.next_player, self.current_player

    def _set_initial_positions_and_board(self, starting_player, other_player):
        """Set initial positions for players and update the board based on the starting player."""
        starting_positions = {(0, 3): CellState.PLAYER_1, (7, 2): CellState.PLAYER_2}
        if starting_player == self.players[1]:
            starting_positions = {(0, 3): CellState.PLAYER_2, (7, 2): CellState.PLAYER_1}

        for position, state in starting_positions.items():
            row, col = position
            self.board.set_cell_state(row, col, state)

        if starting_player:
            starting_player.position = (0, 3)
        if other_player:
            other_player.position = (7, 2)


    def apply_move(self, player, move):
        """Applies the player's move on the board, assumes valid move is given."""
        if move is None:
            raise ValueError("Invalid move provided. No move received from the player.")
        
        row, col = move
        # Check if the provided move is a valid cell within the board
        if not Board.is_within_board(row, col):
            raise ValueError(f"Invalid move. Position ({row}, {col}) is out of board boundaries.")
        
        # Update player's current position to EMPTY
        curr_row, curr_col = player.position
        self.board.set_cell_state(curr_row, curr_col, CellState.EMPTY)
        
        # Set the new position to the player's state
        self.board.set_cell_state(row, col, CellState.PLAYER_1 if player == self.players[0] else CellState.PLAYER_2)
        
        # Update the player's position attribute to the new position
        player.position = (row, col)


    def apply_remove_token(self, player, position):
        """Removes a token from the board, assumes valid remove is given."""
        if position is None:
            raise ValueError("Invalid token removal position provided. No position received from the player.")

        row, col = position
        # Check if the provided position is a valid cell within the board
        if not Board.is_within_board(row, col):
            raise ValueError(f"Invalid token removal position. Position ({row}, {col}) is out of board boundaries.")

        if self.board.get_cell_state(row, col) == CellState.EMPTY:
            self.board.set_cell_state(row, col, CellState.REMOVED)
        else:
            raise ValueError("Invalid token removal position. The cell is not empty.")

    def is_game_over(self):
        """Checks if the game is over."""
        row, col = self.current_player.position
        # Check all possible moves (up, down, left, right, and diagonally)
        moves = Board.get_possible_moves(row, col)
        for move in moves:
            if self.current_player._is_valid_move(*move, self.board):
                return False  # A valid move exists for the current player
        return True  # No valid moves left for the current player

    def play(self):
        print("Starting the game of Isolation!")
        while not self.is_game_over():
            print(self.board.display())
            print(f"{str(self.current_player)}'s turn:")

            # Make the player move with error handling
            try:
                move = self.current_player.move(self.board)
                self.apply_move(self.current_player, move)

                # If it's the computer player's turn:
                if type(self.current_player).__name__ == "ComputerPlayer":
                    token_removal = self.current_player.remove_token(self.board)
                else:
                    # If it's a human player's turn, ask for token removal input
                    token_removal = self.current_player.remove_token(self.board)

                self.apply_remove_token(self.current_player, token_removal)

            except Exception as e:
                print(f"Error: {e}")
                continue

            # Switch to the other player
            self.switch_players()

        print("Game over!")
        print(self.board.display())  # Display the final board state
        print(f"{str(self.next_player)} wins!")
        # The current player is the one who lost. The next_player is the winner.

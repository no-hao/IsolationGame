import time
import copy
import logging
from .player import ComputerPlayer
logger = logging.getLogger("IsolationGameLogger")


class Isolation:
    """Represents the Isolation game state.

    Attributes:
        board (list[list[int]]): The game board.
        players (list[Player]): The list of players.
        current_player_index (int): Index of the current player.
        start_time (float): The start time of the game.
        player_positions (dict): Current positions of the players.
        awaiting_token_removal (bool): If True, the game is waiting for a token removal action.
        tokens_removed_by_player (dict): Count of tokens removed by each player.
        moves_by_player (dict): Count of moves made by each player.
    """
    def __init__(self, player1, player2):
        """Initializes the game board and players."""
        self.board = [[0 for _ in range(6)] for _ in range(8)]  # 0 represents available cell
        self.players = [player1, player2]
        self.current_player_index = 0
        self.start_time = None

        # Initial positions for the players
        self.player_positions = {
            self.players[0]: (0, 3),
            self.players[1]: (7, 2)
        }

        self.update_board_with_players()
        self.awaiting_token_removal = False

        # Initialize the count of tokens removed by each player
        self.tokens_removed_by_player = {player1: 0, player2: 0}
        self.moves_by_player = {self.players[0]: 0, self.players[1]: 0}

    def get_cell_value(self, row, col):
        """Returns the value of a cell at the given row and column."""
        return self.board[row][col]

    def set_cell_value(self, row, col, value):
        """Sets the value of a cell at the given row and column."""
        self.board[row][col] = value

    def get_player_position(self, player):
        """Returns the current position of the given player."""
        # print("Player positions keys:", self.player_positions.keys())  # Debugging statement
        return self.player_positions[player]

    def get_available_moves(self, player):
        """Return a list of available moves for the given player."""
        current_row, current_col = self.get_player_position(player)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        valid_moves = [(current_row + dr, current_col + dc) for dr, dc in directions if self.is_valid_move(player, current_row + dr, current_col + dc)]
        return valid_moves

    def get_available_tokens_to_remove(self):
        """Return a list of available tokens to remove from the board."""
        available_tokens = [(i, j) for i in range(8) for j in range(6) if self.is_valid_token_removal(i, j)]
        return available_tokens

    def update_board_with_players(self):
        """Updates the board with the current positions of the players."""
        for player, position in self.player_positions.items():
            row, col = position
            self.set_cell_value(row, col, player)

    def is_valid_move(self, player, row, col):
        """Checks if a move is valid for the given player to the specified row and column."""
        # Check if move is within board boundaries
        if not (0 <= row < 8 and 0 <= col < 6):
            return False

        # Check if the cell is empty and not occupied by the other player or a removed token
        if self.get_cell_value(row, col) != 0:
            return False

        # Check if the move is adjacent to the player's current position
        current_row, current_col = self.get_player_position(player)
        if abs(current_row - row) > 1 or abs(current_col - col) > 1:
            return False

        return True

    def mock_move(self, player, move):
        """Creates a mock game state after making a move without altering the actual game state."""
        mock_game = copy.deepcopy(self)

        # Ensure the copied game state refers to the same player objects as the original game state
        mock_game.players[0] = self.players[0]
        mock_game.players[1] = self.players[1]
        mock_game.player_positions[self.players[0]] = self.player_positions[self.players[0]]
        mock_game.player_positions[self.players[1]] = self.player_positions[self.players[1]]

        mock_game.moves_by_player[self.players[0]] = self.moves_by_player[self.players[0]]
        mock_game.moves_by_player[self.players[1]] = self.moves_by_player[self.players[1]]

        mock_game.make_move(player, *move)
        
        # Log the heuristic value for the move chosen
        if isinstance(player, ComputerPlayer):
            heuristic_value = player.heuristic(mock_game, player)
            # logging for checking evaluations of minimax
            # logger.info(f"evaluated Move: {move} with Heuristic Value: {heuristic_value}")

        return mock_game

    def mock_remove_token(self, row, col):
        """Simulate removing a token without affecting the actual game state."""
        if not self.is_valid_token_removal(row, col):
            return None

        mock_game = copy.deepcopy(self)

        # Ensure the copied game state refers to the same player objects as the original game state
        mock_game.players[0] = self.players[0]
        mock_game.players[1] = self.players[1]
        mock_game.player_positions[self.players[0]] = self.player_positions[self.players[0]]
        mock_game.player_positions[self.players[1]] = self.player_positions[self.players[1]]
        
        mock_game.moves_by_player[self.players[0]] = self.moves_by_player[self.players[0]]
        mock_game.moves_by_player[self.players[1]] = self.moves_by_player[self.players[1]]

        # Explicitly maintain other attributes
        mock_game.awaiting_token_removal = self.awaiting_token_removal
        mock_game.tokens_removed_by_player = self.tokens_removed_by_player.copy()

        mock_game.board[row][col] = -1  # Represent a removed token with -1
        
        return mock_game

    def make_move(self, player, row, col):
        """Makes a move for the given player to the specified row and column."""
        if self.is_valid_move(player, row, col):
            old_row, old_col = self.get_player_position(player)
            self.set_cell_value(old_row, old_col, 0)  # Reset the old cell
            self.player_positions[player] = (row, col)
            self.update_board_with_players()
            self.awaiting_token_removal = True
            self.moves_by_player[player] += 1
            return True
        logger.warning(f"Invalid move attempted by {player.name} to ({row}, {col}).")
        return False

    def is_valid_token_removal(self, row, col):
        """Checks if a token removal is valid at the specified row and column."""
        # Check if removal is within board boundaries
        if not (0 <= row < 8 and 0 <= col < 6):
            return False

        # Get the cell value
        cell_value = self.get_cell_value(row, col)

        # Check if the cell is not occupied by a player and has a token
        if cell_value in self.players or cell_value == -1:
            return False

        return True

    def remove_token(self, row, col):
        """Removes a token from the board at the specified row and column."""
        if self.is_valid_token_removal(row, col):
            self.set_cell_value(row, col, -1)
            self.awaiting_token_removal = False
            current_player = self.players[self.current_player_index]
            self.tokens_removed_by_player[current_player] += 1
            return True
        logger.warning(f"Invalid token removal attempted at ({row}, {col}).")
        return False

    def display_stats(self):
        """Displays game statistics such as moves made and tokens removed by each player."""
        logger.info(f"Moves made by {self.players[0].name}: {self.moves_by_player[self.players[0]]}")
        logger.info(f"Moves made by {self.players[1].name}: {self.moves_by_player[self.players[1]]}")
        logger.info(f"Tokens Removed by {self.players[0].name}: {self.tokens_removed_by_player[self.players[0]]}")
        logger.info(f"Tokens Removed by {self.players[1].name}: {self.tokens_removed_by_player[self.players[1]]}")
        elapsed_time = time.time() - self.start_time
        logger.info(f"Time taken for the game: {elapsed_time:.2f} seconds")

    def is_game_over(self):
        """Checks if the game is over."""
        # Check if the current player can make any valid moves
        current_player = self.players[self.current_player_index]
        current_row, current_col = self.get_player_position(current_player)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            if self.is_valid_move(current_player, current_row + dr, current_col + dc):
                return False
        logger.info("Game over!")
        return True

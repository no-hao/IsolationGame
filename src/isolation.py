import copy
import logging
from .player import ComputerPlayer
logger = logging.getLogger("IsolationGameLogger")


class Isolation:
    def __init__(self, player1, player2):
        self.board = [[0 for _ in range(6)] for _ in range(8)]  # 0 represents available cell
        self.players = [player1, player2]
        self.current_player_index = 0

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
        return self.board[row][col]

    def set_cell_value(self, row, col, value):
        self.board[row][col] = value

    def get_player_position(self, player):
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
        for player, position in self.player_positions.items():
            row, col = position
            self.set_cell_value(row, col, player)

    def is_valid_move(self, player, row, col):
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
            logger.info(f"Chose Move: {move} with Heuristic Value: {heuristic_value}")

        return mock_game


    def mock_remove_token(self, row, col):
        """Simulate removing a token without affecting the actual game state."""
        mock_game = copy.deepcopy(self)

        # Ensure the copied game state refers to the same player objects as the original game state
        mock_game.players[0] = self.players[0]
        mock_game.players[1] = self.players[1]
        mock_game.player_positions[self.players[0]] = self.player_positions[self.players[0]]
        mock_game.player_positions[self.players[1]] = self.player_positions[self.players[1]]
        mock_game.moves_by_player[self.players[0]] = self.moves_by_player[self.players[0]]
        mock_game.moves_by_player[self.players[1]] = self.moves_by_player[self.players[1]]
        
        mock_game.board[row][col] = -1  # Represent a removed token with -1
        
        return mock_game


    def make_move(self, player, row, col):
        if self.is_valid_move(player, row, col):
            old_row, old_col = self.get_player_position(player)
            self.set_cell_value(old_row, old_col, 0)  # Reset the old cell
            self.player_positions[player] = (row, col)
            self.update_board_with_players()
            self.awaiting_token_removal = True
            logger.info(f"{player.name} moved to ({row}, {col}).")
            logger.info("Board State:")
            for row in self.board:
                logger.info(row)
            logger.info("Awaiting token removal...")
            self.moves_by_player[player] += 1
            return True
        logger.warning(f"Invalid move attempted by {player.name} to ({row}, {col}).")
        return False

    def is_valid_token_removal(self, row, col):
        # Check if removal is within board boundaries
        if not (0 <= row < 8 and 0 <= col < 6):
            return False

        # Check if the cell is not occupied by a player and has a token
        if self.get_cell_value(row, col) in [player for player in self.players] or self.get_cell_value(row, col) == -1:
            return False

        return True

    def remove_token(self, row, col):
        if self.is_valid_token_removal(row, col):
            self.set_cell_value(row, col, -1)
            self.awaiting_token_removal = False
            current_player = self.players[self.current_player_index]
            self.tokens_removed_by_player[current_player] += 1
            logger.info(f"{current_player.name} removed a token at ({row}, {col}).")
            logger.info("Board State:")
            for row in self.board:
                logger.info(row)
            return True
        logger.warning(f"Invalid token removal attempted at ({row}, {col}).")
        return False

    def display_stats(self):
        logger.info(f"Moves made by {self.players[0].name}: {self.moves_by_player[self.players[0]]}")
        logger.info(f"Moves made by {self.players[1].name}: {self.moves_by_player[self.players[1]]}")
        logger.info(f"Tokens Removed by {self.players[0].name}: {self.tokens_removed_by_player[self.players[0]]}")
        logger.info(f"Tokens Removed by {self.players[1].name}: {self.tokens_removed_by_player[self.players[1]]}")

    def is_game_over(self):
        # Check if the current player can make any valid moves
        current_player = self.players[self.current_player_index]
        current_row, current_col = self.get_player_position(current_player)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            if self.is_valid_move(current_player, current_row + dr, current_col + dc):
                return False
        logger.info("Game over!")
        return True

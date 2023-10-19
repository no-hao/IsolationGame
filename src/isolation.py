import logging
logger = logging.getLogger(__name__)


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

    def get_cell_value(self, row, col):
        return self.board[row][col]

    def set_cell_value(self, row, col, value):
        self.board[row][col] = value

    def get_player_position(self, player):
        return self.player_positions[player]

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

    def make_move(self, player, row, col):
        if self.is_valid_move(player, row, col):
            old_row, old_col = self.get_player_position(player)
            self.set_cell_value(old_row, old_col, 0)  # Reset the old cell
            self.player_positions[player] = (row, col)
            self.update_board_with_players()
            self.awaiting_token_removal = True
            logger.info(f"{player.name} moved to ({row}, {col}). Awaiting token removal.")
            return True
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
            logger.info(f"Token removed at ({row}, {col}).")
            return True
        return False

    def is_game_over(self):
        # Check if the current player can make any valid moves
        current_player = self.players[self.current_player_index]
        current_row, current_col = self.get_player_position(current_player)
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            if self.is_valid_move(current_player, current_row + dr, current_col + dc):
                return False
        return True

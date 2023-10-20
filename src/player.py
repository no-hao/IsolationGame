import random
import logging
logger = logging.getLogger("IsolationGameLogger")

from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def choose_move(self, game_state):
        pass

    @abstractmethod
    def choose_token_to_remove(self, game_state):
        pass

class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def choose_move(self, game_state):
        # Logic for human player to choose a move
        pass

    def choose_token_to_remove(self, game_state):
        # Logic for human player to choose a token to remove
        pass

class ComputerPlayer(Player):
    def __init__(self, name, heuristic=None):
        super().__init__(name)
        self.heuristic = heuristic if heuristic else self.frontier_cells_heuristic

    def best_move_using_heuristics(self, game_state):
        """Choose the best move using the provided heuristic function."""
        valid_moves = game_state.get_available_moves(self)
        if not valid_moves:
            return None

        scores = {}
        for move in valid_moves:
            mock_game_state = game_state.mock_move(self, move)
            score = self.heuristic(mock_game_state, self)
            logger.info(f"Move: {move}, Heuristic Value: {score}")  # <-- Using logger to log the heuristic values
            scores[move] = score

        return max(scores, key=scores.get)

    def choose_move(self, game_state):
        """Choose a move using heuristics."""
        return self.best_move_using_heuristics(game_state)

    def choose_token_to_remove(self, game_state):
        """Choose a random valid token to remove."""
        available_tokens = game_state.get_available_tokens_to_remove()
        return random.choice(available_tokens) if available_tokens else None

    def frontier_cells_heuristic(self, game_state, player):
        # Compute the positions after the move
        row, col = game_state.get_player_position(player)

        # Define possible directions to check
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        non_empty_count = 0
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 6 and game_state.get_cell_value(new_row, new_col) == 0:
                non_empty_count += 1
        return non_empty_count

    def aggressive_approach_heuristic(self, game_state, player):
        opponent = game_state.players[0] if player == game_state.players[1] else game_state.players[1]
        our_valid_moves = game_state.get_available_moves(player)
        opponent_valid_moves = game_state.get_available_moves(opponent)
        return 2 * len(our_valid_moves) - len(opponent_valid_moves)

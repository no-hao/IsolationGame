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
    DEPTH = 5  # Default depth

    def __init__(self, name, heuristic=None):
        super().__init__(name)
        self.heuristic = heuristic if heuristic else self.frontier_cells_heuristic

    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        # Base case: terminal state or depth reached
        if depth == 0:  # We'll add the is_terminal check later
            return self.heuristic(game_state, self)

        # Check for terminal state
        if not game_state.get_available_moves(self):
            return float("inf") if maximizing_player else float("-inf")

        # Max player's turn (Computer)
        if maximizing_player:
            max_eval = float('-inf')
            for move in game_state.get_available_moves(self):
                mock_game_state = game_state.mock_move(self, move)
                eval = self.minimax(mock_game_state, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        # Min player's turn (Opponent)
        else:
            min_eval = float('inf')
            opponent = game_state.players[0] if self == game_state.players[1] else game_state.players[1]
            for move in game_state.get_available_moves(opponent):
                mock_game_state = game_state.mock_move(opponent, move)
                eval = self.minimax(mock_game_state, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def best_token_to_remove_using_heuristics(self, game_state):
        """Choose the best token to remove using the heuristic that minimizes the opponent's available moves."""
        available_tokens = game_state.get_available_tokens_to_remove()
        if not available_tokens:
            return None

        # Determine the opponent
        opponent = game_state.players[0] if self == game_state.players[1] else game_state.players[1]

        scores = {}
        for token in available_tokens:
            mock_game_state = game_state.mock_remove_token(*token)
            opponent_moves = len(mock_game_state.get_available_moves(opponent))
            
            # Add a small random perturbation to the score
            perturbed_score = opponent_moves + random.uniform(-0.01, 0.01)
            
            scores[token] = perturbed_score

        # Choose the token whose removal minimizes the opponent's available moves (after perturbation)
        return min(scores, key=scores.get)

    def choose_move(self, game_state):
        """Choose a move using MiniMax with Alpha-Beta pruning."""
        # If only one valid move is available, return it immediately.
        valid_moves = game_state.get_available_moves(self)
        if len(valid_moves) == 1:
            return valid_moves[0]

        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        depth = ComputerPlayer.DEPTH

        # Evaluate all possible moves and return the best one
        for move in game_state.get_available_moves(self):
            mock_game_state = game_state.mock_move(self, move)
            move_value = self.minimax(mock_game_state, depth-1, alpha, beta, False)
            if move_value > best_value:
                best_value = move_value
                best_move = move
        return best_move

    def choose_token_to_remove(self, game_state):
        """Choose a token to remove using heuristics."""
        return self.best_token_to_remove_using_heuristics(game_state)

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

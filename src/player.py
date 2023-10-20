import time
import random
import logging
logger = logging.getLogger("IsolationGameLogger")

from abc import ABC, abstractmethod

class Player(ABC):
    """Abstract base class for a Player in the Isolation game.

    Attributes:
        name (str): Name of the player.
    """

    def __init__(self, name):
        """Initializes the player with a name."""
        self.name = name

    @abstractmethod
    def choose_move(self, game_state):
        """Abstract method for choosing a move based on the current game state."""
        pass

    @abstractmethod
    def choose_token_to_remove(self, game_state):
        """Abstract method for choosing a token to remove based on the current game state."""
        pass

class HumanPlayer(Player):
    """Represents a human player in the Isolation game."""

    def __init__(self, name):
        """Initializes the human player with a name."""
        super().__init__(name)

    def choose_move(self, game_state):
        """Logic for the human player to choose a move."""
        pass

    def choose_token_to_remove(self, game_state):
        """Logic for the human player to choose a token to remove."""
        pass

class ComputerPlayer(Player):
    """Represents a computer player in the Isolation game using Minimax and heuristics.

    Attributes:
        DEPTH (int): Search depth for Minimax algorithm.
        heuristic (func): Heuristic function to evaluate game states.
    """

    DEPTH = 7  # Default depth

    def __init__(self, name, heuristic=None):
        """Initializes the computer player with a name and heuristic function."""
        super().__init__(name)
        self.heuristic = heuristic if heuristic else self.aggressive_approach_heuristic

    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        """Implements the Minimax algorithm with Alpha-Beta pruning."""
        # Base case: terminal state or depth reached
        if depth == 0:
            return self.heuristic(game_state, self)

        # Check for terminal state
        opponent = game_state.players[1 - game_state.current_player_index]
        available_moves = game_state.get_available_moves(self if maximizing_player else opponent)
        
        if not available_moves:
            # If we're not at the maximum depth and there are no valid moves, this is a bad state.
            if depth != ComputerPlayer.DEPTH:
                return float("-inf") if maximizing_player else float("inf")
            return self.heuristic(game_state, self)

        # Max player's turn (Computer)
        if maximizing_player:
            max_eval = float('-inf')
            for move in available_moves:
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
            for move in available_moves:
                mock_game_state = game_state.mock_move(opponent, move)
                eval = self.minimax(mock_game_state, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def choose_move(self, game_state):
        """Chooses the best move for the computer player based on Minimax."""
        start_time = time.time()
        time_limit = 8.0  # Adjust as necessary

        valid_moves = game_state.get_available_moves(self)
        if len(valid_moves) == 1:
            return valid_moves[0]

        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for depth in range(1, ComputerPlayer.DEPTH + 1):
            for move in valid_moves:
                mock_game_state = game_state.mock_move(self, move)
                move_value = self.minimax(mock_game_state, depth-1, alpha, beta, False)

                if move_value > best_value:
                    best_value = move_value
                    best_move = move

                # Check if we've surpassed our time limit
                if time.time() - start_time > time_limit:
                    break

            if time.time() - start_time > time_limit:
                break

        if best_move is None:
            best_move = random.choice(valid_moves)

        # Log the chosen move
        logger.info(f"{self.name} chooses move: {best_move}")

        return best_move

    def choose_token_to_remove(self, game_state):
        """Choose a token to remove using the new heuristic."""
        return self.token_removal_heuristic(game_state)

    def composite_heuristic(self, game_state, player):
        """Combines multiple heuristics to evaluate the game state."""
        w1, w2, w3 = 0.4, 0.3, 0.3  # These weights can be tuned
        
        mobility_score = w1 * self.enhanced_mobility_heuristic(game_state, player)
        center_control_score = w2 * self.control_of_center_heuristic(game_state, player)
        difference_score = w3 * self.enhanced_difference_heuristic(game_state, player)
        
        return mobility_score + center_control_score + difference_score

    def frontier_cells_heuristic(self, game_state, player):
        """Evaluates the game state based on the frontier cells around the player."""
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
        """Evaluates the game state based on the aggressive approach strategy."""
        opponent = game_state.players[0] if player == game_state.players[1] else game_state.players[1]
        our_valid_moves = game_state.get_available_moves(player)
        opponent_valid_moves = game_state.get_available_moves(opponent)
        return 2 * len(our_valid_moves) - len(opponent_valid_moves)

    def enhanced_mobility_heuristic(self, game_state, player):
        """Evaluates the game state based on the mobility of the player."""
        immediate_moves = game_state.get_available_moves(player)
        lambda_factor = 0.5
        future_mobility = sum([len(game_state.mock_move(player, move).get_available_moves(player)) for move in immediate_moves])
        return len(immediate_moves) + lambda_factor * future_mobility

    def control_of_center_heuristic(self, game_state, player):
        """Evaluates the game state based on control of the center of the board."""
        row, col = game_state.get_player_position(player)
        center_row, center_col = 4, 3
        distance_from_center = abs(center_row - row) + abs(center_col - col)
        return -distance_from_center  # We want to minimize this distance

    def enhanced_difference_heuristic(self, game_state, player):
        """Evaluates the game state based on the difference in valid moves."""
        opponent = game_state.players[0] if player == game_state.players[1] else game_state.players[1]
        
        our_moves = len(game_state.get_available_moves(player))
        opponent_moves = len(game_state.get_available_moves(opponent))
        
        our_future_mobility = sum([len(game_state.mock_move(player, move).get_available_moves(player)) for move in game_state.get_available_moves(player)])
        opponent_future_mobility = sum([len(game_state.mock_move(opponent, move).get_available_moves(opponent)) for move in game_state.get_available_moves(opponent)])
        
        return 2 * (our_moves - opponent_moves) + (our_future_mobility - opponent_future_mobility)

    def token_removal_heuristic(self, game_state):
        """Chooses a token to remove based on various factors and heuristics."""
        available_tokens = game_state.get_available_tokens_to_remove()
        if not available_tokens:
            logger.warning("No valid tokens to remove.")
            return None

        if len(available_tokens) == 1:
            return available_tokens[0]

        opponent = game_state.players[0] if self == game_state.players[1] else game_state.players[1]
        our_position = game_state.get_player_position(self)
        opponent_position = game_state.get_player_position(opponent)

        total_tokens = sum([1 for row in game_state.board for cell in row if cell != 0])
        token_factor = total_tokens / (8 * 6)  # Assuming 8x6 is the board size

        scores = {}
        for token in available_tokens:
            score = 0

            # Proximity to the opponent
            distance_to_opponent = abs(opponent_position[0] - token[0]) + abs(opponent_position[1] - token[1])
            score -= distance_to_opponent * token_factor

            # Proximity to the center
            center_distance = abs(4 - token[0]) + abs(3 - token[1])
            score -= center_distance * (1 - token_factor)

            # Predictive blocking (1 move ahead for now)
            mock_game_state = game_state.mock_remove_token(*token)
            opponent_best_move_value = max([self.frontier_cells_heuristic(mock_game_state.mock_move(opponent, move), opponent) for move in mock_game_state.get_available_moves(opponent)], default=0)
            score -= opponent_best_move_value

            # Effect on opponent's moves
            opponent_moves_after_removal = len(mock_game_state.get_available_moves(opponent))
            original_opponent_moves = len(game_state.get_available_moves(opponent))
            move_difference = original_opponent_moves - opponent_moves_after_removal
            score += move_difference

            # Random factor
            score += random.uniform(0, 1)

            scores[token] = score

        best_token = max(scores, key=scores.get)

        
        self.previous_token = best_token
        logger.info(f"{self.name} chose to remove a token at ({best_token}).")
        return best_token

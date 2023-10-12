from abc import ABC, abstractmethod
from .board import CellState, Board


class Player(ABC):
    def __init__(self, player_id: str, player_type: str):
        self.player_id = player_id
        self.player_type = player_type
        self.position = None

    def __str__(self):
        return f"Player {self.player_id}"

    @abstractmethod
    def move(self, board: Board) -> tuple:
        pass

    @abstractmethod
    def remove_token(self, board: Board) -> tuple:
        pass

    def _is_valid_move(self, row: int, col: int, board: Board) -> bool:
        curr_row, curr_col = self.position
        dx = abs(curr_row - row)
        dy = abs(curr_col - col)
        return ((dx + dy) != 0 and
                dx <= 1 and dy <= 1 and
                Board.is_within_board(row, col) and board.get_cell_state(row, col) == CellState.EMPTY)

    def _is_valid_removal(self, row: int, col: int, board: Board) -> bool:
        return Board.is_within_board(row, col) and board.get_cell_state(row, col) == CellState.EMPTY

    def update(self):
        print(f"[DEBUG] Player {self.player_id} is being updated due to board change.")


class Heuristics:
    @staticmethod
    def mobility(game, board, player_position):
        w1, w2 = 1, 1
        self_moves = [move for move in board.get_possible_moves(*player_position) if game.move_is_legal(move)]
        opponent_position = game.get_opponent_position()
        opponent_moves = [move for move in board.get_possible_moves(*opponent_position) if game.move_is_legal(move)]
        return w1 * len(self_moves) - w2 * len(opponent_moves)

    @staticmethod
    def frontier_minimization(game, player_position):
        WIDTH, HEIGHT = 8, 6
        opponent_position = game.get_opponent_position()
        distance_to_edge = min(
            opponent_position[0], 
            WIDTH - 1 - opponent_position[0], 
            opponent_position[1], 
            HEIGHT - 1 - opponent_position[1]
        )
        return -distance_to_edge


class PlayerFactory:
    @staticmethod
    def create_player(player_type: str, player_id: str, game=None, board=None, heuristic_function=None) -> Player:
        if player_type == "Human":
            return HumanPlayer(player_id=player_id, player_type="Human")
        elif player_type == "Computer":
            return ComputerPlayer(player_id=player_id, player_type="Computer", game=game, board=board, heuristic_function=heuristic_function)
        else:
            raise ValueError(f"Unknown player type: {player_type}")


class HumanPlayer(Player):
    def move(self, board: Board) -> tuple:
        while True:
            try:
                row, col = map(int, input("Enter your move (row col): ").split())
                if self._is_valid_move(row, col, board):
                    return row, col
                else:
                    print("Invalid move. Please try again.")
            except ValueError:
                print("Invalid input format. Please enter row and column separated by space.")

    def remove_token(self, board: Board) -> tuple:
        while True:
            try:
                row, col = map(int, input("Enter the token position to remove (row col): ").split())
                if self._is_valid_removal(row, col, board):
                    return row, col
                else:
                    print("Invalid position. Please try again.")
            except ValueError:
                print("Invalid input format. Please enter row and column separated by space.")

    def update(self):
        print(f"[DEBUG] Human Player {self.player_id} is being updated due to board change.")
        # Additional logic can be added here if needed


class ComputerPlayer(Player):
    def __init__(self, player_id: str, player_type: str, game, board, heuristic_function):
        super().__init__(player_id, player_type)
        self.heuristic = heuristic_function
        self.mcts = MCTS(game, board, heuristic_function)

    def move(self, board: Board) -> tuple:
        # Use MCTS to decide the move
        best_move = self.mcts.search(board)
        return best_move

    def remove_token(self, board: Board) -> tuple:
        # Integrate logic to decide which token to remove, possibly using heuristics or other strategies
        # Placeholder: For now, removing a random token
        import random
        empty_cells = [(i, j) for i in range(8) for j in range(6) if board.get_cell_state(i, j) == CellState.EMPTY]
        return random.choice(empty_cells)

    def update(self):
        print(f"[DEBUG] Computer Player {self.player_id} is being updated due to board change.")
        # The AI can recompute its strategies or prepare for the next move here


# Usage:
# ai_player = HeuristicAIPlayer(game_instance, board_instance, mobility_heuristic)
# move = ai_player.get_move()

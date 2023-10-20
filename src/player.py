import random
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
    def choose_move(self, game_state):
        # Logic for human player to choose a move
        pass

    def choose_token_to_remove(self, game_state):
        # Logic for human player to choose a token to remove
        pass

class ComputerPlayer(Player):
    def choose_move(self, game_state):
        """Choose a random valid move."""
        valid_moves = game_state.get_available_moves(self)
        return random.choice(valid_moves) if valid_moves else None

    def choose_token_to_remove(self, game_state):
        """Choose a random valid token to remove."""
        available_tokens = game_state.get_available_tokens_to_remove()
        return random.choice(available_tokens) if available_tokens else None


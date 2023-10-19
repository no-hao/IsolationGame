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
        # Logic for computer to choose a move
        pass

    def choose_token_to_remove(self, game_state):
        # Logic for computer to choose a token to remove
        pass

from src.board import Board
from src.player import HumanPlayer, PlayerFactory
from src.game import Game


def get_player_type(player_number):
    while True:
        player_type = input(f"Choose type for Player {player_number} (Human/Computer): ").capitalize()
        if player_type in ["Human", "Computer"]:
            return player_type
        print("Invalid choice. Please choose either 'Human' or 'Computer'.")


def main():
    # Prompt user to choose the type of matchup
    player1_type = get_player_type(1)
    player2_type = get_player_type(2)

    # Create players using PlayerFactory
    player1 = PlayerFactory.create_player(player1_type, name=f"Player 1 ({player1_type})")
    player2 = PlayerFactory.create_player(player2_type, name=f"Player 2 ({player2_type})")

    # Initialize the game with the two players
    game = Game(player1, player2)

    # Start the game
    game.play()


if __name__ == "__main__":
    main()

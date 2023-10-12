from src.player import PlayerFactory
from src.game import Game


def get_player_type(player_num):
    while True:
        player_type = input(f"Choose type for Player {player_num} (Human/Computer): ").capitalize()
        if player_type in ["Human", "Computer"]:
            return player_type
        print("Invalid choice. Please choose either 'Human' or 'Computer'.")


def main():
    # Get player types
    player1_type = get_player_type(1)
    player2_type = get_player_type(2)

    # Create players using the PlayerFactory
    player1 = PlayerFactory.create_player(player1_type, player_id="1")
    player2 = PlayerFactory.create_player(player2_type, player_id="2")

    # Instantiate the game
    game = Game(player1, player2)

    # Register players as observers to the board
    game.board.add_observer(player1)
    game.board.add_observer(player2)

    # Start the game loop
    game.play()


if __name__ == "__main__":
    main()

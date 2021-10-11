"""
main.py:
    Main method to start the whole snake game
    This is just a simple game of classic snake that everybody loves :)
"""

from snake_game_controller import GameController


def main():
    game = GameController()
    game.start_snake_game()


if __name__ == '__main__':
    main()

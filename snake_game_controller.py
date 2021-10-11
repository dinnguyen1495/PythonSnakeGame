"""
snake_game_controller.py
    Snake game controller
"""

from tkinter import Tk, Canvas, Menu
from turtle import TurtleScreen, RawTurtle
from typing import Any
import time
from snakey import Snake


def get_move_function_from_key(snake: Snake, key: str) -> Any:
    """
    Get function for snake's movement when key is pressed
    :param snake:
        Player's snake
    :param key:
        The pressed key, can only be 'w', 'a', 's', or 'd'
    :return:
        Move functions
    """
    try:
        move = snake.get_move_from_key(key)
        if move == 1:
            return snake.move_right
        elif move == 2:
            return snake.move_left
    except ValueError:
        return None


class GameController:
    """
    Controller for the whole snake game
    """

    def __init__(self, snake_block_size=25, speed=0.1, width_blocks=20, height_blocks=20):
        """
        Initialize the controller
        :param snake_block_size:
            Size of a snake block in pixel. Default is 25
        :param speed:
            Speed of the snake. Default is 0.1, smaller number for greater speed
        :param width_blocks:
            Width of the board for snake to play around
        :param height_blocks:
            Height of the board for snake to play around
        """
        self.snake_block_size = snake_block_size
        self.width = (width_blocks + 1.5) * snake_block_size + (width_blocks - 1) * 2
        self.height = (height_blocks + 1.5) * snake_block_size + (height_blocks - 1) * 2
        self.width_range = int(width_blocks / 2)
        self.height_range = int(height_blocks / 2)
        self.speed = speed

        self.window = Tk()
        self.window.title("Simple Snake Game")

        self.canvas = Canvas(self.window, width=self.width * 1.25, height=self.height * 1.25)
        self.canvas.pack()
        self.board = TurtleScreen(self.canvas)

        self.menu_bar = Menu(self.window)
        self.window.config(menu=self.menu_bar)
        file_menu = Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Game (R)", command=self.start_snake_game)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.window.destroy)
        self.menu_bar.add_cascade(label="Game", menu=file_menu)

    def start_snake_game(self):
        """
        UI for the snake game and its controller
        """
        self.board.clear()
        self.board.tracer(0)

        border = RawTurtle(self.board)
        border.penup()
        border.setpos((-self.width_range - 1) * (self.snake_block_size + 2),
                      (self.height_range + 1) * (self.snake_block_size + 2))
        border.pendown()
        border.setpos((self.width_range + 1) * (self.snake_block_size + 2),
                      (self.height_range + 1) * (self.snake_block_size + 2))
        border.setpos((self.width_range + 1) * (self.snake_block_size + 2),
                      (-self.height_range - 1) * (self.snake_block_size + 2))
        border.setpos((-self.width_range - 1) * (self.snake_block_size + 2),
                      (-self.height_range - 1) * (self.snake_block_size + 2))
        border.setpos((-self.width_range - 1) * (self.snake_block_size + 2),
                      (self.height_range + 1) * (self.snake_block_size + 2))
        border.hideturtle()

        snake = Snake(self.board, self.snake_block_size, self.width_range, self.height_range)
        score = RawTurtle(self.board)
        score.hideturtle()
        score.penup()
        score.setpos((-self.width_range - 2) * self.snake_block_size,
                     (self.height_range + 2) * self.snake_block_size)

        self.board.listen()
        while not snake.is_game_over():
            score.clear()
            score.write(f'Score: {snake.score}', False, align='left')
            self.board.onkeypress(get_move_function_from_key(snake, 'w'), 'w')
            self.board.onkeypress(get_move_function_from_key(snake, 'a'), 'a')
            self.board.onkeypress(get_move_function_from_key(snake, 'd'), 'd')
            self.board.onkeypress(get_move_function_from_key(snake, 's'), 's')
            self.board.onkey(self.start_snake_game, 'r')
            if not snake.key_pressed:
                snake.move_forward()
            else:
                snake.key_pressed = False
            self.board.update()
            time.sleep(self.speed)
        score.clear()
        score.write(f'FINAL SCORE: {snake.score}. Press R to restart', False, align='left')
        self.board.update()
        self.board.mainloop()
        self.window.mainloop()

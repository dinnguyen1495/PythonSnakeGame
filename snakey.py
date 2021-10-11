"""
snakey.py
    Player's snake and food
"""

from turtle import RawTurtle, TurtleScreen
from collections import deque
from random import sample


# Bind key to snake's movement
# 3 - nord, 2 - west, 1 - south, 0 - east
MOVEMENT_TO_KEY = {
    3: ('w', 'd', 'a'),
    2: ('a', 'w', 's'),
    1: ('s', 'a', 'd'),
    0: ('d', 's', 'w')
}

# Calculate adjustment for next position of the snake based on movement
MOVEMENT_TO_POSITION = {
    3: ((0, 1), (1, 0), (-1, 0)),
    2: ((-1, 0), (0, 1), (0, -1)),
    1: ((0, -1), (-1, 0), (1, 0)),
    0: ((1, 0), (0, -1), (0, 1))
}


class Snake:
    """
    A class for the snake and its food
    """

    def __init__(self, turtle_screen: TurtleScreen, snake_block_size: float, width_range: int, height_range: int):
        """
        Initialize the snake and its food
        :param snake_block_size:
            Width and height of 1 snake's block in pixel.
        :param width_range:
            Width of the board for snake to play around
        :param height_range:
            Height of the board for snake to play around
        """
        self.turtle_screen = turtle_screen
        self.snake_block_size = snake_block_size
        self.direction = 0
        self.score = 0
        self.dead = False
        self.body = deque([(-2, 0), (-1, 0), (0, 0)])
        self.body_blocks = deque()
        for block in self.body:
            new_block = self.create_new_block(block, 'square', 'black')
            self.body_blocks.append(new_block)
        self.key_pressed = False
        self.width_range = width_range
        self.height_range = height_range
        self.available = set()
        for i in range(-self.width_range, self.width_range + 1):
            for j in range(-self.height_range, self.height_range + 1):
                self.available.add((i, j))
        self.food_position = self.create_food_position()
        self.food = self.create_new_block(self.food_position, 'circle', 'blue')

    def create_food_position(self) -> tuple[int, int]:
        """
        Create new position for food from available blocks set
        :return: new food position
        """
        sample_set = self.available - set(self.body)
        new_food_position = sample(sample_set, 1)
        return new_food_position[0]

    def set_food_position(self) -> None:
        """
        Draw food in the screen
        """
        self.food.ht()
        self.food.setpos(self.food_position[0] * (self.snake_block_size + 2),
                         self.food_position[1] * (self.snake_block_size + 2))
        self.food.st()

    def is_game_over(self):
        """
        Check if snake is dead or alive
        :return: State of the snake
        """
        return self.dead

    def get_body_blocks(self) -> deque[RawTurtle]:
        """
        Getter for snake's visual body blocks
        :return: queue that contains visualized blocks of snake
        """
        return self.body_blocks

    def create_new_block(self, new_pos: tuple[int, int], block_shape: str, block_color: str):
        """
        Create new visual body blocks for snake
        :param new_pos:
            New position in the board that contains snake block
        :param block_shape:
            Shape of new snake block
        :param block_color:
            Color of new snake block
        :return:
            New visualized snake block
        """
        new_block = RawTurtle(self.turtle_screen, block_shape)
        new_block.fillcolor(block_color)
        new_block.speed(10)
        new_block.penup()
        new_block.shapesize(self.snake_block_size / 20)
        new_block.setpos(new_pos[0] * (self.snake_block_size + 2), new_pos[1] * (self.snake_block_size + 2))
        return new_block

    def set_new_direction(self, move: int) -> None:
        """
        Set new direction of snake after a move
        :param move:
            0 - move forward, 1 - turn right, -1 - turn left
        """
        self.direction = (self.direction + move) % 4 if self.direction + move >= 0 else 3

    def get_move_from_key(self, key: str) -> int:
        """
        Return movement from key pressed on keyboard
        :param key:
            The pressed key, can only be 'w', 'a', 's', or 'd'
        :return:
             3 - nord, 2 - west, 1 - south, 0 - east
        """
        return MOVEMENT_TO_KEY[self.direction].index(key)

    def is_dead_by_border(self, pos: tuple[int, int]):
        """
        Check if snake is dead by slamming its head on the border of playground
        :param pos:
            Position of the snake
        :return:
            True or False
        """
        return -self.width_range > pos[0] or self.width_range < pos[0] \
               or -self.height_range > pos[1] or self.height_range < pos[1]

    def update_body(self, next_move: int) -> None:
        """
        Update state and score of snake after each move
        :param next_move:
            0 - move forward, 1 - turn right, -1 - turn left
        """
        new_head = (self.body[-1][0] + MOVEMENT_TO_POSITION[self.direction][next_move][0],
                    self.body[-1][1] + MOVEMENT_TO_POSITION[self.direction][next_move][1])
        if new_head in self.body:
            self.score -= 1
            self.dead = True
            return
        if new_head != self.food_position:
            self.body.popleft()
        self.body.append(new_head)
        if self.is_dead_by_border(self.body[-1]):
            self.dead = True

    def update_body_blocks(self) -> None:
        """
        Update position for every snake block while moving
        """
        for i in range(0, len(self.body_blocks) - 1):
            self.body_blocks[i].setpos(self.body_blocks[i + 1].pos())

    def create_new_tail(self) -> None:
        """
        Create tail for the snake after it eats a food
        """
        new_tail_pos = (int(self.body[0][0] * (self.snake_block_size + 2)),
                        int(self.body[0][1] * (self.snake_block_size + 2)))
        new_tail = self.create_new_block(new_tail_pos, 'square', 'black')
        self.body_blocks.appendleft(new_tail)
        self.score += 1
        self.food_position = self.create_food_position()
        self.set_food_position()

    def head_forward(self) -> None:
        """
        Behaviour of visual snake when moving forward
        """
        self.update_body_blocks()
        self.body_blocks[-1].forward(self.snake_block_size + 2)
        if len(self.body) == len(self.body_blocks) + 1:
            self.create_new_tail()

    def head_left(self):
        """
        Behaviour of visual snake when turning left
        """
        self.set_new_direction(-1)
        self.update_body_blocks()
        self.body_blocks[-1].left(90)
        self.body_blocks[-1].forward(self.snake_block_size + 2)
        if len(self.body) == len(self.body_blocks) + 1:
            self.create_new_tail()

    def head_right(self):
        """
        Behaviour of visual snake when turning right
        """
        self.set_new_direction(1)
        self.update_body_blocks()
        self.body_blocks[-1].right(90)
        self.body_blocks[-1].forward(self.snake_block_size + 2)
        if len(self.body) == len(self.body_blocks) + 1:
            self.create_new_tail()

    def move_forward(self):
        """
        Snakes's behaviours when moving forward
        """
        self.update_body(0)
        if self.dead:
            return
        self.head_forward()
        self.body_blocks[-1].color('yellow')

    def move_left(self):
        """
        Snakes's behaviours when turning left
        """
        self.update_body(-1)
        self.key_pressed = True
        if self.dead:
            return
        self.head_left()
        self.body_blocks[-1].color('yellow')

    def move_right(self):
        """
        Snakes's behaviours when turning right
        """
        self.update_body(1)
        self.key_pressed = True
        if self.dead:
            return
        self.head_right()
        self.body_blocks[-1].color('yellow')

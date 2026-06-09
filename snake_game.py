from enum import IntEnum
from collections import namedtuple
import numpy as np
import random

class Direction(IntEnum):
    RIGHT = 0
    DOWN  = 1
    LEFT  = 2
    UP    = 3

Point = namedtuple('Point', ['x', 'y'])

# Clockwise order нужен чтобы повороты считались через индекс
_CW = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]

# Смещения головы для каждого направления
_DELTA = {
    Direction.RIGHT: ( 1,  0),
    Direction.LEFT:  (-1,  0),
    Direction.DOWN:  ( 0,  1),
    Direction.UP:    ( 0, -1),
}


class SnakeGame:
    """
    Чистая логика змейки без отрисовки.

    Сетка width×height клеток, координаты в клетках (не пикселях).
    Action: 0 = прямо, 1 = повернуть вправо, 2 = повернуть влево
            (относительно текущего направления движения)
    """

    def __init__(self, width: int = 20, height: int = 20):
        self.width  = width
        self.height = height
        self.reset()

    # ------------------------------------------------------------------
    def reset(self) -> np.ndarray:
        cx, cy = self.width // 2, self.height // 2
        self.direction = Direction.RIGHT
        self.head      = Point(cx, cy)
        self.snake     = [self.head, Point(cx - 1, cy), Point(cx - 2, cy)]
        self.score     = 0
        self.frame     = 0
        self._place_food()
        return self._state()

    # ------------------------------------------------------------------
    def step(self, action: int):
        """
        Сделать один шаг.
        Возвращает (reward, done, score).
        """
        self.frame += 1

        # Обновляем направление
        idx = _CW.index(self.direction)
        if action == 1:
            self.direction = _CW[(idx + 1) % 4]   # вправо по часовой
        elif action == 2:
            self.direction = _CW[(idx - 1) % 4]   # влево против часовой

        # Двигаем голову
        dx, dy = _DELTA[self.direction]
        self.head = Point(self.head.x + dx, self.head.y + dy)

        # Если слишком долго не ел — считаем зависшим, заканчиваем эпизод
        if self.frame > 150 * len(self.snake) or self._collision():
            return -10, True, self.score

        self.snake.insert(0, self.head)

        if self.head == self.food:
            self.score += 1
            self._place_food()
            return 10, False, self.score

        self.snake.pop()
        return 0, False, self.score

    # ------------------------------------------------------------------
    def _collision(self, pt: Point = None) -> bool:
        if pt is None:
            pt = self.head
        # Вышли за границы?
        if pt.x < 0 or pt.x >= self.width or pt.y < 0 or pt.y >= self.height:
            return True
        # Врезались в тело? (snake[0] — голова, её не считаем)
        return pt in self.snake[1:]

    def _place_food(self):
        while True:
            p = Point(random.randint(0, self.width  - 1),
                      random.randint(0, self.height - 1))
            if p not in self.snake:
                self.food = p
                break

    # ------------------------------------------------------------------
    def _state(self) -> np.ndarray:
        """
        Возвращает вектор из 11 признаков, которые нейросеть получает как вход.

        [0]  опасность прямо       — там стена или тело?
        [1]  опасность вправо
        [2]  опасность влево
        [3]  текущее направление: влево
        [4]  текущее направление: вправо
        [5]  текущее направление: вверх
        [6]  текущее направление: вниз
        [7]  еда левее головы
        [8]  еда правее головы
        [9]  еда выше головы
        [10] еда ниже головы
        """
        h   = self.head
        idx = _CW.index(self.direction)

        def look(turn: int) -> Point:
            dx, dy = _DELTA[_CW[(idx + turn) % 4]]
            return Point(h.x + dx, h.y + dy)

        straight = look(0)   # клетка прямо
        right    = look(1)   # клетка вправо
        left     = look(-1)  # клетка влево

        d = self.direction
        return np.array([
            # опасность
            self._collision(straight),
            self._collision(right),
            self._collision(left),
            # направление
            d == Direction.LEFT,
            d == Direction.RIGHT,
            d == Direction.UP,
            d == Direction.DOWN,
            # еда
            self.food.x < h.x,
            self.food.x > h.x,
            self.food.y < h.y,
            self.food.y > h.y,
        ], dtype=np.float32)

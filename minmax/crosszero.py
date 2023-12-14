import numpy as np
from pprint import pprint
import random
from .point import Point


class CrossZeroException(Exception):
    ...


class CrossZero():
    def __init__(self, N: int) -> None:
        self.n = N
        self.field = np.zeros((N, N), dtype=str)
        self.current_player = 'X'

    def _toggle_player(self) -> None:
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def _isAvailable(self, point: Point) -> bool:
        print(point.y, self.n)
        if point.x >= self.n or point.x < 0 or point.y >= self.n or point.y < 0:
            return False
            # raise CrossZeroException(
            # f'{point} не входит в рамки ({self.n}, {self.n})!')
        if self.field[point.y, point.x] != '':
            return False
            raise CrossZeroException(f'{point} уже занята!')
        return True

    def _checkWin(self, point: Point) -> bool:
        def reset(point: Point) -> tuple[int, int]:
            return (point.x, point.y)

        # (x, y)
        indexes = (
            ((0, 1),  # вниз
             (0, -1)),  # вверх
            ((1, 0),  # вправо
             (-1, 0)),  # влево
            ((1, 1),  # в правый нижний уголв
             (-1, -1)),  # левый верхний угол
            ((-1, 1),  # левый нижний угол
             (1, -1)  # левый нижний угол # левый верхний угол
             ),
        )

        for index in indexes:
            count = 1
            for dx, dy in index:
                x, y = reset(point)
                y += dy
                x += dx
                while y > -1 and y < self.n and x > -1 and x < self.n:
                    if self.field[y, x] == self.current_player:
                        count += 1
                        y += dy
                        x += dx
                        continue
                    else:
                        y += dy
                        x += dx
                        break
                else:
                    if count == self.n:
                        return True
                if count == self.n:
                    return True
        if count == self.n:
            return True
        return False

    def move(self, point: Point) -> bool | None:
        if self._isAvailable(point):
            self.field[point.y, point.x] = self.current_player

            if self._checkWin(point):
                print(f'{self.current_player} победил!')
                return True
            self._toggle_player()
            return False
        else:
            return None

    def showField(self):
        print("  y0, y1, y2")
        for y in range(self.field.shape[0]):
            print(f"x{y}", end='')
            print(self.field[:, y])

    def ai_move(self, f: np.ndarray) -> Point:
        field = f.copy()

        points = []

        for y in range(field.shape[0]):
            for x in range(field.shape[1]):
                if field[y, x] == '':
                    points.append(Point(x, y))

        return random.choice(points)

    def startGame(self):
        self.current_player = 'X'

        win = False

        self.showField()
        while True:
            print(f'Ход {self.current_player}, введите x, y:')
            x, y = map(int, input().split(','))
            win = self.move(Point(x, y))
            while win is None:
                print(
                    f'Неверный ход! Попробуйте еще раз!\nХод {self.current_player}, введите x, y:')
                x, y = map(int, input().split(','))
                win = self.move(Point(x, y))
            self.showField()
            if win:
                break

            ai_move = self.ai_move(self.field)
            print(ai_move)
            win = self.move(ai_move)
            self.showField()
            if win:
                break

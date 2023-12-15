"""
Здесь я пытался сделать свой метод оценивания, который мог бы применяться
к любому состоянию. Не используется(
"""

import numpy as np

from .point import Point


INFINITY = 999
Ka = 2


def _ray(point: Point, field: np.ndarray, player: str) -> tuple[int, int, int]:
    def reset(point: Point) -> tuple[int, int]:
        return (point.x, point.y)

    enemy = 'X' if player == 'O' else 'O'
    Kfl = 0
    Kl = 0
    Kel = 0
    n = field.shape[0]

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
        countAllias = 0
        countLine = 0
        isLineEmptyFromEnemies = True
        count = 0
        for dx, dy in index:
            x, y = reset(point)
            y += dy
            x += dx
            while y > -1 and y < n and x > -1 and x < n:
                isNotEdge = True
                if field[y, x] == '':
                    count += 1
                    y += dy
                    x += dx
                    continue
                if field[y, x] == player:
                    count += 1
                    countAllias += 1
                    y += dy
                    x += dx
                    continue
                elif field[y, x] == enemy:
                    isLineEmptyFromEnemies = False
                    Kel += 1
                    y += dy
                    x += dx
                    continue
            countLine += isLineEmptyFromEnemies
            if countLine == 2 and isNotEdge and count == 2:
                Kfl += countAllias
                Kl += 1
    return (Kfl, Kl, Kel)


def _calculateWeight(Kfl: int, Kl: int, Kel: int):
    return (1 + 2 * Kfl) * Kl + Ka * Kel


def estimate(state: np.ndarray, player: str) -> np.ndarray:
    weights = np.zeros_like(state, dtype=int)

    for x in range(state.shape[1]):
        for y in range(state.shape[0]):
            if state[y, x] == '':
                Kfl, Kl, Kel = _ray(Point(x, y), state, player)
                print(Kfl, Kl, Kel, _calculateWeight(Kfl, Kl, Kel))
                weights[y, x] = _calculateWeight(Kfl, Kl, Kel)

    print(weights)

    return weights.astype(int)

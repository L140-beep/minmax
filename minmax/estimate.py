import numpy as np

from .point import Point


INFINITY = 99999
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
        isNotEdge = False
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
                    y += dy
                    x += dx
                    continue
            countLine += isLineEmptyFromEnemies
            if countLine == n - 1 and isNotEdge and count == n - 1:
                Kfl += countAllias
                if countAllias == n - 1:
                    Kfl += countAllias * 20
                Kl += 1

    for index in indexes:
        count = 0
        steps = 0
        for dx, dy in index:
            x, y = reset(point)
            y += dy
            x += dx
            is_enemy_line = False
            is_not_edge = False
            while y > -1 and y < n and x > -1 and x < n:
                is_not_edge = True
                if field[y, x] == '':
                    steps += 1
                    y += dy
                    x += dx
                    continue
                if field[y, x] == player:
                    is_enemy_line = False
                    break
                elif field[y, x] == enemy:
                    steps += 1
                    is_enemy_line = True
                    y += dy
                    x += dx
                    continue
            count += is_enemy_line
            if is_not_edge and count > 0 and steps == n - 1:
                Kel += 1

    return (Kfl, Kl, Kel)


def _calculateWeight(Kfl: int, Kl: int, Kel: int):
    return (1 + 2 * Kfl) * Kl + Ka * Kel


def estimate(state: np.ndarray, player: str) -> float:
    weights1 = np.zeros_like(state, dtype=int)
    weights2 = np.zeros_like(state, dtype=int)

    for x in range(state.shape[1]):
        for y in range(state.shape[0]):
            if state[y, x] == '':
                Kfl, Kl, Kel = _ray(Point(x, y), state, player)
                # print(Kfl, Kl, Kel, _calculateWeight(Kfl, Kl, Kel))
                weights1[y, x] = _calculateWeight(Kfl, Kl, Kel)
                # weights1[y, x] = Kel
                Kfl, Kl, Kel = _ray(Point(x, y), state,
                                    'O' if player == 'X' else 'X')
                # print(Kfl, Kl, Kel, _calculateWeight(Kfl, Kl, Kel))
                weights2[y, x] = _calculateWeight(Kfl, Kl, Kel)

    s1 = weights1.sum()
    s2 = weights2.sum()

    if s1 + s2 != 0:
        return (weights1.sum() / (weights2.sum() + weights1.sum())) - 0.5
    return 0

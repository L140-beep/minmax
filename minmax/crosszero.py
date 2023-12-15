import numpy as np
from pprint import pprint
import random
from copy import deepcopy
from .point import Point


WIN_SCORE = 10
LOSE_SCORE = -10
DRAW_SCORE = 0


class CrossZeroException(Exception):
    ...


class CrossZero():
    def __init__(self, N: int) -> None:
        self.n = N
        self.field = np.zeros((N, N), dtype=str)
        self.current_player = 'X'

    def _toggle_player(self) -> None:
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def _isAvailable(self, point: Point, field) -> bool:
        # print(point.y, self.n)
        if point.x >= self.n or point.x < 0 or point.y >= self.n or point.y < 0:
            return False
            # raise CrossZeroException(
            # f'{point} не входит в рамки ({self.n}, {self.n})!')
        if field[point.y, point.x] != '':
            return False
        return True

    def _checkDraw(self, field) -> bool:
        return np.where(field == '', True, False).sum() == 0

    def _checkWin(self, point: Point, field) -> bool:
        def reset(point: Point) -> tuple[int, int]:
            return (point.x, point.y)
        player = field[point.y, point.x]
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
                    if field[y, x] == player:
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

    def move(self, field: np.ndarray, point: Point, player: str) -> int | None:
        if self._isAvailable(point, field):
            field[point.y, point.x] = player

            if self._checkWin(point, field):
                return 1
            if np.where(field == '', True, False).sum() == 0:
                return 0
            return -1
        else:
            return None

    def showField(self):
        print("  y0, y1, y2")
        for y in range(self.field.shape[0]):
            print(f"x{y}", end='')
            print(self.field[y, :])

    # def minmax(self, field: np.ndarray, point: Point, player: str, is_ai_move: bool) -> int:
    #     move_result = self.move(field, point, player)
    #     if move_result == 1:
    #         if player == 'O':
    #             return WIN_SCORE
    #         else:
    #             return LOSE_SCORE
    #     elif move_result == 0:
    #         return DRAW_SCORE
    #     elif move_result is None:
    #         print(field)
    #         raise CrossZeroException(f'Неправильный ход {point}')

    #     if is_ai_move:
    #         best_score = -9999
    #         for x in range(field.shape[1]):
    #             for y in range(field.shape[0]):
    #                 if field[y, x] == '':
    #                     score = self.minmax(field, point=Point(
    #                         x, y), is_ai_move=False, player='O')
    #                     best_score = max(best_score, score)
    #                     field[y, x] = ''
    #     else:
    #         best_score = 9999
    #         for x in range(field.shape[1]):
    #             for y in range(field.shape[0]):
    #                 if field[y, x] == '':
    #                     score = self.minmax(field, point=Point(
    #                         x, y), is_ai_move=True, player='X')
    #                     best_score = min(best_score, score)
    #                     field[y, x] = ''

    #     return best_score

    def minmax(self, depth: int, field: np.ndarray, point: Point, is_ai_moved: bool) -> float:
        if self._checkWin(point, field):
            if field[point.y, point.x] == 'O':
                # print(field)
                # print('win')
                # print(field)
                return WIN_SCORE / depth
            else:
                # print('lose')
                # print(field)
                # if depth == 1:
                    # print("player: ", field[point.y, point.x])
                    # print(field)
                return LOSE_SCORE / depth
        elif self._checkDraw(field):
            # print('draw')
            # print(field)
            return 0.01 * depth
        # elif move_result is None:
        #     print(field)
        #     raise CrossZeroException(f'Неправильный ход {point}')

        if is_ai_moved:
            best_score = -9999.
            for x in range(field.shape[0]):
                for y in range(field.shape[1]):
                    if field[y, x] == '':
                        field[y, x] = 'O'
                        score = self.minmax(depth + 1, field, point=Point(
                            x, y), is_ai_moved=False)
                        field[y, x] = ''
                        best_score = max(best_score, score)
                        # if best_score < score:
                        #     best_score = score
                        #     bfield = f
            # if best_move is not None:
            #     field[best_move.y, best_move.x] = 'O'
        else:
            best_score = 9999.
            for x in range(field.shape[0]):
                for y in range(field.shape[1]):
                    if field[y, x] == '':
                        field[y, x] = 'X'
                        score = self.minmax(depth + 1, field, point=Point(
                            x, y), is_ai_moved=True)
                        field[y, x] = ''
                        best_score = min(best_score, score)

            # if best_move is not None:
            #     field[best_move.y, best_move.x] = 'X'
        return best_score

    def ai_move(self, f: np.ndarray) -> Point | None:
        move = None
        best_score = -9999.
        field = deepcopy(f)
        moves = []
        for x in range(field.shape[0]):
            for y in range(field.shape[1]):
                if field[y, x] == '':
                    field[y, x] = 'O'
                    score = self.minmax(1, field, Point(
                        x, y), False)
                    field[y, x] = ''
                    print(Point(x, y), score)
                    if score > best_score:
                        best_score = score
                        moves = [Point(x, y)]
                    elif score == best_score:
                        moves.append(Point(x, y))

        # for bfield in fields:
        #     print(bfield)
        #     print('---------')

        return random.choice(moves)
        # field = f.copy()

        # points = []

        # for y in range(field.shape[0]):
        #     for x in range(field.shape[1]):
        #         if field[y, x] == '':
        #             points.append(Point(x, y))

        # return random.choice(points)

    def startGame(self):
        self.current_player = 'X'

        win = False

        self.showField()
        while True:
            print(f'Ход {self.current_player}, введите y, x:')
            x, y = map(int, input().split(','))
            win = self.move(self.field, Point(x, y), self.current_player)
            while win is None:
                print(
                    f'Неверный ход! Попробуйте еще раз!\nХод {self.current_player}, введите y, x через запятую:')
                x, y = map(int, input().split(','))
                win = self.move(self.field, Point(x, y), self.current_player)
            self.showField()
            if win == 1:
                print(f'{self.current_player} победил!')
                break
            elif win == 0:
                print('Ничья!')
                break
            self._toggle_player()
            ai_move = self.ai_move(self.field)
            win = self.move(self.field, ai_move, self.current_player)
            self.showField()
            if win == 1:
                print(f'{self.current_player} победил!')
                break
            elif win == 0:
                print('Ничья!')
                break
            self._toggle_player()

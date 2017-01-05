from rules import EDGE_SIZE
from math import sqrt
import itertools


def getMyPointOfView(game):
    '''
    Assume that now there is enemy turn
    Returns rotated game data so that we can
    assume that on the beggining of game there
    was my checker on pos (0,0).
    :return: correctly rotated game data
    :return: list of list of (checker or None)
    '''
    myColor = not game.currentPlayer
    ret = [[None for r in range(EDGE_SIZE)] for c in range(EDGE_SIZE)]
    data = game.data
    for r in range(EDGE_SIZE):
        for c in range(EDGE_SIZE):
            if (r + c) % 2 != 0:
                assert data[r][c] is None
                continue
            if myColor == 0:
                d = data[r][c]
            else:
                d = data[EDGE_SIZE - 1 - r][EDGE_SIZE - 1 - c]
            ret[r][c] = d
    return ret


class Property:
    '''
    Base class
    '''

    def __init__(self, name):
        '''
        :param name: may be used for debugging/printing results
        '''
        self._name = name

    def evaluate(self, game):
        '''
        Assume that now there is enemy turn
        '''
        assert 0, 'This is abstract'

    def copy(self):
        return type(self)(self.name)

    @property
    def name(self):
        return self._name


class PropertyMyCheckersDistance(Property):

    def __init__(self, fun, name):
        '''
        :param fun: see evaluate method
        '''
        super().__init__(name)
        self._fun = fun

    def evaluate(self, game):
        '''
        Returns value of self._fun with list of distances
        of my checkers from the first row of the board
        as argument

        :return: self._fun(list of float)
        :rtype: float
        '''
        ret = []
        myColor = not game.currentPlayer
        board = getMyPointOfView(game)
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    assert board[r][c] is None
                    continue
                d = board[r][c]
                if d is not None and d.color == myColor:
                    ret.append(r)
        return self._fun(ret)

    def copy(self):
        return type(self)(self._fun, self._name)


class PropertyMyCheckersRadius(Property):

    def __init__(self, fun, name):
        '''
        :param fun: see evaluate method
        '''
        super().__init__(name)
        self._fun = fun

    def evaluate(self, game):
        '''
        Returns value of self._fun with list of distances
        of my checkers from the center of the board

        :return: self._fun(list of float)
        :rtype: float
        '''
        ret = []
        myColor = not game.currentPlayer
        board = getMyPointOfView(game)
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    assert board[r][c] is None
                    continue
                d = board[r][c]
                if d is not None and d.color == myColor:
                    ret.append(sqrt((EDGE_SIZE / 2 - r) **
                                    2 + (EDGE_SIZE / 2 - c)**2))
        return self._fun(ret)

    def copy(self):
        return type(self)(self._fun, self._name)


class PropertyMyCheckersRadius(Property):

    def __init__(self, fun, name):
        '''
        :param fun: see evaluate method
        '''
        super().__init__(name)
        self._fun = fun

    def evaluate(self, game):
        '''
        Returns value of self._fun with list of distances
        of my checkers from the center of the board

        :return: self._fun(list of float)
        :rtype: float
        '''
        ret = []
        myColor = not game.currentPlayer
        board = getMyPointOfView(game)
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    assert board[r][c] is None
                    continue
                d = board[r][c]
                if d is not None and d.color == myColor:
                    ret.append(sqrt((EDGE_SIZE / 2 - r) **
                                    2 + (EDGE_SIZE / 2 - c)**2))
        return self._fun(ret)

    def copy(self):
        return type(self)(self._fun, self._name)


class PropertyMyCheckersCloseness(Property):

    def __init__(self, fun, name):
        '''
        :param fun: see evaluate method
        '''
        super().__init__(name)
        self._fun = fun

    def evaluate(self, game):
        '''
        Returns value of self._fun with list of distances
        of my checkers from the center of the board

        :return: self._fun(list of float)
        :rtype: float
        '''
        ret = []
        myColor = not game.currentPlayer
        board = getMyPointOfView(game)
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    assert board[r][c] is None
                    continue
                d = board[r][c]
                if d is not None and d.color == myColor:
                    counter = 0
                    for dr, dc in itertools.product((-1, 1), (-1, 1)):
                        newR = r + dr
                        newC = c + dc
                        if not (0 <= newR < EDGE_SIZE and 0 <= newC < EDGE_SIZE):
                            continue
                        newD = board[newR][newC]
                        if newD is not None and newD.color == myColor:
                            counter += 1
                    ret.append(counter)
        return self._fun(ret)

    def copy(self):
        return type(self)(self._fun, self._name)

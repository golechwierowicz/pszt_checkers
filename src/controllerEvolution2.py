from rules import EDGE_SIZE
import random
from controller import Controller
import copy
from math import tanh


def matmul(a, b):
    a = list(map(list, a))
    b = list(map(list, b))
    assert len(a[0]) == len(b)
    assert len(a) > 0
    assert len(b[0]) > 0
    return ((sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip(*b)) for row_a in a)

INPUT_DATA_SIZE = EDGE_SIZE * (EDGE_SIZE // 2) * 3


class AIEvolution2(Controller):

    def __init__(self, layersDimensions=None):
        # TODO: add bias?
        if layersDimensions == None:
            layersCount = 2
            self._layersDimensions = [INPUT_DATA_SIZE, 8, 1]
        else:
            layersCount = len(layersDimensions) - 1
            self._layersDimensions = layersDimensions.copy()
        assert layersCount == len(self._layersDimensions) - 1
        di = self._layersDimensions

        self._layers = [
            [[0.0 for i in range(di[k])]
             for j in range(di[k + 1])]
            for k in range(layersCount)
        ]

        assert len(self._layers) == layersCount
        assert len(self._layers[0]) == self._layersDimensions[1]

        # for assertion
        self._variablesCount = sum(di[i] * di[i + 1]
                                   for i in range(len(di) - 1))
        self._checkIntegrity()

    def _generateInputData(self, game):
        """
        Convert given game state into list of floats,
        that will be used as input data for evaluation
        :param game: game state
        :type game: Game
        :return: list with input data
        :rtpye: list of floats
        """
        board = game.data
        myColor = not game.currentPlayer
        data = []
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    continue
                if myColor == 0:
                    d = board[r][c]
                else:
                    d = board[EDGE_SIZE - 1 - r][EDGE_SIZE - 1 - c]

                if d == None:
                    data += [0.0, 0.0, 1.0]
                else:
                    if d.color == myColor:
                        data += [0.0, 1.0, 0.0]
                    else:
                        data += [1.0, 0.0, 0.0]
        assert len(data) == INPUT_DATA_SIZE
        assert type(data[0]) == float
        return data

    def _calcScore(self, game):
        """
        How much I want my opponent to has such state.
        """

        data = self._generateInputData(game)
        ret = [[d] for d in data]

        assert len(self._layers) == len(self._layersDimensions) - 1
        assert len(ret) == INPUT_DATA_SIZE
        assert len(ret) == self._layersDimensions[0]
        for i, l in enumerate(self._layers):
            ret = matmul(l, ret)
            ret = list(ret)
            assert len(ret) == self._layersDimensions[i + 1]

        ret = list(ret)
        assert len(ret) == 1
        ret = list(ret[0])
        assert len(ret) == 1
        assert type(ret[0]) == float
        return ret[0]

    # def getBoardScore(self, game):
    #     """
    #     Say how much I want to be in this state
    #     """
    #     return -self._calcScore(game)

    def decideNextMove(self, board, possibleMoves):
        if len(possibleMoves) == 1:
            return possibleMoves[0]
        ret = None
        curMax = -1000 * 1000
        for pm in possibleMoves:
            state = board.getAppliedBoard(pm)
            sc = self._calcScore(state)
            if sc > curMax:
                ret = pm
                curMax = sc
        return ret

    def copy(self):
        self._checkIntegrity()
        newone = type(self)(layersDimensions=self._layersDimensions.copy())
        newone._checkIntegrity()
        newone._layers = copy.deepcopy(self._layers)
        newone._checkIntegrity()
        return newone

    def mutate(self):
        counter = 0
        for l in range(len(self._layers)):
            for r in range(len(self._layers[l])):
                for c in range(len(self._layers[l][r])):
                    self._layers[l][r][c] += random.gauss(0, 1)
                    counter += 1
        assert counter == self._variablesCount

    def serialize(self, filename):
        open(filename, 'w').write(str((self._layersDimensions, self._layers)))

    def _checkIntegrity(self):
        '''
        Check if layers has proper dimensions
        '''
        assert len(self._layersDimensions) == len(self._layers) + 1
        for i in range(len(self._layers)):
            assert len(self._layers[i]) == self._layersDimensions[i + 1]
            assert len(self._layers[i][0]) == self._layersDimensions[i]

    def deserialize(self, filename):
        self._layersDimensions, self._layers = eval(open(filename, 'r').read())
        self._checkIntegrity()

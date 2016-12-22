from rules import EDGE_SIZE
import random
from controller import Controller
import copy
from math import tanh

# numpy is somehow slower in this case
# (maybe it's because of constructing arrays in the bottleneck)


def matmul(a, b):
    return ((sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip(*b)) for row_a in a)


class AIEvolution2(Controller):

    def __init__(self, layersDimensions=None):
        # TODO: add bias?
        if layersDimensions == None:
            # self.layersCount = 2
            # self.layersDimensions = [EDGE_SIZE * (EDGE_SIZE // 2) * 3, 10, 1]
            self.layersCount = 1
            self.layersDimensions = [1, EDGE_SIZE * (EDGE_SIZE // 2) * 3]
        else:
            self.layersCount = len(layersDimensions)
            self.layersDimensions = layersDimensions.copy()
        assert self.layersCount == len(self.layersDimensions) - 1
        di = self.layersDimensions

        self.layers = [
            [[random.gauss(0, 1) for i in range(di[k + 1])]
             for j in range(di[k])]
            for k in range(self.layersCount)
        ]

        assert len(self.layers) == self.layersCount

        # for assertion
        self.variablesCount = sum(di[i] * di[i + 1]
                                  for i in range(len(di) - 1))

    def generateInputData(self, board):
        data = []
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    continue
                if self.myColor == 0:
                    d = board[r][c]
                else:
                    d = board[EDGE_SIZE - 1 - r][EDGE_SIZE - 1 - c]

                if d == None:
                    data += [0, 0, 1]
                else:
                    if d.color == self.myColor:
                        data += [0, 1, 0]
                    else:
                        data += [1, 0, 0]
        assert len(data) == EDGE_SIZE * (EDGE_SIZE // 2) * 3
        return data

    def calcScore(self, board):
        # think if I want my opponent to has such state.
        # Bigger ret means that I want it more.
        data = self.generateInputData(board)

        assert len(self.layers) == self.layersCount
        assert len(self.layers) == len(self.layersDimensions) - 1
        ret = [[d] for d in data]
        assert len(ret) == EDGE_SIZE * (EDGE_SIZE // 2) * 3
        assert len(self.layers[0]) == 1
        assert len(self.layers) == 1
        for l in self.layers:
            ret = matmul(l, ret)

        # print(list(ret))
        ret = list(ret)
        assert len(ret) == 1
        ret = list(ret[0])
        assert len(ret) == 1
        assert type(ret[0]) == float
        return ret[0]

    def getBoardScore(self, board):
        self.myColor = board.currentPlayer
        return self.calcScore(board.data)

    def decideNextMove(self, board, possibleMoves):
        self.myColor = board.currentPlayer
        if len(possibleMoves) == 1:
            return possibleMoves[0]
        ret = None
        curMax = -1000 * 1000
        for pm in possibleMoves:
            d = board.getAppliedData(pm)
            sc = self.calcScore(d)
            if sc > curMax:
                ret = pm
                curMax = sc
        return ret

    def copy(self):
        newone = type(self)()
        # newone.__dict__.update(self.__dict__)
        newone.layers = copy.deepcopy(self.layers)
        return newone

    def mutate(self):
        assert self.layersDimensions[0] == 1
        counter = 0
        for l in range(len(self.layers)):
            for r in range(len(self.layers[l])):
                for c in range(len(self.layers[l][r])):
                    self.layers[l][r][c] += random.gauss(0, 1)
                    counter += 1
        assert counter == self.variablesCount

    def serialize(self, filename):
        open(filename, 'w').write(str(self.layers))

    def deserialize(self, filename):
        self.layers = eval(open(filename, 'r').read())

from rules import EDGE_SIZE, Game
import random
from controller import Controller
import copy
from nNetwork import NNetwork

curData = []
lastData = []


def matmul(a, b):
    a = list(map(list, a))
    b = list(map(list, b))
    assert len(a[0]) == len(b)
    assert len(a) > 0
    assert len(b[0]) > 0
    return ((sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
             for col_b in zip(*b)) for row_a in a)


INPUT_DATA_SIZE = EDGE_SIZE * (EDGE_SIZE // 2) * 3


class AIEvolution3(Controller):

    def __init__(self, layersDimensions=[INPUT_DATA_SIZE, 20, 10, 1]):
        self._nNetwork = NNetwork(layersDimensions, firstRandomDeviation=0.5)
        self._nNetwork.setLearningRate(1.5)

    def packInputData(self, game):
        data = []
        self.myColor = game.currentPlayer
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    continue
                if self.myColor == 0:
                    d = game.data[r][c]
                else:
                    d = game.data[EDGE_SIZE - 1 - r][EDGE_SIZE - 1 - c]

                if d == None:
                    data += [0.0, 0.0, 1.0]
                else:
                    if d.color == self.myColor:
                        data += [0.0, 1.0, 0.0]
                    else:
                        data += [1.0, 0.0, 0.0]
        assert len(data) == EDGE_SIZE * (EDGE_SIZE // 2) * 3
        return data

    def getBoardScore(self, game):
        """
        Say how much I want to be in this state
        """
        inputData = [self.packInputData(game)]
        ret = self._nNetwork.evaluate(inputData)
        assert len(ret) == 1
        assert len(ret[0]) == 1
        return ret[0][0]

    def decideNextMove(self, game, possibleMoves):
        self.myColor = game.currentPlayer
        if len(possibleMoves) == 1:
            return possibleMoves[0]
        ret = None
        curMin = float('inf')
        for pm in possibleMoves:
            d = game.getAppliedData(pm)
            sc = self.getBoardScore(d)
            if sc < curMin:
                ret = pm
                curMin = sc
        return ret

    def copy(self):
        assert 0, 'not implemented'
        newone = type(self)()
        return newone

    def train(self, games, results):
        '''
        :param games: list of Game objects
        :param results: list of floats - expected games evaluations
        '''
        assert type(games) in (list, tuple)
        assert type(results) in (list, tuple)
        assert type(games[0]) == Game
        assert type(results[0]) == float

        inputDataList = list(map(self.packInputData, games))
        results = [[r] for r in results]

        assert len(inputDataList[0]) == INPUT_DATA_SIZE
        assert len(results[0]) == 1
        assert len(results) == len(inputDataList)
        assert type(inputDataList[0][0]) in (float, int)
        assert type(results[0][0]) == float
        self._nNetwork.train(inputDataList, results)

        # this comment below is for DEBUGGING
        # if random.random() < 0.0001:
        #    global curData, lastData

        #    games[0].printBoard(False)
        #    print('results: ',results)
        #    print('speculated: ', list(map(self.getBoardScore, games)))
        #    print('current LR: ',self._nNetwork.getLearningRate())
        #    print(self._nNetwork._data[2].get_value())

        #    curData  = [d.get_value() for d in self._nNetwork._data]
        #    if lastData != []:
        #        print('data diff:')
        #        for d1,d2 in zip(curData,lastData):
        #            for r1,r2 in zip(d1,d2):
        #                assert len(r1) == len(r2)
        #                for f1,f2 in zip(r1,r2):
        #                    if f1 != f2:
        #                        print('it is different! ',f1, f2)
        #    else:
        #        print('there is no last data yet')
        #    lastData = [d.get_value() for d in self._nNetwork._data]
        #    input()

    def serialize(self, filename):
        assert 0, 'not implemented'
        #open(filename, 'w').write(str((self.layersDimensions, self.layers)))

    def deserialize(self, filename):
        assert 0, 'not implemented'
        #self.layersDimensions, self.layers = eval(open(filename, 'r').read())

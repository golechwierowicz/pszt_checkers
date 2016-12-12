from rules import EDGE_SIZE
import random
from controller import Controller
import copy


class AIEvolution2(Controller):

    def __init__(self):
        self.coefs = [random.random()
                      for col in range(3)
                      for c in range(EDGE_SIZE // 2)
                      for r in range(EDGE_SIZE)]

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
        assert len(data) == len(self.coefs)
        return data

    def calcScore(self, board):
        # think if I want my opponent to has such state.
        # Bigger ret means that I want it more.
        data = self.generateInputData(board)
        ret = 0
        for i in range(len(data)):
            ret += data[i] * self.coefs[i]
        return ret

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
        newone.coefs = copy.deepcopy(self.coefs)
        return newone

    def mutate(self):
        for i in range(len(self.coefs)):
            if random.random() < 0.6:
                continue
            for col in range(3):
                if random.random() < 0.9:
                    self.coefs[i] += 6 * (0.51 - random.random())
                else:
                    self.coefs[i] *= 6 * (0.7 - random.random())

    def serialize(self, filename):
        open(filename, 'w').write(str(self.coefs))

    def deserialize(self, filename):
        self.coefs = eval(open(filename, 'r').read())

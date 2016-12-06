from rules import EDGE_SIZE
import random
from controller import Controller
import copy


class AISimpleEvolution1(Controller):

    def __init__(self):
        self.coefs = [[[random.random()
                        for col in range(3)]
                       for c in range(EDGE_SIZE)]
                      for r in range(EDGE_SIZE)]
        # coefs[row][collumn][color] - color==2 means that there is no checker

    def calcScore(self, data):
        # think if I want my opponent to has such state.
        # Bigger ret means that I want it more.
        ret = 0
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    continue
                d = data[r][c]
                if d == None:
                    ret += self.coefs[r][c][2]
                else:
                    ret += self.coefs[r][c][d.color]
        return ret

    def decideNextMove(self, board, possibleMoves):
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
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    continue
                if random.random() < 0.6:
                    continue
                for col in range(3):
                    if random.random() < 0.9:
                        self.coefs[r][c][col] += 6 * (0.51 - random.random())
                    else:
                        self.coefs[r][c][col] *= 6 * (0.7 - random.random())

    def serialize(self, filename):
        open(filename, 'w').write(str(self.coefs))

    def deserialize(self, filename):
        self.coefs = eval(open(filename, 'r').read())

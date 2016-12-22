from rules import EDGE_SIZE
import random
from controller import Controller
import copy


class AISimpleEvolution1(Controller):

    def __init__(self):
        self.coefs = [[[random.gauss(0, 1) if (r + c) % 2 == 0 else 0
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
                if self.myColor == 0:
                    d = data[r][c]
                else:
                    d = data[EDGE_SIZE - 1 - r][EDGE_SIZE - 1 - c]
                if d == None:
                    ret += self.coefs[r][c][2]
                else:
                    ret += self.coefs[r][c][d.color == self.myColor]
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
        counter = 0
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                if (r + c) % 2 != 0:
                    continue
                for col in range(3):
                    self.coefs[r][c][col] += random.gauss(0, 1)
                    counter += 1
        assert counter == EDGE_SIZE * (EDGE_SIZE // 2) * 3

    def serialize(self, filename):
        open(filename, 'w').write(str(self.coefs))

    def deserialize(self, filename):
        self.coefs = eval(open(filename, 'r').read())

from rules import EDGE_SIZE
import random
from controller import Controller
from math import tanh
from property import PropertyMyCheckersDistance
import pickle


class AIEvolutionProp(Controller):
    # TODO: crossing method

    def __init__(self):
        self._props = []
        self._coefs = []

        fun = lambda x: sum(x) / len(x)
        self._props.append(PropertyMyCheckersDistance(fun, 'meanDistance'))
        self._coefs.append(random.gauss(0, 1))

        fun = lambda x: max(x)
        self._props.append(PropertyMyCheckersDistance(fun, 'maxDistance'))
        self._coefs.append(random.gauss(0, 1))

        fun = lambda x: min(x)
        self._props.append(PropertyMyCheckersDistance(fun, 'minDistance'))
        self._coefs.append(random.gauss(0, 1))

        fun = lambda x: sum(map(lambda x: x * x, x)) / len(x)
        self._props.append(PropertyMyCheckersDistance(
            fun, 'meanDistanceSquare'))
        self._coefs.append(random.gauss(0, 1))

        # TODO: more properties
        # TODO: add standard deviations vector

    def _calcScore(self, game):
        '''
        How much I want my opponent to be in given state
        '''
        # for DEBUG
        # if random.random() < 0.0001:
        # #if False:
        #     print('------------------------------------------------')
        #     game.printBoard(False)
        #     print('my color: ', 'B' if not game.currentPlayer else 'B')
        #     for prop, co in zip(self._props, self._coefs):
        #         print('prop name:', prop.name)
        #         print('prop value:', prop.evaluate(game))
        #     input()

        ret = 0
        # TODO: maybe try sometching different than simple linear combination?
        for prop, coeficient in zip(self._props, self._coefs):
            ret += coeficient * prop.evaluate(game)
        return ret

    def copy(self):
        newone = type(self)()
        newone._coefs = self._coefs.copy()
        newone._props = [p.copy() for p in self._props]
        return newone

    def decideNextMove(self, board, possibleMoves):
        if len(possibleMoves) == 1:
            return possibleMoves[0]
        ret = None
        curMax = -float('inf')
        for pm in possibleMoves:
            state = board.getAppliedBoard(pm)
            sc = self._calcScore(state)
            if sc > curMax:
                ret = pm
                curMax = sc
        return ret

    def mutate(self):
        self._coefs = [c + random.gauss(0, 1) for c in self._coefs]

    def serialize(self, filename):
        pickle.dump(self._coefs, open(filename, 'wb'))

    def deserialize(self, filename):
        self._coefs = pickle.load(open(filename, 'rb'))
        assert len(self._coefs) == len(self._props)

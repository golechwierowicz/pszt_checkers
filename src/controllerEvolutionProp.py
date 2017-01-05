from rules import EDGE_SIZE
import random
from controller import Controller
from math import tanh, sqrt, exp
from property import PropertyMyCheckersDistance
from property import PropertyMyCheckersRadius
from property import PropertyMyCheckersCloseness
import pickle


class AIEvolutionProp(Controller):
    # TODO: crossing method

    def __init__(self):
        self._props = []
        self._coefs = []
        self._deviations = []

        funs = [
            ('mean', lambda x: sum(x) / len(x)),
            ('max', lambda x: max(x)),
            ('min', lambda x: min(x)),
            ('meanSquared', lambda x: sum(map(lambda x: x * x, x)) / len(x)),
        ]

        for funName, fun in funs:
            self._appendProperty(
                PropertyMyCheckersDistance(fun, funName + 'Distance'))
            self._appendProperty(
                PropertyMyCheckersRadius(fun, funName + 'Radius'))
            self._appendProperty(PropertyMyCheckersCloseness(
                fun, funName + 'Closeness'))

        # TODO: more properties

    def _appendProperty(self, property):
        self._props.append(property)
        self._coefs.append(random.gauss(0, 1))
        self._deviations.append(1.0)

    def _calcScore(self, game):
        '''
        How much I want my opponent to be in given state
        :rtype: float
        '''
        # for DEBUG
        # if random.random() < 0.0001:
        if False:
            print('------------------------------------------------')
            game.printBoard(False)
            print('my color: ', 'B' if not game.currentPlayer else 'B')
            for prop, co, devi in zip(self._props, self._coefs, self._deviations):
                print('prop name:', prop.name)
                print('prop value:', prop.evaluate(game))
                print('prop coef:', co)
                print('prop deviation:', devi)
                print()

            input()

        ret = 0
        # TODO: maybe try sometching different than simple linear combination?
        for prop, coeficient in zip(self._props, self._coefs):
            ret += coeficient * prop.evaluate(game)
        return ret

    def copy(self):
        newone = type(self)()
        newone._coefs = self._coefs.copy()
        newone._props = [p.copy() for p in self._props]
        newone._deviations = self._deviations.copy()
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
        #self._coefs = [c + random.gauss(0, 1) for c in self._coefs]
        def mutateDeviations():
            assert len(self._deviations) == len(self._coefs)
            n = len(self._deviations)
            ksi = random.gauss(0, 1)
            tau = 1 / sqrt(2 * n)
            tauLocal = 1 / sqrt(2 * sqrt(n))
            newDeviations = []
            for sigma in self._deviations:
                ksiLocal = random.gauss(0, 1)
                sigma = sigma * exp(tau * ksi + tauLocal * ksiLocal)
                newDeviations.append(sigma)
            self._deviations = newDeviations

        def mutateCoefs():
            self._coefs = [
                x + random.gauss(0, 1) * d for x, d in zip(self._coefs, self._deviations)]

        mutateDeviations()
        mutateCoefs()

    def serialize(self, filename):
        pickle.dump((self._coefs, self._deviations), open(filename, 'wb'))

    def deserialize(self, filename):
        self._coefs, self._deviations = pickle.load(open(filename, 'rb'))
        assert len(self._coefs) == len(self._props)
        assert len(self._coefs) == len(self._deviations)

from controller import AIRandom
from minimax import MiniMax
import random
from itertools import islice
from rules import Game, EDGE_SIZE

# def generateInputData(game):
#    data = []
#    board = game.data
#    myColor = game.currentPlayer
#
#    for r in range(EDGE_SIZE):
#        for c in range(EDGE_SIZE):
#            if (r + c) % 2 != 0:
#                continue
#            if myColor == 0:
#                d = board[r][c]
#            else:
#                d = board[EDGE_SIZE - 1 - r][EDGE_SIZE - 1 - c]
#
#            if d == None:
#                data += [0, 0, 1]
#            else:
#                if d.color == myColor:
#                    data += [0, 1, 0]
#                else:
#                    data += [1, 0, 0]
#    assert len(data) == EDGE_SIZE*(EDGE_SIZE//2)*3
#    return data


class StateGenerator:
    """
    Class for generating possible game states
    """

    def __init__(self, n):
        self._ai1 = AIRandom()
        self._ai2 = AIRandom()
        self._n = n

        states = []

        while(len(states) < n):
            g = Game(self._ai1, self._ai2)
            s = []
            while not g.finished():
                g.nextMove()
                if random.random() < 0.02:
                    s.append(g.copy())
            if g.getWinner() != 2:
                states += s
        self.states = states

    def __iter__(self):
        random.shuffle(self.states)
        return islice(self.states, 0, self._n)


class LearningSetGenerator:

    def __init__(self, n, depth=5, useDelta=False):
        self._n = n
        self._depth = depth
        self._useDelta = useDelta

    def _evalState(self, s):
        m = MiniMax(depth=self._depth)
        if self._useDelta:
            return min(max(m.getBoardScoreDelta(s), -12.0), 12.0)
        else:
            return min(max(m.getBoardScore(s), -12.0), 12.0)

    def __iter__(self):
        return ((s, self._evalState(s)) for s in StateGenerator(self._n))

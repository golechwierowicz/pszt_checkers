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
        self.ai1 = AIRandom()
        self.ai2 = AIRandom()
        self.n = n

        states = []

        while(len(states) < n):
            g = Game(self.ai1, self.ai2)
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
        return islice(self.states, 0, self.n)


class LearningSetGenerator:

    def __init__(self, n, depth=5):
        self.n = n
        self.depth = depth

    def evalState(self, s):
        m = MiniMax(depth=self.depth)
        return m.getBoardScore(s)

    def __iter__(self):
        return ((s, self.evalState(s)) for s in StateGenerator(self.n))

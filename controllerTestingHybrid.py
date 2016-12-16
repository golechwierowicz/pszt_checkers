from rules import EDGE_SIZE
import random
from minimax import MiniMax
import copy


# not determined, and not completely random
class AITestingHybrid(MiniMax):

    def __init__(self):
        super(AITestingHybrid, self).__init__()

    def decideNextMove(self, board, possibleMoves):
        if random.random() < 0.2:
            return super(AITestingHybrid, self).decideNextMove(board, possibleMoves)
        else:
            return random.choice(possibleMoves)

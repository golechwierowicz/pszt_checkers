#!/usr/bin/python
from collections import namedtuple

# classic version
EDGE_SIZE = 8  # must be even
HOW_MANY_ROWS_OF_CHECKERS = 3  # must be smaller than EDGE_SIZE/2


class Controller:

    def decideNextMove(self, board, possibleMoves):
        pass


class AIEvolution(Controller):

    def decideNextMove(self, board, possibleMoves):
        # TODO: implement
        raise


class AIMiniMax(Controller):

    def decideNextMove(self, board, possibleMoves):
        # TODO: implement
        raise


class Human(Controller):

    def decideNextMove(self, board, possibleMoves):
        # TODO: implement
        raise


Checker = namedtuple('Checker', [
    'p', 'type', 'color'
])
Move = namedtuple('Move', [
    'p1', 'p2', 'beatenCheckers'
])


class Board:

    def __init__(self, controller1, controller2):
        self.currentPlayer = 0
        self.controller1 = controller1
        self.controller2 = controller2

        # TODO: consider rotating coordinates by 45 degrees
        self.data = [[None for a in range(EDGE_SIZE)]
                     for b in range(EDGE_SIZE)]

        # place starting checkers
        for r in range(HOW_MANY_ROWS_OF_CHECKERS):
            # TODO: implement
            raise

    def getPossibleMoves(self):
        ret = []
        # TODO: implement
        raise
        # ex. ret.append( Move((1,2) , (2,3), listOfBeatenCheckers ) )
        return ret

    def applyMove(self, move):
        # TODO: implement
        raise

    # check if any checker reached end of the board
    # and evolve if it's true
    def evolveCheckers(self):
        # TODO: implement
        raise

    def nextMove(self):
        possibleMoves = self.getPossibleMoves()
        if currentPlayer == 0:
            nextMove = self.controller1.decideNextMove(
                self, possibleMoves)
        else:
            nextMove = self.controller2.decideNextMove(
                self, possibleMoves)
        self.currentPlayer = not self.currentPlayer
        if nextMove not in possibleMoves:
            raise 'wrong move'
        applyMove(nextMove)
        self.evolveCheckers()

    def finished(self):
        # TODO: implement
        raise
        return  # if any of players has won


# w innym pliku
def evaluate(board):
    # TODO: implement
    raise


def playGame(ai1, ai2):
    b = Board(ai1, ai2)
    while not b.finished():
        b.nextMove()
    return evaluate(b)

if __name__ == '__main__':
    # TODO: implement (evolution strategy itp.)
    print("Checkers AI for PSZT..")
    ai1 = AIEvolution()
    ai2 = AIEvolution()
    playGame(ai1, ai2)

#!/usr/bin/python
from collections import namedtuple
import random
import os

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


class AIRandom(Controller):

    def decideNextMove(self, board, possibleMoves):
        return random.choice(possibleMoves)


class Human(Controller):

    def decideNextMove(self, board, possibleMoves):
        # TODO: implement
        raise


Checker = namedtuple('Checker', [
    'p', 'color', 'type'
])
Move = namedtuple('Move', [
    'p1', 'p2', 'removedCheckers',
])


class Game:

    def __init__(self, controller1, controller2):
        self.currentPlayer = 0
        self.controller1 = controller1
        self.controller2 = controller2

        self.data = [[None for a in range(EDGE_SIZE)]
                     for b in range(EDGE_SIZE)]

        # place starting checkers
        for r in range(HOW_MANY_ROWS_OF_CHECKERS):
            for c in range(r % 2, EDGE_SIZE, 2):
                self.data[r][c] = Checker((r, c), 0, 0)
            for c in range(EDGE_SIZE - 1 - (r) % 2, -1, -2):
                r1 = EDGE_SIZE - 1 - r
                self.data[r1][c] = Checker((r1, c), 1, 0)

    def printBoard(self):
        # TODO: make it look nice, add colors itp.
        os.system('clear')
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                d = self.data[r][c]
                if type(d) == Checker:
                    if d.color == 0:
                        print('W ', end='')
                    elif d.color == 1:
                        print('B ', end='')
                    else:
                        raise 'unknown color'
                else:
                    # empty field
                    print('. ', end='')
            print()

    def getPossibleMoves(self):
        def insideBoard(p):
            return (p[0] >= 0 and p[1] >= 0
                    and p[0] < EDGE_SIZE and p[1] < EDGE_SIZE)

        def empty(p):
            return insideBoard(p) and self.data[p[0]][p[1]] == None
        # TODO: implement beating
        # this is just moving forward,
        # without possibility of beating any checkers
        # for now rules are fake for testing
        ret = []
        data = self.data
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                d = data[r][c]
                if d == None:
                    continue
                if d.color != self.currentPlayer:
                    continue
                p1 = (r, c)
                if d.color == 0:
                    p2 = (r + 1, c + 1)
                    if insideBoard(p2) and empty(p2):
                        ret.append(Move(p1, p2, ()))
                    p2 = (r + 1, c - 1)
                    if insideBoard(p2) and empty(p2):
                        ret.append(Move(p1, p2, ()))
                else:
                    p2 = (r - 1, c + 1)
                    if insideBoard(p2) and empty(p2):
                        ret.append(Move(p1, p2, ()))
                    p2 = (r - 1, c - 1)
                    if insideBoard(p2) and empty(p2):
                        ret.append(Move(p1, p2, ()))
        return ret

    def applyMove(self, move):
        p1 = move.p1
        p2 = move.p2
        data = self.data
        for ch in move.removedCheckers:
            assert data[ch[0]][ch[1]] != None
            data[ch[0]][ch[1]] = None
        assert data[p1[0]][p1[1]] != None
        assert data[p2[0]][p2[1]] == None
        data[p2[0]][p2[1]] = data[p1[0]][p1[1]]
        data[p1[0]][p1[1]] = None

    # check if any checker reached end of the board
    # and evolve it into queen if it's true
    def evolveCheckers(self):
        # TODO: implement
        pass

    def nextMove(self):
        possibleMoves = self.getPossibleMoves()
        assert len(possibleMoves) > 0
        if self.currentPlayer == 0:
            nextMove = self.controller1.decideNextMove(
                self, possibleMoves)
        else:
            nextMove = self.controller2.decideNextMove(
                self, possibleMoves)
        self.currentPlayer = not self.currentPlayer
        assert nextMove in possibleMoves
        self.applyMove(nextMove)
        self.evolveCheckers()

    def finished(self):
        # TODO: return if any of players has won
        return len(self.getPossibleMoves()) == 0

    def getWinner(self):
        # TODO: implement
        return 'not implemented'  # 0 or 1 or 2


def playGame(ai1, ai2):
    g = Game(ai1, ai2)
    g.printBoard()
    while not g.finished():
        input()  # to see anything for now
        g.nextMove()
        g.printBoard()
    return g.getWinner()

if __name__ == '__main__':
    # TODO: evolution strategy itp.
    print("Checkers AI for PSZT..")
    ai1 = AIRandom()
    ai2 = AIRandom()
    w = playGame(ai1, ai2)
    print("winner is:", w)

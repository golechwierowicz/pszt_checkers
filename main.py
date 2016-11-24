#!/bin/env python3
from controller import AIRandom
from rules import Game


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
    print("winner is:", 'B' if w else 'W')

#!/bin/env pypy3

from controllerSimpleEvolution1 import AISimpleEvolution1
from controller import AIRandom
from rules import Game
import sys

#-------------------------------------------------------------\
# in this scenario 1+1 algorithm is used to teach evolving ai |
#-------------------------------------------------------------/


def playGame(ai1, ai2):
    g = Game(ai1, ai2)
    # g.printBoard()
    while not g.finished():
        # input()  # to see anything for now
        g.nextMove()
        # g.printBoard()
    return g.getWinner()

# check how good is given ai against random choices


def checkScore(ai):
    winCounter = [0, 0]
    ai2 = AIRandom()
    for a in range(20):
        w = playGame(ai, ai2)
        winCounter[w] += 1
    # and now second player moves first
    for a in range(20):
        w = playGame(ai2, ai)
        winCounter[not w] += 1
    if winCounter[1]==0:
        # always win
        return 40
    return winCounter[0] / winCounter[1]

if __name__ == '__main__':
    # TODO: implement proper 1+1 algorithm

    # this is AI we will evolwe
    ai = AISimpleEvolution1()

    # assume that always loses
    bestScore = 0.0

    # try teaching in iterations
    for a in range(1200):
        potentialBetterAi = ai.copy()
        potentialBetterAi.mutate()
        s = checkScore(potentialBetterAi)

        if s > bestScore:
            # mutation was worth
            print('\nsuccess with score: ', s)
            ai = potentialBetterAi
            bestScore = s
        else:
            # mutation was not worth
            print('.', end='')
            sys.stdout.flush()

    # save ai data
    ai.serialize('test.ai')

    print('\nis this ai really good now?')
    print('checking with more games...')
    winCounter = [0, 0]
    ai2 = AIRandom()
    for a in range(2000):
        w = playGame(ai, ai2)
        winCounter[w] += 1
    for a in range(2000):
        w = playGame(ai2, ai)
        winCounter[not w] += 1
    if winCounter[1]==0:
        print("PERFECT !")
    else:
        print('result: ', winCounter[0] / winCounter[1])

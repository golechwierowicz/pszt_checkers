#!/bin/env pypy3

from controllerSimpleEvolution1 import AISimpleEvolution1
from controller import AIRandom
from rules import Game
import argparse
import sys
import random

#-------------------------------------------------------------\
# in this scenario 1+1 algorithm is used to teach evolving ai |
#-------------------------------------------------------------/


def playGame(ai1, ai2):
    g = Game(ai1, ai2)
    while not g.finished():
        g.nextMove()
    return g


def checkScore(ai, args):
    # check how good is given ai against random choices
    samples = args.m
    winCounter = [0.0, 0.0]
    additionalPoints = 0.0
    ai2 = AIRandom()

    for playAs in range(2):
        for a in range(samples // 2):
            if playAs == 0:
                # play as first player
                w = playGame(ai, ai2)
            else:
                w = playGame(ai2, ai)

            if w.getWinner() == playAs:
                winCounter[0] += 1
                if args.scoreCheckersCount:
                    # normal checkers
                    additionalPoints += 0.05 * w.getCheckersCount()[playAs][0]
                    # queens
                    additionalPoints += 0.15 * w.getCheckersCount()[playAs][1]
            else:
                winCounter[1] += 1
    if args.scoreCheckersCount:
        return (winCounter[0] + additionalPoints) / samples, winCounter[0] / samples
    else:
        return winCounter[0] / samples


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Teaching scenario for AISimpleEvolution1.')
    parser.add_argument('-o', '--output', help='Output file for AI data',
                        dest='outputFile', required=True)
    parser.add_argument('-n', '--number-of-iterations', help='Number of iterations of learning',
                        dest='n', default=1000, type=int)
    parser.add_argument('-m', '--number-of-samples', help='Number of games for 1 learning iteration',
                        dest='m', default=128, type=int)
    parser.add_argument('-i', '--input', help='AI data used for the beggining if learning',
                        dest='inputFile', default=None)
    parser.add_argument('-e', '--experimental-score',
                        help='While calculating score, add remaining checkers count with coeficient',
                        dest='scoreCheckersCount', action='store_true', default=False)
    parser.add_argument('-d', '--determined-cases',
                        help='Mutations and random AI behavior are determined',
                        dest='determinedCases', action='store_true', default=False)
    return parser.parse_args()

if __name__ == '__main__':

    args = parseArguments()

    # TODO: implement proper 1+1 algorithm

    # this is AI we will evolve
    ai = AISimpleEvolution1()
    if args.inputFile != None:
        ai.deserialize(args.inputFile)

    # assume that always loses
    bestScore = checkScore(ai, args)

    # try teaching in iterations
    try:
        for a in range(args.n):
            potentialBetterAi = ai.copy()
            if args.determinedCases:
                random.seed(a)
            potentialBetterAi.mutate()
            if args.determinedCases:
                random.seed(0)
            s = checkScore(potentialBetterAi, args)

            if s >= bestScore:
                # mutation was worth
                if args.scoreCheckersCount:
                    print('\nsuccess with (score, winRatio): ', s)
                else:
                    print('\nsuccess with score==winRatio: ', s)
                ai = potentialBetterAi
                bestScore = s
            else:
                # mutation was not worth
                print('.', end='')
                sys.stdout.flush()
    except KeyboardInterrupt:
        print('KeyboardInterrup catched')

    # save ai data
    print('Saving data to file')
    ai.serialize(args.outputFile)

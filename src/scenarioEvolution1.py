#!/bin/env pypy3
# as far as I know, for now only pypy2 can use numpy

from controllerSimpleEvolution1 import AISimpleEvolution1
from controllerEvolution2 import AIEvolution2
from controller import AIRandom
from controllerTestingHybrid import AITestingHybrid
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
    winCounter = [0.0, 0.0, 0.0]
    additionalPoints = 0.0

    if args.randomChoiceOpponent:
        ai2 = AIRandom()
    else:
        ai2 = AITestingHybrid()

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
                if w.getWinner() == 2:
                    winCounter[2] += 1
                winCounter[1] += 1

    if winCounter[2] > 0:
        print("Draw occured")
        # draw is like half of a win
        additionalPoints += winCounter[2] / samples / 2

    if args.scoreCheckersCount:
        return (winCounter[0] + additionalPoints) / samples, winCounter[0] / samples
    else:
        return (winCounter[0] + additionalPoints) / samples


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
    parser.add_argument('-t', '--type',
                        help='Type of AI to train',
                        dest='aiType', default='AIEvolution2')
    parser.add_argument('-r', '--random-choice-opponent',
                        help='Use random choices as an opponent in target function',
                        dest='randomChoiceOpponent', action='store_true', default=False)

    return parser.parse_args()

def initAI(args):
    # which AI we will evolve
    if args.aiType == 'AISimpleEvolution1':
        ai = AISimpleEvolution1()
        if args.inputFile != None:
            ai.deserialize(args.inputFile)
    elif args.aiType == 'AIEvolution2':
        ai = AIEvolution2()
        if args.inputFile != None:
            ai.deserialize(args.inputFile)
    else:
        raise Exception('unknown ai type')
    return ai


def onePlusOne(ai, checkScoreFun, args):
    try:
        bestScore = checkScoreFun(ai, args)
        for a in range(args.n):
            potentialBetterAi = ai.copy()
            if args.determinedCases:
                random.seed(a)
            potentialBetterAi.mutate()
            if args.determinedCases:
                random.seed(0)
            s = checkScoreFun(potentialBetterAi, args)

            if s >= bestScore:
                # mutation was beneficial
                if type(s) == tuple:
                    print('\nsuccess with (score, winRatio): ', s)
                else:
                    print('\nsuccess with score: ', s)
                ai = potentialBetterAi
                bestScore = s
            else:
                # mutation was not beneficial
                print('.', end='')
                sys.stdout.flush()
    except KeyboardInterrupt:
        print('KeyboardInterrup catched')

    # save ai data
    print('Saving data to file')
    ai.serialize(args.outputFile)

if __name__ == '__main__':

    args = parseArguments()

    # TODO: implement proper 1+1 algorithm

    ai = initAI(args)

    print('Given AI:', args.aiType)
    if args.randomChoiceOpponent:
        print('Opponent: AIRandom')
    else:
        print('Opponent: AITestingHybrid')

    onePlusOne(ai, checkScore, args)

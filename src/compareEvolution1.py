#!/bin/env pypy3
from controller import AIRandom
from controllerSimpleEvolution1 import AISimpleEvolution1
from minimax import MiniMax
from rules import Game
import argparse


def playGame(ai1, ai2):
    g = Game(ai1, ai2)
    while not g.finished():
        g.nextMove()
    return g.getWinner()


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Test AISimpleEvolution1 vs random choices')
    parser.add_argument('-i', '--input', help='Input AI data for testing',
                        dest='inputFile', default=None)
    parser.add_argument('-n', '--number-of-games', help='Number of played test games',
                        dest='n', default=3000, type=int)
    parser.add_argument('-t', '--type', help='Testing AI type',
                        dest='aiType', default='controllerSimpleEvolution1')
    return parser.parse_args()

if __name__ == '__main__':
    print("Comparing given AI with random choices...")

    args = parseArguments()

    if args.aiType == 'controllerSimpleEvolution1':
        print('Given AI: controllerSimpleEvolution1')
        ai1 = AISimpleEvolution1()
        assert args.inputFile != None
        ai1.deserialize(args.inputFile)
    elif args.aiType == 'minimax':
        print('Given AI: minimax')
        ai1 = MiniMax()
    else:
        raise 'given AI type is unknown'

    ai2 = AIRandom()

    # number of games
    n = args.n
    winCounter = [0, 0]
    for a in range(n // 2):
        w = playGame(ai1, ai2)
        winCounter[w] += 1
    for a in range(n // 2):
        w = playGame(ai2, ai1)
        winCounter[not w] += 1

    if winCounter[1] == 0:
        print("PERFECT !")
    else:
        print('result: ', winCounter[0] / n)
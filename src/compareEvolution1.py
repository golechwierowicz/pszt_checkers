#!/bin/env pypy3
from controller import AIRandom
from controllerSimpleEvolution1 import AISimpleEvolution1
from controllerEvolution2 import AIEvolution2
from controllerEvolutionProp import AIEvolutionProp

from controllerTestingHybrid import AITestingHybrid
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
                        dest='aiType', default='AIEvolution2')
    parser.add_argument('-o', '--opponent', help='Opponent for testing',
                        dest='opponent', default='AIRandom')
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArguments()

    if args.aiType in ('AISimpleEvolution1', '1'):
        ai1 = AISimpleEvolution1()
        assert args.inputFile != None
        ai1.deserialize(args.inputFile)
    elif args.aiType in ('AIEvolution2', '2'):
        ai1 = AIEvolution2()
        assert args.inputFile != None
        ai1.deserialize(args.inputFile)
    elif args.aiType in ('AINNetwork', '3'):
        from controllerNNetwork import AINNetwork
        ai1 = AINNetwork()
        assert args.inputFile != None
        ai1.deserialize(args.inputFile)
    elif args.aiType in ('AIEvolutionProp', '4', 'prop'):
        ai1 = AIEvolutionProp()
        assert args.inputFile != None
        ai1.deserialize(args.inputFile)
    elif args.aiType == 'AITestingHybrid':
        ai1 = AITestingHybrid()
    elif args.aiType == 'minimax':
        ai1 = MiniMax()
    else:
        raise BaseException('unknown ai type')

    if args.opponent in ('AITestingHybrid', 'hybrid'):
        ai2 = AITestingHybrid()
    elif args.opponent in ('AIRandom', 'random'):
        ai2 = AIRandom()
    else:
        raise BaseException('unknown ai type')

    print("Comparing:")
    print('Given AI:', args.aiType)
    print('Opponent: ', args.opponent)

    # number of games
    n = args.n
    winCounter = [0, 0, 0]
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

    print('draw ratio:', winCounter[2] / n)

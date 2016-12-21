#!/bin/env python3
from controller import AIRandom
from controllerSimpleEvolution1 import AISimpleEvolution1
from minimax import MiniMax
from rules import Game
from display import DisplayHelper
from queue import *
import argparse


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Checkers visualisation')
    parser.add_argument('-i', '--input', help='Input AI data for playting vs random choices',
                        dest='inputFile', required=True)
    return parser.parse_args()


def playGame(ai1, ai2):
    q = Queue()
#   window = DisplayHelper(q)
#   window.run()

    g = Game(ai1, ai2)
    g.printBoard()
    while not g.finished():
        q.put(g.getBoard())
        input()  # to see anything for now
        g.nextMove()
        g.printBoard()
    return g.getWinner()

if __name__ == '__main__':
    args = parseArguments()

    ai1 = MiniMax()
    ai2 = AISimpleEvolution1()
    ai2.deserialize(args.inputFile)

    w = playGame(ai2, ai1)
    w2 = playGame(ai1, ai2)

    print('Game1 result')
    if w == 2:
        print('Draw')
    else:
        print("winner is:", 'Minimax' if w else 'Evolved')

    print('Game2 result')
    if w2 == 2:
        print('Draw')
    else:
        print("winner is:", 'Evolved' if w2 else 'Minimax')

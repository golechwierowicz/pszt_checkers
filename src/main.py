#!/bin/env python3
from rules import Game
from queue import *
import argparse

from aiInfo import initAI, getAIName

display = False

def parseArguments():
    parser = argparse.ArgumentParser(
        description='Checkers visualisation')
    parser.add_argument('-t1', '--type1', help='Which AI will play white checkers',
                        dest='aiType1', default='AIRandom')
    parser.add_argument('-t2', '--type2', help='Which AI will play white checkers',
                        dest='aiType2', default='minimax')
    parser.add_argument('-i1', '--input1', help='Input AI data for aiType1',
                        dest='inputFile1', default=None)
    parser.add_argument('-i2', '--input2', help='Input AI data for aiType2',
                        dest='inputFile2', default=None)
    parser.add_argument('-r', '--reversed',
                        help='ai of type2 starts firsts',
                        dest='reversed', action='store_true', default=False)
    parser.add_argument('-d', '--display',
                        help='Show game in separate gui window ',
                        dest='display', action='store_true', default=False)
    return parser.parse_args()


def playGame(ai1, ai2):
    q = Queue()
    if display:
        from display import DisplayHelper
        window = DisplayHelper(q)
        window.run()

    g = Game(ai1, ai2)

    # for DEBUG
    # import pickle
    # g = pickle.load(open('qwe','rb'))
    # g.controller1 = ai1
    # g.controller2 = ai2

    g.printBoard()
    while not g.finished():
        q.put(g.getBoard())
        input()  # to see anything for now
        g.nextMove()
        g.printBoard()
    return g.getWinner()

if __name__ == '__main__':
    args = parseArguments()
    draw = 2

    print('starting duel:')

    if args.reversed:
        ai1 = initAI(args.aiType2, args.inputFile2)
        print('vs')
        ai2 = initAI(args.aiType1, args.inputFile1)
    else:
        ai1 = initAI(args.aiType1, args.inputFile1)
        print('vs')
        ai2 = initAI(args.aiType2, args.inputFile2)

    display = args.display

    input('Press return to start duel ...')
    w = playGame(ai1, ai2)

    print('Game result')
    if w == draw:
        print('Draw')
    else:
        print("winner is:", getAIName(ai2) if w else getAIName(ai1))

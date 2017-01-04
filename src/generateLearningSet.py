#!/usr/bin/env pypy3

from StateGenerator import LearningSetGenerator
import pickle
import argparse


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Learning set generator for scenarioEvolution2'
    )
    parser.add_argument('-o', '--output', help='Output file for AI data',
                        dest='outputFile', required=True)
    parser.add_argument('-n', '--learning-set-size', help='Size of learning set to generate',
                        dest='n', default=1000, type=int)
    parser.add_argument('-d', '--depth', help='Depth of minimax recursion',
                        dest='depth', default=3, type=int)
    parser.add_argument('--delta', help='Use minimax getBoardScoreDelta method for evaluating states',
                        dest='scoreDelta', action='store_true', default=False)
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArguments()

    lsg = LearningSetGenerator(
        n=args.n, depth=args.depth, useDelta=args.scoreDelta)

    print('generating %d samples, '
          'with depth=%d to file: %s ...' % (args.n, args.depth, args.outputFile))

    states = []
    scores = []
    for st, sc in lsg:
        states.append(st)
        scores.append(sc)

        # for DEBUG
        # print('------------')
        # st.printBoard(False)
        # print('score: ', sc)
        # with open('qwe','wb') as fi:
        #     pickle.dump(st, fi)
        # qwe = input()
        # if qwe=='q':
        #     break

    pickle.dump((states, scores), open(args.outputFile, 'wb'))

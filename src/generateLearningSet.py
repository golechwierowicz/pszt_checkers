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
    return parser.parse_args()

if __name__ == '__main__':
    args = parseArguments()

    lsg = LearningSetGenerator(n=args.n, depth=args.depth)

    print('generating %d samples, '
          'with depth=%d to file: %s ...' % (args.n, args.depth, args.outputFile))

    states = []
    scores = []
    for st, sc in lsg:
        states.append(st)
        scores.append(sc)

    pickle.dump((states, scores), open(args.outputFile, 'wb'))

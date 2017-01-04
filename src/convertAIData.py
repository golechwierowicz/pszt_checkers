#!/bin/env pypy3

from controllerSimpleEvolution1 import AISimpleEvolution1
from controllerEvolution2 import AIEvolution2
import argparse
from rules import EDGE_SIZE


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Convert SimpleEvolution to Evolution2 AI data with 1 layer')
    parser.add_argument('-o', '--output', help='',
                        dest='outputFile', required=True)
    parser.add_argument('-i', '--input', help='',
                        dest='inputFile', required=True)

    return parser.parse_args()


if __name__ == '__main__':

    args = parseArguments()

    data = eval(open(args.inputFile, 'r').read())

    newData = []
    for r in range(EDGE_SIZE):
        for c in range(EDGE_SIZE):
            if (r + c) % 2 != 0:
                continue
            assert len(data[r][c]) == 3
            assert 0 not in data[r][c]
            newData += data[r][c]

    assert type(newData[0]) == float
    assert len(newData) == EDGE_SIZE * (EDGE_SIZE // 2) * 3

    outData = [[newData]]
    open(args.outputFile, 'w').write(str(outData))

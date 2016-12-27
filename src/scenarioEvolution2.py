#!/usr/bin/env python3
'''
FIXME: investigate why it won't learn
'''
from scenarioEvolution1 import onePlusOne, initAI
from StateGenerator import LearningSetGenerator
import argparse
from controllerEvolution3 import AIEvolution3
import pickle
from rules import Game
from itertools import chain
import random
from plotUtils import Plot2Lines, PlotHistory


def parseArguments():
    parser = argparse.ArgumentParser(
        description='Teaching scenario for AIEvolution3. FIXME: investigate why it won\'t learn')
    parser.add_argument('-o', '--output', help='Output file for AI data',
                        dest='outputFile', required=False)
    parser.add_argument('-n', '--learning-set-size', help='Size of learning set to generate',
                        dest='n', default=500, type=int)
    parser.add_argument('-b', '--batch-size', help='Number of learning set elements  for 1 train iteration',
                        dest='batchSize', default=10, type=int)
    parser.add_argument('-i', '--input', help='AI data used for the beggining if learning',
                        dest='inputFile', default=None)
    parser.add_argument('-l', '--learning-set', help='Path to file with learning set',
                        dest='learningSetFilePath', default=None)
    parser.add_argument('-r', '--repeat-times', help='Number of learning set repetitions during learning',
                        dest='repeatTimes', default=300, type=int)
    parser.add_argument('-c', '--learning-rate', help='Learning rate of NN (coeficient when adding gradient)',
                        dest='learningRate', default=0.00115, type=float)
    parser.add_argument('-d', '--random-deviation', help='Deviation for randomizing begining NN data.',
                        dest='firstRandomDeviation', default=0.04, type=float)
    return parser.parse_args()


def getLearningSet(n, depth=4):
    states = []
    scores = []
    for state, score in LearningSetGenerator(n, depth):
        states.append(state)
        scores.append(score)
    return states, scores


#plot1 = Plot2Lines()


def checkScore(ai, args, data=LearningSetGenerator(10, depth=3)):
    #global plot1

    deltas = []
    for state, score in data:
        speculatedScore = ai.getBoardScore(state)

        # for DEBUGGING
        # if abs(speculatedScore)>1.0:# > 1.0 or random.random() < 0.01:
        # if random.random() < 0.003:
        if False:
            state.printBoard(False)
            print('result: ', score)
            print('speculated: ', speculatedScore)
            print(ai._nNetwork._data[2].get_value())
            print('current LR: ', ai._nNetwork.getLearningRate())
            input()

        assert abs(score) != float('inf')

        d = (speculatedScore - score)**2
        deltas.append(d)
    #plot1.update(deltas, deltas)
    return sum(deltas) / len(deltas)

if __name__ == "__main__":
    args = parseArguments()

    print('initializing AI, with learningRate=%f' % args.learningRate)
    print('firstRandomDeviation=%f' % args.firstRandomDeviation)
    ai = AIEvolution3(learningRate=args.learningRate,
                      firstRandomDeviation=args.firstRandomDeviation)

    if args.learningSetFilePath == None:
        samplesCount = args.n
        depth = 3
        print('learning set not given.')
        print('generating %d samples, '
              'with depth=%d ...' % (samplesCount, depth))
        states, scores = getLearningSet(samplesCount, depth=depth)
    else:
        states, scores = pickle.load(open(args.learningSetFilePath, 'rb'))

    assert len(states) == len(scores)
    assert type(states[0]) == Game
    assert type(scores[0]) == float

    checkingStates, checkingScores = getLearningSet(100, depth=3)
    # checkingStates, checkingScores = states, scores # for DEBUGGING
    #checkingStates, checkingScores = states[0:200],scores[0:200]

    print('begin learning with learning set of size %d, '
          'and batchSize=%d.' % (len(states), args.batchSize))
    print('learning set will be repeated %d times.' % args.repeatTimes)

    def chunks(container, chunkSize):
        zipIter = iter(container)
        return zip(*[zipIter] * chunkSize)

    historyPlot = PlotHistory(2)

    lset = list(zip(states, scores))
    counter = 0
    for q in range(args.repeatTimes):
        for batch in chunks(lset, args.batchSize):
            assert len(batch) == args.batchSize
            b = list(zip(*batch))

            assert len(b) == 2
            assert len(b[0]) == args.batchSize
            assert type(b[0][0]) == Game
            assert len(b[1]) == args.batchSize
            assert type(b[1][0]) == float

            cost = ai.train(b[0], b[1])

            if counter % (1050 // args.batchSize) == 0:
                print('after train cost:', cost)
                sc = (checkScore(ai, args, data=zip(
                    checkingStates, checkingScores)))
                print('checked cost: ', sc)
                historyPlot.entry([cost, sc])
            counter += 1

        # for DEBUGGING
        # print('-----------------next repeat')
        # sc = (checkScore(ai, args, data=zip(
        #     checkingStates, checkingScores)))
        # print('checked cost: ', sc)
        # historyPlot.entry([cost,sc])
        # print('press return to continue...')
        # DEBUG
        # ai._nNetwork.setLearningRate(ai._nNetwork.getLearningRate()/2)
        # input()

    print('learning finished')
    print('score on checking set: ', checkScore(ai, args, data=zip(
        checkingStates, checkingScores)))
    input()

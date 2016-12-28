#!/bin/env pypy3

from controllerSimpleEvolution1 import AISimpleEvolution1
from controllerEvolution2 import AIEvolution2
from controller import AIRandom, Controller
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
        description='Learning scenario for AISimpleEvolution1 and AIEvolution2.')
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
    parser.add_argument('-a', '--algorithm',
                        help='Evolutionary algorithm to be used',
                        dest='algorithm', default='onePlusOne')
    parser.add_argument('--sw', '--save-whole-population',
                        help='Save whole population after learning',
                        dest='saveWholePopulation', action='store_true', default=False)
    parser.add_argument('--lw', '--load-whole-population',
                        help='Load whole population on process beginning',
                        dest='loadWholePopulation', action='store_true', default=False)
    parser.add_argument('--mu', help='Value of mu used in some algorithms',
                        dest='mu', default=10, type=int)
    parser.add_argument('--lambda', help='Value of lambda used in some algorithms',
                        dest='lambd', default=4, type=int)

    return parser.parse_args()


def initAI(args, inputFile=None):
    # which AI we will evolve
    if args.aiType in ('AISimpleEvolution1', '1'):
        ai = AISimpleEvolution1()
        if inputFile != None:
            ai.deserialize(inputFile)
    elif args.aiType in ('AIEvolution2', '2'):
        ai = AIEvolution2()
        if inputFile != None:
            ai.deserialize(inputFile)
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

    print('Saving data to file')
    ai.serialize(args.outputFile)


def muPlusLambda(checkScoreFun, args):
    '''
    (mu + lambda) evolutionary algorithm
    :return: best individual after evolution process
    :rtype: Controller
    '''

    def reproduce(population):
        '''
        reproduce lambda individuals from given population
        '''
        # TODO: crossing
        assert isinstance(population[0], Controller)
        reproduced = [p.copy() for p in population]
        for i in range(len(reproduced)):
            reproduced[i].mutate()
        return reproduced

    def chooseBest(population, mu, args):
        l = [(checkScoreFun(i, args), i) for i in population]
        l.sort(key=lambda x: x[0])
        l.reverse()
        print('mu+lambda results sorted: ', [i[0] for i in l])
        return [i[1] for i in l][0:mu]

    def initPopulation(args):
        '''
        :return: loaded/initialized population
        '''

        if args.loadWholePopulation:
            assert args.inputFile is not None
            print('loading population of size: ', args.mu)
            print('using files:', args.inputFile +
                  '[0-' + str(args.mu - 1) + ']')
            population = [initAI(args, args.inputFile + str(i))
                          for i in range(args.mu)]
        else:
            print('initializing population of size: ', args.mu)
            ai = initAI(args, args.inputFile)
            aiType = type(ai)
            lam = args.lambd
            population = [aiType() for u in range(args.mu)]

            if args.inputFile is not None:
                print('replacing first individual with loaded individual:',
                      args.inputFile)
                population[0] = ai
        return population

    population = initPopulation(args)

    mu = args.mu
    lam = args.lambd

    try:
        for a in range(args.n):
            print('--------------------------next iteration')
            random.shuffle(population)
            temporary = population[0:lam]
            reproduced = reproduce(temporary)
            assert len(reproduced) == lam

            allOfThem = reproduced + population
            assert len(allOfThem) == mu + lam

            newPopulation = chooseBest(allOfThem, mu, args)
            assert len(newPopulation) == mu

            newCount = len([i for i in reproduced if i in newPopulation])
            oldCount = len([i for i in population if i in newPopulation])
            print('taking', newCount, 'new individuals')
            print('taking', oldCount, 'old individuals')
            assert newCount + oldCount == mu

            population = newPopulation
            assert len(population) == mu

            print()
    except KeyboardInterrupt:
        print('KeyboardInterrup catched')

    if args.saveWholePopulation:
        assert len(population) == mu
        print('Saving whole population ai data to files: ',
              args.outputFile + '[0-' + str(mu - 1) + ']')
        for i, p in enumerate(population):
            p.serialize(args.outputFile + str(i))
    else:
        bestOne = chooseBest(population, 1, args)[0]
        print('Saving best individual ai data to file: ', args.outputFile)
        bestOne.serialize(args.outputFile)

if __name__ == '__main__':
    args = parseArguments()

    print('Given AI:', args.aiType)
    if args.randomChoiceOpponent:
        print('Opponent: AIRandom')
    else:
        print('Opponent: AITestingHybrid')

    if args.algorithm in ('onePlusOne', '1'):
        print('using 1+1 algorithm')
        ai = initAI(args, args.inputFile)
        onePlusOne(ai, checkScore, args)
    elif args.algorithm in ('muPlusLambda', '2'):
        print('using mu+lambda algorithm with mu=%d, lambda=%d' %
              (args.mu, args.lambd))
        muPlusLambda(checkScore, args)

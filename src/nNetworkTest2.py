#!/usr/bin/env python3
'''
2 arguments function approximation using NNetwork
'''
from nNetwork import NNetwork
import matplotlib.pyplot as plt
import random
import math
import numpy as np
from itertools import product, islice


class LearningSetGenerator:

    def __init__(self, fun, batchSize=5):
        self._targetFun = lambda x: fun(*x)
        self._batchSize = batchSize

    def __iter__(self):
        return self

    def __next__(self):
        batch = np.array([[random.random()] for i in range(self._batchSize)])

        batch = [[random.random(), random.random()]
                 for x, y in product(range(self._batchSize), range(self._batchSize))]

        expected = np.array([[self._targetFun(b)] for b in batch])
        return batch, expected


class MyPlot:

    def __init__(self, nn, targetFun):
        self._nn = nn
        self._figure = plt.figure()
        self._targetFun = targetFun

        samplesCount = 64
        d = [[0.0 for y in range(samplesCount)] for x in range(samplesCount)]

        self._p1 = plt.subplot(3, 1, 1)
        self._p1.pcolor(d, cmap=plt.get_cmap('seismic'),
                        vmin=-np.max(np.abs(d)), vmax=np.max(np.abs(d)))

        self._p2 = plt.subplot(3, 1, 2)
        self._p2.pcolor(d, cmap=plt.get_cmap('seismic'),
                        vmin=-np.max(np.abs(d)), vmax=np.max(np.abs(d)))

        plt.show(False)

    def update(self):
        samplesCount = 64

        samples = [[x / samplesCount, y / samplesCount]
                   for x, y in product(range(samplesCount), range(samplesCount))]

        d = [[self._targetFun(x / samplesCount, y / samplesCount)
              for y in range(samplesCount)] for x in range(samplesCount)]
        self._p1.pcolor(d, cmap=plt.get_cmap('seismic'),
                        vmin=-np.max(np.abs(d)), vmax=np.max(np.abs(d)))

        d = [[self._nn.evaluate([[x / samplesCount, y / samplesCount]])[0][0]
              for y in range(samplesCount)] for x in range(samplesCount)]
        self._p2.pcolor(d, cmap=plt.get_cmap('seismic'),
                        vmin=-np.max(np.abs(d)), vmax=np.max(np.abs(d)))

        plt.pause(0.001)


def f(x, y):
    arg1 = 6 * np.pi * x
    arg2 = 6 * np.pi * y
    return math.sin(arg1) + math.sin(arg2)

nn = NNetwork([2, 30, 50, 30, 1])
lsg = LearningSetGenerator(f, batchSize=20)
mp = MyPlot(nn, f)

counter = 0
print('begin learning ...')
while True:
    try:
        for batch, expected in lsg:
            res = nn.train(batch, expected)
            if counter % 200 == 0:
                print(res)
                mp.update()
            counter += 1
    except KeyboardInterrupt:
        print('------Interrupted-choose-action---')
        print('current learning rate: ', nn.getLearningRate())
        print('current batch size: ', lsg._batchSize)
        action = input()
        if action == 'd':
            lr = nn.getLearningRate()
            newLr = lr / 2
            print('new learning rate: ', newLr)
            nn.setLearningRate(newLr)
        elif action == 's':
            print('new learning rate: ')
            newLr = float(input())
            print('setting learning rate: ', newLr)
            nn.setLearningRate(newLr)
        elif action == 'q':
            print('exitting')
            break
        elif action == 'b':
            print('new batch size: ')
            newBatchSize = int(input())
            print('setting batch size: ', newBatchSize)
            lsg = LearningSetGenerator(f, batchSize=newBatchSize)

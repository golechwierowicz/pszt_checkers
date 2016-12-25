#!/usr/bin/env python3
'''
Sine approximation using NNetwork
'''
from nNetwork import NNetwork
import matplotlib.pyplot as plt
import random
import math
import numpy as np


class LearningSetGenerator:

    def __init__(self, fun, batchSize=5):
        self._targetFun = lambda x: fun(*x)
        self._batchSize = batchSize

    def __iter__(self):
        return self

    def __next__(self):
        batch = np.array([[random.random()] for i in range(self._batchSize)])
        expected = np.array([list(map(self._targetFun, batch))])
        batch = batch.transpose()
        return batch, expected


class MyPlot:

    def __init__(self, nn, targetFun):
        self._nn = nn
        self._figure = plt.figure()
        self._targetFun = targetFun

        samplesX = [-0.5, 1.5]
        samplesY = [-1.5, 1.5]
        self._p1, = plt.plot(samplesX, samplesY)
        self._p2, = plt.plot(samplesX, samplesY)
        plt.show(False)

    def update(self):
        samplesCount = 1000
        samples = [x / samplesCount for x in range(samplesCount)]

        s1 = list(self._nn.evaluate([samples]))
        assert len(s1) == 1
        assert len(s1[0]) == len(samples)
        #s1 = [self._nn.evaluate([[s]])[0][0] for s in samples]

        s2 = list(map(self._targetFun, samples))

        self._p1.set_xdata(samples)
        self._p1.set_ydata(s1[0])
        # self._p1.set_ydata(s1)

        self._p2.set_xdata(samples)
        self._p2.set_ydata(s2)

        plt.pause(0.001)


def f(x):
    arg = 12 * np.pi * x
    return math.sin(arg)

nn = NNetwork([1, 30, 50, 30, 1])
lsg = LearningSetGenerator(f, batchSize=20)
mp = MyPlot(nn, f)

counter = 0
print('begin learning ...')
while True:
    try:
        for batch, expected in lsg:
            res = nn.train(batch, expected)
            if counter % 2000 == 0:
                print(res)
            if counter % 1000 == 0:
                mp.update()
            counter += 1
    except KeyboardInterrupt:
        print('------Interrupted-choose-action---')
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

# for a in range(len(nn._data)):
#     print('-----------------------------------------')
#     print('layer number: ',str(a))
#     print('layer data:\n',nn._data[a].get_value())
#     print('layer bias data:\n',nn._bias[a].get_value())
#     assert len(nn._data)==len(nn._bias)

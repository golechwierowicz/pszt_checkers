import theano.tensor as T
import numpy as np
from theano import function, shared, pp
import random
import math


class NNetwork:
    '''
    Generic neural network.
    '''

    def __init__(self, layersSizes, firstRandomDeviation=0.1):
        '''
        :param layersSizes: list of layers sizes: [input, hidden1, ... , output]
        :type layersSizes: list of int
        '''
        self._layersSizes = layersSizes

        def initMatrix(height, width):
            return np.array([[random.gauss(0, firstRandomDeviation)
                              for col in range(width)]for row in range(height)])

        def initVector(height):
            return np.array([random.gauss(0, firstRandomDeviation)
                             for row in range(height)])

        ldi = self._layersSizes
        self._data = [shared(initMatrix(ldi[i + 1], ldi[i]))
                      for i in range(len(ldi) - 1)]
        self._bias = [shared(initVector(ldi[i + 1]))
                      for i in range(len(ldi) - 1)]

        mx = T.dmatrix('mx')
        my = mx

        activationFun = T.nnet.relu  # seems to work best
        # activationFun = T.nnet.sigmoid
        # activationFun = T.tanh # seems to be generally worse than relu
        # activationFun = lambda x: x

        # myList = [my]
        for i in range(len(ldi) - 2):
            my = activationFun(
                T.dot(self._data[i], my) + T.reshape(self._bias[i], (ldi[i + 1], 1)))
            # myList.append(my)
        my = (T.dot(self._data[-1], my) +
              T.reshape(self._bias[-1], (ldi[-1], 1)))
        # myList.append(my)

        #my = activationFun( T.dot(self._data[0],my) + T.reshape(self._bias[0],(ldi[1],1)) )
        #my = activationFun( T.dot(self._data[1],my) + T.reshape(self._bias[1],(ldi[2],1)) )
        #my =              ( T.dot(self._data[2],my) + T.reshape(self._bias[2],(ldi[3],1)) )

        # assert len(myList) == len(self._data)+1
        self._evaluate = function(
            [mx], my
        )

        mexpect = T.dmatrix('mexpect')
        cost = T.mean((my - mexpect) * (my - mexpect))
        #cost = T.mean(my - mexpect)
        #cost = T.mean(abs((my - mexpect)))

        self._learningRate = shared(0.05)

        #delta = [0.01*a for a in T.grad(cost, self._data)]
        delta = [self._learningRate * T.grad(cost, d) for d in self._data]
        assert len(delta) == len(self._data)
        newData = [a - b for a, b in zip(self._data, delta)]
        assert len(self._data) == len(newData)

        biasDelta = [self._learningRate * T.grad(cost, d) for d in self._bias]
        assert len(biasDelta) == len(self._bias)
        newBias = [a - b for a, b in zip(self._bias, biasDelta)]
        assert len(self._bias) == len(newBias)

        self._train = function(
            [mx, mexpect], cost,
            #updates=list(zip(self._data, newData))
            updates=(
                [(self._data[i], newData[i]) for i in range(len(ldi) - 1)] +
                # (self._data[0], newData[0]),
                # (self._data[1], newData[1]),
                # (self._data[2], newData[2]),

                [(self._bias[i], newBias[i]) for i in range(len(ldi) - 1)]
                #[(self._bias[0], newBias[0]),
                #(self._bias[1], newBias[1]),
                #(self._bias[2], newBias[2]),]
            )
        )

    def evaluate(self, batch):
        '''
        :param batch: list of input vectors
        :return: list of output vectors
        '''
        assert len(batch) > 0
        assert len(batch[0]) == self._layersSizes[0]

        batch = list(zip(*batch))

        ret = list(zip(*self._evaluate(batch)))
        assert len(ret) > 0
        assert len(ret[0]) == self._layersSizes[-1]
        return ret

    def train(self, batch, expected):
        '''
        :param batch: list of input vectors
        :param expected: list of expected output vectors
        :return: cost value
        :rtype: float
        '''
        assert len(batch) > 0
        assert len(batch[0]) == self._layersSizes[0]

        assert len(expected) > 0
        assert len(expected[0]) == self._layersSizes[-1]

        batch = list(zip(*batch))
        expected = list(zip(*expected))

        assert len(batch[0]) == len(expected[0])
        assert len(batch) == self._layersSizes[0]
        assert len(expected) == self._layersSizes[-1]

        return self._train(batch, expected)

    def setLearningRate(self, value):
        self._learningRate.set_value(value)

    def getLearningRate(self):
        return self._learningRate.get_value()

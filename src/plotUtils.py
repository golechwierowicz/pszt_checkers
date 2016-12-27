import matplotlib.pyplot as plt


class Plot2Lines:

    def __init__(self):
        self._figure = plt.figure()

        samplesX = [-0.5, 1.5]
        samplesY = [-5.5, 5.5]
        self._p1, = plt.plot(samplesX, samplesY)
        self._p2, = plt.plot(samplesX, samplesY)
        plt.show(False)

    def update(self, line1, line2):
        samplesCount = len(line1)
        assert len(line1) == len(line2)

        samples = [x / samplesCount for x in range(samplesCount)]

        self._p1.set_xdata(samples)
        self._p1.set_ydata(line1)

        self._p2.set_xdata(samples)
        self._p2.set_ydata(line2)

        plt.pause(0.001)

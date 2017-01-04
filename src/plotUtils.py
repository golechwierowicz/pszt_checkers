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


class PlotHistory:

    def __init__(self, numberOfPlots):
        self._figure = plt.figure()
        self._plots = [plt.plot([-10.0, 10.0], [-10.0, 10.0])[0]
                       for i in range(numberOfPlots)]
        self._data = [[] for i in range(numberOfPlots)]

        plt.show(False)

    def entry(self, values):
        assert len(values) == len(self._plots)
        assert len(values) == len(self._data)

        for i in range(len(self._data)):
            self._data[i].append(values[i])

        xData = list(range(len(self._data[0])))
        for i, p in enumerate(self._plots):
            assert len(xData) == len(self._data[i])
            p.set_xdata(xData)
            p.set_ydata(self._data[i])

            ax = plt.gca()
            # recompute the ax.dataLim
            ax.relim()
            # update ax.viewLim using the new dataLim
            ax.autoscale_view()
            plt.draw()

        plt.autoscale(enable=True, axis='both')

        plt.pause(0.001)

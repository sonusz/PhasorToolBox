#!/usr/bin/env python3

"""
This is an real-time frequency meter of two PMUs.
This code connects to two PMUs, plot the frequency of the past 300 time-stamps and update the plot in real-time.
"""

from phasortoolbox import PDC,Client
import matplotlib.pyplot as plt
import numpy as np
import gc
import logging
logging.basicConfig(level=logging.DEBUG)


class FreqMeter(object):
    def __init__(self):
        x = np.linspace(-10.0, 0.0, num=300, endpoint=False)
        y = [60.0]*300

        plt.ion()
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(211)
        self.line1, = self.ax1.plot(x, y)
        plt.title('PMU1 Frequency Plot')
        plt.xlabel('Time (s)')
        plt.ylabel('Freq (Hz)')
        self.ax2 = self.fig.add_subplot(212)
        self.line2, = self.ax2.plot(x, y)
        plt.title('PMU2 Frequency Plot')
        plt.xlabel('Time (s)')
        plt.ylabel('Freq (Hz)')
        plt.tight_layout()

    def update_plot(self, synchrophasors):
        y_data = [[],[]]
        for synchrophasor in synchrophasors:
            for i, msg in enumerate(synchrophasor):
                y_data[i].append(msg.data.pmu_data[0].freq)

        self.line1.set_ydata(y_data[0])
        self.line2.set_ydata(y_data[1])
        self.ax1.set_ylim(min(y_data[0]),max(y_data[0]))
        self.ax2.set_ylim(min(y_data[1]),max(y_data[1]))
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        del(synchrophasors)
        gc.collect()


if __name__ == '__main__':
    pmu_client1 = Client(remote_ip='10.0.0.1', remote_port=4722, idcode=1, mode='TCP')
    pmu_client2 = Client(remote_ip='10.0.0.2', remote_port=4722, idcode=2, mode='TCP')

    fm = FreqMeter()
    pdc = PDC(clients=[pmu_client1,pmu_client2],history=300)
    pdc.callback = fm.update_plot

    pdc.run()

#!/usr/bin/env python3

"""
This is an example usage of the PDC module.
This code connects to two PMUs, collects 100 synchronized measurements, store the measurement in a buffer, and then show the content of the 10th measurement.

This example can be used to get a sample of a single PMU measurement, explore the structure of the message.
"""

import time
from datetime import datetime
import sys
from phasortoolbox import PDC
from phasortoolbox import Client
# Remove the following two lines if you don't need to print out the log.
import logging
logging.basicConfig(level=logging.DEBUG)


class SyncFreq(PDC):
    """
    This class include a synchrophasors buffer, a method to add received synchrophasors to the buffer, and a method to print the performent of the Client module.
    """
    def __init__(self):
        super(SyncFreq, self).__init__()
        self.buf = []  # The buffer store all measurement data
        self.total_perf_count = 0
        self.total_synchrophasors_count = 0


    def perf(self):
        print('{} synchrophasors received.'.format(self.total_synchrophasors_count))
        print('Average delay on each synchrophasor: {}'.format(self.total_perf_count/self.total_synchrophasors_count))


    def callback(self, synchrophasors):
        """This is the callback function for the PDC instance.
        This function should take synchrophasors as input argumnet.
        """
        now = time.perf_counter()
        self.total_perf_count += now-synchrophasors[-1].perf_counter # Check the delay since the last message is received.
        self.total_synchrophasors_count += 1
        self.buf.append(synchrophasors[-1])  # Store the synchrophasors with the newiest time stamp to buffer

        time_tag = datetime.utcfromtimestamp(
            synchrophasors[-1].time).strftime(
            "UTC: %m-%d-%Y %H:%M:%S.%f")  # Get the time tag from the message and formatting for printing

        freqlist = ''
        for my_msg in synchrophasors[-1]:
            if my_msg is None:
                freqlist += 'No Data '
            else:
                for pmu_d in my_msg.data.pmu_data:
                    freqlist += '%.4f' % (pmu_d.freq) + 'Hz '

        sys.stdout.write(
            'Time Stamp: %ss Network delay: %.4fs Local delay: %.4fs ' % (
                time_tag,
                synchrophasors[-1].arr_time - synchrophasors[-1].time,
                now - synchrophasors[-1].perf_counter
            ) + freqlist + '\r'
        )
        sys.stdout.flush()  # Print the real-time measurement


if __name__ == '__main__':
    pmus = [Client(remote_ip='10.0.0.1',remote_port=4712, idcode=1, mode='TCP'),
            Client(remote_ip='10.0.0.2',remote_port=4713, local_port=4713, idcode=2, mode='UDP')]

    pdc = SyncFreq()
    pdc.clients=pmus
    pdc.run(100)
    pdc.perf()
    synchrophasor = pdc.buf[10]
    synchrophasor.show()


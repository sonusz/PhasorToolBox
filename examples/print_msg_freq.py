#!/usr/bin/env python3

"""
This is an example usage of the Client module.
This code connects to single PMU, collects 100 measurements, store the measurement in a buffer, and then show the content of the 10th measurement.

This example can be used to get a sample of a single PMU measurement, explore the structure of the message.
"""

import time
from datetime import datetime
import sys
from phasortoolbox import PDC
from phasortoolbox import Client
# Remove the following two lines if you don't need to print out the log.
import gc
import logging
logging.basicConfig(level=logging.DEBUG)


class MsgFreq(object):
    """
    This class include a message buffer, a method to add received message to the buffer, and a method to print the performent of the Client module.
    """
    def __init__(self):
        self.buf = []  # The buffer store all measurement data
        self.total_perf_count = 0

    def perf(self):
        print('{} messages received.'.format(len(self.buf)))
        print('Average delay on each messages: {}'.format(self.total_perf_count/len(self.buf)))

    def add_msg(self, msg):
        """This is the callback function for the Client instance.
        This function should take msg as input argumnet.
        """
        now = time.perf_counter()
        self.total_perf_count += now-msg.perf_counter  # Check the delay since the message is received.

        self.buf.append(msg)  # Store the message to buffer

        time_tag = datetime.utcfromtimestamp(
            msg.time).strftime(
            "UTC: %m-%d-%Y %H:%M:%S.%f")  # Get the time tag from the message and formatting for printing

        freqlist = ' '.join("%.4fHz " % (
            pmu_d.freq) for pmu_d in msg.data.pmu_data)  # Get all frequency measurements in the message

        sys.stdout.write(
            "Time Stamp: %ss Network delay: %.4fs Local delay: %.4fs " % (
                time_tag,
                msg.arr_time - msg.time,
                now - msg.perf_counter
            ) + freqlist + "\r"
        )
        sys.stdout.flush()  # Print the real-time measurement


if __name__ == '__main__':

    pmu_client1 = Client(remote_ip='10.0.0.1',remote_port=4712, idcode=1, mode='TCP')  # Example usage of the Client module
    mf = MsgFreq()  # This is your class
    pmu_client1.callback = mf.add_msg  # Assign your function to the client instance
    pmu_client1.run(100)  # Run and stop after received 100 measurements
    mf.perf()  # Check performance
    msg = mf.buf[10]  # Get the 10th message in the buffer
    msg.show()  # Show the 10th message
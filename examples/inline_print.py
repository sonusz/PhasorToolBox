#!/usr/bin/env python

import sys
import time
from datetime import datetime
from phasortoolbox import Client, PDC, UDPDevice, DeviceControl


def inline_print_freq(buffer_msgs):

    now = time.time()

    time_tag = datetime.utcfromtimestamp(
        buffer_msgs[-1][0].time).strftime(
        "UTC: %m-%d-%Y %H:%M:%S.%f")

    freqlist = [pmu_d.freq for msg in buffer_msgs[-1]
                for pmu_d in msg.data.pmu_data]

    freq_str = ' '.join("%.4f" % (
        my_msg) + 'Hz ' if my_msg is not None else
        'No Data' for
        my_msg in freqlist)

    sys.stdout.write(
        "Network delay:%.4fs Software delay:%.4fs " % (
            now - buffer_msgs[-1][0].time,
            now - max([_msg._arrtime for _msg in buffer_msgs[-1]])
        ) + time_tag + " " + freq_str + "\r"
    )
    sys.stdout.flush()


def main():

    pmu7 = Client(SERVER_IP='10.0.0.7',
                  SERVER_TCP_PORT=4712, IDCODE=7, MODE='TCP')
    pmu9 = Client(SERVER_IP='10.0.0.9',
                  SERVER_TCP_PORT=4712, IDCODE=9, MODE='TCP')
    pdc = PDC()
    pdc.CALLBACK = inline_print_freq

    dc = DeviceControl()
    dc.device_list = [pmu7, pmu9, pdc]
    dc.connection_list = [
        [[pmu7, pmu9], [pdc]]
    ]

    dc.run()


if __name__ == '__main__':
    main()

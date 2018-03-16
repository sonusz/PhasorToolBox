#!/usr/local/bin/env python3

import sys
import time
from datetime import datetime
from phasortoolbox import Client, PDC, DeviceControl


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
    return [time_tag]+freqlist


class data_writer(object):

    def __init__(self, file):
        self.file = file

    def write_(self, buffer_msgs):

        freqlist = inline_print_freq(buffer_msgs)
        with open(self.file, 'a') as f:
            f.write(','.join([str(freq) for freq in freqlist]))
            f.write('\n')


def main():

    my_writer = data_writer('freq_sample.txt')

    my_pmus = [
        Client(SERVER_IP='10.0.0.5', SERVER_TCP_PORT=4712, IDCODE=5),
        Client(SERVER_IP='10.0.0.6', SERVER_TCP_PORT=4712, IDCODE=6),
        Client(SERVER_IP='10.0.0.7', SERVER_TCP_PORT=4712, IDCODE=7),
        Client(SERVER_IP='10.0.0.8', SERVER_TCP_PORT=4712, IDCODE=8),
    ]

    my_pdc = PDC(count=300)
    my_pdc.CALLBACK = my_writer.write_

    my_devices = DeviceControl()
    my_devices.device_list = my_pmus + [my_pdc]
    my_devices.connection_list = [[my_pmus, [my_pdc]]]

    my_devices.run()


if __name__ == '__main__':
    main()

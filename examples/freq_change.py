#!/usr/bin/env python

import sys
import time
from datetime import datetime
from phasortoolbox import Client, PDC, UDPDevice, DeviceControl


def freq_change(buffer_msgs):
    now = time.time()
    time_tag = datetime.utcfromtimestamp(
        buffer_msgs[-1][0].time).strftime(
        "UTC: %m-%d-%Y %H:%M:%S.%f")
    old_freqlist = [pmu_d.freq for msg in buffer_msgs[-2]
                    for pmu_d in msg.data.pmu_data]
    current_freqlist = [pmu_d.freq for msg in buffer_msgs[-1]
                        for pmu_d in msg.data.pmu_data]
    freq_change_list = [current_freqlist[i] - old_freqlist[i]
                        for i in range(len(current_freqlist))]
    freq_change_str = ' '.join("%.4f" % (
        my_msg) + 'Hz ' for
        my_msg in freq_change_list)
    sys.stdout.write(
        "Network delay:%.4fs Software delay:%.4fs " % (
            now - buffer_msgs[-1][0].time,
            now - max([_msg._arrtime for _msg in buffer_msgs[-1]])
        ) + time_tag + " " + freq_change_str + "\r"
    )
    sys.stdout.flush()


def main():
    pmu7 = Client(SERVER_IP='10.0.0.7',
                  SERVER_TCP_PORT=4712, IDCODE=7, MODE='TCP')
    pmu9 = Client(SERVER_IP='10.0.0.9',
                  SERVER_TCP_PORT=4712, IDCODE=9, MODE='TCP')
    pdc = PDC(BUF_SIZE=2)
    pdc.CALLBACK = freq_change
    dc = DeviceControl()
    dc.device_list = [pmu7, pmu9, pdc]
    dc.connection_list = [
        [[pmu7, pmu9], [pdc]]
    ]
    dc.run()


if __name__ == '__main__':
    main()

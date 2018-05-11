import time
from datetime import datetime
import sys
from phasortoolbox import PDC
from phasortoolbox import Client


class MsgFreq(object):
    def __init__(self, sample=False):
        self.buf = []
        self.sample = sample
        self.c = 0
        self.total_perf_count = 0

    def perf(self):
        print('{} messages received.'.format(self.c))
        print('Average delay on each messages: {}'.format(self.total_perf_count/self.c))

    def add_msg(self, msg):
        now = time.perf_counter()
        self.c += 1
        self.total_perf_count += now-msg.perf_counter
        if self.sample:
            self.buf.append(msg)
        time_tag = datetime.utcfromtimestamp(
            msg.time).strftime(
            "UTC: %m-%d-%Y %H:%M:%S.%f")
        freqlist = ' '.join("%.4fHz " % (
            pmu_d.freq) for pmu_d in msg.data.pmu_data)
        sys.stdout.write(
            "Time Stamp: %ss Network delay: %.4fs Local delay: %.4fs " % (
                time_tag,
                msg.arr_time - msg.time,
                now - msg.perf_counter
            ) + freqlist + "\r"
        )
        sys.stdout.flush()


if __name__ == '__main__':

    pmu_client1 = Client(remote_ip='10.0.0.1',remote_port=4712, idcode=1, mode='TCP')
    mf = MsgFreq(sample=True)
    pmu_client1.callback = mf.add_msg
    pmu_client1.run(100)
    mf.perf()
    msg = mf.buf[10]
    msg.show()
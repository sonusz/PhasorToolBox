import time
from datetime import datetime
import sys

class SyncFreq(object):
    def __init__(self, sample=False):
        self.buf = []
        self.sample = sample
        self.c = 0
        self.total_perf_count = 0

    def perf(self):
        print('{} synchrophasors received.'.format(self.c))
        print('Average delay on each synchrophasor: {}'.format(self.total_perf_count/self.c))

    def add_msg(self, synchrophasors):
        now = time.perf_counter()
        self.c += 1
        self.total_perf_count += now-synchrophasors[-1].perf_counter
        if self.sample:
            self.buf.append(synchrophasors)
        time_tag = datetime.utcfromtimestamp(
            synchrophasors[-1].time).strftime(
            "UTC: %m-%d-%Y %H:%M:%S.%f")
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
        sys.stdout.flush()


if __name__ == '__main__':
    pmu_client1 = Client(remote_ip='10.0.0.1',remote_port=4712, idcode=1, mode='TCP')
    pmu_client2 = Client(remote_ip='10.0.0.2',remote_port=4713, local_port=4713, idcode=2, mode='UDP')

    sf = SyncFreq()
    pdc = PDC(clients=[pmu_client1,pmu_client2])
    
    pdc.callback = sf.add_msg
    pdc.run(100)
    sf.perf()

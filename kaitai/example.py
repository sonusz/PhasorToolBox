#!/usr/bin/env python3

from common import Common
from timeit import default_timer as timer
import cProfile

def parse_stream():
    file = open('/Users/s/Dropbox/SouceTree/PhasorToolBox/samples/stream.bin', 'rb')
    raw_data = file.read()
    t0 = timer()
    P = Synchrphasor(raw_data)
    for message in P.message:
        try:
            print(message.data.pmu_data[0].freq.freq.freq)
        except Exception as e:
            print(e)
            pass
    t1 = timer()
    print('Time per message:', (t1 - t0)/len(P.message))

if __name__ == '__main__':
    #cProfile.run('parse_stream()')
    parse_stream()
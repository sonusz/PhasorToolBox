from parser import Parser
from timeit import default_timer as timer
import cProfile, pstats, io

def parse_stream():
    file = open('/Users/s/Dropbox/SouceTree/PhasorToolBox/samples/stream.bin', 'rb')
    raw_data = file.read()
    t0 = timer()
    p = Parser(raw_data)
    for message in p.message:
        try:
            print(message.data.pmu_data[0].freq.freq.freq)
            pass
        except Exception as e:
            print(e)
            pass
    t1 = timer()
    print('Time per message:', (t1 - t0)/len(p.message))




if __name__ == '__main__':
    #cProfile.run('parse_stream()')
    parse_stream()
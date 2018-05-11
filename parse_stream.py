#!/usr/bin/env python3

"""
Some examples as well as a simple performance test to parse C37.118 binary data stream using phasortoolbox.Parser module
"""
import sys
import time
import phasortoolbox

def parse_test(binary_data):
    my_parser = phasortoolbox.Parser()
    return my_parser.parse(binary_data)

if __name__ == '__main__':
    print('Read binary data from file...')
    with open(sys.argv[1], "rb") as f:
        binary_data = f.read()

    print('Performance test...')
    start = time.perf_counter()
    measurement_data = parse_test(binary_data)
    result = time.perf_counter() - start
    print('\n',len(measurement_data),'packets parsed in',result,'seconds')
    print('Time takes per packet:',\
        result / len(measurement_data))

    print('\nSome example usage:')
    print('Packet type of the first packet: ', \
        measurement_data[0].sync.frame_type.name)
    print('The command in the second packet: ', \
        measurement_data[1].data.cmd.name)
    print('The name of the first station in stream ID', \
        measurement_data[2].idcode ,':', measurement_data[2].data.station[0].stn.name)
    print('Frequency measurement in packet 200:', \
        measurement_data[199].data.pmu_data[1].freq,'Hz')

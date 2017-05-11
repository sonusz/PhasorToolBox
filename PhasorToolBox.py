#!/usr/bin/env python3

"""
Use one RawStreamIO object to handle multiple inputs and outputs
For each RawStream, use one RawStreamParser to parse the raw stream
"""

from multiprocessing import Process, Pipe

import traceback


def reader(args):
    try:
        # Insert stuff to be multiprocessed here
        return args[0]['that']
    except:
        print "FATAL: reader({0}) exited while multiprocessing".format(args)
        traceback.print_exc()

class RawStreamIO(object):  # Get data stream from either real-time traffic or pcap(ng) files
    def __init__(self):
        self.data = []
    def RealTime(self,ips):  # Get data stream from hardware PMU
        stream=0
        return rawStreams
    def Pcap(self,pcapDirectory):  # Get data stream from pcap files
        stream=0
        return rawStreams

class RawStreamParser(object):
    def __init__(self):
        self.CF2=()
    def Parser(self):

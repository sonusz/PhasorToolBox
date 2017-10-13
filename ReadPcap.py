#!/usr/bin/env python3

import os
from timeit import default_timer as timer
from pcap import Pcap

fn = "/root/Dropbox/SouceTree/PhasorToolBox/411R3.pcap"

sum = 0

t1 = timer()

r = Pcap.from_file(fn)

t2 = timer()

for packet in r.packets:
    try:
        eth = packet.ethernet_body.ipv4_body
        if eth:
            try:
                ipv4 = eth.ipv4_body
                if ipv4:
                    sum += ipv4.total_length
            except Exception as e:
                #raise e
                pass
    except Exception as e:
        #raise e
        pass

t3 = timer()
    
print("sum = %d" % sum)
print(t2 - t1)
print(t3 - t2)
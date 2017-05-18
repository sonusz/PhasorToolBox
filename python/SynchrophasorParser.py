#!/usr/bin/env python3

from kaitaistruct import KaitaiStream, BytesIO
from common import Common
from command import Command
from cfg_2 import Cfg2
from cfg_2_station import Cfg2Station
from timeit import default_timer as timer
import cProfile

def parse_cmd():
    """
Parse a command packet:
"""
    file = open('common_command.bin','rb')
    payload = file.read()
    print('Payload:',payload)
    stream = KaitaiStream(BytesIO(payload))
    obj = Common(stream)
    print('Packet type:', obj.sync.frame_type.name)
    print('Synchrphasor data frame(s):', obj.data)
    
    stream = KaitaiStream(BytesIO(obj.data))
    obj = Command(stream)
    print('Synchrphasor command code:', obj.cmd.name)


def parse_cfg2():
    """
Parse a cfg-2 packet:
"""
    file = open('common_cfg2.bin','rb')
    payload = file.read()
    s=0.0
    t1 = timer()
    for i in range(1000):
        stream = KaitaiStream(BytesIO(payload))
        obj = Common(stream)
        #print('Packet type:', obj.sync.frame_type.name)
        print(obj.sync.frame_type)
        print(obj.data)
        ##print('Time Base:', obj.time_base.time_base)
        ##print('Number of PMUs:', obj.num_pmu)
        #for i in range(obj.num_pmu):
        #    #print('Station name: \"', obj.station[i].stn.name, end='\" [')
        #    for j in range(obj.station[i].phnmr):
        #        #print(obj.station[i].phunit[j].voltage_or_current.name, end='|')
        #        s+=obj.station[i].phunit[j].raw_conversion_factor
        #    #print(']')

    t2 = timer()
    print('s:',s,'everage time:',(t2-t1)/10000.0)   

if __name__ == '__main__':
    #parse_cmd()
    cProfile.run('parse_cfg2()')
    #parse_cfg2()
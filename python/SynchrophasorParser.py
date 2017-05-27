#!/usr/bin/env python3

import sys
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from collections import defaultdict
from common import Common
from minicfg import MiniCfg
from timeit import default_timer as timer
import cProfile


class Synchrphasor(object):
    def __init__(self, raw_byte: bytes = None, cfg_pkt: bytes = None):  # Add cfg
        """

        :type cfg_pkt: configuration packet raw data
        """
        self.raw_data = raw_byte
        self.cfg_pkt = cfg_pkt
        self.message = []
        if self.raw_data:
            self.parse()

    def parse(self):
        _io = KaitaiStream(BytesIO(self.raw_data))
        if self.cfg_pkt:
            self._mini_cfg = MiniCfg(self.cfg_pkt)
        else:
            self._mini_cfg = None
            print('Try parsing without configuration frame.')
        while not _io.is_eof():
            pkt = Common(_io, _mini_cfg = self._mini_cfg)
            if (pkt.sync.frame_type.name == 'configuration_frame_2') or (pkt.sync.frame_type.name == 'configuration_frame_3'):
                self._mini_cfg = MiniCfg(pkt.pkt)
            self.message.append(pkt)

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
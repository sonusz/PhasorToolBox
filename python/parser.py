#!/usr/bin/env python3

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from common import Common
from minicfg import MiniCfgs


class Parser(object):
    def __init__(self, raw_byte: bytes = None, cfg_pkts: bytes = None):  # Add cfg
        """
        This is used to parse bytes packet or stream.
        :type cfg_pkt: configuration packet raw data
        """
        self.raw_data = raw_byte
        self._mini_cfgs = MiniCfgs()
        if cfg_pkts:
            _io = KaitaiStream(BytesIO(cfg_pkts))
            while not _io.is_eof():
                pkt = Common(_io)
                self._mini_cfgs.add_cfg(pkt.pkt)
        self.message = []
        if self.raw_data:
            self.parse(self.raw_data)

    def parse(self, raw_byte: bytes):
        self.raw_data = raw_byte
        _io = KaitaiStream(BytesIO(self.raw_data))
        while not _io.is_eof():
            pkt = Common(_io, _mini_cfgs = self._mini_cfgs)
            if (pkt.sync.frame_type.name == 'configuration_frame_2') or (pkt.sync.frame_type.name == 'configuration_frame_3'):
                self._mini_cfgs.add_cfg(pkt.pkt)
            self.message.append(pkt)


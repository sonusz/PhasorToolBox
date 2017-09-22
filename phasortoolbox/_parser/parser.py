#!/usr/bin/env python3

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from .common import Common
from .minicfg import MiniCfgs


class Parser(object):
    def __init__(self, _bytes: bytes = None, raw_cfg_pkt: bytes = None):
        """
        This is used to parse bytes packet or stream.
        :type cfg_pkt: configuration packet raw data
        """

        self._raw_data = _bytes
        self._mini_cfgs = MiniCfgs()
        if raw_cfg_pkt:
            _io = KaitaiStream(BytesIO(raw_cfg_pkt))
            while not _io.is_eof():
                pkt = Common(_io)
                self._mini_cfgs.add_cfg(pkt.raw_pkt)
        if self._raw_data:
            self.parse(self._raw_data)

    def parse(self, raw_byte: bytes):
        message = []
        self._raw_data = raw_byte
        _io = KaitaiStream(BytesIO(self._raw_data))
        while not _io.is_eof():
            pkt = Common(_io, _mini_cfgs = self._mini_cfgs)
            if (pkt.sync.frame_type.name == 'configuration_frame_2') or (pkt.sync.frame_type.name == 'configuration_frame_3'):
                self._mini_cfgs.add_cfg(pkt.raw_pkt)
            message.append(pkt)
        return message


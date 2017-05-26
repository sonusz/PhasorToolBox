#!/usr/bin/env python3

import sys
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from common import Common

class MiniCfg(object):
    def __init__(self, cfg_pkt):
        io = KaitaiStream(BytesIO(cfg_pkt))
        self._cfg_pkt = Common(io)
        self._type = self._cfg_pkt.sync.frame_type.name
        self._cfg = self._cfg_pkt.data
        self.num_pmu = self._cfg.num_pmu
        self.time_base = self.TimeBase(self._cfg.time_base)
        self.station = [None] * (self.num_pmu)
        for i in range(self.num_pmu):
            self.station[i] = self.Station(self._cfg.station[i])

    class TimeBase(object):
        def __init__(self, _time_base):
            self._time_base = _time_base
            self.time_base = self._time_base.time_base

    class Station(object):
        def __init__(self, _station):
            self._station = _station
            self.format = self.Format(self._station.format)
            self.phnmr = self._station.phnmr
            self.annmr = self._station.annmr
            self.dgnmr = self._station.dgnmr
            self.phunit = [None] * self.phnmr
            for i in range(self.phnmr):
                self.phunit[i] = self.Phunit(self._station.phunit[i])
            self.anunit = [None] * self.annmr
            for i in range(self.annmr):
                self.anunit[i] = self.Anunit(self._station.anunit[i])
            self.digunit = [None] * self.dgnmr
            for i in range(self.dgnmr):
                self.digunit[i] = self.Digunit(self._station.digunit[i])

        class Format(object):
            def __init__(self, _format):
                self._format = _format
                self.unused = self.unused.name
                self.freq_data_type = self.freq_data_type.name
                self.analogs_data_type = self.analogs_data_type.name
                self.phasors_data_type = self.phasors_data_type.name
                self.rectangular_or_polar = self.rectangular_or_polar.name

        class Phunit(object):
            def __init__(self, _phunit):
                self._phunit = _phunit
                self.conversion_factor = self._phunit.conversion_factor

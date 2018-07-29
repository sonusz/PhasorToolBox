#!/usr/bin/env python3

from collections import defaultdict, UserList
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from .common import PhasorMessage


class MiniCfgs(object):
    def __init__(self):
        self.mini_cfg = defaultdict(lambda: None)

    def add_cfg(self, _cfg_pkt_idcode, _cfg_pkt_data):
        self.mini_cfg[_cfg_pkt_idcode] = MiniCfg(_cfg_pkt_data)


class MiniCfg(object):
    def __init__(self, _cfg_pkt_data):
        #io = KaitaiStream(BytesIO(cfg_pkt))
        #self._cfg_pkt = Common(io)
        #self._type = self._cfg_pkt.sync.frame_type.name
        #self._cfg = self._cfg_pkt.data
        self.num_pmu = _cfg_pkt_data.num_pmu
        self.time_base = self.TimeBase(_cfg_pkt_data.time_base)
        self.station = [None] * (self.num_pmu)
        for i in range(self.num_pmu):
            self.station[i] = self.Station(_cfg_pkt_data.station[i])

    class TimeBase(object):
        def __init__(self, _time_base):
            self.time_base = _time_base.time_base

    class Station(object):
        def __init__(self, _station):
            self._station = _station
            self.stn = self._station.stn.name
            self.format = self.Format(self._station.format)
            self.phnmr = self._station.phnmr
            self.annmr = self._station.annmr
            self.dgnmr = self._station.dgnmr
            self.phunit = [None] * self.phnmr
            for i in range(self.phnmr):
                self.phunit[i] = self.Phunit(self._station.phunit[i], self._station.chnam.phasor_names[i].name)
            self.anunit = [None] * self.annmr
            for i in range(self.annmr):
                self.anunit[i] = self.Anunit(self._station.anunit[i], self._station.chnam.analog_names[i].name)
            self.digunit = [None] * self.dgnmr
            for i in range(self.dgnmr):
                self.digunit[i] = self.Digunit(self._station.digunit[i], self._station.chnam.digital_status_labels[i*16: (i+1)*16])
            self.fnom = self._station.fnom

        class Format(object):
            def __init__(self, _format):
                self.unused = _format.unused
                self.freq_data_type = _format.freq_data_type.name[:]
                self.analogs_data_type = _format.analogs_data_type.name[:]
                self.phasors_data_type = _format.phasors_data_type.name[:]
                self.rectangular_or_polar = _format.rectangular_or_polar.name[:]

        class Phunit(object):
            def __init__(self, _phunit, name):
                self.conversion_factor = _phunit.conversion_factor
                self.name = name

        class Anunit(object):
            def __init__(self, _anunit, name):
                self.conversion_factor = _anunit.conversion_factor
                self.name = name

        class Digunit(UserList):
            def __init__(self, _digunit, names):
                self.data = [None] * 16
                for i in range(16):
                    self.data[i] = self.Flag(
                        names[i],
                        _digunit.normal_status[i],
                        _digunit.current_valid_inputs[i]
                        )

            class Flag(object):
                def __init__(self, name, normal_status, current_valid_input):
                    self.name = name.name
                    self.normal_status = normal_status
                    self.current_valid_input = current_valid_input


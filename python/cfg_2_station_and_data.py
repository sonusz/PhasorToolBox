# This is a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import array
import struct
import zlib
from enum import Enum
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception("Incompatible Kaitai Struct Python API: 0.7 or later is required, but you have %s" % (ks_version))

from cfg_2_station import Cfg2Station
class Cfg2StationAndData(KaitaiStruct):
    def __init__(self, _io, _parent=None, _root=None):
        self._io = _io
        self._parent = _parent
        self._root = _root if _root else self
        self.station = Cfg2Station(self._io)
        self.stat = self._root.Stat(self._io, self, self._root)
        self.phasors = [None] * (self._root.station.phnmr)
        for i in range(self._root.station.phnmr):
            self.phasors[i] = self._root.Phasors(self._io, self, self._root)

        self.freq = self._root.Freq(self._io, self, self._root)
        self.dfreq = self._root.Dfreq(self._io, self, self._root)
        self.analog = [None] * (self._root.station.annmr)
        for i in range(self._root.station.annmr):
            self.analog[i] = self._root.Analog(self._io, self, self._root)

        self.digital = [None] * (self._root.station.dgnmr)
        for i in range(self._root.station.dgnmr):
            self.digital[i] = self._io.read_bits_int(16)


    class Freq(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            _on = self._root.station.format.freq_data_type
            if _on == False:
                self.freq = self._root.Freq.Int(self._io, self, self._root)
            elif _on == True:
                self.freq = self._root.Freq.Float(self._io, self, self._root)

        class Int(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.raw_freq = self._io.read_s2be()

            @property
            def freq(self):
                if hasattr(self, '_m_freq'):
                    return self._m_freq if hasattr(self, '_m_freq') else None

                self._m_freq = ((self.raw_freq / 1000.0) + self._root.station.fnom.fundamental_frequency)
                return self._m_freq if hasattr(self, '_m_freq') else None


        class Float(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.raw_freq = self._io.read_f4be()

            @property
            def freq(self):
                if hasattr(self, '_m_freq'):
                    return self._m_freq if hasattr(self, '_m_freq') else None

                self._m_freq = self.raw_freq
                return self._m_freq if hasattr(self, '_m_freq') else None



    class Stat(KaitaiStruct):

        class PmuTimeQualityEnum(Enum):
            not_used = 0
            estimated_maximum_time_error_less_than_100_nanosecond = 1
            estimated_maximum_time_error_less_than_1_microsecond = 2
            estimated_maximum_time_error_less_than_10_microsecond = 3
            estimated_maximum_time_error_less_than_100_microsecond = 4
            estimated_maximum_time_error_less_than_1_ms = 5
            estimated_maximum_time_error_less_than_10_ms = 6
            estimated_maximum_time_error_larger_than_10_ms_or_time_error_unknown = 7

        class TriggerReasonEnum(Enum):
            manual = 0
            magnitude_low = 1
            magnitude_high = 2
            phase_angle_diff = 3
            frequency_high_or_low = 4
            df_or_dt_high = 5
            reserved = 6
            digital = 7

        class PmuTriggerDetectedEnum(Enum):
            no_trigger = 0
            trigger_detected = 1

        class ConfigurationChangeEnum(Enum):
            change_effected = 0
            will_change_in_one_min = 1

        class DataModifiedEnum(Enum):
            not_modified = 0
            data_modified_by_post_processing = 1

        class PmuSyncEnum(Enum):
            in_sync_with_a_utc_traceable_time_source = 0
            not_in_sync_with_a_utc_traceable_time_source = 1

        class DataSortingEnum(Enum):
            by_time_stamp = 0
            by_arrival = 1

        class DataErrorEnum(Enum):
            good_measurement_data_no_errors = 0
            pmu_error_no_information_about_data_do_not_use = 1
            pmu_in_test_mode_or_absent_data_tags_have_been_insereted_do_not_use = 2
            pmu_error_do_not_use = 3

        class UnlockedTimeEnum(Enum):
            sync_locked_or_unlocked_less_than_10_s_best_quality = 0
            unlocked_time_less_than_100_s_larger_than_10_s = 1
            unlocked_time_less_than_1000_s_larger_than_100_s = 2
            unlocked_time_larger_than_1000_s = 3
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            self.data_error = self._root.Stat.DataErrorEnum(self._io.read_bits_int(2))
            self.pmu_sync = self._root.Stat.PmuSyncEnum(self._io.read_bits_int(1))
            self.data_sorting = self._root.Stat.DataSortingEnum(self._io.read_bits_int(1))
            self.pmu_trigger_detected = self._root.Stat.PmuTriggerDetectedEnum(self._io.read_bits_int(1))
            self.configuration_change = self._root.Stat.ConfigurationChangeEnum(self._io.read_bits_int(1))
            self.data_modified = self._root.Stat.DataModifiedEnum(self._io.read_bits_int(1))
            self.pmu_time_quality = self._root.Stat.PmuTimeQualityEnum(self._io.read_bits_int(3))
            self.unlocked_time = self._root.Stat.UnlockedTimeEnum(self._io.read_bits_int(2))
            self.trigger_reason = self._root.Stat.TriggerReasonEnum(self._io.read_bits_int(4))


    class Dfreq(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            _on = self._root.station.format.freq_data_type
            if _on == False:
                self.dfreq = self._root.Dfreq.Int(self._io, self, self._root)
            elif _on == True:
                self.dfreq = self._root.Dfreq.Float(self._io, self, self._root)

        class Int(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.raw_dfreq = self._io.read_s2be()

            @property
            def dfreq(self):
                if hasattr(self, '_m_dfreq'):
                    return self._m_dfreq if hasattr(self, '_m_dfreq') else None

                self._m_dfreq = (self.raw_dfreq / 100.0)
                return self._m_dfreq if hasattr(self, '_m_dfreq') else None


        class Float(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                self.raw_dfreq = self._io.read_f4be()

            @property
            def dfreq(self):
                if hasattr(self, '_m_dfreq'):
                    return self._m_dfreq if hasattr(self, '_m_dfreq') else None

                self._m_dfreq = self.raw_dfreq
                return self._m_dfreq if hasattr(self, '_m_dfreq') else None



    class Phasors(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            _on = self._root.station.format.phasors_data_type
            if _on == False:
                self.phasors = self._root.Phasors.Int(self._io, self, self._root)
            elif _on == True:
                self.phasors = self._root.Phasors.Float(self._io, self, self._root)

        class Int(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                _on = self._root.station.format.rectangular_or_polar
                if _on == False:
                    self.phasors = self._root.Phasors.Int.Rectangular(self._io, self, self._root)
                elif _on == True:
                    self.phasors = self._root.Phasors.Int.Polar(self._io, self, self._root)

            class Rectangular(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.value1 = self._io.read_s2be()
                    self.value2 = self._io.read_s2be()

                @property
                def real(self):
                    if hasattr(self, '_m_real'):
                        return self._m_real if hasattr(self, '_m_real') else None

                    self._m_real = self.value1
                    return self._m_real if hasattr(self, '_m_real') else None

                @property
                def imaginary(self):
                    if hasattr(self, '_m_imaginary'):
                        return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                    self._m_imaginary = self.value2
                    return self._m_imaginary if hasattr(self, '_m_imaginary') else None


            class Polar(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.value1 = self._io.read_u2be()
                    self.value2 = self._io.read_s2be()

                @property
                def magnitude(self):
                    if hasattr(self, '_m_magnitude'):
                        return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                    self._m_magnitude = self.value1
                    return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                @property
                def angle(self):
                    if hasattr(self, '_m_angle'):
                        return self._m_angle if hasattr(self, '_m_angle') else None

                    self._m_angle = self.value2
                    return self._m_angle if hasattr(self, '_m_angle') else None



        class Float(KaitaiStruct):
            def __init__(self, _io, _parent=None, _root=None):
                self._io = _io
                self._parent = _parent
                self._root = _root if _root else self
                _on = self._root.station.format.rectangular_or_polar
                if _on == False:
                    self.phasors = self._root.Phasors.Float.Rectangular(self._io, self, self._root)
                elif _on == True:
                    self.phasors = self._root.Phasors.Float.Polar(self._io, self, self._root)

            class Rectangular(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.value1 = self._io.read_f4be()
                    self.value2 = self._io.read_f4be()

                @property
                def real(self):
                    if hasattr(self, '_m_real'):
                        return self._m_real if hasattr(self, '_m_real') else None

                    self._m_real = self.value1
                    return self._m_real if hasattr(self, '_m_real') else None

                @property
                def imaginary(self):
                    if hasattr(self, '_m_imaginary'):
                        return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                    self._m_imaginary = self.value2
                    return self._m_imaginary if hasattr(self, '_m_imaginary') else None


            class Polar(KaitaiStruct):
                def __init__(self, _io, _parent=None, _root=None):
                    self._io = _io
                    self._parent = _parent
                    self._root = _root if _root else self
                    self.value1 = self._io.read_f4be()
                    self.value2 = self._io.read_f4be()

                @property
                def magnitude(self):
                    if hasattr(self, '_m_magnitude'):
                        return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                    self._m_magnitude = self.value1
                    return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                @property
                def angle(self):
                    if hasattr(self, '_m_angle'):
                        return self._m_angle if hasattr(self, '_m_angle') else None

                    self._m_angle = self.value2
                    return self._m_angle if hasattr(self, '_m_angle') else None




    class Analog(KaitaiStruct):
        def __init__(self, _io, _parent=None, _root=None):
            self._io = _io
            self._parent = _parent
            self._root = _root if _root else self
            _on = self._root.station.format.analogs_data_type
            if _on == False:
                self.analog = self._io.read_bits_int(16)
            elif _on == True:
                self.analog = self._io.read_f4be()




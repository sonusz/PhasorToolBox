# This is modified from a generated file! Please edit source .ksy file and use kaitai-struct-compiler to rebuild

import array
import struct
import zlib
from enum import Enum
from collections import UserList

import cmath
from pkg_resources import parse_version

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO


if parse_version(ks_version) < parse_version('0.7'):
    raise Exception(
        "Incompatible Kaitai Struct Python API:\
         0.7 or later is required, but you have %s" % (ks_version))


class Data(KaitaiStruct):
    def __init__(self, _io, _mini_cfg):
        """

        :param _io:
        :param _parent:
        :param _root:
        :param _mini_cfg:
        """
        self._mini_cfg = _mini_cfg
        self._io = _io
        self.pmu_data = [self.PmuData(
                self._io, _station=self._mini_cfg.station[i]) for i in range(self._mini_cfg.num_pmu)]

    class PmuData(KaitaiStruct):
        def __init__(self, _io, _station=None):
            self._station = _station
            self._io = _io
            self.stat = self.Stat(self._io)
            self.phasors = [self.Phasors(
                    self._io, self._station.format, self._station.phunit[i]) for i in range(self._station.phnmr)]

            self.freq = self.Freq(
                self._io, self._station.format.freq_data_type, self._station.fnom.fundamental_frequency).freq.freq
            self.dfreq = self.Dfreq(self._io, self._station.format.freq_data_type).dfreq.dfreq

            self.analog = [self.Analog(
                    self._io, self._station.format.analogs_data_type, self._station.anunit[i]) for i in range(self._station.annmr)]

            self.digital = [None] * (self._station.dgnmr)
            for i in range(self._station.dgnmr):
                _d = "{0:016b}".format(self._io.read_bits_int(16))
                self.digital[i] = [None] * 16
                for j in range(16):
                    self.digital[i][j] = self.Flag(
                        self._station.digunit[i][j].name,
                        self._station.digunit[i][j].normal_status,
                        self._station.digunit[i][j].current_valid_input,
                        _d[j]
                        )

        class Flag():
            def __init__(self, name, normal_status, current_valid_inputs, value):
                self.name = name
                self.normal_status = normal_status
                self.current_valid_inputs = current_valid_inputs
                self.value = value

        class Freq(KaitaiStruct):
            def __init__(self, _io, freq_data_type, fundamental_frequency=None):
                self._io = _io
                _on = freq_data_type
                if _on == 'int':
                    self.freq = self.Int(self._io, fundamental_frequency)
                elif _on == 'float':
                    self.freq = self.Float(self._io)

            class Int(KaitaiStruct):
                def __init__(self, _io, fundamental_frequency):
                    self._io = _io
                    self.raw_freq = self._io.read_s2be()
                    self.fundamental_frequency = fundamental_frequency

                @property
                def freq(self):
                    if hasattr(self, '_m_freq'):
                        return self._m_freq if hasattr(self, '_m_freq') else None

                    self._m_freq = (
                        (self.raw_freq / 1000.0) + self.fundamental_frequency)
                    return self._m_freq if hasattr(self, '_m_freq') else None

            class Float(KaitaiStruct):
                def __init__(self, _io):
                    self._io = _io
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
                user_def_8 = 8
                user_def_9 = 9
                user_def_10 = 10
                user_def_11 = 11
                user_def_12 = 12
                user_def_13 = 13
                user_def_14 = 14
                user_def_15 = 15

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

            def __init__(self, _io):
                self._io = _io
                self.data_error = self.DataErrorEnum(
                    self._io.read_bits_int(2))
                self.pmu_sync = self.PmuSyncEnum(
                    self._io.read_bits_int(1))
                self.data_sorting = self.DataSortingEnum(
                    self._io.read_bits_int(1))
                self.pmu_trigger_detected = self.PmuTriggerDetectedEnum(
                    self._io.read_bits_int(1))
                self.configuration_change = self.ConfigurationChangeEnum(
                    self._io.read_bits_int(1))
                self.data_modified = self.DataModifiedEnum(
                    self._io.read_bits_int(1))
                self.pmu_time_quality = self.PmuTimeQualityEnum(
                    self._io.read_bits_int(3))
                self.unlocked_time = self.UnlockedTimeEnum(
                    self._io.read_bits_int(2))
                self.trigger_reason = self.TriggerReasonEnum(
                    self._io.read_bits_int(4))

        class Dfreq(KaitaiStruct):
            def __init__(self, _io, freq_data_type):
                self._io = _io
                _on = freq_data_type
                if _on == 'int':
                    self.dfreq = self.Int(self._io)
                elif _on == 'float':
                    self.dfreq = self.Float(self._io)

            class Int(KaitaiStruct):
                def __init__(self, _io):
                    self._io = _io
                    self.raw_dfreq = self._io.read_s2be()

                @property
                def dfreq(self):
                    if hasattr(self, '_m_dfreq'):
                        return self._m_dfreq if hasattr(self, '_m_dfreq') else None

                    self._m_dfreq = (self.raw_dfreq / 100.0)
                    return self._m_dfreq if hasattr(self, '_m_dfreq') else None

            class Float(KaitaiStruct):
                def __init__(self, _io):
                    self._io = _io
                    self.raw_dfreq = self._io.read_f4be()

                @property
                def dfreq(self):
                    if hasattr(self, '_m_dfreq'):
                        return self._m_dfreq if hasattr(self, '_m_dfreq') else None

                    self._m_dfreq = self.raw_dfreq
                    return self._m_dfreq if hasattr(self, '_m_dfreq') else None

        class Phasors(KaitaiStruct):
            def __repr__(self):
                _repr_list = []
                for item in ["name", "real", "imaginary", "magnitude", "angle"]:
                    _r = getattr(self, item)
                    _repr_list.append("=".join((item, _r.__repr__())))
                return "<Phasors |"+", ".join(_repr_list)+">"

            def show(self, parent_path):
                for item in ["name", "real", "imaginary", "magnitude", "angle"]:
                    _r = getattr(self, item)
                    print(parent_path+'.'+item+" == "+_r.__repr__())


            @property
            def real(self):
                return self.phasors.phasors.real

            @property
            def imaginary(self):
                return self.phasors.phasors.imaginary

            @property
            def magnitude(self):
                return self.phasors.phasors.magnitude

            @property
            def angle(self):
                return self.phasors.phasors.angle

            def __init__(self, _io, _format, _phunit=None):
                self._phunit = _phunit
                self._format = _format
                self._io = _io
                self.name = self._phunit.name
                _on = _format.phasors_data_type
                if _on == 'int':
                    self.phasors = self.Int(
                        self._io, self._format.rectangular_or_polar, self._phunit.conversion_factor)
                elif _on == 'float':
                    self.phasors = self.Float(
                        self._io, self._format.rectangular_or_polar)

            class Int(KaitaiStruct):
                def __init__(self, _io, rectangular_or_polar, _conversion_factor=None):
                    self._conversion_factor = _conversion_factor
                    self._io = _io
                    _on = rectangular_or_polar
                    if _on == 'rectangular':
                        self.phasors = self.Rectangular(
                            self._io, self._conversion_factor)
                    elif _on == 'polar':
                        self.phasors = self.Polar(
                            self._io, self._conversion_factor)

                class Rectangular(KaitaiStruct):
                    def __init__(self, _io, _conversion_factor=None):
                        self._conversion_factor = _conversion_factor
                        self._io = _io
                        self.raw_real = self._io.read_s2be()
                        self.raw_imaginary = self._io.read_s2be()

                    @property
                    def real(self):
                        if hasattr(self, '_m_real'):
                            return self._m_real if hasattr(self, '_m_real') else None

                        self._m_real = self.raw_real * self._conversion_factor
                        return self._m_real if hasattr(self, '_m_real') else None

                    @property
                    def imaginary(self):
                        if hasattr(self, '_m_imaginary'):
                            return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                        self._m_imaginary = self.raw_imaginary * self._conversion_factor
                        return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                    @property
                    def magnitude(self):
                        if hasattr(self, '_m_magnitude'):
                            return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                        self._m_magnitude, self._m_angle = cmath.polar(
                            complex(self.real, self.imaginary))
                        return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                    @property
                    def angle(self):
                        if hasattr(self, '_m_angle'):
                            return self._m_angle if hasattr(self, '_m_angle') else None

                        self._m_magnitude, self._m_angle = cmath.polar(
                            complex(self.real, self.imaginary))
                        return self._m_angle if hasattr(self, '_m_angle') else None

                class Polar(KaitaiStruct):
                    def __init__(self, _io, _conversion_factor=None):
                        self._conversion_factor = _conversion_factor
                        self._io = _io
                        self.raw_magnitude = self._io.read_u2be()
                        self.angle = self._io.read_s2be()

                    @property
                    def real(self):
                        if hasattr(self, '_m_real'):
                            return self._m_real if hasattr(self, '_m_real') else None

                        z = cmath.rect(self.magnitude, self.angle)
                        self._m_real, self._m_imaginary = z.real, z.imag
                        return self._m_real if hasattr(self, '_m_real') else None

                    @property
                    def imaginary(self):
                        if hasattr(self, '_m_imaginary'):
                            return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                        z = cmath.rect(self.magnitude, self.angle)
                        self._m_real, self._m_imaginary = z.real, z.imag
                        return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                    @property
                    def magnitude(self):
                        if hasattr(self, '_m_magnitude'):
                            return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                        self._m_magnitude = self.raw_magnitude * self._conversion_factor
                        return self._m_magnitude if hasattr(self, '_m_magnitude') else None

            class Float(KaitaiStruct):
                def __init__(self, _io, rectangular_or_polar):
                    self._io = _io
                    _on = rectangular_or_polar
                    if _on == 'rectangular':
                        self.phasors = self.Rectangular(
                            self._io)
                    elif _on == 'polar':
                        self.phasors = self.Polar(
                            self._io)

                class Rectangular(KaitaiStruct):
                    def __init__(self, _io):
                        self._io = _io
                        self.real = self._io.read_f4be()
                        self.imaginary = self._io.read_f4be()

                    @property
                    def magnitude(self):
                        if hasattr(self, '_m_magnitude'):
                            return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                        self._m_magnitude, self._m_angle = cmath.polar(
                            complex(self.real, self.imaginary))
                        return self._m_magnitude if hasattr(self, '_m_magnitude') else None

                    @property
                    def angle(self):
                        if hasattr(self, '_m_angle'):
                            return self._m_angle if hasattr(self, '_m_angle') else None

                        self._m_magnitude, self._m_angle = cmath.polar(
                            complex(self.real, self.imaginary))
                        return self._m_angle if hasattr(self, '_m_angle') else None

                class Polar(KaitaiStruct):
                    def __init__(self, _io):
                        self._io = _io
                        self.magnitude = self._io.read_f4be()
                        self.angle = self._io.read_f4be()

                    @property
                    def real(self):
                        if hasattr(self, '_m_real'):
                            return self._m_real if hasattr(self, '_m_real') else None

                        z = cmath.rect(self.magnitude, self.angle)
                        self._m_real, self._m_imaginary = z.real, z.imag
                        return self._m_real if hasattr(self, '_m_real') else None

                    @property
                    def imaginary(self):
                        if hasattr(self, '_m_imaginary'):
                            return self._m_imaginary if hasattr(self, '_m_imaginary') else None

                        z = cmath.rect(self.magnitude, self.angle)
                        self._m_real, self._m_imaginary = z.real, z.imag
                        return self._m_imaginary if hasattr(self, '_m_imaginary') else None

        class Analog(KaitaiStruct):
            def __repr__(self):
                _repr_list = []
                for item in ["name", "value"]:
                    _r = getattr(self, item)
                    _repr_list.append("=".join((item, _r.__repr__())))
                return "<Analog |"+", ".join(_repr_list)+">"

            def show(self, parent_path):
                for item in ["name", "value"]:
                    _r = getattr(self, item)
                    print(parent_path+'.'+item+" == "+_r.__repr__())


            def __init__(self, _io, analogs_data_type, _anunit=None):
                self._io = _io
                self.name = _anunit.name
                _on = analogs_data_type
                if _on == 'int':
                    self.analog = self.Int(
                        self._io, _anunit.conversion_factor)
                elif _on == 'float':
                    self.analog = self.Float(
                        self._io)

            @property
            def value(self):
                return self.analog.analog
            

            class Int(KaitaiStruct):
                def __init__(self, _io, _conversion_factor=None):
                    self._conversion_factor = _conversion_factor
                    self._io = _io
                    self.raw_analog = self._io.read_bits_int(16)

                @property
                def analog(self):
                    if hasattr(self, '_m_analog'):
                        return self._m_analog if hasattr(self, '_m_analog') else None

                    self._m_analog = self.raw_analog * self._conversion_factor
                    return self._m_analog if hasattr(self, '_m_analog') else None

            class Float(KaitaiStruct):
                def __init__(self, _io):
                    self._io = _io
                    self.analog = self._io.read_f4be()

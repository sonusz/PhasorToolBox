meta:
  id: cfg_3
  endian: be
seq:
  - id: cont_idx
    type: u2
    doc: >
      Continuation index for fragmented frames:
      0: only frame in configuration, no further frames
      1: first frame in series, more to follow
      2–65534: number of each succeeding frame, in order 
      65535 (hex FFFF): last frame in series
  - id: time_base
    type: time_base
    doc: >
      Resolution of the fractional second time stamp (FRACSEC) in all frames.
  - id: num_pmu
    type: u2
    doc: The number of PMUs included in the data frame. No limit specified.
  - id: station
    type: cfg_3_station
    repeat: expr
    repeat-expr: num_pmu
  - id: data_rate
    type: s2
    doc: >
      Rate of phasor data transmissions―2-byte integer word (–32 767 to 
      +32 767)
      If DATA_RATE > 0, rate is number of frames per second.
      If DATA_RATE < 0, rate is negative of seconds per frame.
      E.g., DATA_RATE = 15 is 15 frames per second; DATA_RATE = –5 is 1 frame
      per 5 s.
types:
  time_base:
    seq:
      - id: flags
        type: b8
        doc: Reserved for flags (high 8 bits).
      - id: time_base
        type: b24
        doc: >
          24-bit unsigned integer, which is the subdivision of the second that
           the FRACSEC is based on. The actual “fractional second of the data 
           frame” = FRACSEC / TIME_BASE.
  cfg_3_station:
    seq:
      - id: stn
        type: name
        doc: >
          Station Name―in UTF-8 format, up to 255 bytes using the name field 
          format 
      - id: idcode
        type: u2
        doc: Data stream ID number.
      - id: g_pmu_id
        size: 16
        doc: >
          This 128-bit Global PMU ID shall be a user-assigned value. It shall 
          be stored in the PMU or other sending device so it can be sent with 
          this configuration 3 message. It allows uniquely identifying PMUs in 
          a system that has more than 65535 PMUs. The coding for the 16 bytes 
          is left to the user for assignment.
      - id: format
        type: format
        doc: Data format in the data frames.
      - id: phnmr
        type: u2
        doc: Number of phasors.
      - id: annmr
        type: u2
        doc: Number of analog values.
      - id: dgnmr
        type: u2
        doc: >
          Number of digital status words.
          Digital status words are normally 16-bit Boolean numbers with each 
          bit representing a digital status channel measured by a PMU. A 
          digital status word may be used in other user-designated ways.
      - id: chnam
        type: chnam
        doc: >
          Phasor and channel names―in ASCII with field index (see Table 12). 
          Minimum of 1 byte for each phasor, analog, and digital channel. 
          Names are in the same order as they are transmitted: all phasors, 
          all analogs, and all digitals. For digital channels, the channel 
          name order will be from the least significant to the most 
          significant. (The first name is for bit 0 of the first 16-bit status 
          word, the second is for bit 1, etc., up to bit 15. If there is more 
          than 1 digital status, the next name will apply to bit 0 of the 
          second word and so on.)
      - id: phscale
        type: phscale
        repeat: expr
        repeat-expr: phnmr
        doc: >
          Magnitude and angle scaling for phasors with data flags. This factor 
          has three 4-byte long words: the first is bit-mapped flags, the 
          second is a magnitude scale factor, and the third is an angle offset.
      - id: anscale
        type: anscale
        repeat: expr
        repeat-expr: annmr
        doc: Linear scaling for analog channels.
      - id: digunit
        type: digunit
        repeat: expr
        repeat-expr: dgnmr
        doc: >
          Mask words for digital status words. Two 16-bit words are provided 
          for each digital word. If digital status words are used for something 
          other than Boolean status indications, the use of masks is left to the 
          user, such as min or max settings.
      - id: pmu_lat
        type: f4
        doc: >
          PMU Latitude in degrees, range –90.0 to +90.0. Positive values are N 
          of equator. WGS 84 datum. Number in 32-bit IEEE floating-point 
          format. For unspecified locations, infinity shall be used.
      - id: pmu_lon
        type: f4
        doc: >
          PMU Longitude in degrees, range –179.99999999 to +180. Positive 
          values are E of the prime meridian. WGS 84 datum. Number in 32-bit 
          IEEE floating-point format. For unspecified locations, infinity 
          shall be used.
      - id: pmu_elev
        type: f4
        doc: >
          PMU Elevation in meters, Positive values are above mean sea level. 
          WGS 84 datum. Number in 32-bit IEEE floating-point format. For 
          unspecified locations, infinity shall be used.
      - id: svc_class
        type: str
        size: 1
        encoding: UTF-8
        doc: >
          Service class, as defined in IEEE Std C37.118.1, a single ASCII 
          character. In 2011 it is M or P.
      - id: window
        type: u4
        doc: >
          Phasor measurement window length including all filters and 
          estimation windows in effect. Value is in microseconds, 4-byte 
          signed integer value (to nearest microsecond). (For information 
          only, any required compensation is already applied to the 
          measurement.)
      - id: grp_dly
        type: u4
        doc: >
          Phasor measurement group delay including all filters and estimation 
          windows in effect. Value is in microseconds, 4-byte signed integer 
          value (to nearest microsecond). (For information only, any required 
          compensation is already applied to the measurement.)
      - id: fnom
        type: fnom
        doc: Nominal line frequency code and flags (16 bit unsigned integer)
      - id: cfgcnt
        type: u2
        doc: >
          Configuration change count is incremented each time a change is made 
          in the PMU configuration. 0 is the factory default and the initial 
          value.
    types:  
      name:
        seq:
          - id: len
            type: u1
            doc: >
              An unsigned 8-bit integer that indicates the length of the name 
              in bytes. A length of 0 indicates no further bytes (no name). 
              All name fields will have at least one byte that is the name 
              length. All names shall use UTF-8 coding.
          - id: name
            type: str
            size: len
            encoding: UTF-8
            doc: >
              Name, UTF-8 coding
              Note that standard 7-bit ASCII characters are the same as UTF-8 
              and no conversions are required.
      format:
        seq:
          - id: unused
            type: b12
            doc: >
              Bits 15–4: Unused
          - id: freq_data_type
            type: b1
            enum: int_float
            doc: >
              Bit 3: 0 = FREQ/DFREQ 16-bit integer, 1 = floating point
          - id: analogs_data_type
            type: b1
            enum: int_float
            doc: >
              Bit 2: 0 = analogs 16-bit integer, 1 = floating point
          - id: phasors_data_type
            type: b1
            enum: int_float
            doc: >
              Bit 1: 0 = phasors 16-bit integer, 1 = floating point
          - id: rectangular_or_polar
            type: b1
            enum: rectangular_polar
            doc: >
              Bit 0: 0 = phasor real and imaginary (rectangular), 1 = 
              magnitude and angle (polar)
        enums:
          int_float:
            0: int
            1: float
          rectangular_polar:
            0: rectangular
            1: polar
      chnam:
        seq:
          - id: phasor_names
            type: name
            repeat: expr
            repeat-expr: _parent.phnmr
          - id: analog_names
            type: name
            repeat: expr
            repeat-expr: _parent.annmr
          - id: digital_status_labels
            type: name
            repeat: expr
            repeat-expr: _parent.dgnmr*16
      phscale:
        seq:
          - id: modification_flags
            type: modification_flags
            doc: >
              First 2 bytes: 16-bit flag that indicates the type of data 
              modification when data is being modified by a continuous 
              process. When no modification process is being applied, all bits 
              shall be set to 0. (Bit 0 is the LSB, Bit 15 is the MSB.)
          - id: phasor_type_indication
            type: phasor_type_indication
            doc: >
              phasor type indication (Bit 0 is the LSB, Bit 7 is the MSB)
              Bits 07–04: Reserved for future use
              Bit 03: 0―voltage; 1―current.
              Bits 02–00: Phasor component
          - id: user_designation
            size: 1
            doc: Available for user designation
          - id: scale_factor
            type: f4
            doc: >
              Scale factor Y in 32-bit IEEE floating point. This scales phasor 
              data to primary volts or amperes. If phasors are transmitted in 
              floating-point format and scaled already, this value shall be 
              set to 1. (Check IEEE Std C37.118.2-2011 page 23 Table 11
              configuration frame 3 for more information)
          - id: phasor_angle_adjustment
            type: f4
            doc: >
              phasor angle adjustment θ in radians represented in 32-bit IEEE 
              floating point. If phasors are transmitted in floating-point 
              format and scaled already, this value shall be set to 0. (Check 
              IEEE Std C37.118.2-2011 page 23 Table 11 configuration frame 3 
              for more information)
        types:
          modification_flags:
            seq:
              - id: modification_applied
                type: b1
                doc: Modification applied, type not here defined
              - id: reserved
                type: b4
                doc: Reserved for future assignment
              - id: pseudo_phasor_value
                type: b1
                doc: Pseudo-phasor value (combined from other phasors) 
              - id: phasor_phase_adjusted_for_rotation
                type: b1
                doc: Phasor phase adjusted for rotation ( ±30o, ±120o, etc.) 
              - id: phasor_phase_adjusted_for_calibration
                type: b1
                doc: Phasor phase adjusted for calibration
              - id: phasor_magnitude_adjusted_for_calibration
                type: b1
                doc: Phasor magnitude adjusted for calibration
              - id: filtered_without_changing_sampling
                type: b1
                doc: Filtered without changing sampling
              - id: down_sampled_with_nonfir_filter
                type: b1
                doc: Down sampled with non-FIR filter
              - id: down_sampled_with_fir_filter
                type: b1
                doc: Down sampled with FIR filter
              - id: down_sampled_by_reselection
                type: b1
                doc: Down sampled by reselection (selecting every Nth sample) 
              - id: up_sampled_with_extrapolation
                type: b1
                doc: Upsampled with extrapolation
              - id: up_sampled_with_interpolation
                type: b1
                doc: Up sampled with interpolation
              - id: reserved
                type: b1
                doc: Not used, reserved
          phasor_type_indication:
            seq:
              - id: reserved
                type: b4
                doc: >
                  Bits 7-4: Reserved for future use
              - id: voltage_or_current
                type: b1
                enum: voltage_or_current_enum
                doc: >
                  Bit 3: 0―voltage; 1―current.
              - id: phasor_component
                type: b3
                enum: phasor_component_enum
                doc: >
                  Bits 2-0:
                  Phasor component, coded as follows
                  111: Reserved
                  110: Phase C
                  101: Phase B
                  100: Phase A
                  011: Reserved
                  010: Negative sequence
                  001: Positive sequence
                  000: Zero sequence
            enums:
              voltage_or_current_enum:
                0: voltage
                1: current
              phasor_component_enum:
                7: reserved_111
                6: phase_c
                5: phase_b
                4: phase_a
                3: reserved_011
                2: negative_sequence
                1: positive_sequence
                0: zero_sequence
      anscale:
        seq:
          - id: magnitude_scaling
            type: f4
            doc: Magnitude scaling M in 32-bit floating point.
          - id: offset
            type: f4
            doc: Offset B in 32-bit floating point.
      digunit:
        seq:
          - id: normal_status
            type: b16
            doc: >
              Indicate the normal status of the digital inputs by returning a 
              0 when exclusive Ored (XOR) with the status word. 
          - id: current_valid_inputs
            type: b16
            doc: >
              Indicate the current valid inputs to the PMU by having a bit set 
              in the binary position corresponding to the digital input and 
              all other bits set to 0. 
      fnom:
        seq:
          - id: reserved
            type: b15
            doc: >
              Bits 15–1:Reserved
          - id: raw_fundamental_frequency
            type: b1
            doc: >
              0―Fundamental frequency = 60 Hz
              1―Fundamental frequency = 50 Hz
        instances:
          fundamental_frequency:
            value: 60-raw_fundamental_frequency.to_i*10

meta:
  id: data
  endian: be
seq:
  - id: cfg_2
    type: cfg_2
    doc: >
      \\\\\\\\\\\\\\\\\\\\\\\\\\\\\IMPORTANT!!!!\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
      This is a dummy field. This is only used to help KSC to compile. This 
      field as well as related references need to be removed and replaced with 
      input arguments in the generated code.
  - id: pmu_data
    type: pmu_data
    repeat:  expr
    repeat-expr: cfg_2.num_pmu
types:
  cfg_2:
    seq:
      - id: time_base
        type: time_base
        doc: >
          Resolution of the fractional second time stamp (FRACSEC) in all frames.
      - id: num_pmu
        type: u2
        doc: >
          The number of PMUs included in the data frame. No limit specified.
    types:  
      time_base:
        seq:
          - id: flags
            type: b8
            doc: >
              Reserved for flags (high 8 bits).
          - id: time_base
            type: b24
            doc: >
              24-bit unsigned integer, which is the subdivision of the second that 
              the FRACSEC is based on. The actual “fractional second of the data 
              frame” = FRACSEC / TIME_BASE.
  pmu_data:
    seq:
      - id: station
        type: cfg_2_station
        doc: >
          \\\\\\\\\\\\\\\\\\\\\\\\\\\\\IMPORTANT!!!!\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
          This is a dummy field. This is only used to help KSC to compile. This 
          field as well as related references need to be removed and replaced with 
          input arguments in the generated code.
      - id: stat
        type: stat
        doc: Bit mapped flags.
      - id: phasors
        type: phasors
        repeat: expr
        repeat-expr:  station.phnmr
        doc: >
          Data type indicated by the FORMAT field in configuration 1, 2, and 3 
          frames.
      - id: freq
        type: freq
        doc: Frequency
      - id: dfreq
        type: dfreq
        doc: >
          ROCOF, in hertz per second times 100
          Range –327.67 to +327.67 Hz per second
      - id: analog
        type: analog
        repeat: expr
        repeat-expr:  station.annmr
      - id: digital
        type: b16
        repeat: expr
        repeat-expr:  station.dgnmr
    types:
      stat:
        seq:
          - id: data_error
            type: b2
            enum: data_error_enum
          - id: pmu_sync
            type: b1
            enum: pmu_sync_enum
            doc: 0 when in sync with a UTC traceable time source
          - id: data_sorting
            type: b1
            enum: data_sorting_enum
            doc: 0 by time stamp, 1 by arrival
          - id: pmu_trigger_detected
            type: b1
            enum: pmu_trigger_detected_enum
            doc: 0 when no trigger
          - id: configuration_change
            type: b1
            enum: configuration_change_enum
            doc: >
              Configuration change, set to 1 for 1 min to advise configuration 
              will change, and clear to 0 when change effected.
          - id: data_modified
            type: b1
            enum: data_modified_enum
            doc: 1 if data modified by post processing, 0 otherwise
          - id: pmu_time_quality
            type: b3
            enum: pmu_time_quality_enum
            doc: >
              PMU Time Quality
              111: Estimated maximum time error > 10 ms or time error unknown
              110: Estimated maximum time error < 10 ms
              101: Estimated maximum time error < 1 ms
              100: Estimated maximum time error < 100 μs
              011: Estimated maximum time error < 10 μs
              010: Estimated maximum time error < 1 μs
              001: Estimated maximum time error < 100 ns
              000: Not used (indicates code from previous version of profile)
          - id: unlocked_time
            type: b2
            enum: unlocked_time_enum
            doc: >
              00 = sync locked or unlocked < 10 s (best quality)
              01 = 10 s ≤ unlocked time < 100 s 
              10 = 100 s < unlock time ≤ 1000 s 
              11 = unlocked time > 1000 s
          - id: trigger_reason
            type: b4
            enum: trigger_reason_enum
            doc: >
              1111–1000: Available for user definition
              0111: Digital
              0110: Reserved
              0101: df/dt High 
              0100: Frequency high or low 
              0011: Phase angle diff 
              0010: Magnitude high
              0001: Magnitude low
              0000: Manual
        enums:
          data_error_enum:
            0: good_measurement_data_no_errors
            1: pmu_error_no_information_about_data_do_not_use
            2: pmu_in_test_mode_or_absent_data_tags_have_been_insereted_do_not_use
            3: pmu_error_do_not_use
          pmu_sync_enum:
            0: in_sync_with_a_utc_traceable_time_source
            1: not_in_sync_with_a_utc_traceable_time_source
          data_sorting_enum:
            0: by_time_stamp
            1: by_arrival
          pmu_trigger_detected_enum:
            0: no_trigger
            1: trigger_detected
          configuration_change_enum:
            0: change_effected
            1: will_change_in_one_min
          data_modified_enum:
            0: not_modified
            1: data_modified_by_post_processing
          pmu_time_quality_enum:
            7: estimated_maximum_time_error_larger_than_10_ms_or_time_error_unknown
            6: estimated_maximum_time_error_less_than_10_ms
            5: estimated_maximum_time_error_less_than_1_ms
            4: estimated_maximum_time_error_less_than_100_microsecond
            3: estimated_maximum_time_error_less_than_10_microsecond
            2: estimated_maximum_time_error_less_than_1_microsecond
            1: estimated_maximum_time_error_less_than_100_nanosecond
            0: not_used
          unlocked_time_enum:
            0: sync_locked_or_unlocked_less_than_10_s_best_quality
            1: unlocked_time_less_than_100_s_larger_than_10_s
            2: unlocked_time_less_than_1000_s_larger_than_100_s
            3: unlocked_time_larger_than_1000_s
          trigger_reason_enum:
            9:  user_def_9
            10:  user_def_10
            11:  user_def_11
            12:  user_def_12
            13:  user_def_13
            14:  user_def_14
            15:  user_def_15
            7: digital
            6: reserved
            5: df_or_dt_high
            4: frequency_high_or_low
            3: phase_angle_diff
            2: magnitude_high
            1: magnitude_low
            0: manual
      phasors:
        seq:
          - id: phasors
            type:
              switch-on: _parent.station.format.phasors_data_type
              cases:
                false: int
                true: float
        types:
          int:
            seq:
              - id: phasors
                type:
                  switch-on: _parent._parent.station.format.rectangular_or_polar
                  cases:
                    false: rectangular
                    true: polar
            types:
              rectangular:
                seq:
                  - id: raw_real
                    type: s2
                  - id: raw_imaginary
                    type: s2
              polar:
                seq:
                  - id: raw_magnitude
                    type: u2
                  - id: angle
                    type: s2
          float:
            seq:
              - id: phasors
                type:
                  switch-on: _parent._parent.station.format.rectangular_or_polar
                  cases:
                    false: rectangular
                    true: polar
            types:
              rectangular:
                seq:
                  - id: real
                    type: f4
                  - id: imaginary
                    type: f4
                instances:
                  magnitude:
                    value: real * 321
                  angle:
                    value: imaginary * 321
              polar:
                seq:
                  - id: magnitude
                    type: f4
                  - id: angle
                    type: f4
                instances:
                  real:
                    value: magnitude * 321
                  imaginary:
                    value: angle * 321
      freq:
        seq:
          - id: freq
            type:
              switch-on: _parent.station.format.freq_data_type
              cases:
                false: int
                true: float
        types:
          int:
            seq:
              - id: raw_freq
                type: s2
            instances:
              freq:
                value: raw_freq/1000.0 + _parent._parent.station.fnom.fundamental_frequency
          float:
            seq:
              - id: raw_freq
                type: f4
            instances:
              freq:
                value: raw_freq
      dfreq:
        seq:
          - id: dfreq
            type:
              switch-on: _parent.station.format.freq_data_type
              cases:
                false: int
                true: float
        types:
          int:
            seq:
              - id: raw_dfreq
                type: s2
            instances:
              dfreq:
                value: raw_dfreq/100.0
          float:
            seq:
              - id: raw_dfreq
                type: f4
            instances:
              dfreq:
                value: raw_dfreq
      analog:
        seq:
          - id: analog
            type:
              switch-on: _parent.station.format.analogs_data_type
              cases:
                false: int
                true: float
            doc: >
              Analog word. 16-bit integer. It could be sampled data such as control 
              signal or transducer value. Values and ranges defined by user. Can be 
              16-bit integer or IEEE floating point. Data type indicated by the 
              FORMAT field in configuration 1, 2, and 3 frames.
              raw_analog needs to be scaled with anunit.conversion_factor.
        types:
          int:
            seq:
              - id: raw_analog
                type: b16
          float:
            seq:
              - id: analog
                type: f4
      cfg_2_station:
        seq:
          - id: stn
            type: name
            doc: Station Name―16 bytes in ASCII format.
          - id: idcode
            type: u2
            doc: >
              Data stream ID number, 16-bit integer. It identifies the data stream 
              in field 3 and the data source in fields 9 and higher. Field 3 
              identifies the stream that is being received. The IDCODEs in field 
              9 (and higher if more than one PMU data is present) identify the 
              original source of the data and will usually be associated with a 
              particular PMU. The IDCODEs in a data stream received directly 
              from a PMU will usually be the same.
          - id: format
            type: format
            doc: >
              Data format in data frames, 16-bit flag.
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
              Phasor and channel names―16 bytes for each phasor, analog, and each 
              digital channel (16 channels in each digital word) in ASCII format 
              in the same order as they are transmitted. For digital channels, 
              the channel name order will be from the least significant to the 
              most significant. (The first name is for bit 0 of the first 16-bit 
              status word, the second is for bit 1, etc., up to bit 15. If there 
              is more than 1 digital status, the next name will apply to bit 0 
              of the second word and so on.)
          - id: phunit
            type: phunit
            repeat: expr
            repeat-expr: phnmr
            doc: >
              Conversion factor for phasor channels. Four bytes for each phasor. 
          - id: anunit
            type: anunit
            repeat: expr
            repeat-expr: annmr
            doc: >
              Conversion factor for analog channels. Four bytes for each analog 
              value. 
          - id: digunit
            type: digunit
            repeat: expr
            repeat-expr: dgnmr
            doc: >
              Mask words for digital status words. Two 16-bit words are provided 
              for each digital word. If digital status words are used for something 
              other than Boolean status indications, the use of masks is left to the 
              user, such as min or max settings.
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
              - id: name
                type: str
                size: 16
                encoding: UTF-8
          format:
            seq:
              - id: unused
                type: b12
                doc: >
                  Bits 15–4: Unused
              - id: freq_data_type
                type: b1
                doc: >
                  Bit 3: 0 = FREQ/DFREQ 16-bit integer, 1 = floating point
              - id: analogs_data_type
                type: b1
                doc: >
                  Bit 2: 0 = analogs 16-bit integer, 1 = floating point
              - id: phasors_data_type
                type: b1
                doc: >
                  Bit 1: 0 = phasors 16-bit integer, 1 = floating point
              - id: rectangular_or_polar
                type: b1
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
          phunit:
            seq:
              - id: voltage_or_current
                type: u1
                enum: voltage_or_current_enum
                doc: >
                  Most significant byte: 0―voltage; 1―current.
              - id: raw_conversion_factor
                type: b24
                doc: >
                  Least significant bytes: An unsigned 24-bit word in 10^(–5) V or 
                  amperes per bit to scale 16-bit integer data (if transmitted data is 
                  in floating-point format, this 24-bit value shall be ignored).
            instances:
              conversion_factor:
                value: raw_conversion_factor/100000.0
            enums:
              voltage_or_current_enum:
                0: voltage
                1: current
          anunit:
            seq:
              - id: analog_input
                type: u1
                doc: >
                  Most significant byte: 0―single point-on-wave, 1―rms of 
                  analog input, 2―peak of analog input, 5–64―reserved for future 
                  definition; 65–255―user definable. 
              - id: conversion_factor
                type: b24
                doc: >
                  Least significant bytes: A signed 24-bit word, user defined scaling.
          digunit:
            seq:
              - id: normal_status
                type: b16
                doc: >
                  The first will be used to indicate the normal status of the digital 
                  inputs by returning a 0 when exclusive ORed (XOR) with the status 
                  word.
              - id: current_valid_inputs
                type: b16
                doc: >
                  The second will indicate the current valid inputs to the PMU by 
                  having a bit set in the binary position corresponding to the digital 
                  input and all other bits set to 0.
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
    
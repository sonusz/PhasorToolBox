meta:
  id: cfg_2_station_and_data
  endian: be
  imports:
    - cfg_2_station
seq:
  - id: station
    type: cfg_2_station
    doc: Attach corresponded cfg_2_station string at the begining
  - id: stat
    type: stat
    doc: Bit mapped flags.
  - id: phasors
    type: phasors
    repeat: expr
    repeat-expr:  _root.station.phnmr
    doc: >
      Data type indicated by the FORMAT field in configuration 1, 2, and 3 
      frames.
  - id: freq
    type: freq
    doc: Frequency deviation from nominal, in mHz
  - id: dfreq
    type: freq
    doc: >
      ROCOF, in hertz per second times 100
      Range –327.67 to +327.67 Hz per second
  - id: analog
    type: analog
    repeat: expr
    repeat-expr:  _root.station.annmr
  - id: digital
    type: b16
    repeat: expr
    repeat-expr:  _root.station.dgnmr
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
          switch-on: _root.station.format.phasors_data_type
          cases:
            false: int
            true: float
    types:
      int:
        seq:
          - id: phasors
            type:
              switch-on: _root.station.format.rectangular_or_polar
              cases:
                false: rectangular
                true: polar
        types:
          rectangular:
            seq:
              - id: value1
                type: s2
              - id: value2
                type: s2
            instances:
              real:
                value: value1
              imaginary:
                value: value2
          polar:
            seq:
              - id: value1
                type: u2
              - id: value2
                type: s2
            instances:
              magnitude:
                value: value1
              angle:
                value: value2
      float:
        seq:
          - id: phasors
            type:
              switch-on: _root.station.format.rectangular_or_polar
              cases:
                false: rectangular
                true: polar
        types:
          rectangular:
            seq:
              - id: value1
                type: f4
              - id: value2
                type: f4
            instances:
              real:
                value: value1
              imaginary:
                value: value2
          polar:
            seq:
              - id: value1
                type: f4
              - id: value2
                type: f4
            instances:
              magnitude:
                value: value1
              angle:
                value: value2
  freq:
    seq:
      - id: freq
        type:
          switch-on: _root.station.format.freq_data_type
          cases:
            false: int
            true: float
    types:
      int:
        seq:
          - id: freq
            type:
              switch-on: _root.station.fnom.fundamental_frequency
              cases:
                false: sixty
                true: fifty
        types:
          sixty:
            seq:
              - id: freq
                type: s2
            instances:
              acutall_freq:
                value: freq/1000 + 60
          fifty:
            seq:
              - id: freq
                type: s2
            instances:
              acutall_freq:
                value: freq/1000 + 50
      float:
        seq:
          - id: freq
            type:
              switch-on: _root.station.fnom.fundamental_frequency
              cases:
                false: sixty
                true: fifty
        types:
          sixty:
            seq:
              - id: freq
                type: f4
            instances:
              acutall_freq:
                value: freq/1000 + 60
          fifty:
            seq:
              - id: freq
                type: f4
            instances:
              acutall_freq:
                value: freq/1000 + 50
  analog:
    seq:
      - id: analog
        type:
          switch-on: _root.station.format.analogs_data_type
          cases:
            false: int
            true: float
    types:
      int:
        seq:
          - id: analog
            type: b16
            doc:  Values and ranges defined by user.
      float:
        seq:
          - id: analog
            type: f4
            doc:  IEEE floating point.

meta:
  id: common_header
  endian: be
seq:
  - id: sync
    type: sync_word
    doc: Frame synchronization word.
  - id: framesize
    type: u2
    doc: >
     Total number of bytes in the frame, including CHK.
     16-bit unsigned number. Range = maximum 65535
  - id: idcode
    type: u2
    doc: >
      Data stream ID number, 16-bit integer, assigned by user, 1–65534 (0 and 
      65535 are reserved). Identifies destination data stream for commands 
      and source data stream for other messages. A stream will be hosted by 
      a device that can be physical or virtual. If a device only hosts one 
      data stream, the IDCODE identifies the device as well as the stream. 
      If the device hosts more than one data stream, there shall be a 
      different IDCODE for each stream.
  - id: soc
    type: u4
    doc: >
      Time stamp, 32-bit unsigned number, SOC count starting at midnight 
      01-Jan-1970 (UNIX time base).
      Range is 136 years, rolls over 2106 AD.
      Leap seconds are not included in count, so each year has the same number 
      of seconds except leap years, which have an extra day (86 400 s).
  - id: fracsec
    type: fracsec
    doc: >
      Fraction of second and Time Quality, time of measurement for data frames 
      or time of frame transmission for non-data frames.
types:
  sync_word:
    seq:
      - id: magic
        contents: [0xaa]
        doc: >
          Leading byte: AA hex
      - id: reserved
        type: b1
        doc: >
          Bit 7: Reserved for future definition, must be 0 for this standard 
          version.
      - id: frame_type
        type: b3
        enum: frame_type_enum
        doc: >
          Frame type
          000: Data Frame
          001: Header Frame
          010: Configuration Frame 1
          011: Configuration Frame 2
          101: Configuration Frame 3
          100: Command Frame (received message)
      - id: version_number
        type: b4
        enum: version_number_enum
        doc: >
          Version number
          Version 1 (0001) for messages defined in IEEE Std C37.118-2005. 
          Version 2 (0010) for messages added in this revision, IEEE Std 
          C37.118.2-2011.
    enums:
      frame_type_enum:
        0: data_frame
        1: header_frame
        2: configuration_frame_1
        3: configuration_frame_2
        4: command_frame
        5: configuration_frame_3
      version_number_enum:
        1: c_37_118_2005
        2: c_37_118_2_2011
  fracsec:
    seq:
      - id: reserved
        type: b1
        doc: >
          Bit 7: Reserved
      - id: leap_second_direction
        type: b1
        enum: leap_second_direction_enum
        doc: >
          Bit 6: Leap Second Direction―0 for add, 1 for delete
      - id: leap_second_occurred
        type: b1
        enum: leap_second_occurred_enum
        doc: >
          Bit 5: Leap Second Occurred―set in the first second after the leap 
          second occurs and remains set for 24 h
      - id: leap_second_pending
        type: b1
        enum: leap_second_pending_enum
        doc: >
          Bit 4: Leap Second Pending―shall be set not more than 60 s nor less 
          than 1 s before a leap second occurs, and cleared in the second 
          after the leap second occurs.
      - id: time_quality
        type: b4
        enum: msg_tq
        doc: >
          Bit 3-0: Time quality flags.
      - id: raw_fraction_of_second
        type: b24
        doc: >
          When divided by TIME_BASE yields the actual fractional second. 
          FRACSEC used in all messages to and from a given PMU shall use the 
          same TIME_BASE that is provided in the configuration message from 
          that PMU.
    enums:
      leap_second_direction_enum:
        0: add
        1: delete
      leap_second_occurred_enum:
        0: no_leap_second_occurred_in_the_last_24hs
        1: leap_second_occurred_in_the_last_24hs
      leap_second_pending_enum:
        0: no_leap_second_occurs_in_the_next_60s
        1: leap_second_occurs_in_60s
      msg_tq:
        15: fault_clock_failure_time_not_reliable
        11: time_within_10_s_of_utc
        10: time_within_1_s_of_utc
        9: time_within_10_to_1_s_of_utc
        8: time_within_10_to_2_s_of_utc
        7: time_within_10_to_3_s_of_utc
        6: time_within_10_to_4_s_of_utc
        5: time_within_10_to_5_s_of_utc
        4: time_within_10_to_6_s_of_utc
        3: time_within_10_to_7_s_of_utc
        2: time_within_10_to_8_s_of_utc
        1: time_within_10_to_9_s_of_utc
        0: normal_operation_clock_locked_to_utc_traceable_source

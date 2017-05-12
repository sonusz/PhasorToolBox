meta:
  id: synchrophasor_common
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
      Data stream ID number, 16-bit integer, assigned by user, 1–65534 (0 and 65535 are reserved). 
      Identifies destination data stream for commands and source data stream for other messages. A 
      stream will be hosted by a device that can be physical or virtual. If a device only hosts one 
      data stream, the IDCODE identifies the device as well as the stream. If the device hosts more 
      than one data stream, there shall be a different IDCODE for each stream.
  - id: soc
    type: u4
    doc: >
      Time stamp, 32-bit unsigned number, SOC count starting at midnight 01-Jan-1970 (UNIX time base).
      Range is 136 years, rolls over 2106 AD.
      Leap seconds are not included in count, so each year has the same number of seconds except leap 
      years, which have an extra day (86 400 s).
  - id: fracsec
    type: fraction_of_second
    doc: >
      Fraction of second and Time Quality, time of measurement for data frames or time of frame transmission for non-data frames.
  - id: data
    size: framesize - 16
  - id: chk
    type: u2  
    doc: CRC-CCITT check sum
instances:
  chk_body:
    pos: 0x0
    size: framesize - 2
    doc: All data excluding the check sum bytes. CRC-CCITT(chk_body) == chk
types:
  sync_word:
    seq:
      - id: magic
        contents: [0xaa]
        doc: Leading byte: AA hex
      - id: reserved
        type: b1
        doc: Bit 7: Reserved for future definition, must be 0 for this standard version.
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
          Version 1 (0001) for messages defined in IEEE Std C37.118-2005 [B6]. 
          Version 2 (0010) for messages added in this revision, IEEE Std C37.118.2-2011.
    enums:
      frame_type_enum:
        0: data_frame
        1: header_frame
        2: configuration_frame_1
        3: configuration_frame_2
        4: configuration_frame_3
        5: command_frame
      version_number_enum:
        1: c371182005
        2: c3711822011
  fraction_of_second:
    seq:
      - id: time_quailty
        type: b8
        enum: msg_tq
        doc: Time quality flags.
      - id: raw_fraction_of_second
        type: b24
        doc: >
          When divided by TIME_BASE yields the actual fractional second. FRACSEC used in all messages to 
          and from a given PMU shall use the same TIME_BASE that is provided in the configuration message 
          from that PMU.
    enums:
      msg_tq:
        1111: Fault―clock_failure_time_not_reliable
        1011: Time_within_10_s_of_UTC
        1010: Time_within_1_s_of_UTC
        1001: Time_within_10–1_s_of_UTC
        1000: Time_within_10–2_s_of_UTC
        0111: Time_within_10–3_s_of_UTC
        0110: Time_within_10–4_s_of_UTC
        0101: Time_within_10–5_s_of_UTC
        0100: Time_within_10–6_s_of_UTC
        0011: Time_within_10–7_s_of_UTC
        0010: Time_within_10–8_s_of_UTC
        0001: Time_within_10–9_s_of_UTC
        0000: Normal_operation_clock_locked_to_UTC_traceable_source

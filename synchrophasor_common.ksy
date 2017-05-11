meta:
  id: synchrophasor_common
  endian: be
seq:
  - id: magic
    contents: [0xaa] 
  - id: reserved
    type: b1
  - id: sync
    type: b3
    enum: synchronization_word
    doc: Frame type
  - id: ver
    type: b4
    enum: version_number
    doc: Version number
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
  - id: time_quailty
    type: b8
    doc: Time quality flags.
  - id: fracsec
    type: b24
    doc: >
      When divided by TIME_BASE yields the actual fractional second. FRACSEC used in all messages to 
      and from a given PMU shall use the same TIME_BASE that is provided in the configuration message 
      from that PMU.
  - id: body
    size: framesize - 16
  - id: chk
    type: u2  
    doc: CRC-CCITT check sum
enums:
  synchronization_word:
    0: data
    1: header
    2: cf1
    3: cf2
    4: cf3
    5: command
  version_number:
    1: c371182005
    2: c3711822011

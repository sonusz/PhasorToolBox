meta:
  id: synchrophasor_cf2
  endian: be
seq:
  - id: time_base
    type: time_base
    doc: >
      Resolution of the fractional second time stamp (FRACSEC) in all frames.
  - id: num_pmu
    type: u2
    doc: >
      The number of PMUs included in the data frame. No limit specified.
  - id: station
    type: station
    repeat: expr
    repeat-expr: num_pmu
  - id: data_rate
    type: s2
    doc: >
      Rate of phasor data transmissions―2-byte integer word (–32767 to 
      +32767)
      If DATA_RATE > 0, rate is number of frames per second.
      If DATA_RATE < 0, rate is negative of seconds per frame.
      E.g., DATA_RATE = 15 is 15 frames per second; DATA_RATE = –5 is 1 
      frame per 5 s.
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
  station:
    seq:
      - id: stn
        type: str
        size: 16
        encoding: UTF-8
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
        type: u4
        repeat: expr
        repeat-expr: phnmr
        doc: >
          Conversion factor for phasor channels. Four bytes for each phasor. 
          Most significant byte: 0―voltage; 1―current. Least significant 
          bytes: An unsigned 24-bit word in 10^(–5) V or amperes per bit to scale 
          16-bit integer data (if transmitted data is in floating-point 
          format, this 24-bit value shall be ignored).
      - id: anunit
        type: u4
        repeat: expr
        repeat-expr: annmr
        doc: >
          Conversion factor for analog channels. Four bytes for each analog 
          value. Most significant byte: 0―single point-on-wave, 1―rms of 
          analog input, 2―peak of analog input, 5–64―reserved for future 
          definition; 65–255―user definable. Least significant bytes: A 
          signed 24-bit word, user defined scaling.
      - id: digunit
        type: u4
        repeat: expr
        repeat-expr: dgnmr
        doc: >
          Mask words for digital status words. Two 16-bit words are provided 
          for each digital word. The first will be used to indicate the 
          normal status of the digital inputs by returning a 0 when 
          exclusive ORed (XOR) with the status word. The second will 
          indicate the current valid inputs to the PMU by having a bit set 
          in the binary position corresponding to the digital input and all 
          other bits set to 0. See NOTE.
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
      format:
        seq:
          - id: unused
            type: b12
            doc: Bits 15–4: Unused
          - id: freq_data_type
            type: b1
            doc: Bit 3: 0 = FREQ/DFREQ 16-bit integer, 1 = floating point
          - id: analogs_data_type
            type: b1
            doc: Bit 2: 0 = analogs 16-bit integer, 1 = floating point
          - id: phasors_data_type
            type: b1
            doc: Bit 1: 0 = phasors 16-bit integer, 1 = floating point
          - id: rectangular_or_polar
            type: b1
            doc: >
              Bit 0: 0 = phasor real and imaginary (rectangular), 1 = 
              magnitude and angle (polar)
      chnam:
        seq:
          - id: phasor_names
            type: str
            size: 16
            encoding: UTF-8
            repeat: expr
            repeat-expr: _parent.phnmr
          - id: analog_names
            type: str
            size: 16
            encoding: UTF-8
            repeat: expr
            repeat-expr: _parent.annmr
          - id: digital_status_labels
            type: str
            size: 16
            encoding: UTF-8
            repeat: expr
            repeat-expr: _parent.dgnmr*16
      fnom:
        seq:
          - id: reserved
            type: b15
            doc: Bits 15–1:Reserved
          - id: fundamental_frequency
            type: b1
            doc: >
              1―Fundamental frequency = 50 Hz
              0―Fundamental frequency = 60 Hz

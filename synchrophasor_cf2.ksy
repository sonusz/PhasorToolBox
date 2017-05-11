meta:
  id: synchrophasor_cf2
  endian: be
seq:
  - id: time_quailty
    type: b8
    doc: Time quality flags.
  - id: time_base
    type: b24
    doc: >
      the subdivision of the second that the FRACSEC is based on.
      The actual “fractional second of the data frame” = FRACSEC / TIME_BASE.
  - id: num_pmu
    type: u2
    doc: The number of PMUs included in the data frame. No limit specified.
  - id: station_conf
    type: station
    repeat: expr
    repeat-expr: num_pmu
  - id: data_rate
    type: u2
    doc: >
      Rate of phasor data transmissions―2-byte integer word (–32 767 to +32 767)
      If DATA_RATE > 0, rate is number of frames per second.
      If DATA_RATE < 0, rate is negative of seconds per frame.
types:
  station:
    seq:
      - id: stn
        type: str
        size: 16
        encoding: UTF-8
        doc: Station Name―16 bytes in ASCII format.
      - id: idcode
        type: u2
        doc: Data stream ID number.
      - id: format_unused
        type: b12
        doc: Data format in data frames
      - id: format3
        type: b1
        doc: 0 = FREQ/DFREQ 16-bit integer, 1 = floating point
      - id: format2
        type: b1
        doc: 0 = analogs 16-bit integer, 1 = floating point
      - id: format1
        type: b1
        doc: 0 = phasors 16-bit integer, 1 = floating point
      - id: format0
        type: b1
        doc: 0 = phasor real and imaginary (rectangular), 1 = magnitude and angle (polar)
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
          Digital status words are normally 16-bit Boolean numbers with each bit representing a digital 
          status channel measured by a PMU. A digital status word may be used in other user-designated 
          ways.
      - id: phasor_names
        type: str
        size: 16
        encoding: UTF-8
        repeat: expr
        repeat-expr: phnmr
      - id: analog_names
        type: str
        size: 16
        encoding: UTF-8
        repeat: expr
        repeat-expr: annmr
      - id: digital_status_labels
        type: str
        size: 16
        encoding: UTF-8
        repeat: expr
        repeat-expr: dgnmr*16
      - id: phunit
        type: u4
        repeat: expr
        repeat-expr: phnmr
        doc: >
          Conversion factor for phasor channels. Four bytes for each phasor. 
          Most significant byte: 0―voltage; 1―current.
          Least significant bytes: An unsigned 24-bit word in 10–5 V or amperes per bit to scale 16-bit 
          integer data (if transmitted data is in floating-point format, this 24-bit value shall be 
          ignored).
      - id: anunit
        type: u4
        repeat: expr
        repeat-expr: annmr
        doc: >
          Conversion factor for analog channels. Four bytes for each analog value.
          Most significant byte: 0―single point-on-wave, 1―rms of analog input,
          2―peak of analog input, 5–64―reserved for future definition; 65–255―user definable. Least 
          significant bytes: A signed 24-bit word, user defined scaling.
      - id: digunit
        type: u4
        repeat: expr
        repeat-expr: dgnmr
        doc: >
          Mask words for digital status words. Two 16-bit words are provided for each digital word. The 
          first will be used to indicate the normal status of the digital inputs by returning a 0 when 
          exclusive ORed (XOR) with the status word. The second will indicate the current valid inputs to 
          the PMU by having a bit set in the binary position corresponding to the digital input and all 
          other bits set to 0. See NOTE.
      - id: fnom_reserved
        type: b15
      - id: fnom
        type: b1
        doc: >
          1―Fundamental frequency = 50 Hz
          0―Fundamental frequency = 60 Hz
      - id: cfgcnt
        type: u2
        doc: >
          Configuration change count is incremented each time a change is made in the PMU 
          configuration. 0 is the factory default and the initial value.
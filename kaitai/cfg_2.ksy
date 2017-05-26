meta:
  id: cfg_2
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
    type: cfg_2_station
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
          - id: raw_conversion_factor
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

meta:
  id: synchrophasor_cf3
  endian: be
  imports:
    - cfg_3_station
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

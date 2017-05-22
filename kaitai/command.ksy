meta:
  id: command
  endian: be
seq:
  - id: cmd
    type: u2
    enum: command_code 
    doc: >
      2-byte command code
      0000 0000 0000 0001: Turn off transmission of data frames.
      0000 0000 0000 0010: Turn on transmission of data frames.
      0000 0000 0000 0011: Send HDR frame.
      0000 0000 0000 0100: Send CFG-1 frame.
      0000 0000 0000 0101: Send CFG-2 frame.
      0000 0000 0000 0110: Send CFG-3 frame (optional command).
      0000 0000 0000 1000: Extended frame.
      0000 0000 xxxx xxxx: All undesignated codes reserved.
      0000 yyyy xxxx xxxx: All codes where yyyy ≠ 0 available for user 
      designation.
      zzzz xxxx xxxx xxxx: All codes where zzzz ≠ 0 reserved.
  - id: extframe
    size-eos: true
enums:
  command_code:
    1: turn_off_transmission_of_data_frames
    2: turn_on_transmission_of_data_frames
    3: send_hdr_frame
    4: send_cfg_1_frame
    5: send_cfg_2_frame
    6: send_cfg_3_frame
    8: extended_frame
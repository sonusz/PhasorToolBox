#!/usr/bin/env python3

import time
import binascii


class Message():
    """This object returns a synchrophasor message in bytes.
    It would be easier to use classes that inherited from this class,
    such as command(), data(), cfg2()

    Note:
        This creates an empty Version 1 (0001) DATA frame defined by IEEE Std
        C37.118.2-2011 by default. Only the CFG-3 frame is Version 2 (0010)
        TIME, TQ_FLAGS and MSG_TQ are used to generate SOC and FRACSEC of the
        synchrophasor message.

    Example:
        my_msg = message()
        my_msg = message(SYNC=b'\xaa\x01', IDCODE=1, DATA=b'\x00\x00')

    Args:
        SYNC (bytes): Frame synchronization word. Defaults to b'\xaa\x01'.
        IDCODE (int): Data stream ID number. Defaults to 0.
        TIME (float): Epoch time. Defaults to current time.
        TQ_FLAGS (str): Four bytes string indicates time quality flags.
                        Defaults to '0000'
        MSG_TQ (str): Four bytes string indicates message time quality (
                      MSG_TQ). Defaults to '1111'
        TIME_BASE (int): TIME_BASE. Defaults to 16777215.
    """

    def __new__(
            self,
            SYNC=b'\xaa\x01',
            IDCODE=1,
            TIME=None,
            TQ_FLAGS='0000',
            MSG_TQ='1111',
            TIME_BASE=16777215,
            DATA=b''
    ):
        TIME = time.time() if not TIME else TIME
        raw_data = b''.join((
            SYNC,
            (len(DATA) + 16).to_bytes(2, 'big'),  # FRAMESIZE
            IDCODE.to_bytes(2, 'big'),
            int(TIME).to_bytes(4, 'big'),         # SOC
            int(TQ_FLAGS + MSG_TQ, 2).to_bytes(1, 'big'),
            int(TIME % 1 * TIME_BASE).to_bytes(3, 'big'),  # Frac of sec
            DATA
        ))
        chk_sum = binascii.crc_hqx(raw_data, -1).to_bytes(2, 'big')
        return bytes.__new__(bytes, raw_data+chk_sum)


class Command():
    """This object returns a command message in bytes.
    Note:
        This creates a Version 1 (0001) command message defined by IEEE Std
        C37.118.2-2011.
        TIME, TQ_FLAGS and MSG_TQ are used to generate SOC and FRACSEC of the
        synchrophasor message.

    Example:
        my_msg = Command(1,'on') # Data stream 1 turn on transmission.
        my_msg = Command(IDCODE=2, CMD='off') # Data stream 2 turn off
        transmission.
        my_msg = Command(IDCODE=3, CMD='ext', EXT = b'User defined message')
        # Send extended command frame with user defined message to the source
        # of Data stream 3.

    Args:
        IDCODE (int)    :Data stream ID number. Defaults to 1. 1–65534 (0 and
        65535 are reserved).
        CMD (str)       :Commands designated by user.
                        Options are:
                            'off' :Turn off transmission of data frames.
                            'on'  :Turn on transmission of data frames.
                            'hdr' :Send HDR frame.
                            'cfg1':Send CFG-1 frame.
                            'cfg2':Send CFG-2 frame.
                            'cfg3':Send CFG-3 frame (optional command).
                            'ext':Extended frame.
        TIME (float)    :Epoch time. Defaults to current time.
        TQ_FLAGS (str)  :Four bytes string indicates time quality flags.
                        Defaults to '0000'
        MSG_TQ (str)    :Four bytes string indicates message time quality (
                        MSG_TQ). Defaults to '1111'
        TIME_BASE (int) :TIME_BASE. Defaults to 16777215.
        USER_DEF (str)  :Four bytes string codes designated by user. Defaults
                        to '0000'
        EXT (bytes)     :Extended frame data, 16-bit words, 0 to 65518
                        bytes as indicated by frame size, data user defined.
    """

    CommandCode = {
        'off': 1,
        'on': 2,
        'hdr': 3,
        'cfg1': 4,
        'cfg2': 5,
        'cfg3': 6,
        'ext': 8
    }

    def __new__(
        self,
        IDCODE=1,
        CMD='off',
        TIME=None,
        TQ_FLAGS='0000',
        MSG_TQ='1111',
        TIME_BASE=16777215,
        USER_DEF='0000',
        EXT=b''
    ):
        return Message.__new__(
            Message,
            SYNC=b'\xaaA',
            IDCODE=IDCODE,
            TIME=TIME,
            TQ_FLAGS=TQ_FLAGS,
            MSG_TQ=MSG_TQ,
            TIME_BASE=TIME_BASE,
            DATA=b''.join((
                int('0000'+USER_DEF, 2).to_bytes(1, 'big'),
                self.CommandCode[CMD].to_bytes(1, 'big'),
                EXT
            ))
        )

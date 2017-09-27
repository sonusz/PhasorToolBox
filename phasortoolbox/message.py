#!/usr/bin/env python3
import time
import binascii


class message(bytes):
    """This object returns a synchrphasor message in bytes.
    It would be easyer to use classes that inheritaged from this class,
    such as command(), data(), cfg2()
    Note:
        This creates a Version 2 (0010) message defined by IEEE Std
        C37.118.2-2011.
        TIME, TQ_FLAGS and MSG_TQ are used to generate SOC and FRACSEC of the
        synchrophasor message.
    Example:
        my_msg = message()
        my_msg = message(DATA=b'\x00\x00')
    Args:
        SYNC (bytes): Frame synchronization word. Defaults to b'\xaa\x00'.
        IDCODE (int): Data stream ID number. Defaults to 0.
        TIME (float): Epoch time. Defaults to current time.
        TQ_FLAGS (str): Four bytes string indicates time quatity flags. 
                        Defaults to '0000'
        MSG_TQ (str): Four bytes string indicates message time quatity (
                      MSG_TQ). Defaults to '1111'
        TIME_BASE (int): TIME_BASE. Defaults to 16777215.
    """

    def __new__(
            self, SYNC=b'\xaa\x00', IDCODE=1,
            TIME=time.time(), TQ_FLAGS='0000', MSG_TQ='1111',
            TIME_BASE=16777215, DATA=b''):
        FRAMESIZE = (len(DATA) + 16).to_bytes(2, 'big')
        SOC_FRACSEC = self.soc_fracsec(
            self, TIME=TIME, TIME_QUALITY_FLAGS=TQ_FLAGS + MSG_TQ,
            TIME_BASE=TIME_BASE)
        raw_data = SYNC + FRAMESIZE + \
            IDCODE.to_bytes(2, 'big') + SOC_FRACSEC + DATA
        raw_data += self.checksum(self, raw_data)
        return super(message, self).__new__(self, raw_data)

    def soc_fracsec(
            self, TIME, TIME_QUALITY_FLAGS, TIME_BASE):
        """
        Check IEEE Std C37.118.2-2011 Table 3 Table 4 for Time quality flags
        """
        return int(TIME).to_bytes(4, 'big') \
            + int(TIME_QUALITY_FLAGS, 2).to_bytes(1, 'big') \
            + int(TIME % 1 * TIME_BASE).to_bytes(3, 'big')

    def checksum(self, raw_data):
        return binascii.crc_hqx(raw_data, -1).to_bytes(2, 'big')


class command(message):
    """This object returns a command message in bytes.
    Note:
        This creates a Version 2 (0010) command message defined by IEEE Std
        C37.118.2-2011.
        TIME, TQ_FLAGS and MSG_TQ are used to generate SOC and FRACSEC of the
        synchrophasor message.

    Example:
        my_msg = command(IDCODE=0, CMD='on') # Turn on transmission of data 
        frames.
        my_msg = command(IDCODE=0, CMD='ext', EXT = b'User defined message') 
        # An extended command frame with user defined message.
    Args:
        IDCODE (int)    :Data stream ID number. Defaults to 1. 1–65534 (0 and 65535 are reserved).
        TIME (float)    :Epoch time. Defaults to current time.
        TQ_FLAGS (str)  :Four bytes string indicates time quatity flags. 
                        Defaults to '0000'
        MSG_TQ (str)    :Four bytes string indicates message time quatity (
                        MSG_TQ). Defaults to '1111'
        TIME_BASE (int) :TIME_BASE. Defaults to 16777215.
        USER_DEF (str)  :Four bytes string codes designated by user. Defaults 
                        to '0000'
        CMD (str)       :Commands designated by user. 
                        Options are:
                            'off' :Turn off transmission of data frames.
                            'on'  :Turn on transmission of data frames.
                            'hdr' :Send HDR frame.
                            'cfg1':Send CFG-1 frame.
                            'cfg2':Send CFG-2 frame.
                            'cfg3':Send CFG-3 frame (optional command).
                            'ext':Extended frame.
        EXT (bytes)     :Extended frame data, 16-bit words, 0 to 65518 
                        bytes as indicated by frame size, data user defined.
    """

    def __new__(self, IDCODE=1,
                TIME=time.time(), TQ_FLAGS='0000', MSG_TQ='1111',
                TIME_BASE=16777215,
                USER_DEF='0000', CMD='off', EXT=b''
                ):
        return super().__new__(
            self, SYNC=b'\xaaB', IDCODE=IDCODE,
            TIME=TIME, TQ_FLAGS=TQ_FLAGS, MSG_TQ=MSG_TQ,
            TIME_BASE=16777215,
            DATA=self._command_code(
                self, USER_DEF, CMD) + EXT,
        )

    def _command_code(self, USER_DEF, CMD):
        CommandCode = {
            'off': 1,
            'on': 2,
            'hdr': 3,
            'cfg1': 4,
            'cfg2': 5,
            'cfg3': 6,
            'ext': 8
        }
        return int('0000' + USER_DEF, 2).to_bytes(1, 'big') + \
            CommandCode[CMD].to_bytes(1, 'big')


#my_msg = command(IDCODE=0, CMD='ext', EXT=b'User defined message')
#print(P.parse(my_msg)[0].data.ext)

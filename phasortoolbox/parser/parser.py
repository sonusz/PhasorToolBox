#!/usr/bin/env python3
from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from .common import PhasorMessage
from .minicfg import MiniCfgs
from .pcap import Pcap
import logging
LOG=logging.getLogger('phasortoolbox.parser')
import struct


class Parser(object):
    """ A Parser that parses synchrphasor messages defined by IEEE Std
    C37.118.2-2011.

    Note:
        When parsing a stream, the parser automatically detects and stores
        configuration messages and use the most recent received configuration
        message to parse the subsequent data messages. Multiple synchrophasor
        message streams can be parsed using one parser instance. The parser
        identifies each synchrophasor message stream by using its IDCODE and
        then apply the corresponded configuration message to parse the data
        message.

    Example:
    # The first example creates a command message and then creates a parser to
    parse the message.
        my_msg = command(CMD='off') # Creates a command message.
        print(my_msg)               # Just to show the content.
        my_parser = parser()        # Creates a parser
        my_msgs = my_parser.parse(msg)  # Parse the previously created mseeage\
                                        and returns a list of parsed messages
        print(my_msgs[0].data.cmd.name) # Print the contant of the command
    """

    def __init__(self, raw_cfg_pkt=None):
        self._mini_cfgs = MiniCfgs()
        if raw_cfg_pkt:
            self.parse(raw_cfg_pkt)

    def parse(self, raw_bytes):
        """Parse synchrphasor message stream


        """
        stream = []
        _io = KaitaiStream(BytesIO(raw_bytes))
        while not _io.is_eof():
            try:
                message = PhasorMessage(_io, _mini_cfgs=self._mini_cfgs)
                if type(message.data) != type(b''):
                    stream.append(message)
            except Exception as e:
                LOG.debug("Parsing error.")
                print(len(stream))
                raise
        return stream


class PcapParser(object):
    """ A Parser that parses synchrphasor messages captured in pcap file
    """
    def __init__(self):
        self._parser = Parser()

    def from_pcap(self, file_name):
        self._pcap = Pcap.from_file(file_name)


        _r_stream = b''  # Get all bytes from pcap
        for pkt in self._pcap.packets:
            try:
                _raw_data = pkt.body.body.body.body
                _r_stream += _raw_data
            except Exception as e:
                LOG.debug("Pcap message parsing error.")
                pass


        _p_stream = b''  # Extract synchrophasor bytes
        l = 1  # Expect to get at least one byte
        while len(_r_stream) >= l:
            if l == 1:  # Looking for header
                i = 0
                for b in _r_stream:
                    if b == 170:
                        l = 4 # Looking for length info
                        break
                    i += 1
                _r_stream = _r_stream[i:]  # Remove unrecognized bytes
            if l == 4 and len(_r_stream)>=4:
                l = struct.unpack('>H',_r_stream[2:4])[0]  # Get synchrophasor msg length
            if l > 4 and l <= len(_r_stream):
                _p_stream += _r_stream[:l]
                _r_stream = _r_stream[l:]
                l = 1

        return self._parser.parse(_p_stream)


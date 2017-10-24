#!/usr/bin/env python3

from kaitaistruct import __version__ as ks_version, KaitaiStruct, KaitaiStream, BytesIO
from .common import PhasorMessage
from .minicfg import MiniCfgs


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

    def __init__(self, raw_cfg_pkt: bytes = None):
        self._mini_cfgs = MiniCfgs()
        if raw_cfg_pkt:
            self.parse(raw_cfg_pkt)

    def parse(self, raw_bytes: bytes):
        """Parse synchrphasor message stream


        """
        stream = []
        self._raw_data = raw_bytes
        _io = KaitaiStream(BytesIO(self._raw_data))
        while not _io.is_eof():
            message = PhasorMessage(_io, _mini_cfgs=self._mini_cfgs)
            stream.append(message)
        return stream

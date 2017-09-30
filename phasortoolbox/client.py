#!/usr/bin/env python3

import asyncio
from phasortoolbox.message import Command
from phasortoolbox import Parser

    """A synchrphaor protocol connection clinet.

    Connects to any devices that follow IEEE Std C37.118.2-2011, send
    commands, and receiving data.
    According to IEEE Std C37.118.2-2011 'The device providing data is the
    server and the device receiving data is the client.'

    Example:
        tcpServer = {
            'MODE' : 'TCP'
            'IDCODE' : 1
            'SERVER_IP' : '10.0.0.1'
            'SERVER_TCP_PORT' : 4712
            'CLIENT_TCP_PORT' : 'AUTO'
            }
        udpServer = {
            'MODE' : 'UDP'
            'IDCODE' : 1
            'SERVER_IP' : '10.0.0.1'
            'SERVER_UDP_PORT' : 4713
            'CLIENT_UDP_PORT' : 'AUTO'
            }
        tcpudpServer = {
            'MODE' : 'TCPUDP'
            'IDCODE' : 1
            'SERVER_IP' : '10.0.0.1'
            'SERVER_TCP_PORT' : 4712
            'CLIENT_TCP_PORT' : 'AUTO'
            'SERVER_UDP_PORT' : 4713
            'CLIENT_UDP_PORT' : 4713
            }
        spontaneousServer = {
            'MODE' : 'SPON'
            'IDCODE' : 1
            'SERVER_IP' : '10.0.0.1'
            'SERVER_UDP_PORT' : 4713
            'CLIENT_UDP_PORT' : 4713
            }

        Client(**tcpServer)
    """


class Client(object):
    def __init__(self,
                 MODE='TCP',
                 IDCODE=1,
                 SERVER_IP='10.0.0.1',
                 SERVER_TCP_PORT=4712,
                 CLIENT_TCP_PORT='AUTO',
                 SERVER_UDP_PORT=4713,
                 CLIENT_UDP_PORT='AUTO',):
        self.MODE = MODE
        self.IDCODE = IDCODE
        self.SERVER_IP = SERVER_IP
        self.SERVER_TCP_PORT = SERVER_TCP_PORT
        self.CLIENT_TCP_PORT = CLIENT_TCP_PORT
        self.SERVER_UDP_PORT = SERVER_UDP_PORT
        self.CLIENT_UDP_PORT = CLIENT_UDP_PORT
        self.loop = asyncio.get_event_loop()
    def connect(self):
        if self.MODE == 'TCP':
            connect= self.loop.create_connection(
                lambda: self._tcp(self.loop, self.IDCODE), self.SERVER_IP,
                self.SERVER_TCP_PORT)
        print('Connecting to',self.SERVER_IP,'...')
        self.transport, self.protocol = self.loop.run_until_complete(connect)


    @asyncio.coroutine
    def transmit(self):
        self.transport.write(command(IDCODE=self.IDCODE, CMD='on'))
    def stop(self):
        self.transport.write(command(IDCODE=self.IDCODE, CMD='off'))
        self.transport.close()
    class _tcp(asyncio.Protocol):
        def __init__(self, loop, IDCODE=1):
            self.IDCODE = IDCODE
            self.loop = loop
        def connection_made(self, transport):
            print('Connected!')
        def data_received(self, data):
            print('Data received: {!r}'.format(data.decode()))
        def connection_lost(self, exc):
            print('The server closed the connection')
            print('Stop the event loop')
            self.loop.stop()


pmu = client(SERVER_IP='130.127.88.146', SERVER_TCP_PORT=4722, IDCODE=1)

pmu.connect()
pmu.transmit()pmu
pmu.stop()

    def __init__(self, **kwargs):
        self.loop = asyncio.get_event_loop()
        self.tsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.usock =
        if kwargs['mode'] == 'tcp':
            self._tcp(**kwargs)
        pass

    def connect(self):

    def close(self):
        if (not self.mode == 'spontaneous') and self.transmision == 'on':
            self.send_command('off')
            print('Stream ', self.IDCODE, 'transmision off.')
        self.disconnect()

    def stransmit(self):
        self.loop()
        try:
            pass
        finally:
            self.close()
            pass

    def _tcp(self, **kwargs):

    def _udp(self, **kwargs):

    def __init__(self, ip='127.0.0.1', idcode=0, mode='tcp', parse=True):
        self.ip = ip
        self.idcode = idcode
        self.mode = mode
        # A Parser() can automatically parse received packet, and remember's
        # the latest configurations.
        self.ifparser = parser

    def connect(self):
        """
        TCP client
        :return: 
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.ip, self.port)
        try:
            self.sock.connect(server_address)
            print('Connected to ', str(server_address))
        except Exception as e:
            print('Connection ', str(server_address), ' failed!')
            print(e)
            pass
        return

    def _tcp(self):
        pass

    def _udp(self):
        pass

    def _tcpudp(self):
        pass

    def _spontaneous(self):
        pass

        if mode == 'tcp':
            self.port = 4712
        elif mode == 'udp':
            self.port = 4713
        elif mode == 'tcpudp'

        elif mode == 'spontaneous'
            usock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            usock.bind(())

    def transmit(self, q):
        mp.Process(target=self._transmit,
                   args=(q,)).start()

    def _transmit(self, q):
        """
        q is a mp.Queue(), used to send collected data out.
        :param q:
        :return:
        """
        msg = command(idcode=self.idcode, cmd='off')
        self.sock.sendall(msg)
        msg = command(idcode=self.idcode, cmd='cfg2')
        self.sock.sendall(msg)
        msg = command(idcode=self.idcode, cmd='on')
        self.sock.sendall(msg)
        self.status = 'on'
        while self.status == 'on':
            try:
                _header = self.sock.recv(4)
                tZero = timer()
                t0 = timer()
                raw_pkt = _header + \
                    self.sock.recv(int.from_bytes(
                        _header[2:4], byteorder='big'))
                # Right now, always parse and try to get frequency from station 0
                messages = self.parser.parse(raw_pkt)
                print('Time to parse:', timer() - t0)
                try:
                    t0 = timer()
                    soc = str(messages[0].soc) + '.' + \
                        str(messages[0].fracsec.raw_fraction_of_second)
                    idcode = messages[0].idcode
                    freq = messages[0].data.pmu_data[0].freq.freq.freq
                    print(soc, idcode, freq)
                    if freq:
                        q.put({'Arrive_time': tZero, 'soc': soc,
                               'idcode': idcode, 'freq': freq, 'timer': timer()})
                    print('Time to insert to Queue:', timer() - t0)
                except Exception as e:
                    print(e)
                    pass
            except Exception as e:
                print(e)
                self.close()
                break

    def close(self):
        self.status = 'off'
        msg = command(idcode=self.idcode, cmd='off')
        self.sock.sendall(msg)
        self.sock.close()
        return

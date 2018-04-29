#!/usr/bin/env python3
import time
import asyncio
from concurrent.futures import Executor
from phasortoolbox.message import Command
from phasortoolbox import Parser

"""A synchrphaor protocol connection clinet.

Connects to any devices that follow IEEE Std C37.118.2-2011, send
commands, and receiving data.
According to IEEE Std C37.118.2-2011 'The device providing data is the
server and the device receiving data is the client.'

Examples:

    F.2.1 TCP-only method:
    "The client needs to know only the server address and port. "
    pmu_client = Client(remote_ip='130.127.88.170',remote_port=4722, id_code=16, mode='TCP')

    F.2.2 UDP-only method:
    "The client must know the server address and port number. The server can respond to the client port or a different port by prior arrangement."
    local_port is optional if not configured on the PMU.
    pmu_client = Client(remote_ip='130.127.88.160',remote_port=41180, local_port=4713 , id_code=15, mode='UDP')

    F.2.3 TCP/UDP method:
    "The server address and port must be known to the client, and the client port UDP port must be known to the server (PMU)."
    pmu_client = Client(remote_ip='130.127.88.159',remote_port=4722, local_port=4713 , id_code=14, mode='TCP_UDP')

    
    F.2.4 Spontaneous data transmission method:
    "The drawback to this method is lack of ability to turn the data stream on and off, ... "
    remote_ip is optional.
    pmu_client = Client(remote_ip='130.127.88.160',local_port=4713, id_code=15, mode='UDP_S')
    pmu_client.run()
"""


class Client():
    def __init__(self, id_code, remote_ip=None, remote_port=None, local_port=None, mode='TCP', callback=lambda msg: None, filter_key={'data'}, loop=asyncio.get_event_loop(), executor=None):
        self.remote_ip = remote_ip  # ('10.0.0.1', 4712)
        self.remote_port = remote_port
        self.local_port = local_port  # ('0.0.0.0', 4712)
        self.id_code = id_code
        self.callback = callback
        self.mode = mode
        self.loop = loop
        self.executor = executor
        self.filter_key = filter_key
        self._parser = Parser()
        self._transport = None
        self._protocol = None

    def callback(self, data):
        """
        Impliment your function
        """
        pass

    def run(self, c=0):
        _old_loop, self.loop = self.loop, asyncio.new_event_loop()
        self.loop.create_task(self.cor_run(c))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.run_until_complete(self.close())
        self.loop.close()
        self.loop = _old_loop

    async def cor_run(self, c=0):
        self._receive_counter = 0
        self.c = c
        if self.mode == 'TCP':
            print('Connecting to: (\'{}\', {}) ...'.format(self.remote_ip, self.remote_port))
            self._transport, self._protocol = await self.loop.create_connection(lambda: _TCPOnly(self.id_code, self.receive_data), self.remote_ip, self.remote_port)

        elif self.mode == 'UDP':
            self._transport, self._protocol = await self.loop.create_datagram_endpoint(lambda: _UDPOnly(self.id_code, self.receive_data), local_addr=('0.0.0.0', self.local_port) if self.local_port else None, remote_addr=(self.remote_ip, self.remote_port))

        elif self.mode == 'TCP_UDP':
            print('Connecting to: (\'{}\', {}) ...'.format(self.remote_ip, self.remote_port))
            await self.loop.create_datagram_endpoint(
                lambda: _UDP_Spontaneous(self.remote_ip, None, self.receive_data),
                local_addr=('0.0.0.0', self.local_port))
            self._transport, self._protocol = await self.loop.create_connection(lambda: _TCPOnly(self.id_code, self.receive_data),
                              self.remote_ip, self.remote_port)

        elif self.mode == 'UDP_S':
            print('Waiting for configuration packet ...')
            self._transport, self._protocol = await self.loop.create_datagram_endpoint(
                lambda: _UDP_Spontaneous(self.remote_ip, self.remote_port, self.receive_data),
                local_addr=('0.0.0.0', self.local_port))  #,
                              #remote_addr=(self.IP, None))

    def receive_data(self, data):
        arr_time = time.time()
        msgs = self._parser.parse(data)
        for msg in msgs:
            if msg.sync.frame_type.name not in self.filter_key:
                print('"{}" message received from: {}'.format(msg.sync.frame_type.name, self._transport.get_extra_info('peername')))
                continue
            msg.arr_time = arr_time
            msg.parse_time = time.time() - arr_time
            self.callback(msg)
            self._receive_counter += 1
            #self.loop.run_in_executor(self.executor, self.callback, msg)
            if self.c == 0:
                return
            elif self.c > 1:
                self.c -= 1
                return
            elif self.c == 1:
                self.loop.stop()

    def check_receive_counter(self):
        if self._receive_counter == 0:
            print('No packet received. Are you using the correct IP, port, and id_code?')
        else:
            print(self._receive_counter, 'messages received.')

    async def close(self):
        if self._transport:
            if not self._transport.is_closing():
                if self.mode != 'UDP_S':
                    self._protocol.close()
                    self._transport.close()
        self.check_receive_counter()


class _TCPOnly(asyncio.Protocol):
    def __init__(self, id_code, callback=lambda data: None):
        self.id_code = id_code
        self.data_received = callback

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        print('Connected to:', self.peername)
        self.transport.write(Command(self.id_code, 'off'))
        print('Command "data off" sent to:', self.peername)
        self.transport.write(Command(self.id_code, 'cfg2'))
        print('Command "send configuration2" sent to:', self.peername)
        self.transport.write(Command(self.id_code, 'on'))
        print('Command "data on" sent to:', self.peername)

    def close(self):
        self.transport.write(Command(self.id_code, 'off'))
        print('Command "data off" sent to:', self.peername)

    def connection_lost(self, exc):
        print('Connection', self.peername, 'closed.')


class _UDPOnly(asyncio.DatagramProtocol):
    def __init__(self, id_code, callback=lambda data: None):
        self.id_code = id_code
        self.callback = callback

    def datagram_received(self, data, addr):
        self.callback(data)

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        print('Connected to:', self.peername)
        self.transport.sendto(Command(self.id_code, 'off'))
        print('Command "data off" sent to:', self.peername)
        self.transport.sendto(Command(self.id_code, 'cfg2'))
        print('Command "send configuration2" sent to:', self.peername)
        self.transport.sendto(Command(self.id_code, 'on'))
        print('Command "data on" sent to:', self.peername)

    def close(self):
        self.transport.sendto(Command(self.id_code, 'off'))
        print('Command "data off" sent to:', self.peername)

    def connection_lost(self, exc):
        print('Connection', self.peername, 'closed.')


class _UDP_Spontaneous(asyncio.DatagramProtocol):
    def __init__(self, remote_ip=None, remote_port=None,
                 callback=lambda data: None):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self.callback = callback
        self._pass_score = (self.remote_ip is not None) + (self.remote_port is not None)

    def datagram_received(self, data, addr):
        if (addr[0] == self.remote_ip) + (addr[1] == self.remote_port) == self._pass_score:
            self.callback(data)














#!/usr/bin/env python3
import gc
import logging
import time
import asyncio
import struct
import socket
from concurrent.futures import Executor, ThreadPoolExecutor
from phasortoolbox.message import Command
from phasortoolbox import Parser
LOG=logging.getLogger('phasortoolbox.client')


class Client():
    """A synchrophasor protocol connection client.

This class automates the communication to any devices that follow the IEEE Std C37.118.2-2011. The remote device could be a PMU or a PDC. This class automatically connects to the remote device, send commands if necessary, receiving data, parse the received message, and call the callback() function with parsed data messages.

There are four connection methods defined in C37.118.2-2011:

F.2.1 TCP-only method:
"The client needs to know only the server address and port. "
Example:
    >>> pmu_client = Client(remote_ip='10.0.0.1',remote_port=4712, idcode=1, mode='TCP')
    >>> pmu_client.run()

F.2.2 UDP-only method:
"The client must know the server address and port number. The server can respond to the client port or a different port by prior arrangement."
local_port is optional if not configured.
Example:
    >>> pmu_client = Client(remote_ip='10.0.0.2',remote_port=4713, local_port=4713, idcode=2, mode='UDP')
    >>> pmu_client.run()

F.2.3 TCP/UDP method:
"The server address and port must be known to the client, and the client port UDP port must be known to the server (PMU)."
Example:
    >>> pmu_client = Client(remote_ip='10.0.0.3',remote_port=4712, local_port=4713 , idcode=3, mode='TCP_UDP')
    >>> pmu_client.run()

    
F.2.4 Spontaneous data transmission method:
"The drawback to this method is lack of ability to turn the data stream on and off, ... " 
remote_ip and remote_port is optional if not known.
    >>> pmu_client = Client(remote_ip='10.0.0.4',local_port=4713, idcode=4, mode='UDP_S')
    >>> pmu_client.run()

You need to define the callback function. Once received a data message, the callback function will be called.
Example:
    >>> f = lambda message: print(message)
    >>> pmu_client.callback = f
    >>> pmu_client.run()
    """
    def __init__(self, idcode, remote_ip=None, remote_port=None, local_port=None, mode='TCP', callback=None, process_pool=False):
        """docstring for __init__
        Args:
            idcode (int):  The idcode of the remote device. This argument must be provided.
            remote_ip (str): The IP address of the remote device. e.g. '10.0.0.1'. This argument is optional under "UDP_S" mode.
            remote_port (int):  The port number of the remote device. e.g. 4712. This argument is optional under "UDP_S" mode.
            local_port (int):  The local port number. e.g. 4712. This argument is optional under "TCP", and "UDP" mode.
            mode (str): The operation mode. Options are: "TCP" for TCP-only method; "UDP" for UDP-only method; "TCP_UDP" for TCP/UDP method; "UDP_S" for Spontaneous data transmission method.
            callback (function): The function called when a data message is received. 
        """
        self.remote_ip = remote_ip  # '10.0.0.1'
        self.remote_port = remote_port  # 4712
        self.local_port = local_port  # 4712
        self.idcode = idcode  # 1
        if callback is not None:
            self.callback = callback  # lambda x: None
        self.mode = mode
        self.receive_counter = 0
        self.process_pool = process_pool
        self._parser = Parser()
        self._transport = None
        self._protocol = None
        self._pdc_callbacks = {}
        self._garbage_collection = True
        self.set_loop()

    def callback(self, data):
        """Called when a data message is received. 
        This is an empty function. 
        Args:
            data (PhasorMessage): This is the parsed data message
        """
        pass

    def run(self, c=0, loop=None, executor=None):
        """An event loop warper.
        This function creates a new event loop and schedule the coro_run() then let the event loop run_forever(). When stopped, do some clean up.
        Args:
            c (int): defines the number of data messages received before stop. The default value is 0, which means run forever.
        """
        self.set_loop(loop, executor)
        self.loop.create_task(self.coro_run(c))
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.run_until_complete(self.coro_close())
            self.checkreceive_counter()
        self.loop.close()

    async def coro_run(self, c=0):
        """Make the connection.
        This is a coroutine. After a connection is made, send command messages to require configuration messages and start transmission if necessary according to the running mode.
        Args:
            c (int): defines the number of data messages received before stop. The default value is 0, which means run forever.
        """
        self.receive_counter = 0
        self.c = c
        if self.mode == 'TCP':
            LOG.info('Connecting to: (\'{}\', {}) ...'.format(self.remote_ip, self.remote_port))
            self._transport, self._protocol = await self.loop.create_connection(lambda: _TCPOnly(self.idcode, self._data_received), self.remote_ip, self.remote_port)

        elif self.mode == 'UDP':
            self._transport, self._protocol = await self.loop.create_datagram_endpoint(lambda: _UDPOnly(self.idcode, self._data_received), local_addr=('0.0.0.0', self.local_port) if self.local_port else None, remote_addr=(self.remote_ip, self.remote_port))

        elif self.mode == 'TCP_UDP':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                  socket.IPPROTO_UDP)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            sock.bind(('0.0.0.0', self.local_port))
            LOG.info('Connecting to: (\'{}\', {}) ...'.format(self.remote_ip, self.remote_port))
            await self.loop.create_datagram_endpoint(
                lambda: _UDP_Spontaneous(self.remote_ip, None, self._data_received), sock=sock)
            self._transport, self._protocol = await self.loop.create_connection(lambda: _TCPOnly(self.idcode, self._data_received),
                              self.remote_ip, self.remote_port)

        elif self.mode == 'UDP_S':
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM,
                                  socket.IPPROTO_UDP)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            sock.bind(('0.0.0.0', self.local_port))
            LOG.warning('Waiting for configuration packet, this may last a minute ...')
            self._transport, self._protocol = await self.loop.create_datagram_endpoint(
                lambda: _UDP_Spontaneous(self.remote_ip, self.remote_port, self._data_received), sock=sock)

    def _data_received(self, data, perf_counter, arr_time, addr=None):
        if self.process_pool:
            future = self.executor.submit(self._parser.parse, data)
            if future.exception():
                raise future.exception()
            msgs = future.result()
        else:
            msgs = self._parser.parse(data)
        if len(msgs)>0:
            parse_time = (time.perf_counter() - perf_counter)/len(msgs)
        for msg in msgs:
            if msg.sync.frame_type.name == 'data':
                msg.perf_counter = perf_counter
                msg.arr_time = arr_time
                msg.parse_time = parse_time
                self.receive_counter += 1
                #if self.process_pool:
                #    future = self.executor.submit(self.callback, msg)
                #    if future.exception():
                #        raise future.exception()
                #else:
                self.callback(msg)
                for pdc_id in self._pdc_callbacks:
                    self._pdc_callbacks[pdc_id](msg)
    
                if self._garbage_collection:
                    gc.collect()
    
                if self.c == 0:
                    return
                elif self.c > 1:
                    self.c -= 1
                    return
                elif self.c == 1:
                    self.loop.stop()
            else:
                LOG.warning('"{}" message received from: {}.'.format(msg.sync.frame_type.name, self._transport.get_extra_info('peername') if addr is None else addr))

    def checkreceive_counter(self):
        """Print the number of data messages received in the last run
        """
        LOG.warning('{} data messages received from device "idcode {}".'.format(self.receive_counter, self.idcode))

    async def coro_close(self):
        """Close the connection.
        This is a coroutine. Before a connection is closed, send command messages to stop transmission if necessary according to the running mode.
        """
        if self._transport:
            if not self._transport.is_closing():
                if self.mode != 'UDP_S':
                    self._protocol.close()
                    self._transport.close()


    def set_loop(self, loop=None, executor=None):
        """Assign an event loop and and executor to the instance.
        Call this function if you want the instance to run on external event loop and executor. 
        Args:
            loop (asyncio.AbstractEventLoop): Default value is asyncio.new_event_loop()
            executor (concurrent.futures.Executor): Default value is ThreadPoolExecutor()
        """
        self.loop = loop if loop is not None else asyncio.new_event_loop()
        self.executor = executor if executor is not None else ThreadPoolExecutor()

    def _add_pdc(self, _pdc_id, _pdc_callback, loop, executor):
        self._pdc_callbacks[_pdc_id] = _pdc_callback
        self._garbage_collection = False
        self.set_loop(loop, executor)

    def _remove_pdc(self, _pdc_id):
        del(self._pdc_callbacks[_pdc_id])
        if self._pdc_callbacks == {}:
            self._garbage_collection = True
        self.set_loop()


class _TCPOnly(asyncio.Protocol):
    def __init__(self, idcode, callback=lambda data: None):
        self.idcode = idcode
        self.buf = _stream_buffer(callback)

    def data_received(self, data):
        perf_counter = time.perf_counter()
        arr_time = time.time()
        self.buf.add_bytes(data, perf_counter, arr_time)

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        LOG.warning('Connected to: {}.'.format(str(self.peername)))
        self.transport.write(Command(self.idcode, 'off'))
        LOG.info('Command "data off" sent to: {}.'.format(str(self.peername)))
        self.transport.write(Command(self.idcode, 'cfg2'))
        LOG.info('Command "send configuration2" sent to: {}.'.format(str(self.peername)))
        self.transport.write(Command(self.idcode, 'on'))
        LOG.info('Command "data on" sent to: {}.'.format(str(self.peername)))

    def close(self):
        self.transport.write(Command(self.idcode, 'off'))
        LOG.info('Command "data off" sent to: {}.'.format(str(self.peername)))

    def connection_lost(self, exc):
        LOG.warning('Connection {} closed.'.format(str(self.peername)))


class _UDPOnly(asyncio.DatagramProtocol):
    def __init__(self, idcode, callback=lambda data: None):
        self.idcode = idcode
        self.buf = _stream_buffer(callback)

    def datagram_received(self, data, addr):
        perf_counter = time.perf_counter()
        arr_time = time.time()
        self.buf.add_bytes(data, perf_counter, arr_time, addr)

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        LOG.warning('Connected to: {}.'.format(str(self.peername)))
        self.transport.sendto(Command(self.idcode, 'off'))
        LOG.info('Command "data off" sent to: {}.'.format(str(self.peername)))
        self.transport.sendto(Command(self.idcode, 'cfg2'))
        LOG.info('Command "send configuration2" sent to: {}.'.format(str(self.peername)))
        self.transport.sendto(Command(self.idcode, 'on'))
        LOG.info('Command "data on" sent to: {}.'.format(str(self.peername)))

    def close(self):
        self.transport.sendto(Command(self.idcode, 'off'))
        LOG.info('Command "data off" sent to: {}.'.format(str(self.peername)))

    def connection_lost(self, exc):
        LOG.warning('Connection {} closed.'.format(str(self.peername)))


class _UDP_Spontaneous(asyncio.DatagramProtocol):
    def __init__(self, remote_ip=None, remote_port=None,
                 callback=lambda data, addr: None):
        self.remote_ip = remote_ip
        self.remote_port = remote_port
        self._pass_score = (self.remote_ip is not None) + (self.remote_port is not None)
        self.buf = _stream_buffer(callback)

    def datagram_received(self, data, addr):
        perf_counter = time.perf_counter()
        arr_time = time.time()
        #print('ha',addr[0],self.remote_ip,addr[1],self.remote_port,self._pass_score)
        if (addr[0] == self.remote_ip) + (addr[1] == self.remote_port) == self._pass_score:
            self.buf.add_bytes(data, perf_counter, arr_time, addr)

class _stream_buffer():
    def __init__(self, callback):
        self.data = b''
        self.l = 1 # 1 means waiting for header, larger than 1 means waiting to process l bytes
        self.callback = callback

    def add_bytes(self, bytes_, perf_counter, arr_time, addr=None):
        self.data += bytes_
        while len(self.data) >= self.l:
            if self.l == 1:
                self.find_header()
            if self.l == 4 and len(self.data)>=4:
                self.l = struct.unpack('>H',self.data[2:4])[0]
            if self.l > 4 and self.l <= len(self.data):
                self.callback(self.data[:self.l], perf_counter, arr_time, addr)
                self.data=self.data[self.l:]
                self.l = 1

    def find_header(self):
        i = 0
        for b in self.data:
            if b == 170:
                self.l = 4 # waiting for length info
                break
            i += 1
        self.data = self.data[i:]








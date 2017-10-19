#!/usr/bin/env python3
import time
import asyncio
from concurrent import futures
#import functools
from phasortoolbox.message import Command
from phasortoolbox import Parser
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
"""A synchrphaor protocol connection clinet.

Connects to any devices that follow IEEE Std C37.118.2-2011, send
commands, and receiving data.
According to IEEE Std C37.118.2-2011 'The device providing data is the
server and the device receiving data is the client.'

Examples:

    # To quickly test a remote host:
    loop = asyncio.get_event_loop()
    remote_pmu = Client(SERVER_IP='10.0.0.1',
              SERVER_TCP_PORT=4712, IDCODE=1, loop=loop)
    remote_pmu.connection_test()
"""


class Client(object):
    def __init__(
        self,
        SERVER_IP='10.0.0.1',
        SERVER_TCP_PORT=4712,
        CLIENT_TCP_PORT='AUTO',
        SERVER_UDP_PORT=4713,
        CLIENT_UDP_PORT='AUTO',
        MODE='TCP',
        IDCODE=1,
        loop: asyncio.AbstractEventLoop() = None,
        executor: futures.Executor() = None,
        parser: Parser() = None,
        output_list=[]
    ):
        self.IDCODE = IDCODE
        self.SERVER_IP = SERVER_IP
        self.SERVER_TCP_PORT = SERVER_TCP_PORT
        self.CLIENT_TCP_PORT = CLIENT_TCP_PORT
        self.SERVER_UDP_PORT = SERVER_UDP_PORT
        self.CLIENT_UDP_PORT = CLIENT_UDP_PORT
        self.MODE = MODE
        self.executor = executor
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        if parser:
            self.parser = parser
        else:
            self.parser = Parser()
        self.output_list = output_list
        if self.MODE == 'TCP':
            async def connect():
                print('Connecting to:', self.SERVER_IP, '...')
                await self.loop.create_connection(
                    lambda: self._TCP(self),
                    host=self.SERVER_IP, port=self.SERVER_TCP_PORT)

            async def close():
                self.cmd_transport.close()
        self.connect = connect
        self.close = close

    async def send_cmd(self, CMD):
        self.cmd_transport.write(Command(self.IDCODE, CMD))
        print('Command \"' + CMD + '\" sent to', self.SERVER_IP)

    async def run(self):
        await self.connect()
        await self.send_cmd('off')
        await self.send_cmd('cfg2')
        await self.send_cmd('on')

    async def handle_message(self, data):
        """
        This function will only be called if self.client.output_list
        is not None
        when connected.
        """
        _arrtime = time.time()
        #_msgs_future = self.loop.run_in_executor(
        #    self.executor, functools.partial(self.parser.parse, data))
        # await asyncio.sleep(0)
        # msgs = await _msgs_future
        msgs = self.parser.parse(data)
        _parse_time = time.time() - _arrtime
        for msg in msgs:
            msg._arrtime = _arrtime
            msg._parse_time = _parse_time
        for q in self.output_list:
            await q.put(msg)

    async def clean_up(self):
        await self.send_cmd('off')
        await self.close()

    class _TCP(asyncio.Protocol):
        def __init__(self, client):
            self.client = client
            self.transport = None

        def connection_made(self, transport):
            self.transport = transport
            self.client.cmd_transport = self.transport
            print('Connected to:', self.transport.get_extra_info('peername'))
            if not self.client.output_list:
                print('No output_list defined. Received data will be dropped.')

        def data_received(self, data):
            asyncio.ensure_future(self.client.handle_message(data))

        def connection_lost(self, exc):
            print('Connection ', self.transport.get_extra_info(
                'peername'), 'closed.')

    def connection_test(self):
        try:
            task = self.loop.create_task(self.run())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.call_soon_threadsafe(task.cancel)
            self.loop.run_until_complete(self.clean_up())

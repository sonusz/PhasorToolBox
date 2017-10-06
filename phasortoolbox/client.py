#!/usr/bin/env python3

import socket
import asyncio
import functools
from phasortoolbox.message import Command
from phasortoolbox import Parser
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

    # An easy way to process a received message would be use function
    # 'Client.transmit_callback()' to callback your function when a packet
    # is received:

    from datetime import datetime
    from phasortoolbox import Parser


    def your_print_time_tag_fun(raw_pkt, my_parser):
        message = my_parser.parse_message(raw_pkt)
        time_tag = float(message.soc) + \
                    float(message.fracsec.fraction_of_second)
        time_tag = datetime.utcfromtimestamp(
            time_tag).strftime("UTC: %m-%d-%Y %H:%M:%S.%f")
        print(time_tag)

    def main():
        my_parser = Parser()
        try:
            loop.run_until_complete(
            remote_pmu.transmit_callback(your_print_time_tag_fun, my_parser))
        except KeyboardInterrupt:
            loop.run_until_complete(remote_pmu.cleanup())

    if __name__ == '__main__':
        main()


    # Overwrite the transmit_callback() function:

"""


class Client(object):
    def __init__(self,
                 SERVER_IP='10.0.0.1',
                 SERVER_TCP_PORT=4712,
                 CLIENT_TCP_PORT='AUTO',
                 SERVER_UDP_PORT=4713,
                 CLIENT_UDP_PORT='AUTO',
                 MODE='TCP',
                 IDCODE=1,
                 loop=None,
                 executor=None,
                 parser=None
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
        if self.MODE == 'TCP':
            async def connect():
                self.tsock = socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM)
                self.tsock.setblocking(False)
                self.server_address = (self.SERVER_IP, self.SERVER_TCP_PORT)
                if self.CLIENT_TCP_PORT != 'AUTO':
                    self.tsock.bind('', self.CLIENT_TCP_PORT)
                try:
                    await self.loop.sock_connect(
                        self.tsock, self.server_address)
                except Exception as e:
                    print('Connection', str(self.server_address),
                          'failed. Please check IP and PORT settings')
                    print('Exit the program and try again.')
                    print(e)
                    raise

            async def send_command(CMD):
                await self.loop.sock_sendall(
                    self.tsock, Command(self.IDCODE, CMD))

            async def receive_data_message():
                raw_pkt = await self.loop.sock_recv(self.tsock, 4)
                raw_pkt += await self.loop.sock_recv(
                    self.tsock, int.from_bytes(
                        raw_pkt[2:4], byteorder='big'))
                return raw_pkt
            receive_conf = receive_data_message
            # No different under TCP mode

            async def close_connection():
                self.tsock.close()
        self.connect = connect
        self.send_command = send_command
        self.receive_conf = receive_conf
        self.receive_data_message = receive_data_message
        self.close_connection = close_connection

    async def transmit_callback(self, target, *args):
        if not callable(target):
            raise TypeError("target must be a callable, "
                            "not {!r}".format(type(target)))
        await self.connect()
        await self.send_command('off')
        await self.send_command('cfg2')
        raw_pkt = await self.receive_conf()
        self.loop.run_in_executor(
            self.executor, functools.partial(target, raw_pkt, *args))
        await self.send_command('on')
        try:
            while True:
                raw_pkt = await self.receive_data_message()
                self.loop.run_in_executor(
                    self.executor, functools.partial(target, raw_pkt, *args))
        except KeyboardInterrupt:
            pass
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print("\n")
            print(e)
            print("Last packet received:", raw_pkt)
            await self.cleanup()

    async def _connection_test(self):
        import sys
        from datetime import datetime
        from itertools import cycle
        await self.connect()
        print('Connected to', self.SERVER_IP)
        try:
            await self.send_command('off')
            await self.send_command('cfg2')
            try:
                raw_pkt = await asyncio.wait_for(self.receive_conf(), 5)
            except asyncio.TimeoutError:
                print(
                    'No response, Please check IDCODE setting.'
                )
                return
            message = self.parser.parse_message(raw_pkt)
            print(message.sync.frame_type.name,
                  'received from', self.SERVER_IP)
            await self.send_command('on')
            print("Transmission ON. (Press 'Ctrl+C' to stop.)")
            for char in cycle('|/-\\'):
                raw_pkt = await self.receive_data_message()
                message = self.parser.parse_message(raw_pkt)
                time_tag = float(message.soc) + \
                    float(message.fracsec.fraction_of_second)
                time_tag = datetime.utcfromtimestamp(
                    time_tag).strftime("UTC: %m-%d-%Y %H:%M:%S.%f")
                freqlist = [str(
                    self.parser.parse_message(raw_pkt)
                    .data.pmu_data[i].freq) + 'Hz\t' for i in range(
                    len(self.parser.parse_message(raw_pkt).data.pmu_data)
                )]
                status = char + time_tag + '\t' + ''.join(freqlist)
                sys.stdout.write(status + "\r")
                sys.stdout.flush()
        except KeyboardInterrupt:
            pass
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print("\n")
            print(e)
            print("Last packet received:", raw_pkt)
            await self.cleanup()

    async def cleanup(self):
        print('\n')
        await self.send_command('off')
        print('Transmission OFF.')
        await self.close_connection()
        print('Connection to', self.SERVER_IP, 'closed.')

    def connection_test(self):
        try:
            task = self.loop.create_task(self._connection_test())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.call_soon_threadsafe(task.cancel)
            self.loop.run_until_complete(self.cleanup())

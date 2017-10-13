#!/usr/bin/env python3

import asyncio
from phasortoolbox import Parser
from phasortoolbox import Client


class PDC(object):
    """docstring for PDC"""

    def __init__(self,
                 WAIT_TIME=0.3,
                 loop=None,
                 executor=None,
                 parser=None):
        self._Clientlist = []
        self.WAIT_TIME = WAIT_TIME
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        if parser:
            self.parser = parser
        else:
            self.parser = Parser()
        self.executor = executor

    def add_client(self, Client):
        Client.loop = self.loop
        Client.executor = self.executor
        self._Clientlist.append(Client)

    async def _connection_test(self):
        import sys
        from datetime import datetime
        from itertools import cycle
        for client in self._Clientlist:
            await client.connect()
            print('Connected to', client.SERVER_IP)
        try:
            raw_stream = b''
            for client in self._Clientlist:
                await client.send_command('off')
                await client.send_command('cfg2')
                try:
                    raw_pkt = await asyncio.wait_for(client.receive_conf(), 5)
                    raw_stream += raw_pkt
                except asyncio.TimeoutError:
                    print(
                        'No response from',client.SERVER_IP,'Please check IDCODE setting.'
                    )
                    return
                message = self.parser.parse_message(raw_pkt)
                print(message.sync.frame_type.name,
                      'received from', client.SERVER_IP)
                await client.send_command('on')
            print("Transmission ON. (Press 'Ctrl+C' to stop.)")
            raw_stream = b''
            for char in cycle('|/-\\'):
                for client in self._Clientlist:
                    raw_stream += await client.receive_data_message()
                messages = self.parser.parse(raw_stream)
                time_tag = float(messages[0].soc) + \
                    float(messages[0].fracsec.fraction_of_second)
                time_tag = datetime.utcfromtimestamp(
                    time_tag).strftime("UTC: %m-%d-%Y %H:%M:%S.%f")
                freqlist = []
                for message in messages:
                    freqlist += [str(
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
        for client in self._Clientlist:
            await client.cleanup()

    def connection_test(self):
        try:
            task = self.loop.create_task(self._connection_test())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.loop.call_soon_threadsafe(task.cancel)
            self.loop.run_until_complete(self.cleanup())

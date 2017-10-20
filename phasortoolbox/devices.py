#!/usr/bin/env python3
import asyncio
from concurrent import futures
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class DevicesControl(object):
    """An event loop warper.

    Use this controler to schedule the 'run()' function designed in each
    device, as well as manage the connections between devices.

    Examples:
        #To create a network that two PDCs are getting data from three PMUs:
        my_devices = DevicesControl()
        my_pdc1 = PDC()
        my_pdc2 = PDC()
        my_pmu1 = Client(SERVER_IP='10.0.0.1',
                  SERVER_TCP_PORT=4712, IDCODE=1)
        my_pmu2 = Client(SERVER_IP='10.0.0.2',
                  SERVER_TCP_PORT=4712, IDCODE=2)
        my_pmu3 = Client(SERVER_IP='10.0.0.3',
                  SERVER_TCP_PORT=4712, IDCODE=3)

        my_devices.device_list = [my_pdc1, my_pdc2, my_pmu1, my_pmu2, my_pmu3]
        my_devices.connection_list = [
        [[my_pmu1,my_pmu2,my_pmu3], [my_pdc1,my_pdc2]]
        ]

        my_devices.run()
    """

    def __init__(
        self,
        device_list=[],
        connection_list=[],
        loop: asyncio.AbstractEventLoop() = None,
        executor: futures.Executor() = None
    ):
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        if executor:
            self.executor = executor
        else:
            self.executor = futures.ProcessPoolExecutor()
        self.loop.set_default_executor(self.executor)
        self.device_list = device_list
        self.connection_list = connection_list

    def connect(self):
        for connection in self.connection_list:
            for source in connection[0]:
                for destination in connection[1]:
                    source._output_list.append(destination)
                    destination._input_list.append(source)

    def disconnect(self):
        for connection in self.connection_list:
            for source in connection[0]:
                for destination in connection[1]:
                    source._output_list = []
                    destination._input_list = []

    def run(self):
        self.connect()
        try:
            tasks = [None] * len(self.device_list)
            for i, device in enumerate(self.device_list):
                tasks[i] = self.loop.create_task(device.run())
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            for i, device in enumerate(self.device_list):
                self.loop.call_soon_threadsafe(tasks[i].cancel)
                self.loop.run_until_complete(device.clean_up())
        self.disconnect()

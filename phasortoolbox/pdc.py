#!/usr/bin/env python3
import time
import collections
import asyncio
from concurrent import futures
from phasortoolbox import Parser
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PDC(object):
    """docstring for PDC"""

    def __init__(
        self,
        WAIT_TIME=0.3,
        BUF_SIZE=1,
        FILTER={'data'},
        loop: asyncio.AbstractEventLoop() = None,
        executor: futures.Executor() = None,
        parser: Parser() = None,
    ):
        self.WAIT_TIME = WAIT_TIME
        self.FILTER = FILTER
        self._input_list = []
        self._input_queue = asyncio.Queue()
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        self.executor = executor

    async def run(self, target=None):
        if not self._input_list:
            print('No input defined.')
        while True:
            try:
                msg = await self._input_queue.get()
                print(msg.sync.frame_type.name)
                if msg.sync.frame_type.name not in self.FILTER:
                    continue
                # self._buffer.add_msg(msg)
                print(self._input_queue.qsize(), msg.idcode, msg._arrtime,
                      time.time() - msg._arrtime, msg._parse_time)
            except asyncio.CancelledError:
                break

    async def clean_up(self):
        pass

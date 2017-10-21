#!/usr/bin/env python3
import time
import bisect
from collections import deque defaultdict
import asyncio
from concurrent import futures
from phasortoolbox import Parser
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PDC(object):
    """docstring for PDC


    Example:
    my_pdc = PDC()


    """

    def __init__(
        self,
        WAIT_TIME=0.1,
        BUF_SIZE=1,
        FILTER={'data'},
        loop: asyncio.AbstractEventLoop() = None,
        executor: futures.Executor() = None,
        parser: Parser() = None,
        step_time=0.01,
        callback=None
    ):
        self.WAIT_TIME = WAIT_TIME
        self.FILTER = FILTER
        self.BUF_SIZE = BUF_SIZE
        self.callback = callback
        self.step_time = step_time
        self._input_list = []
        self._input_queue = asyncio.Queue()
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        self.executor = executor

    async def run(self):
        if not self._input_list:
            print('No input defined.')
            return
        self._ordered_idcode_list = []
        for _input in self._input_list:
            self._ordered_idcode_list.append(_input.IDCODE)
        self._ordered_idcode_list.sort()
        if not self.callback or \
                (self.callback and not callable(self.callback)):
            raise TypeError("Input must be a function, "
                            "not {!r}".format(type(self.callback)))
        self._buf = {}
        self._buf_index = deque()
        while True:
            try:
                ###############################################################
                """Check which data can be send 
                All data are kept in an dictionary. A valid record also
                contains the earlest arrive time and a flag indicated if the
                record has been sent previously. The newest record returned to
                the user callback must be a new record that has never been
                sent before. Thus, first check if the newest data has beend
                sent beforefrom the newest arrived data.
                 """
                _temp_send_list = []
                for time_tag in reversed(self._buf_index):
                    if len(_temp_send_list) == self.BUF_SIZE:
                        break
                    if (len(_temp_send_list) > 0) and
                    (
                        self._buf[time_tag]['sent'] or
                        (
                            (
                                len(self._buf[time_tag]) - 2 ==
                                len(self._input_list)
                            ) or
                            (
                                time.time() -
                                self._buf[time_tag]['_arrtime'] >=
                                self.WAIT_TIME
                            )
                        )
                    ):
                        _temp_send_list.append(time_tag)
                        # Valid to send, also the first one already found.
                        continue

                    elif (len(_temp_send_list) == 0) and
                    (
                        not self._buf[time_tag]['sent']
                    ) and
                    (
                        ((len(self._buf[time_tag]) - 2) ==
                            len(self._input_list)) or
                        ((time.time() - self._buf[time_tag]
                          ['_arrtime']) >= self.WAIT_TIME)
                    ):
                        # The fist item in the list must be the newest recored
                        # valid to send and has never been sent before.
                        _temp_send_list.append(time_tag)
                        continue

                    elif (len(_temp_send_list) == 0) and
                    (self._buf[time_tag]['sent']):
                        # The newest recored valid to send has been sent
                        # before, no need to do anything.
                        break

                if len(_temp_send_list) == self.BUF_SIZE:
                    # Will not do anything if not engough data to send
                    # Prepare send msgs and remove old data.
                    buffer_msgs = [
                        [
                            self._buf[time_tag][idcode] for idcode in
                            self._ordered_idcode_list
                        ]
                        for time_tag in reversed(_temp_send_list)
                    ]
                    for time_tag in _temp_send_list:
                        self._buf[time_tag]['sent'] = True
                    _del_list = []
                    for time_tag in self._buf:
                        if time_tag < _temp_send_list[-1]:
                            _del_list.append(time_tag)
                    for time_tag in _del_list:
                        del self._buf[time_tag]
                        self._buf_index.remove(time_tag)
                    # self.loop.run_in_executor(
                    #    self.executor, self.callback, buffer_msgs)
                    self.callback(buffer_msgs)

                ###############################################################
                """Get all data from queue
                If user's callback function is too slow, queue size will keep
                increase. Get all data from queue if queue have pendding
                data. If user's callback function is fast enough, then wait
                until item available in queue.
                """
                if self._input_queue.qsize >= 1:
                    msgs = []
                    for i in range(self._input_queue.qsize):
                        msgs.append(self._input_queue.get_nowait())
                else:
                    msgs = [None]
                    msgs[0] = await asyncio.wait_for(
                        self._input_queue.get(), self.step_time)

                for msg in msgs:
                    if msg.sync.frame_type.name not in self.FILTER:
                        continue
                    try:
                        self._buf[msg.time][msg.idcode] = msg
                    except KeyError:    # New time tag
                        self._buf[msg.time] = defaultdict(lambda: None)
                        self._buf[msg.time][msg.idcode] = msg
                        self._buf[msg.time]['_arrtime'] = msg._arrtime
                        bisect.insort(self._buf_index, msg.time)
                ###############################################################
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    async def clean_up(self):
        pass

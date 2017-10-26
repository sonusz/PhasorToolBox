#!/usr/bin/env python3
import time
import bisect
from collections import deque, defaultdict
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
        CALLBACK=None,
        BUF_SIZE=1,
        FILTER={'data'},
        WAIT_TIME=0.1,
        loop: asyncio.AbstractEventLoop()=None,
        executor: futures.Executor()=None,
        step_time=0.01,
        returnNone=False,
        count=0
        # Partially Timeout time stamps will be discarded on False
        # None will be returned for timeout data on True.
    ):
        self.WAIT_TIME = WAIT_TIME
        self.FILTER = FILTER
        self.BUF_SIZE = BUF_SIZE
        self.step_time = step_time
        self.buf_time_out = self.BUF_SIZE * self.WAIT_TIME * 2
        self._input_list = []
        self._output_list = []
        self._input_queue = asyncio.Queue()
        if loop:
            self.loop = loop
        else:
            self.loop = asyncio.get_event_loop()
        self.executor = executor
        if CALLBACK:
            self.CALLBACK = CALLBACK
        self.returnNone = returnNone
        self.count = count

    async def run(self, count=None):
        if not self._input_list:
            print('No input defined.')
            return
        self._ordered_idcode_list = []
        for _input in self._input_list:
            self._ordered_idcode_list.append(_input.IDCODE)
        self._ordered_idcode_list.sort()
        if not callable(self.CALLBACK):
            raise TypeError("Input must be a function, "
                            "not {!r}".format(type(self.CALLBACK)))
        self._buf = {}
        self._buf_index = deque()
        if not count:
            count = self.count
        while True:
            try:
                ###############################################################
                """Check which data can be send 
                All data are kept in an dictionary. A valid record also
                contains the earlest arrive time and a flag indicated if the
                record has been sent previously. The newest record returned to
                the user CALLBACK must be a new record that has never been
                sent before. Thus, first check if the newest data has beend
                sent beforefrom the newest arrived data.
                 """
                _temp_send_list = []
                _time_out_by = time.time() - self.WAIT_TIME
                for time_tag in reversed(self._buf_index):
                    if len(_temp_send_list) == self.BUF_SIZE:
                        break
                    if (
                        (len(_temp_send_list) > 0) and
                        (
                            self._buf[time_tag]['sent'] or
                            (
                                len(self._buf[time_tag]) - 2 ==
                                len(self._input_list)
                            ) or
                            (
                                self.returnNone and
                                (
                                    self._buf[time_tag]['_arrtime'] <
                                    _time_out_by
                                )
                            )
                        )
                    ):
                        _temp_send_list.append(time_tag)
                        # Valid to send, also the first one already found.
                        continue
                    elif (
                        (
                            len(_temp_send_list) == 0
                        ) and
                        (
                            not self._buf[time_tag]['sent']
                        ) and
                        (
                            (
                                (len(self._buf[time_tag]) - 2) ==
                                len(self._input_list)
                            ) or
                            (
                                self.returnNone and
                                (
                                    self._buf[time_tag]['_arrtime'] <
                                    _time_out_by
                                )
                            )
                        )
                    ):
                        # The fist item in the list must be the newest recored
                        # valid to send and has never been sent before.
                        _temp_send_list.append(time_tag)
                        continue
                    elif (
                        (len(_temp_send_list) == 0) and
                        (self._buf[time_tag]['sent'])
                    ):
                        # The newest recored valid to send has been sent
                        # before, no need to do anything.
                        break
                if len(_temp_send_list) == self.BUF_SIZE:
                    # Will not do anything if not enough data to send
                    # Prepare send msgs
                    buffer_msgs = [
                        [
                            self._buf[time_tag][idcode] for idcode in
                            self._ordered_idcode_list
                        ]
                        for time_tag in reversed(_temp_send_list)
                    ]
                    # self.loop.run_in_executor(
                    #    self.executor, self.CALLBACK, buffer_msgs)
                    _usr_buffer_msgs = self.CALLBACK(
                        buffer_msgs)  # Call user's function
                    if _usr_buffer_msgs:
                        for _devices in self._output_list:
                            await _devices._input_queue.put(_usr_buffer_msgs)
                    if count == 0:
                        pass
                    elif count > 1:
                        count -= 1
                    elif count == 1:
                        break
                    for time_tag in _temp_send_list:
                        self._buf[time_tag]['sent'] = True
                ###############################################################
                # Remove time out data from _buf
                _del_list = []
                if _temp_send_list:
                    # Remove all data until the last one sent
                    for time_tag in self._buf_index:
                        _del_list.append(time_tag)
                        if time_tag < _temp_send_list[-1]:
                            continue
                        elif time_tag == _temp_send_list[-1]:
                            break
                else:
                    # Remove all data until buffer time out
                    _time_out_by = time.time() - self.buf_time_out
                    for time_tag in self._buf_index:
                        if self._buf[time_tag]['_arrtime'] < _time_out_by:
                            _del_list.append(time_tag)
                            continue
                        else:
                            break
                for time_tag in _del_list:
                    del self._buf[time_tag]
                    self._buf_index.remove(time_tag)
                ###############################################################
                """Get all data from queue
                If user's CALLBACK function is too slow, queue size will keep
                increase. Get all data from queue if queue have pendding
                data. If user's CALLBACK function is fast enough, then wait
                until item available in queue.
                """
                if self._input_queue.qsize() >= 1:
                    msgs = []
                    for i in range(self._input_queue.qsize()):
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
        self.loop.stop()

    async def clean_up(self):
        pass

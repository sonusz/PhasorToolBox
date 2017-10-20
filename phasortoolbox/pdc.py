#!/usr/bin/env python3
import time
from collections import defaultdict
import asyncio
from concurrent import futures
from phasortoolbox import Parser
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PDC(object):
    """docstring for PDC"""

    def __init__(
        self,
        WAIT_TIME=0.1,
        BUF_SIZE=2,
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

    def _check_buf(self):
        """Check which data can be send
        All data are kept in an dictionary. A valid record also contains the
        earlest arrive time and a flag indicated if the record has been sent
        previously. The newest record returned to callback must be a new
        record that has never been sent before. Thus, the loop check all data
        from the newest arrived data.
        """
        _temp_send_list = []
        for time_tag in reversed(self._buf_index):
            # Check from the last received
            if self._buf[time_tag]['sent'] and not _temp_send_list:
                # The newest recored has been sent, no need to keep checking
                return
            elif self._buf[time_tag]['sent'] and _temp_send_list:
                # Continue to add if the first one that has never been sent
                # is found. Keep add until send buffer is full
                _temp_send_list.append(time_tag)
                if len(_temp_send_list) >= self.BUF_SIZE:
                    # Break if list full
                    break
                continue
            elif not self._buf[time_tag]['sent'] and \
                (
                len(self._buf[time_tag]) - 2 == len(self._input_list)
                or
                time.time() - self._buf[time_tag]['_arrtime'] >= self.WAIT_TIME
            ):
                # Find the first one that can be send and never sent before
                _temp_send_list.append(time_tag)  # Add to prepare to send list
                if len(_temp_send_list) >= self.BUF_SIZE:
                    # Break if list full
                    break
                continue
        if len(_temp_send_list) >= self.BUF_SIZE:
            buffer_msgs = [
                [
                    self._buf[time_tag][idcode] for idcode in
                    self._ordered_idcode_list
                ]
                for time_tag in reversed(_temp_send_list)]
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
        self._buf_index = []
        while True:
            try:
                self._check_buf()
                # check if buf is ready for sent
                msg = await asyncio.wait_for(
                    self._input_queue.get(), self.step_time)
                if msg.sync.frame_type.name not in self.FILTER:
                    continue
                try:
                    self._buf[msg.time][msg.idcode] = msg
                except KeyError:    # New time tag
                    self._buf[msg.time] = defaultdict(lambda: None)
                    self._buf[msg.time][msg.idcode] = msg
                    self._buf[msg.time]['_arrtime'] = msg._arrtime
                    self._buf_index.append(msg.time)
                    self._buf_index = sorted(self._buf_index)
                # print(self._input_queue.qsize(), msg.idcode, msg._arrtime,
                #      time.time() - msg._arrtime, msg._parse_time)
            except asyncio.TimeoutError:
                continue
            except asyncio.CancelledError:
                break

    async def clean_up(self):
        pass

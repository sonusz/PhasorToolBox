#!/usr/bin/env python3
import time
import bisect
from collections import defaultdict
import asyncio
from concurrent import futures
from phasortoolbox import Parser
import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


class PDC(object):
    """docstring for PDC


    Example:
    my_pdc = PDC()

    This class aligns in coming synchrophasor messages using time tags.


    """

    def __init__(
        self,
        CALLBACK=None,  # Function which will be executed while data available, defined by user
        BUF_SIZE=1,  # Number of historical data returned to CALLBACK
        returnNone=False,
        # returnNone determines if partially received record should be discarded when timeout. Record will be discarded on False; None will be used as place holder and return partially received record on True.
        WAIT_TIME=0.1,  # The max time to wait for each time tag, will return None if returnNone is True
        count=0,
        FILTER={'data'},  # Type of PMU message will be processed
        loop: asyncio.AbstractEventLoop()=None,
        executor: futures.Executor()=None,
        step_time=0.01  # The time to wait for asyncio when no data coming in
        # Count of data send before stop. 0 for send forever.
    ):
        self.WAIT_TIME = WAIT_TIME
        self.FILTER = FILTER
        self.BUF_SIZE = BUF_SIZE
        self.step_time = step_time
        self.buf_time_out = self.BUF_SIZE * self.WAIT_TIME * 10
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
        self._idcode_list = []
        for _input in self._input_list:
            self._idcode_list.append(_input.IDCODE)
        if not callable(self.CALLBACK):
            raise TypeError("Input must be a function, "
                            "not {!r}".format(type(self.CALLBACK)))
        self._buf = {}
        self._buf_index = []
        if not count:
            count = self.count
        while True:
            try:
                ###############################################################
                """The following chunk of code checks which data can be send
                and generate a list of ordered time tags.
                The returned data should be a list of ordered and aligned
                record. The first record in the returned list should never
                been sent before. The following record needs to be valid or
                has been send before.
                A flag (_buf[time_tag]['sent']) is used to indicate if the
                record has been sent before. True will be assigned if the
                record has been sent before (_buf[time_tag]['sent']==True).
                 """
                _temp_send_list = []
                _time_out_by = time.time() - self.WAIT_TIME
                # This is a time point in the past, time tags earlier/smaller
                # than this point will be sent or discarded.
                if len(self._buf_index) > 0:
                    _newest_tag = self._buf_index[-1]
                    if (self._buf[_newest_tag]['sent'] is not True
                        # The record with newest time tag haven't been sent
                        and (len(self._buf[_newest_tag]) - 2 ==
                            len(self._input_list)
                            # Data ready to send
                            or (self.returnNone
                                and self._buf[_newest_tag]['_arrtime'] <
                                _time_out_by
                                )  # Data time out
                            )
                        ):
                        _temp_send_list.append(_newest_tag)
                        for time_tag in reversed(self._buf_index[:-1]):
                            if len(_temp_send_list) == self.BUF_SIZE:
                                # Exit this loop when get enough data
                                break
                            if (self._buf[time_tag]['sent'] is True
                                # The record have been sent before
                                or len(self._buf[time_tag]) - 2 ==
                                            len(self._input_list)
                                # Data ready to send
                                or self.returnNone
                                # Data time out allow to send
                                ):
                                _temp_send_list.append(time_tag)

                ###############################################################
                """ The following chunk of code prepare buffer_msgs for user's
                function. If multiple time tags are returned, the time tags
                are ordered in the receiving order (The newest received will
                be the last one in the returned list).
                """
                if len(_temp_send_list) == self.BUF_SIZE:
                    # Will not do anything if not enough data to send
                    # Prepare send msgs and call user defined function
                    buffer_msgs = [
                        [
                            self._buf[time_tag][idcode] for idcode in
                            self._idcode_list
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
                if len(_temp_send_list) == self.BUF_SIZE:
                    # Remove all data until the last one sent
                    for time_tag in self._buf_index:
                        if time_tag < _temp_send_list[-1]:
                            _del_list.append(time_tag)
                        else:
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
                increase. Get all data from queue if queue have pending
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


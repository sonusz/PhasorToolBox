#!/usr/bin/env python3

import gc
import time
import bisect
import asyncio
from collections import defaultdict
from concurrent.futures import Executor, ThreadPoolExecutor
from phasortoolbox import Synchrophasor
import logging

LOG=logging.getLogger('phasortoolbox.pdc')

class PDC(object):
    """docstring for PDC


Example:
my_pdc = PDC()

This class aligns in coming synchrophasor messages using time tags.


    """
    def __init__(self, callback=None, clients=[], time_out=0.1, history=1, return_on_time_out=False, process_pool=False):
        if callback is not None:
            self.callback = callback
        self.clients = clients
        self.receive_counter = 0
        self.time_out = time_out
        self.history = history
        self.return_on_time_out = return_on_time_out
        self.process_pool = process_pool

    def callback(self, buf_sync):
        """
        Implement your function
        """
        pass

    def run(self, c=0, loop=None, executor=None):
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
        self.receive_counter = 0
        self.c = c
        idcode_list = [client.idcode for client in self.clients]
        if len(idcode_list) > len(set(idcode_list)):
            raise Exception('Duplicate id_code found. C37.118.2 standard does not support duplicate id_code. idcode list:',idcode_list)
            
        self._buf = _Buffer(idcode_list, self._synchrophasors_created, self.time_out, self.history, self.return_on_time_out)
        self._buf_task = asyncio.ensure_future(self._buf.coro_check_timeout())
        for client in self.clients:
            client._add_pdc(id(self), self._buf.add_msg, self.loop, self.executor)
            asyncio.ensure_future(client.coro_run())

    async def coro_close(self):
        if self._buf_task :
            self._buf_task.cancel()
        for client in self.clients:
            await client.coro_close()
            client._remove_pdc(id(self))

    def checkreceive_counter(self):
        LOG.warning(str(self.receive_counter)+' synchrophasors created.')
        for client in self.clients:
            client.checkreceive_counter()

    def _synchrophasors_created(self, synchrophasors):
        self.receive_counter += 1
        if self.process_pool:
            future = self.executor.submit(self.callback, synchrophasors)
            if future.exception():
                raise future.exception()
        else:
            self.callback(synchrophasors)

        gc.collect()
        if self.c == 0:
            return
        elif self.c > 1:
            self.c -= 1
            return
        elif self.c == 1:
            self.loop.stop()

    def set_loop(self, loop=None, executor=None):
        self.loop = loop if loop is not None else asyncio.new_event_loop()
        self.executor = executor if executor is not None else ThreadPoolExecutor()



class _Buffer(object):
    def __init__(self, idcode_list, callback, time_out, history, return_on_time_out):
        self.idcode_list = idcode_list
        self.callback = callback
        self.time_out = time_out
        self.history = history
        self.return_on_time_out = return_on_time_out
        self._buffer_time_out = 0.2 * (history + 1)
        self._min_sleep = time_out/100
        self._data = defaultdict(lambda: defaultdict(lambda: None))
        self._arr_times = defaultdict(lambda: 0)
        self._perf_counter = defaultdict(lambda: 0)
        self._return_time_outs = {}
        self._buffer_time_outs = {}
        self._sorted_time_tags = []
        self._ready_to_send = []
        self._ready_to_send_s = set()
        self._last_sent_time_tag = None

    def add_msg(self, msg):
        if msg.time not in self._arr_times:
            bisect.insort(self._sorted_time_tags, msg.time)
        self._data[msg.time][msg.idcode] = msg
        self._arr_times[msg.time] = max(msg.arr_time,self._arr_times[msg.time])
        self._perf_counter[msg.time] = max(msg.perf_counter,self._perf_counter[msg.time])
        self._return_time_outs[msg.time] = self._arr_times[msg.time] + self.time_out
        self._buffer_time_outs[msg.time] = self._arr_times[msg.time] + self._buffer_time_out
        self._check_completeness(msg.time)

    def _check_completeness(self, time_tag):
        if len(self._data[time_tag]) == len(self.idcode_list) and time_tag not in self._ready_to_send_s:
            bisect.insort(self._ready_to_send, time_tag)
            self._ready_to_send_s.add(time_tag)
            self._send_synchrophasors_if_ready()

    def _send_synchrophasors_if_ready(self):
        if len(self._ready_to_send) >= self.history:
            if self._ready_to_send[-1] != self._last_sent_time_tag:
                synchrophasors = []
                for i in reversed(range(1, self.history+1)):
                    synchrophasors.append(Synchrophasor([self._data[self._ready_to_send[-i]][idcode] for idcode in self.idcode_list], self._ready_to_send[-i], self._arr_times[self._ready_to_send[-i]], self._perf_counter[self._ready_to_send[-i]]))
                self._last_sent_time_tag = self._ready_to_send[-1]
                self.callback(synchrophasors)

        
    def callback(self, synchrophasors):
        pass

    async def coro_check_timeout(self):
        while True:
            try:
                await asyncio.sleep(self._min_sleep)
                _now = time.time()
                if self.return_on_time_out:
                    for time_tag in self._sorted_time_tags:
                        if _now >= self._return_time_outs[time_tag] and time_tag not in self._ready_to_send_s:
                            bisect.insort(self._ready_to_send, time_tag)
                            self._ready_to_send_s.add(time_tag)
                    self._send_synchrophasors_if_ready()
                _del_tags = []
                for time_tag in self._sorted_time_tags:
                    if _now > self._buffer_time_outs[time_tag]:
                        _del_tags.append(time_tag)
                    else:
                        break
                for time_tag in _del_tags:
                    del(self._data[time_tag])
                    del(self._arr_times[time_tag])
                    del(self._perf_counter[time_tag])
                    del(self._return_time_outs[time_tag])
                    del(self._buffer_time_outs[time_tag])
                    del(self._sorted_time_tags[self._sorted_time_tags.index(time_tag)])
                    if time_tag in self._ready_to_send_s:
                        del(self._ready_to_send[self._ready_to_send.index(time_tag)])
                        self._ready_to_send_s.remove(time_tag)
            except asyncio.CancelledError:
                break
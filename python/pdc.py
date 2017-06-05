#!/usr/bin/env python3

from __future__ import division, print_function
from parser import Parser
from collections import defaultdict, deque
import socket
import multiprocessing as mp
import time
import crc16
import struct
import queue

from timeit import default_timer as timer

class SmartPDC(object):
    """
    Receive data from PMUs, auto infer missing  freq data, send to destination.
    """
    def __init__(self, sample_rate = 30, timeout = 0.00001, buf_size = 10):
        self.timeout = timeout
        self.buf_size = buf_size
        self.buf = defaultdict(lambda : defaultdict(lambda : defaultdict(None)))
        self._buf_index = []
        self.remote_devices = []
        self._in_q = mp.Queue()
        self._out_q = mp.Queue()
    def add_remote_device(self,**args):
        _ip = args['ip']
        _port =  args['port']
        _idcode = args['idcode']
        self.remote_devices.append(Client(ip=_ip, port=_port, idcode=_idcode))
    def add_ouput(self):
        pass
    def align(self):
        while self.status == 'on':
            try:
                data = self._in_q.get(timeout = self.timeout)
                t1 = timer()
                _time_tag = float(data['soc'])
                self.buf[_time_tag][data['idcode']] = data['freq']
                if _time_tag not in self._buf_index:
                    self._buf_index.append(_time_tag)
                    self._buf_index = sorted(self._buf_index)
                    if len(self._buf_index) > self.buf_size:
                        del self.buf[self._buf_index[0]]
                        del self._buf_index[0]
                print('Time to sort:', timer() - t1)
            except queue.Empty:
                pass
        print('PDC stopped.')
    def start(self):
        self.status = 'on'
        mp.Process(target=self.align,
                   args=()).start()
        for device in self.remote_devices:
            device.connect()
            device.transmit(self._in_q)
    def stop(self):
        self.status = 'off'
        for device in self.remote_devices:
            device.close()

    def ccn_predictions(self):
        pass


class Client(object):
    """
    Connects to any devises that follows C37.118.2 standard.
    """
    def __init__(self, ip = '127.0.0.1', port = 4721, idcode = 0):
        self.ip = ip
        self.port = port
        self.idcode = idcode
        self.parser = Parser()  # A Parser() can automatically parse received packet, and remember's the latest configurations.
    def connect(self):
        """
        TCP client
        :return: 
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.ip, self.port)
        try:
            self.sock.connect(server_address)
            print('Connected to ',str(server_address))
        except Exception as e:
            print('Connection ',str(server_address),' failed!')
            print(e)
            pass
        return
    def transmit(self, q):
        mp.Process(target=self._transmit,
                   args=(q,)).start()

    def _transmit(self, q):
        """
        q is a mp.Queue(), used to send collected data out.
        :param q:
        :return:
        """
        msg = command(idcode = self.idcode, cmd = 'off')
        self.sock.sendall(msg)
        msg = command(idcode = self.idcode, cmd = 'cfg2')
        self.sock.sendall(msg)
        msg = command(idcode = self.idcode, cmd = 'on')
        self.sock.sendall(msg)
        self.status = 'on'
        while self.status == 'on':
            try:
                _header = self.sock.recv(4)
                #t0 = timer()
                raw_pkt = _header + self.sock.recv(int.from_bytes(_header[2:4], byteorder='big'))
                messages = self.parser.parse(raw_pkt) # Right now, always parse and try to get frequency from station 0
                #print('Time to parse:',timer() - t0)
                try:
                    soc = str(messages[0].soc)+'.'+str(messages[0].fracsec.raw_fraction_of_second)
                    idcode = messages[0].idcode
                    freq = messages[0].data.pmu_data[0].freq.freq.freq
                    print(soc,idcode,freq)
                    if freq:
                        q.put({'soc': soc, 'idcode': idcode, 'freq': freq})
                    pass
                except Exception as e:
                    print(e)
                    pass
            except Exception as e:
                print(e)
                self.close()
                break

    def close(self):
        self.status = 'off'
        msg = command(idcode = self.idcode, cmd = 'off')
        self.sock.sendall(msg)
        self.sock.close()
        return

class Server(object):
    """
    Waiting for connections from any devises that follows C37.118.2 standard.
    """
    def __init__(self, serverIP = None):
        pass




def command(idcode,cmd):
    """
    Craft a C37.118.2 command message
    """
    idcode = '{:04x}'.format(idcode)
    status = cmd
    switcher = {
        'off': '0001',
        'on': '0002',
        'cfg1': '0004',
        'cfg2': '0005',
        'cfg3': '0006',
    }
    s = 'aa410012' + idcode + soc_time() + switcher.get(cmd)
    data = bytes.fromhex(s + checksum(s))
    return data


def soc_time():
    return '{:08x}'.format(int(time.time()))+'00'+'{:06x}'.format(int(time.time()%1*16777215))


def checksum(s):
    return '{:04x}'.format(crc16.crc16xmodem(bytes.fromhex(s), 0xffff))

if __name__ == "__main__":
    #q = mp.Queue()
    #pmu = Client(ip = '130.127.88.147', port = 4722, idcode = 2)
    #pmu.connect()
    #pmu.transmit(q)
    pdc = SmartPDC()
    pdc.add_remote_device(ip = '130.127.88.146', port = 4722, idcode = 1)
    pdc.add_remote_device(ip = '130.127.88.147', port = 4722, idcode = 2)
    pdc.start()
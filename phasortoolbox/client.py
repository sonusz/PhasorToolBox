#!/usr/bin/env python3


class Client(object):
    """
    Connects to any devises that follows IEEE Std C37.118.2-2011.
    According to IEEE Std C37.118.2-2011 'The device providing data is the
    server and the device receiving data is the client.'
    tcpServer = {
        'mode' : 'tcp'
        'IDCODE' : '0'
        'server_ip' : '10.0.0.1'
        'server_port' : '4712'
        'client_port' : 'Auto'
        }
    udpServer = {
        'mode' : 'udp'
        'IDCODE' : '0'
        'server_ip' : '10.0.0.1'
        'server_port' : '4713'
        'client_port' : 'Auto'
        }
    tcpudpServer = {
        'mode' : 'tcpudp'
        'IDCODE' : '0'
        'server_ip' : '10.0.0.1'
        'server_tcp_port' : '4712'
        'client_tcp_port' : 'Auto'
        'server_udp_port' : '4713'
        'client_udp_port' : '4713'
        }
    spontaneousServer = {
        'mode' : 'spontaneous'
        'server_ip' : '10.0.0.1'
        'client_port' : '4713'
        }
    """

    def __init__(self, ip='127.0.0.1', idcode=0, mode='tcp', parse=True):
        self.ip = ip
        self.idcode = idcode
        self.mode = mode
        # A Parser() can automatically parse received packet, and remember's
        # the latest configurations.
        self.ifparser = parser

    def connect(self):
        """
        TCP client
        :return: 
        """

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.ip, self.port)
        try:
            self.sock.connect(server_address)
            print('Connected to ', str(server_address))
        except Exception as e:
            print('Connection ', str(server_address), ' failed!')
            print(e)
            pass
        return

    def _tcp(self):
        pass

    def _udp(self):
        pass

    def _tcpudp(self):
        pass

    def _spontaneous(self):
        pass

        if mode == 'tcp':
            self.port = 4712
        elif mode == 'udp':
            self.port = 4713
        elif mode == 'tcpudp'

        elif mode == 'spontaneous'
            usock = socket.socket(
                socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            usock.bind(())

    def transmit(self, q):
        mp.Process(target=self._transmit,
                   args=(q,)).start()

    def _transmit(self, q):
        """
        q is a mp.Queue(), used to send collected data out.
        :param q:
        :return:
        """
        msg = command(idcode=self.idcode, cmd='off')
        self.sock.sendall(msg)
        msg = command(idcode=self.idcode, cmd='cfg2')
        self.sock.sendall(msg)
        msg = command(idcode=self.idcode, cmd='on')
        self.sock.sendall(msg)
        self.status = 'on'
        while self.status == 'on':
            try:
                _header = self.sock.recv(4)
                tZero = timer()
                t0 = timer()
                raw_pkt = _header + \
                    self.sock.recv(int.from_bytes(
                        _header[2:4], byteorder='big'))
                # Right now, always parse and try to get frequency from station 0
                messages = self.parser.parse(raw_pkt)
                print('Time to parse:', timer() - t0)
                try:
                    t0 = timer()
                    soc = str(messages[0].soc) + '.' + \
                        str(messages[0].fracsec.raw_fraction_of_second)
                    idcode = messages[0].idcode
                    freq = messages[0].data.pmu_data[0].freq.freq.freq
                    print(soc, idcode, freq)
                    if freq:
                        q.put({'Arrive_time': tZero, 'soc': soc,
                               'idcode': idcode, 'freq': freq, 'timer': timer()})
                    print('Time to insert to Queue:', timer() - t0)
                except Exception as e:
                    print(e)
                    pass
            except Exception as e:
                print(e)
                self.close()
                break

    def close(self):
        self.status = 'off'
        msg = command(idcode=self.idcode, cmd='off')
        self.sock.sendall(msg)
        self.sock.close()
        return

import asyncio
from phasortoolbox.message import Command
from phasortoolbox import Parser


def call_in_background(target, *args, loop=None, executor=None):
    """Schedules and starts target callable as a background task

    If not given, *loop* defaults to the current thread's event loop
    If not given, *executor* defaults to the loop's default executor

    Returns the scheduled task.
    """
    if loop is None:
        loop = asyncio.get_event_loop()
    if callable(target):
        return loop.run_in_executor(executor, target, *args)
    raise TypeError("target must be a callable, "
                    "not {!r}".format(type(target)))


class m_tcp(asyncio.Protocol):
    def __init__(self, loop, IDCODE=1):
        self.IDCODE = IDCODE
        self.loop = loop
    def connection_made(self, transport):
        print('Connected!')
    def data_received(self, data):
        print('Data received',data)
    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()




def receive():
    MODE='TCP'
    IDCODE=1
    SERVER_IP='130.127.88.146'
    SERVER_TCP_PORT=4722
    CLIENT_TCP_PORT='AUTO'
    SERVER_UDP_PORT=4713
    CLIENT_UDP_PORT='AUTO'
    loop = asyncio.get_event_loop()
    connect = loop.create_connection(
                    lambda: m_tcp(loop, IDCODE), SERVER_IP,
                    SERVER_TCP_PORT)
    transport, protocol = loop.run_until_complete(connect)
    transport.write(Command(IDCODE=IDCODE, CMD='on'))
    time.sleep(2)
    transport.write(Command(IDCODE=IDCODE, CMD='off'))
    loop.run_forever()



threaded_ticker = call_in_background(receive)





# loop=asyncio.get_event_loop()
# loop.set_debug(True)
#m_executor = concurrent.futures.ThreadPoolExecutor()
# loop.set_default_executor(m_executor)
pmu1 = Client(SERVER_IP='130.127.88.146',
              SERVER_TCP_PORT=4722, IDCODE=1)  # , loop=loop)
pmu1.connection_test()


m_test = asyncio.sleep(1)
loop.run_until_complete(m_test)




# tasks.append(tcp_mode(loop,'130.127.88.149',4722,4))
# tasks.append(tcp_mode(loop,'130.127.88.150',4722,5))
# tasks.append(tcp_mode(loop,'130.127.88.151',4722,6))
# tasks.append(tcp_mode(loop,'130.127.88.152',4722,7))
# tasks.append(tcp_mode(loop,'130.127.88.153',4722,8))
# tasks.append(tcp_mode(loop,'130.127.88.154',4722,9))
# tasks.append(tcp_mode(loop,'130.127.88.155',4722,10))
# tasks.append(tcp_mode(loop,'130.127.88.156',4722,11))
# tasks.append(tcp_mode(loop,'130.127.88.157',4722,12))
# tasks.append(tcp_mode(loop,'130.127.88.158',4722,13))
# tasks.append(tcp_mode(loop,'130.127.88.159',4722,14))
# tasks.append(tcp_mode(loop,'130.127.88.160',4722,15))
# tasks.append(tcp_mode(loop,'130.127.88.170',4722,16))
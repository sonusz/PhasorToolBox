# PhasorToolBox

The goal of PhasorToolBox is to provide a Synchrophasor Protocol ([IEEE C37.118.2-2011 Standard]) parser as well as tools that are easy to use and efficient for real-time parsing.

Tested on RedHat 7.2 with Python 3.6

## Performance:

The average times take to parse a single packet with the parser module is around 0.85 ms on a 2012 mac laptop.
According to [IEEE C37.118.2-2011 Standard], the typical range of delay caused by PDC processing & alignment is 2 ms to 2+ s.
The methods provided by the client module are coroutines. That makes it possible to connects to hundreds of PMUs/PDCs at the same time with minimal overhead.


#### To install and test the performance of the package on your device:

```bash
git clone https://github.com/sonusz/PhasorToolBox.git
cd PhasorToolBox/
python3 setup.py install
python3 parse_stream.py stream.bin
```
## Examples:

#### Parse a binary stream:
First lets read some bytes from sample measurements. You could find the 'stream.bin' in this repo:
```python
#!/usr/bin/env python3
import phasortoolbox
with open('stream.bin', "rb") as f:
    binary_data = f.read()  
```
Create a parser and parse the bytes:
```python
my_parser = phasortoolbox.Parser() # Create a parser.
measurement_data = my_parser.parse(binary_data) # Parse It!
```
Then you can access the data, e.g., the frequency value of station two stored in packet 200:
```python
print('Frequency measurement in packet 200:', \
        measurement_data[199].data.pmu_data[1].freq,'Hz')
```
#### Explore the message:

#### Test a remote device and capture some sample packets:

Assume you have a remote PMU use the IP over network communications running at "10.0.0.1" with "TCP-only" method, configured to listen to TCP 4712 port, IDCODE is 1 and accept connection from your IP.
The following example will run forever. Press 'Ctrl+C' to stop.
To run a quick test:
```python
>>> from phasortoolbox import Client
>>> my_pmu = Client(SERVER_IP='10.0.0.1',
....SERVER_TCP_PORT=4712, IDCODE=1, MODE='TCP')
>>> messages = my_pmu.test()
```
If everything goes on well, you should see something like this:
```python
Connecting to: 10.0.0.1 ...
Connected to: ('10.0.0.1', 4712)
Command "off" sent to 10.0.0.1
Command "cfg2" sent to 10.0.0.1
Command "on" sent to 10.0.0.1
Network delay:0.0548s Local delay:0.0003s UTC: 10-22-2017 02:16:45.933333 59.9862Hz
```

To capture only 1 packet:
```python
>>> messages = my_pmu.test(count=1)
```
Then, you can check the received messages:
```python
>>> messages
[[[<phasortoolbox.parser.common.Common object at 0x7f8c88423a90>]]]
```

#### Get aligned messages and integrate with your application:
```python
from phasortoolbox import PDC, Client, DevicesControl

def my_print1(buffer_msgs):
    freqlist = ' '.join("%.4f" % (
        pmu_d.freq) + 'Hz' for
        my_msg in buffer_msgs[-1] for
        pmu_d in my_msg.data.pmu_data)
    print('fun1 '+freqlist)

def main():
    my_devices = DevicesControl()

    my_pdc1 = PDC()
    my_pdc1.CALLBACK = my_print1

    my_pmu1 = Client(SERVER_IP='10.0.0.1',
              SERVER_TCP_PORT=4712, IDCODE=1)
    my_pmu2 = Client(SERVER_IP='10.0.0.2',
              SERVER_TCP_PORT=4712, IDCODE=2)
    my_pmu3 = Client(SERVER_IP='10.0.0.3',
              SERVER_TCP_PORT=4712, IDCODE=3)

    my_devices.device_list = [my_pdc1, my_pmu1, my_pmu2, my_pmu3]

    my_devices.connection_list = [
    [[my_pmu1,my_pmu2,my_pmu3], [my_pdc1]]
    ]

    my_devices.run()

if __name__ == '__main__':
    main()
```


#### Get aligned messages and integrate with multipe applications:
Just creat another pdc and function. 
```python
def my_print2(buffer_msgs):
    freqlist = ' '.join("%.4f" % (
        pmu_d.freq) + 'Hz' for
        my_msg in buffer_msgs[-1] for
        pmu_d in my_msg.data.pmu_data)
    print('fun2 '+freqlist)

my_pdc2 = PDC()
my_pdc2.CALLBACK = my_print2
```

Then change above connection_list to:
```python
my_devices.connection_list = [
    [[my_pmu1,my_pmu2,my_pmu3], [my_pdc1,my_pdc2]]
    ]
my_devices.device_list = [my_pdc1, my_pdc2, my_pmu1, my_pmu2, my_pmu3]
my_devices.run()

```


#### Multipe applications from different set of sources:
```python
my_devices.connection_list = [
    [[my_pmu1,my_pmu2], [my_pdc1]],
    [[my_pmu2,my_pmu3], [my_pdc2]]
    ]
my_devices.device_list = [my_pdc1, my_pdc2, my_pmu1, my_pmu2, my_pmu3]
my_devices.run()
```



### Some Features:
The parser can store the configuration frames and parse the following measurement packet according to it.
A parser instance can parse multiple data streams. This is useful when multiple PMU streams are captured and stored in the same file. However, each data stream must have unique 'IDCODE'. The IDCODE is used to identify which configuration frame should be used to parse a data frame.

### Note:
UTF-8, instead of ASCII, is used to parse human readable fields.
Configuration frame 3 is supported, but not tested. 
The binary parser is created with the help of using [Kaitai Struct].



## Module Reference:

##### phasortoolbox.Parser(raw_cfg_pkt=None):
A Parser that parses synchrphasor messages defined by IEEE Std C37.118.2-2011.

Note:
    When parsing a stream, the parser automatically detects and stores
    configuration messages and use the most recent received configuration
    message to parse the subsequent data messages. Multiple synchrophasor
    message streams can be parsed using one parser instance. The parser
    identifies each synchrophasor message stream by using its IDCODE and
    then apply the corresponded configuration message to parse the data
    message.

Example:
```python
# The first example creates a command message and then creates a parser to
parse the message.
>>> my_msg = Command(CMD='off') # Creates a command message.
>>> print(my_msg)               # Just to show the content.
b'\xaaA\x00\x12\x00\x01Y\xec_\xc5\x0ft\x1e#\x00\x01\xbe\x95'
>>> my_parser = Parser()        # Creates a parser
>>> my_msgs = my_parser.parse(my_msg)  # Parse the previously created mseeage\
                                and returns a list of parsed messages
>>> print(my_msgs[0].data.cmd.name) # Print the contant of the command
turn_off_transmission_of_data_frames
```
##### phasortoolbox.Parser.parse(raw_byte):


##### phasortoolbox.Command(IDCODE=1, CMD='off',TQ_FLAGS='0000', MSG_TQ='1111', TIME_BASE=16777215, USER_DEF='0000', EXT=b''):
This object returns a command message in bytes.
The CMD can be one of: 'off','on','hdr','cfg1','cfg2','cfg3','ext'.
Example usage:
```python
# Data stream 1 turn on transmission:
my_msg = Command(1,'on') 
# Data stream 2 turn off transmission:
my_msg = Command(IDCODE=2, CMD='off') 
# Send extended command frame with user defined message to the source of Data stream 3:
my_msg = Command(IDCODE=3, CMD='ext', EXT = b'User defined message')
```
##### phasortoolbox.Client():
A synchrphaor protocol connection clinet.

Connects to any devices that follow IEEE Std C37.118.2-2011, send
commands, and receiving data.
According to IEEE Std C37.118.2-2011 'The device providing data is the
server and the device receiving data is the client.'

Examples:
```python
# To quickly test a remote host:
my_pmu = Client(SERVER_IP='10.0.0.1',
          SERVER_TCP_PORT=4712, IDCODE=1)
my_pmu.test()
```
For most of the times, there is no need to directly access any methods in
this module after initiate. Use the phasortoolbox.DevicesControl() to
control this device instead.
##### phasortoolbox.Client.test(v=True, sample=True, count=0):
Run a quick connection test.
Return captured messages when sample is set to True.
Stop running after capturing 'count' packets if count is not 0. 
Inline print brief info about received messages if v is set to True. 
##### phasortoolbox.PDC():
##### phasortoolbox.PDC.CALLBACK(buffer_msgs):
##### phasortoolbox.DevicesControl():
##### phasortoolbox.DevicesControl.run():










[IEEE C37.118.2-2011 Standard]: <http://ieeexplore.ieee.org/document/6111222/>
[Kaitai Struct]: <https://github.com/kaitai-io/kaitai_struct>

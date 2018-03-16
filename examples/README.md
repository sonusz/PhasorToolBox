# PhasorToolBox Tutorial

In this tutorial, you are expected to learn:
* How Parse a synchrophasor message and get the data field you need.
* Interactive with a hardware PMU and explore the available fields in the received PMU measurement packet.
* Capture and save time-aligned data from multiple PMUs (a simple PDC).
* Send selected data back to RSCAD
* Know how to integrate your experiment with hardware PMU data.
* Understand how the delay of packets is handled.
* Understand how the historical data packets are handled when you need, e.g., ten historical data in each iteration.

## Install and test the performance of the package on your device:

```bash
git clone https://github.com/sonusz/PhasorToolBox.git
cd PhasorToolBox/
python3 setup.py install --user --prefix=
python3 parse_stream.py stream.bin
```

## Tutorial:

This tutorial has two parts. The first part gives examples to interactive with a sample synchrophasor message data stream and get the data field you need. Once you get familiar with how to get desired data fields, you can move on to the second part, where will show you how to connect multiple PMUs and implement your functions with aligned data messages.

### Interactive with a synchrophasor message data stream:
#### Example 1, parse a local binary file:

First lets read some bytes from sample measurements. You could find the 'stream.bin' in this repo:
```python
>>> import phasortoolbox
>>> with open('stream.bin', "rb") as f:
...    binary_data = f.read()  
```

Create a parser and parse the bytes:
```python
>>> my_parser = phasortoolbox.Parser() # Create a parser.
>>> measurement_data = my_parser.parse(binary_data) # Parse It!
```

Then you can access the data, e.g., the frequency value of station two stored in packet 200:
```python
>>> print('Frequency measurement in packet 200:', \
...     measurement_data[199].data.pmu_data[1].freq,'Hz')
Frequency measurement in packet 200: 65.536 Hz
```


#### Example 2, explore synchrophasor messages:
Let's keep using the 'measurement_data' we got in thre previous step as the example.
```python
>>> measurement_data[199]
<PhasorMessage |time=1217607006.04, sync, framesize=456, idcode=60, soc=1217607006, fracsec, data, chk=15394>
>>> measurement_data[199].data
<Data |pmu_data>
>>> measurement_data[199].data.pmu_data
[<PmuData |stat, phasors, freq=50.0, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>]
>>> measurement_data[199].data.pmu_data[0].phasors
[<Phasors |real=0.23024269249787369, imaginary=-100.06470703709206, magnitude=100.06497192382812, angle=-1.5684953927993774>, <Phasors |real=-86.67117694554175, imaginary=49.825644463626084, magnitude=99.9724349975586, angle=2.619847536087036>, <Phasors |real=86.54766181232355, imaginary=50.13071285849788, magnitude=100.01792907714844, angle=0.5250049233436584>]
>>> measurement_data[199].data.pmu_data[0].phasors[0].real
0.23024269249787369
```


### Interactive with remote PMUs:

The PMUs used in the following examples has the following configurations:
        
PMU1: 
IP: 10.0.0.1, IDCODE: 1, Running Mode: TCP, TCP PORT: 4712,
PMU1: 
IP: 10.0.0.2, IDCODE: 2, Running Mode: TCP, TCP PORT: 4712,

#### Example 3, test a remote device connection and capture some sample packets:

Assume you have a remote PMU use the IP over network communications running at "10.0.0.1" with "TCP-only" method, configured to listen to TCP 4712 port, IDCODE is 1 and accept connection from your IP.
To run a quick test:
```python
>>> from phasortoolbox import Client
>>> my_pmu = Client(SERVER_IP='10.0.0.1',
....SERVER_TCP_PORT=4712, IDCODE=1, MODE='TCP')
>>> messages = my_pmu.test(count = 10)
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


Then, you can explore the received messages just like we did in previous examples:
```python
>>> messages[0]
[[<PhasorMessage |time=1508997111.8333333, sync, framesize=154, idcode=3, soc=1508997111, fracsec, data, chk=26901>]]
```


#### Example 4, get aligned messages and integrate with your application:
Also, check pmu_to_file.py, pmu_to_rtds.py and freq_change.py

```python
#!/usr/bin/env python

import sys
import time
from datetime import datetime
from phasortoolbox import Client, PDC, UDPDevice, DeviceControl


def inline_print_freq(buffer_msgs):

    now = time.time()

    time_tag = datetime.utcfromtimestamp(
        buffer_msgs[-1][0].time).strftime(
        "UTC: %m-%d-%Y %H:%M:%S.%f")

    freqlist = [pmu_d.freq for msg in buffer_msgs[-1]
                for pmu_d in msg.data.pmu_data]

    freq_str = ' '.join("%.4f" % (
        my_msg) + 'Hz ' if my_msg is not None else
        'No Data' for
        my_msg in freqlist)

    sys.stdout.write(
        "Network delay:%.4fs Software delay:%.4fs " % (
            now - buffer_msgs[-1][0].time,
            now - max([_msg._arrtime for _msg in buffer_msgs[-1]])
        ) + time_tag + " " + freq_str + "\r"
    )
    sys.stdout.flush()


def main():

    pmu7 = Client(SERVER_IP='10.0.0.1',
                  SERVER_TCP_PORT=4712, IDCODE=1, MODE='TCP')
    pmu9 = Client(SERVER_IP='10.0.0.2',
                  SERVER_TCP_PORT=4712, IDCODE=2, MODE='TCP')
    pdc = PDC()
    pdc.CALLBACK = inline_print_freq  # Patch your function here!

    dc = DeviceControl()
    dc.device_list = [pmu7, pmu9, pdc]
    dc.connection_list = [
        [[pmu7, pmu9], [pdc]]
    ]

    dc.run()


if __name__ == '__main__':
    main()

```



#### Multipe applications from different set of sources:

Need edit

```python
my_devices.connection_list = [
    [[my_pmu1,my_pmu2], [my_pdc1]],
    [[my_pmu2,my_pmu3], [my_pdc2]]
    ]
my_devices.device_list = [my_pdc1, my_pdc2, my_pmu1, my_pmu2, my_pmu3]
my_devices.run()
```



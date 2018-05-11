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
>>> msgs = my_parser.parse(binary_data) # Parse It!
```

Then you can access the data, e.g., the frequency value of station two stored in packet 200:
```python
>>> msgs[199]
<PhasorMessage |time=1217607006.04, sync, framesize=456, idcode=60, soc=1217607006, fracsec, data, chk=15394>
>>> msgs[199].time
1217607006.04
>>> msgs[199].data

``` 


#### Example 2.1, explore synchrophasor messages:
Let's keep using the 'msgs' we got in thre previous step as the example.
```python
>>> msgs[199]
<PhasorMessage |time=1217607006.04, sync, framesize=456, idcode=60, soc=1217607006, fracsec, data, chk=15394>
>>> msgs[199].time
1217607006.04
>>> msgs[199].data
<Data |pmu_data>
>>> msgs[199].data.pmu_data
[<PmuData |stat, phasors, freq=50.0, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>]
>>> msgs[199].data.pmu_data
[<PmuData |stat, phasors, freq=50.0, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>, <PmuData |stat, phasors, freq=65.536, dfreq=0.0, analog, digital>]
```

#### Example 2.2, explore synchrophasor messages:
The show() method for the PhasorMessage shows every fields in the message
```python
>>> msgs[199].show()
    .time == 1217607006.04
    .chk == 15394
    .data.pmu_data[0].dfreq == 0.0
    .data.pmu_data[0].digital[0][0].current_valid_inputs == '0'
    .data.pmu_data[0].digital[0][0].name == 'Dig Channel 1   '
    .data.pmu_data[0].digital[0][0].normal_status == '0'
    .data.pmu_data[0].digital[0][0].value == '0'
    .data.pmu_data[0].digital[0][1].current_valid_inputs == '0'
    .data.pmu_data[0].digital[0][1].name == 'Dig Channel 2   '
    .data.pmu_data[0].digital[0][1].normal_status == '0'
    .data.pmu_data[0].digital[0][1].value == '0'
    .data.pmu_data[0].digital[0][2].current_valid_inputs == '0'
    .data.pmu_data[0].digital[0][2].name == 'Dig Channel 3   '
    .data.pmu_data[0].digital[0][2].normal_status == '0'
    .data.pmu_data[0].digital[0][2].value == '0'
```
.
.
.
```python
    .data.pmu_data[3].stat.pmu_trigger_detected.value == 0
    .data.pmu_data[3].stat.trigger_reason.name == 'manual'
    .data.pmu_data[3].stat.trigger_reason.value == 0
    .data.pmu_data[3].stat.unlocked_time.name == 'sync_locked_or_unlocked_less_than_10_s_best_quality'
    .data.pmu_data[3].stat.unlocked_time.value == 0
    .fracsec.fraction_of_second == 0.04
    .fracsec.leap_second_direction.name == 'add'
    .fracsec.leap_second_direction.value == 0
    .fracsec.leap_second_occurred == False
    .fracsec.leap_second_pending == False
    .fracsec.raw_fraction_of_second == 40000
    .fracsec.reserved == False
    .fracsec.time_quality.name == 'normal_operation_clock_locked_to_utc_traceable_source'
    .fracsec.time_quality.value == 0
    .framesize == 456
    .idcode == 60
    .soc == 1217607006
    .sync.frame_type.name == 'data'
    .sync.frame_type.value == 0
    .sync.magic == b'\xaa'
    .sync.reserved == False
    .sync.version_number.name == 'c_37_118_2005'
    .sync.version_number.value == 1
```

```python
>>> msgs[199].fracsec.time_quality.name
'normal_operation_clock_locked_to_utc_traceable_source'
```


### Connect remote PMUs:
The following examples also show how to retrieve data from remove device and integrate your programs.

There are four connection methods defined in C37.118.2-2011:

F.2.1 TCP-only method:
"The client needs to know only the server address and port. "
Example:
```python
>>> import logging
>>> logging.basicConfig(level=logging.DEBUG)
>>> from phasortoolbox import Client
>>> buf = []
>>> pmu_client1 = Client(remote_ip='10.0.0.1',remote_port=4712, idcode=1, mode='TCP')
>>> pmu_client1.callback = lambda msg: buf.append(msg)
>>> pmu_client1.run(100)
>>> buf[0].show()
```
F.2.2 UDP-only method:
"The client must know the server address and port number. The server can respond to the client port or a different port by prior arrangement."
local_port is optional if not configured.
Example:
```python
>>> import logging
>>> logging.basicConfig(level=logging.DEBUG)
>>> from phasortoolbox import Client
>>> pmu_client2 = Client(remote_ip='10.0.0.2',remote_port=4713, local_port=4713, idcode=2, mode='UDP')
>>> pmu_client2.callback = lambda msg: print(msg.fracsec.time_quality.name)
>>> pmu_client2.run(100)
```
F.2.3 TCP/UDP method:
"The server address and port must be known to the client, and the client port UDP port must be known to the server (PMU)."
Example:
```python
>>> import logging
>>> logging.basicConfig(level=logging.DEBUG)
>>> from phasortoolbox import Client
>>> pmu_client3 = Client(remote_ip='10.0.0.3',remote_port=4712, local_port=4713 , idcode=3, mode='TCP_UDP')
>>> pmu_client3.callback = lambda msg: print(msg.time)
>>> pmu_client3.run(100)
```
    
F.2.4 Spontaneous data transmission method:
"The drawback to this method is lack of ability to turn the data stream on and off, ... " 
remote_ip and remote_port is optional if not known.
```python
>>> import logging
>>> logging.basicConfig(level=logging.DEBUG)
>>> from phasortoolbox import Client
>>> pmu_client4 = Client(remote_ip='10.0.0.4',local_port=4713, idcode=4, mode='UDP_S')
>>> pmu_client4.callback = lambda msg: print(msg.arr_time)
>>> pmu_client4.run(100)
```

### PDC
```python
>>> from phasortoolbox import PDC
>>> pdc = PDC(clients=[pmu_client1, pmu_client2, pmu_client3, pmu_client4])
>>> pdc.callback = lambda synchrophasors: print(synchrophasors[-1].time, [synchrophasors[-1][i].data.pmu_data[0].freq for i in range(4)])
>>> pdc.run(100)
```

### To do: More examples
Check print_freq.py and print_freq2.py for some slightly more conplicated examples.

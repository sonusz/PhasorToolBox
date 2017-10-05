# PhasorToolBox

The goal of PhasorToolBox is to provide a Synchrophasor Protocol ([IEEE C37.118.2-2011 Standard]) parser in python as well as tools that are easy to use and efficient for real-time parsing.
### Performance:
The average time takes to parse a single packet is around 0.85 ms on a 2012 MacBook.
According to [IEEE C37.118.2-2011 Standard], the typical range of delay caused by PDC processing & alignment is 2 ms to 2+ s.

To install and test the performance of the package on your device:
```bash
#!/usr/bin/env bash
python setup.py install
python parse_stream.py stream.bin
```

### Parse a packet on the fly:
Will be updated when the PMU module is finished.


### Parse a binary stream:# PhasorToolBox

The goal of PhasorToolBox is to provide a Synchrophasor Protocol ([IEEE C37.118.2-2011 Standard]) parser as well as tools that are easy to use and efficient for real-time parsing.
## Performance:
The average times take to parse a single packet with the parser module is around 0.85 ms on a 2012 mac laptop.
According to [IEEE C37.118.2-2011 Standard], the typical range of delay caused by PDC processing & alignment is 2 ms to 2+ s.
The methods provided by the client module are coroutines. That makes it possible to connects to hundreds of PMUs/PDCs at the same time with minimal overhead.

#### To install and test the performance of the package on your device:
```bash
#!/usr/bin/env bash
python setup.py install
python parse_stream.py stream.bin
```
## Examples:
#### Connection Tester:
This example uses 10.0.0.1 and port 4712 as an example.
```python
>>> import asyncio
>>> from phasortoolbox import Client
>>> loop = asyncio.get_event_loop()
>>> remote_pmu = Client(SERVER_IP='10.0.0.1',
....SERVER_TCP_PORT=4712, IDCODE=1, MODE='TCP', loop=loop)
>>> remote_pmu.connection_test()
```
If everything goes on well, you should see:
```python
Connected to 10.0.0.1             
configuration_frame_2 received from 10.0.0.1                               
Transmission ON. (Press 'Ctrl+C' to stop.)                                       
\UTC: 10-05-2017 09:19:39.100000        59.98980712890625Hz
```

#### Parse packets on the fly:
This might look complicated ... more explanations will be added
```python
import asyncio
from datetime import datetime
from phasortoolbox import Client
from phasortoolbox import Parser

def your_print_time_tag_fun(raw_pkt, a_parser):
    message = a_parser.parse_message(raw_pkt)
    time_tag = float(message.soc) + \
                float(message.fracsec.fraction_of_second)
    time_tag = datetime.utcfromtimestamp(
        time_tag).strftime("UTC: %m-%d-%Y %H:%M:%S.%f")
    print(time_tag)

def main():
    loop = asyncio.get_event_loop()
    remote_pmu = Client(SERVER_IP='10.0.0.1',
        SERVER_TCP_PORT=4712, IDCODE=1, MODE='TCP', loop=loop)
    my_parser = Parser()
    try:
        loop.run_until_complete(
            remote_pmu.transmit_callback(your_print_time_tag_fun, my_parser))
    except KeyboardInterrupt:
        loop.run_until_complete(remote_pmu.cleanup())

if __name__ == '__main__':
    main()
```



### Parse a binary stream:
First lets read some bytes from previously recorded measurements:
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

### Some Features:
The parser can store the configuration frames and parse the following measurement packet according to it.
A parser instance can parse multiple data streams. This is useful when multiple PMU streams are captured and stored in the same file. However, each data stream must have unique 'IDCODE'. The IDCODE is used to identify which configuration frame should be used to parse a data frame.

### Note:
UTF-8, instead of ASCII, is used to parse human readable fields.
Configuration frame 3 is supported, but not tested. 
The binary parser is created with the help of using [Kaitai Struct].



## Module Reference:

##### phasortoolbox.Parser():
##### phasortoolbox.Parser.parse():
##### phasortoolbox.Parser.parse_message():
##### phasortoolbox.Command():
##### phasortoolbox.Client():
##### phasortoolbox.Client.connection_test():
##### phasortoolbox.Client.transmit_callback():
##### phasortoolbox.Client.connect():
##### phasortoolbox.Client.send_command():
##### phasortoolbox.Client.receive_conf():
##### phasortoolbox.Client.receive_data_message():
##### phasortoolbox.Client.close_connection():
##### phasortoolbox.Client.cleanup():







[IEEE C37.118.2-2011 Standard]: <http://ieeexplore.ieee.org/document/6111222/>
[Kaitai Struct]: <https://github.com/kaitai-io/kaitai_struct>
First lets read some bytes from previously recorded measurements:
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
Function 'parse()' returns a list that contains packets constructed from the raw binary data.
Then you can access the data, e.g., the frequency value of station two stored in packet 200:
```python
print('Frequency measurement in packet 200:', \
        measurement_data[199].data.pmu_data[1].freq,'Hz')
```

### Some Features:
The parser can store the configuration frames and parse the later measurement packet according to it.
A parser instance can parse multiple data streams. This is useful when multiple PMU streams are captured and stored in the same file. However, each data stream must have unique 'IDCODE'. The IDCODE is used to identify which configuration frame should be used to parse a data frame.

### Note:
UTF-8, instead of ASCII, is used to parse human readable fields.
Configuration frame 3 is supported, but not tested. 
The binary parser is created with the help of using [Kaitai Struct].



## Module Reference:

#### phasortoolbox.Parser():



[IEEE C37.118.2-2011 Standard]: <http://ieeexplore.ieee.org/document/6111222/>
[Kaitai Struct]: <https://github.com/kaitai-io/kaitai_struct>
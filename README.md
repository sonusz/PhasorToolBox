# PhasorToolBox

The goal of PhasorToolBox is to provide a Synchrophasor Protocol ([IEEE C37.118.2-2011 Standard]) parser as well as tools that are easy to use and efficient for real-time parsing.
### Performance:
The average times take to parse a single packet is around 0.85 ms on a 2012 mac laptop.
According to [IEEE C37.118.2-2011 Standard], the typical range of delay caused by PDC processing & alignment is 2 ms to 2+ s.

To install and test the performance of the package on your device:
```bash
#!/usr/bin/env bash
python setup.py install
python parse_stream.py stream.bin
```

### Parse a packet on the fly:
Will be updated when the PMU module is finished.


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

#### phasortoolbox.Parser():



[IEEE C37.118.2-2011 Standard]: <http://ieeexplore.ieee.org/document/6111222/>
[Kaitai Struct]: <https://github.com/kaitai-io/kaitai_struct>
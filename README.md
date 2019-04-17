# PhasorToolBox

The goal of PhasorToolBox is to provide a Synchrophasor Protocol ([IEEE C37.118.2-2011 Standard]) parser as well as tools that are easy to use and efficient for real-time parsing.

Tested on RedHat 7.2 with Python 3.6

Please check [examples] folder for examples.

Please consider to cite our paper if this package helped your work:

X. Zhong, P. Arunagirinathan, I. Jayawardene, G. K. Venayagamoorthy and R. Brooks, "PhasorToolBox – A Python Package for Synchrophasor Application Prototyping," 2018 Clemson University Power Systems Conference (PSC), Charleston, SC, USA, 2018, pp. 1-8.

https://ieeexplore.ieee.org/document/8664020

## Performance:

The average time to parse a single packet, where the data messages have four substations and 594 data fields, is 1 ms on a 2012 mac laptop.
According to [IEEE C37.118.2-2011 Standard], the typical range of delay caused by PDC processing & alignment is 2 ms to 2+ s.
The methods provided by the client module are coroutines. That makes it possible to connects to hundreds of PMUs/PDCs at the same time with minimal overhead.


#### To install and test the performance of the package on your device:

```bash
git clone https://github.com/sonusz/PhasorToolBox.git
cd PhasorToolBox/
python3 setup.py install --user  --prefix=
python3 parse_stream.py stream.bin
```


### Update May 11, 2018, Version 0.3
Supports all four connection methods (TCP only, UDP only, TCP/UDP mixed, and  UDP Spontaneous).

Add PhasorMessage.show() method.

Reconstructed Client and PDC modules.

Removed uvloop.

Bug fix.

### Update Mar 16, 2018
Add examples and tutorials in the example folder. 

### Update Jan 13, 2018, Version 0.2
Add PcapParser(). 

Now you can parse synchrophasor messages from a pcap file.

Usage:
```python
from phasortoolbox import PcapParser
my_pcap_parser = PcapParser()
msgs = my_pcap_parser.from_pcap('path/to/pcap/file.pcap')
```


#### To do:
Configuration 3 message scale factor calculations.

[IEEE C37.118.2-2011 Standard]: <http://ieeexplore.ieee.org/document/6111222/>
[Kaitai Struct]: <https://github.com/kaitai-io/kaitai_struct>
[examples]: <https://github.com/sonusz/PhasorToolBox/tree/master/examples>

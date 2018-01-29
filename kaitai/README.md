This directory contains the .ksy files used to generate the original python parser.
# VERY IMPORTANT
The data message .ksy file does not exactly follow the IEEE C37.118.2-2011 Standard.
All other messages exactly follow the IEEE C37.118.2-2011 Standard.
Modifications of the generated code are necessary to parse the synchrophasor protocol.

### Reason
The parse of data messages in the synchrophasor protocol requires the configuration message. To parse every packet on the fly, the configuration message needs to be attached in front of the data message.
However, not all data in the configuration message are necessary. It would be inefficient to append the entire configuration message before every message.

### How
So, we create two fields in the data.ksy that are not included in the standard synchrophasor protocol, which are cfg_2 and cfg_2_station. Those fields are only used to help the kaitaistruct compiler to compile and easier modification to get a working parser later. Those two fields are clearly marked in the data.ksy file.

### What needs to be modified
After generating the targeted code, those two fields need to be replaced with structure and values previously got from the configuration message.
meta:
  id: synchrophasor_header
  endian: be
seq:
  - id: data1
    type: str
    encoding: UTF-8
    size-eos: true
    doc: >
        Human-readable information about the PMU, the data sources, scaling, 
        algorithms, filtering, or other related information. 
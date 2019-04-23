# Introduction 
Tiny python library to determine actual available Cisco AP models, and their full name, specific to the regulatory 
domain of the country you provide.
# Usage

```
>>> from ciscoaplookup import *
>>> print(get_model_for('AIR-CAP1532E', 'Ukraine'))
AIR-CAP1532E-E-K9
# now lets try with a model not supported for Ukraine..
>>> print(get_model_for('AIR-CAP1552H', 'Ukraine'))
ValueError: Found AIR-CAP1552H for Ukraine - but no active regulatory domains?
>>> print(get_models())
['AIR-AP1800I', 'AIR-CAP1532I', 'AIR-AP1852', 'AIR-BLE-USB', 'AIR-AP1562D', 'AIR-AP3802E', 'AIR-OEAP1810', 'AIR-AP1815W', 'AIR-CAP702W', 'AIR-AP2802I', 'AIR-AP2602', 'AIR-CAP1552S', 'AIR-AP1572EC', 'AIR-AP3602', 'AIR-AP1832', 'AIR-AP1815T', 'AIR-AP1572IC', 'AIR-AP1815I', 'AIR-CAP702I', 'AIR-AP702I', 'AIR-RM3010L', 'AIR-SAP702I', 'AIR-CAP2702', 'C9115AXI', 'AIR-AP1542D', 'AIR-AP1602', 'COMMENTS', 'UX AP VERSION', 'AIR-CAP3702', 'AIR-CAP1552H', 'AIR-AP3802P', 'AIR-CAP1532E', 'AIR-AP3702', 'AIR-AP1542I', 'AIR-AP1562I', 'AIR-AP1562E', 'AIR-AP1810W', 'AIR-AP702W', 'C9117AXI', 'AIR-AP2702', 'AIR-AP3802I', 'AIR-CAP1552WU', 'AIR-AP4800', 'AIR-AP1815M', 'AIR-AP1532', 'IW3702-2E-UXK9', 'IW3702-4E-X-K9', 'AIR-CAP3702P', 'IW3702-4E-UXK9', 'AIR-AP1572EAC', 'AIR-AP1800S', 'IW3702-2E-X-K9', 'AIR-AP2802E', 'AIR-CAP1702']

```


# Test and Build
```
python -m unittest -v test.TestCiscoAPLookup
python setup.py sdist bdist_wheel
```
    
# Contribute
Go nuts..
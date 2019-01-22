<p align=center>
    <img src="https://www.stiebel-eltron.de/apps/ste/docroot/images/single/logo-stiebel-eltron.png"/>
</p>
<p align=center>
    <a href="https://pypi.org/project/pystiebeleltron/"><img src="https://img.shields.io/pypi/v/pystiebeleltron.svg"/></a>
    <a href="https://travis-ci.org/fucm/python-stiebel-eltron"><img src="https://img.shields.io/travis/fucm/python-stiebel-eltron.svg"/></a>
    <a href='https://coveralls.io/github/fucm/python-stiebel-eltron?branch=master'><img src='https://coveralls.io/repos/github/fucm/python-stiebel-eltron/badge.svg?branch=master' alt='Coverage Status' /></a>
  <img src="https://img.shields.io/github/license/fucm/python-stiebel-eltron.svg"/></a>
</p>

# python-stiebel-eltron
Python API for interacting with the STIEBEL ELTRON ISG web gateway via modbus for controlling integral ventilation units and heat pumps.

This module is based on the STIEBEL ELTRON [modbus user manual](https://www.stiebel-eltron.ch/content/dam/ste/ch/de/downloads/kundenservice/smart-home/Modbus/Modbus%20Bedienungsanleitung.pdf), but is not official, developed, supported or endorsed by Stiebel Eltron GmbH & Co. KG. For questions and other inquiries, use the issue tracker in this repo please.

## Requirements
You need to have [Python](https://www.python.org) installed.

* STIEBEL ELTRON Internet-Service Gateway [ISG WEB](https://www.stiebel-eltron.com/en/home/products-solutions/renewables/controller_energymanagement/internet_servicegateway/isg_web.html) with enabled [modbus module](https://www.stiebel-eltron.ch/de/home/service/smart-home/modbus.html)
  * You can call the STIEBEL ELTRON support, if your ISG does not have the modbus module enabled. They upgraded mine for free.
* STIEBEL ELTRON heatpumpt (compatible). Successfully used devices:
  * LWZ504e
  * LWZ304
* Network connection to the ISG WEB

## Installation
The package is available in the [Python Package Index](https://pypi.python.org/).

```bash
    $ pip install python-stiebel-eltron
```

## Example usage of the module
The sample below shows how to use this Python module.

```python
    from pystiebeleltron import pystiebeleltron as pyse
    from pymodbus.client.sync import ModbusTcpClient as ModbusClient

    client = ModbusClient(host='IP_ADDRESS_ISG', port=502, timeout=2)
    client.connect()

    unit = pyse.StiebelEltronAPI(client, 1)
    unit.update()
    
    print("get_target_temp: {}".format(unit.get_target_temp))
    
    client.close()
```

## License

``python-stiebel-eltron`` is licensed under MIT, for more details check LICENSE.

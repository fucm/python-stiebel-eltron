#!/usr/bin/env python3
import time
from pystiebeleltron import pystiebeleltron as pyse
from pymodbus.client import ModbusTcpClient as ModbusClient

host_ip = "192.168.1.20"
host_port = 502
slave = 1


def test_function(mod, fun):
    """Executes the given function on the Stiebel Heatpump and prints the result."""
    result = getattr(mod, fun)  # Executes function directly, instead of giving back the function reference
    print("{}: {}".format(str(fun), str(result)))


def execute_tests(unit):
    """Execute the provided tests."""
    test_function(unit, "get_current_temp")
    test_function(unit, "get_current_humidity")
    test_function(unit, "get_target_temp")
    test_function(unit, "get_operation")
    test_function(unit, "get_filter_alarm_status")
    test_function(unit, "get_heating_status")
    test_function(unit, "get_cooling_status")

    # Test set_target_temp
    print("Setting temperature to 20.0")
    current_temp = unit.get_target_temp
    unit.set_target_temp(20.0)
    time.sleep(3)
    unit.update()
    mod_temp = unit.get_target_temp
    if mod_temp != 20.0:
        print("unit.set_target_temp failed!")
    if mod_temp != current_temp:
        unit.set_target_temp(current_temp)
        time.sleep(3)
        unit.update()
    print("get_target_temp: {}".format(unit.get_target_temp))


def main():
    client = ModbusClient(host=host_ip, port=host_port, timeout=2)
    client.connect()

    unit = pyse.StiebelEltronAPI(client, slave)
    unit.update()

    execute_tests(unit)

    client.close()


if __name__ == "__main__":
    main()

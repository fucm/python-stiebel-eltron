#!/usr/bin/env python3
import time
from pystiebeleltron import pystiebeleltron as pyse
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

host_ip = "192.168.1.20"
host_port = 502
slave = 1

def test_function(mod, fun):
    """Executes the given function on the Stiebel Heatpump and prints the result."""
    result = getattr(mod, fun) # Executes function directly, instead of giving back the function reference
    print("{}: {}".format(str(fun), str(result)))


def execute_tests(unit):
    """Execute the provided tests."""
    test_function(unit, "get_current_temp")
    test_function(unit, "get_target_temp")
    test_function(unit, "get_operation")
    test_function(unit, "get_filter_alarm")

    if False:
        print("unit.get_fan_speed {}".format(unit.get_fan_speed))
        print("unit.get_heat_recovery {}".format(unit.get_heat_recovery))
        print("unit.get_heating {}".format(unit.get_heating))
        print("unit.get_heater_enabled {}".format(unit.get_heater_enabled))
        print("unit.get_cooling {}".format(unit.get_cooling))
        print("unit.get_filter_alarm {}".format(unit.get_filter_alarm))


        print("Setting fan to 3")
        unit.set_fan_speed(3)
        time.sleep(3)
        unit.update()
        print("unit.get_fan_speed {}".format(unit.get_fan_speed))

        print("Setting fan to 2")
        unit.set_fan_speed(2)
        time.sleep(3)
        unit.update()
        print("unit.get_fan_speed {}".format(unit.get_fan_speed))

        print("Setting fan to 3 with set_raw_holding_register()")
        unit.set_raw_holding_register('SetAirSpeed', 3)
        time.sleep(2)
        unit.update()
        print("unit.get_fan_speed {}".format(unit.get_fan_speed))

        print("Setting fan to 2 with set_raw_holding_register()")
        unit.set_raw_holding_register('SetAirSpeed', 2)
        time.sleep(2)
        unit.update()
        print("unit.get_fan_speed {}".format(unit.get_fan_speed))


def main():
    client = ModbusClient(host=host_ip,
                          port=host_port,
                          timeout=2)
    client.connect()

    unit = pyse.StiebelEltronAPI(client, slave)
    unit.update()

    execute_tests(unit)

    client.close()

if __name__ is "__main__":
    main()
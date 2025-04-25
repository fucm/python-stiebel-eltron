#!/usr/bin/env python
import os
import time
import pytest

# Import modbus mockup server requirements
from threading import Thread
from .mock_modbus_server import MockModbusServer as ModbusServer

# Import client requirementss
from pymodbus.client import ModbusTcpClient as ModbusClient
from pystiebeleltron import pystiebeleltron as pyse

# Modbus server connection details
host_ip = "127.0.0.1"  # "192.168.1.20"
host_port = 5020  # 502
slave = 1


class TestStiebelEltronApi:
    # __slots__ = 'api'

    @pytest.fixture(scope="module")
    def pymb_s(self, request):
        mb_s = ModbusServer()

        # Cleanup after last test did run (will run as well, if something fails in setup).
        def fin():
            stop_thread = Thread(target=mb_s.stop_async_server, name="StopReactor")
            stop_thread.start()
            if stop_thread.is_alive():
                stop_thread.join()

            if mms_thread.is_alive():
                mms_thread.join()

        request.addfinalizer(fin)

        # Start Mock Modbus server
        mms_thread = Thread(target=mb_s.run_async_server, name="MockModbusServer")
        mms_thread.start()
        time.sleep(0.1)

        return mb_s

    @pytest.fixture(scope="module")
    def pyse_api(self, request, pymb_s):
        # parameter pymb_s leads to call of fixture
        mb_c = ModbusClient(host=host_ip, port=host_port, timeout=2)
        api = pyse.StiebelEltronAPI(mb_c, slave, update_on_read=True)

        # Cleanup after last test (will run as well, if setup fails).
        def fin():
            mb_c.close()
            time.sleep(0.5)

        request.addfinalizer(fin)

        # Connect Modbus client
        connected = mb_c.connect()
        assert connected

        # Read values from device (server)
        success = api.update()
        assert success

        return api

    def test_temperature_read(self, pyse_api, pymb_s):
        pymb_s.update_input_register(0, 21.5 * 10)
        assert pyse_api.get_current_temp() == 21.5

        pymb_s.update_holding_register(1001, 22.5 * 10)
        assert pyse_api.get_target_temp() == 22.5

    def test_temperature_write(self, pyse_api):
        temperature = 22.5
        pyse_api.set_target_temp(temperature)
        time.sleep(3)

        assert pyse_api.get_target_temp() == temperature

    def test_operation(self, pyse_api):
        operation = "DHW"
        pyse_api.set_operation(operation)
        time.sleep(3)

        assert pyse_api.get_operation() == operation

    def test_humidity(self, pyse_api, pymb_s):
        humidity = 49.5
        pymb_s.update_input_register(2, humidity * 10)
        assert pyse_api.get_current_humidity() == humidity

    def test_statuses(self, pyse_api, pymb_s):
        pymb_s.update_input_register(2000, 0x0004)
        assert pyse_api.get_heating_status() is True
        assert pyse_api.get_cooling_status() is False
        assert pyse_api.get_filter_alarm_status() is False

        pymb_s.update_input_register(2000, 0x0008)
        assert pyse_api.get_heating_status() is False
        assert pyse_api.get_cooling_status() is True
        assert pyse_api.get_filter_alarm_status() is False

        pymb_s.update_input_register(2000, 0x2100)
        assert pyse_api.get_heating_status() is False
        assert pyse_api.get_cooling_status() is False
        assert pyse_api.get_filter_alarm_status() is True

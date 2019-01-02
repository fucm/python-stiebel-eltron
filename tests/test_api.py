#!/usr/bin/env python
import os
import time
import pytest

# Import modbus mockup server requirements
from threading import Thread
from tests.MockModbusServer import MockModbusServer as ModbusServer

# Import client requirementss
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pystiebeleltron import pystiebeleltron as pyse

# Modbus server connection details
host_ip = "127.0.0.1" #"192.168.1.20"
host_port = 5020 #502
slave = 1


class TestStiebelEltronApi:
    #__slots__ = 'api'

    @pytest.fixture(scope="module")
    def pyse_api(self, request):

        mb_s = ModbusServer()
        mb_c = ModbusClient(host=host_ip, port=host_port, timeout=2)
        api = pyse.StiebelEltronAPI(mb_c, slave)

        # Cleanup after last test did run (will run as well, if something fails in setup).
        def fin():
            mb_c.close()
            #time.sleep(0.5)

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

        # Connect Modbus client
        connected = mb_c.connect()
        assert connected

        # Read values from device (server)
        success = api.update()
        assert success

        return api

    def test_temperature_read(self, pyse_api):
        temp = pyse_api.get_current_temp
        assert temp >= 20.0 and temp < 25.0

        temp = pyse_api.get_target_temp
        assert temp >= 20.0 and temp < 25.0

    #@pytest.mark.skip
    def test_temperature_write(self, pyse_api):
        # Get old target temperature
        old_temp = pyse_api.get_target_temp
        new_temp = 22.5

        # Set new target temperature
        pyse_api.set_target_temp(new_temp)
        time.sleep(3)
        pyse_api.update()

        mod_temp = pyse_api.get_target_temp
        assert mod_temp == new_temp

        # Restore old target temperature
        if mod_temp != old_temp:
            pyse_api.set_target_temp(old_temp)
            time.sleep(3)
            pyse_api.update()


    @pytest.mark.skip
    def test_fail(self):
        assert 0

#!/bin/env python
"""
Pymodbus Asynchronous Server Example
--------------------------------------------------------------------------

The asynchronous server is a high performance implementation using the
twisted library as its backend.  This allows it to scale to many thousands
of nodes which can be helpful for testing monitoring software.
"""
# --------------------------------------------------------------------------- # 
# import the various server implementations
# --------------------------------------------------------------------------- # 
from pymodbus.server.async import StartTcpServer, StopServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext


class MockModbusServer(object):
    # --------------------------------------------------------------------------- # 
    # configure the service logging
    # --------------------------------------------------------------------------- # 
    import logging
    FORMAT = ('%(asctime)-15s %(threadName)-15s'
              ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
    logging.basicConfig(format=FORMAT)
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)

    def run_async_server(self):
        # ----------------------------------------------------------------------- # 
        # initialize your data store
        # ----------------------------------------------------------------------- # 
        # The datastores only respond to the addresses that they are initialized to
        # Therefore, if you initialize a DataBlock to addresses from 0x00 to 0xFF,
        # a request to 0x100 will respond with an invalid address exception.
        # This is because many devices exhibit this kind of behavior (but not all)
        #
        #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
        #
        # Continuing, you can choose to use a sequential or a sparse DataBlock in
        # your data context.  The difference is that the sequential has no gaps in
        # the data while the sparse can. Once again, there are devices that exhibit
        # both forms of behavior::
        #
        #     block = ModbusSparseDataBlock({0x00: 0, 0x05: 1})
        #     block = ModbusSequentialDataBlock(0x00, [0]*5)
        #
        # Alternately, you can use the factory methods to initialize the DataBlocks
        # or simply do not pass them to have them initialized to 0x00 on the full
        # address range::
        #
        #     store = ModbusSlaveContext(di = ModbusSequentialDataBlock.create())
        #     store = ModbusSlaveContext()
        #
        # Finally, you are allowed to use the same DataBlock reference for every
        # table or you you may use a seperate DataBlock for each table.
        # This depends if you would like functions to be able to access and modify
        # the same data or not::
        #
        #     block = ModbusSequentialDataBlock(0x00, [0]*0xff)
        #     store = ModbusSlaveContext(di=block, co=block, hr=block, ir=block)
        #
        # The server then makes use of a server context that allows the server to
        # respond with different slave contexts for different unit ids. By default
        # it will return the same context for every unit id supplied (broadcast
        # mode).
        # However, this can be overloaded by setting the single flag to False
        # and then supplying a dictionary of unit id to context mapping::
        #
        #     slaves  = {
        #         0x01: ModbusSlaveContext(...),
        #         0x02: ModbusSlaveContext(...),
        #         0x03: ModbusSlaveContext(...),
        #     }
        #     context = ModbusServerContext(slaves=slaves, single=False)
        #
        # The slave context can also be initialized in zero_mode which means that a
        # request to address(0-7) will map to the address (0-7). The default is
        # False which is based on section 4.4 of the specification, so address(0-7)
        # will map to (1-8)::
        #
        #     store = ModbusSlaveContext(..., zero_mode=True)
        # ----------------------------------------------------------------------- # 
        store = ModbusSlaveContext(
            hr=ModbusSequentialDataBlock(0, [0]*3000),
            ir=ModbusSequentialDataBlock(0, [0]*3000))
        self.context = ModbusServerContext(slaves=store, single=True)

        # ----------------------------------------------------------------------- # 
        # initialize the server information
        # ----------------------------------------------------------------------- # 
        # If you don't set this or any fields, they are defaulted to empty strings.
        # ----------------------------------------------------------------------- # 
        identity = ModbusDeviceIdentification()
        identity.VendorName = 'Pymodbus'
        identity.ProductCode = 'PM'
        identity.VendorUrl = 'http://github.com/bashwork/pymodbus/'
        identity.ProductName = 'Pymodbus Server'
        identity.ModelName = 'Pymodbus Server'
        identity.MajorMinorRevision = '1.5'

        # ----------------------------------------------------------------------- # 
        # run the server you want
        # ----------------------------------------------------------------------- # 

        # TCP Server
        StartTcpServer(self.context, identity=identity, address=("localhost", 5020))

    def stop_async_server(self):
        StopServer()

    def update_context(self, register, address, values):
        """ Update values of the active context. It should be noted
        that there is a race condition for the update.

        :param register: Type of register to update,
                            3: holding register
                            4: input register
        :param address: The starting address of the value to be changed
        :param values: List of values
        """
        assert register == 3 or register == 4
        slave_id = 0x00
        old_values = self.context[slave_id].getValues(register,
                                                      address, count=1)
        self.log.debug("Change value at address {} from {} to {}".format(
            address, old_values, values))
        self.context[slave_id].setValues(register, address, values)

    def update_holding_register(self, address, value):
        """ Update value of a holding register.

        :param address: Address to update
        :param value: Value to save
        """
        self.log.debug("Update holding register: {}:{}".format(address,
                                                               int(value)))
        self.update_context(3, address, [int(value)])

    def update_input_register(self, address, value):
        """ Update value of an input register.

        :param address: Address to update
        :param value: Value to save
        """
        self.log.debug("Update input register: {}:{}".format(address,
                                                             int(value)))
        self.update_context(4, address, [int(value)])


if __name__ == "__main__":
    mms = MockModbusServer()
    mms.run_async_server()

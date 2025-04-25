import asyncio

# from python_stiebel_eltron import EnergyManagementSettingsRegisters
from pystiebeleltron.wpm import WpmStiebelEltronAPI, WpmSystemValuesRegisters, WpmSystemParametersRegisters


async def main():
    api = WpmStiebelEltronAPI("192.168.1.209", 502)
    await api.connect()

    await api.async_update()
    for k, v in api._data.items():
        if v is not None:
            print(f"{k.name} ({k.value}): {v}")

    outside_temp = api.get_register_value(WpmSystemValuesRegisters.OUTSIDE_TEMPERATURE)
    print(f"The current outside temperature is {outside_temp} °C")

    comfort_temp = api.get_register_value(WpmSystemParametersRegisters.COMFORT_TEMPERATURE)
    print(f"The current water comfort temperature is {comfort_temp} °C")

    # await api.write_register_value(WpmSystemParametersRegisters.COMFORT_TEMPERATURE, 51)
    await api.async_update()

    comfort_temp = api.get_register_value(WpmSystemParametersRegisters.COMFORT_TEMPERATURE)
    print(f"The new current water comfort temperature is {comfort_temp} °C")

    # await api.write_register_value(EnergyManagementSettingsRegisters.SG_READY_INPUT_2, 1)

    await api.close()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(main())

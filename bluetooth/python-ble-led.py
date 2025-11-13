async def run():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print(f"Connected: {client.is_connected}")

        while True:
            # LED ON
            await client.write_gatt_char(CHARACTERISTIC_UUID, b"1")
            print("LED ON")
            await asyncio.sleep(2)

            # LED OFF
            await client.write_gatt_char(CHARACTERISTIC_UUID, b"0")
            print("LED OFF")
            await asyncio.sleep(2)

asyncio.run(run())


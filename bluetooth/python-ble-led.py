
import asyncio
from bleak import BleakClient

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"
DEVICE_ADDRESS = "80:7d:3a:f4:e8:2e"  # Replace with ESP32 MAC

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




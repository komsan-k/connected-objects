import asyncio
import threading
from bleak import BleakClient

DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"  # <-- Replace with ESP32 BLE MAC

# Three LED characteristic UUIDs
CHARACTERISTIC_UUID1 = "12345678-1234-5678-1234-56789abcdef1"  # LED 1
CHARACTERISTIC_UUID2 = "12345678-1234-5678-1234-56789abcdef2"  # LED 2
CHARACTERISTIC_UUID3 = "12345678-1234-5678-1234-56789abcdef3"  # LED 3

# Global stop flag for keypress
stop_flag = False

# --- Thread to detect any-key press ---
def wait_for_keypress():
    global stop_flag
    input("\nPress ENTER to stop the program...\n")
    stop_flag = True

async def run():
    global stop_flag

    async with BleakClient(DEVICE_ADDRESS) as client:
        print(f"Connected: {client.is_connected}")

        while not stop_flag:

            # --- LED 1 ON ---
            await client.write_gatt_char(CHARACTERISTIC_UUID1, b"1")
            print("LED 1 ON")

            # --- LED 2 ON ---
            await client.write_gatt_char(CHARACTERISTIC_UUID2, b"1")
            print("LED 2 ON")

            # --- LED 3 ON ---
            await client.write_gatt_char(CHARACTERISTIC_UUID3, b"1")
            print("LED 3 ON")

            await asyncio.sleep(2)

            # --- LED 1 OFF ---
            await client.write_gatt_char(CHARACTERISTIC_UUID1, b"0")
            print("LED 1 OFF")

            # --- LED 2 OFF ---
            await client.write_gatt_char(CHARACTERISTIC_UUID2, b"0")
            print("LED 2 OFF")

            # --- LED 3 OFF ---
            await client.write_gatt_char(CHARACTERISTIC_UUID3, b"0")
            print("LED 3 OFF")

            await asyncio.sleep(2)

        print("\nStopping LED toggling...")
        print("Disconnecting...")

# Start keyboard listener thread
keypress_thread = threading.Thread(target=wait_for_keypress, daemon=True)
keypress_thread.start()

# Run BLE main loop
asyncio.run(run())

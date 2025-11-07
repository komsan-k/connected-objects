# Python BLE Central: send incremental counter to ESP32 via Write characteristic.
# Requires: pip install bleak
# Works on Windows/macOS/Linux (Bluetooth adapter required).

import asyncio
import sys
import signal
from bleak import BleakClient, BleakScanner

DEVICE_NAME = "ESP32_BLE_Counter"
SERVICE_UUID = "e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1"
WRITE_CHAR_UUID = "e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1"

stop_flag = False

def ask_exit(signame):
    global stop_flag
    print(f"\nReceived signal {signame}: stopping...")
    stop_flag = True

async def find_device_by_name(name: str, timeout=10.0):
    print(f"Scanning for '{name}' (timeout {timeout}s)...")
    devices = await BleakScanner.discover(timeout=timeout)
    for d in devices:
        if d.name == name:
            print(f"Found device: {d.name} [{d.address}] RSSI={d.rssi}")
            return d
    print(f"Device '{name}' not found. Available devices:")
    for d in devices:
        print(f" - {d.name} [{d.address}] RSSI={d.rssi}")
    return None

async def run():
    dev = await find_device_by_name(DEVICE_NAME, timeout=8.0)
    if dev is None:
        print("Exiting (device not found).")
        return

    async with BleakClient(dev.address) as client:
        print("Connected:", await client.is_connected())

        # Optional: verify characteristic exists
        svcs = await client.get_services()
        target_char = None
        for s in svcs:
            if s.uuid.lower() == SERVICE_UUID.lower():
                for c in s.characteristics:
                    if c.uuid.lower() == WRITE_CHAR_UUID.lower():
                        target_char = c
                        break
        if target_char is None:
            print("Write characteristic not found—check UUIDs and ESP32 sketch.")
            return

        print("Sending incremental counter. Press Ctrl+C to stop.")
        counter = 0
        while not stop_flag:
            payload = str(counter).encode("ascii")
            try:
                # Write without response is usually faster; bleak picks suitable method per platform
                await client.write_gatt_char(WRITE_CHAR_UUID, payload, response=False)
                print(f"→ Wrote: {counter}")
            except Exception as e:
                print("Write error:", e)
                break
            counter += 1
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    for s in ("SIGINT", "SIGTERM"):
        try:
            loop.add_signal_handler(getattr(signal, s), lambda s=s: ask_exit(s))
        except (NotImplementedError, AttributeError):
            # Windows event loop prior to Python 3.8 may not support add_signal_handler
            pass
    try:
        loop.run_until_complete(run())
    finally:
        loop.close()

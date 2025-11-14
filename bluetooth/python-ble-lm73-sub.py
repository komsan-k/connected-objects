import asyncio
from bleak import BleakClient, BleakError

# 👉 Replace with your ESP32 BLE MAC
DEVICE_ADDRESS = "40:91:51:37:0A:0A"

SERVICE_UUID = "e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1"
CHARACTERISTIC_UUID = "e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1"


def notification_handler(sender: int, data: bytearray):
    """Called whenever ESP32 sends LM73 notification."""
    try:
        text = data.decode("utf-8").strip()
    except UnicodeDecodeError:
        text = repr(data)
    print(f"[LM73] {text}")


async def main():
    print(f"Connecting to ESP32 at {DEVICE_ADDRESS} ...")

    client = BleakClient(DEVICE_ADDRESS)

    try:
        await client.connect(timeout=10.0)
        print(f"Connected: {client.is_connected}")

        if not client.is_connected:
            print("❌ Failed to connect to ESP32")
            return

        # One-time read
        try:
            value = await client.read_gatt_char(CHARACTERISTIC_UUID)
            print("Initial value:", value.decode("utf-8").strip())
        except Exception as e:
            print("Read error:", e)

        # Start notification subscription
        await client.start_notify(CHARACTERISTIC_UUID, notification_handler)
        print("📡 Listening for LM73 updates. Press Ctrl+C to disconnect.")

        # Main loop
        while True:
            if not client.is_connected:
                print("❌ Device disconnected unexpectedly!")
                break
            await asyncio.sleep(1)

    except BleakError as e:
        print("BLE Error:", e)

    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C pressed. Disconnecting...")

    finally:
        if client.is_connected:
            try:
                await client.stop_notify(CHARACTERISTIC_UUID)
            except Exception:
                pass
            await client.disconnect()
            print("🔌 Disconnected from ESP32.")

        print("✅ Program ended cleanly.")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
# BLE → MQTT Bridge (Bleak + Paho MQTT)
# - Subscribes to BLE notifications and publishes JSON frames to MQTT
# - Listens to MQTT commands (JSON) and writes them to a BLE write characteristic
#
# Usage:
#   python ble_mqtt_bridge.py --name ESP32_BLE_DASH \
#       --notify e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1 \
#       --write  e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1 \
#       --mqtt-host localhost --pub iot/ble/esp32/frame --sub iot/ble/esp32/cmd
#
# If --address is omitted, the bridge scans for a device whose name matches --name.

import asyncio
import argparse
import json
import logging
import signal
from typing import Optional

from bleak import BleakClient, BleakScanner
import paho.mqtt.client as mqtt

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
log = logging.getLogger("ble-mqtt")

def parse_args():
    ap = argparse.ArgumentParser(description="BLE → MQTT bridge (notifications + commands)")
    g_ble = ap.add_argument_group("BLE")
    g_ble.add_argument("--address", help="BLE MAC/UUID address (preferred on Linux/macOS)")
    g_ble.add_argument("--name", default="ESP32_BLE_DASH", help="BLE device name to search for if --address not given")
    g_ble.add_argument("--notify", required=True, help="Notify characteristic UUID")
    g_ble.add_argument("--write", required=True, help="Write characteristic UUID")
    g_ble.add_argument("--timeout", type=float, default=10.0, help="Scan/connect timeout (s)")

    g_mqtt = ap.add_argument_group("MQTT")
    g_mqtt.add_argument("--mqtt-host", default="localhost")
    g_mqtt.add_argument("--mqtt-port", type=int, default=1883)
    g_mqtt.add_argument("--mqtt-username")
    g_mqtt.add_argument("--mqtt-password")
    g_mqtt.add_argument("--pub", default="iot/ble/esp32/frame", help="Publish topic (BLE → MQTT)")
    g_mqtt.add_argument("--sub", default="iot/ble/esp32/cmd", help="Subscribe topic (MQTT → BLE)")
    g_mqtt.add_argument("--client-id", default="ble-mqtt-bridge")

    return ap.parse_args()

async def find_address_by_name(name: str, timeout: float) -> Optional[str]:
    log.info(f"Scanning for BLE device named '{name}'...")
    devices = await BleakScanner.discover(timeout=timeout)
    for d in devices:
        if (d.name or "").strip() == name:
            log.info(f"Found {name} at address {d.address}")
            return d.address
    log.error(f"Device named '{name}' not found.")
    return None

class Bridge:
    def __init__(self, address, notify_uuid, write_uuid, mqtt_client, pub_topic, sub_topic):
        self.address = address
        self.notify_uuid = notify_uuid
        self.write_uuid = write_uuid
        self.mqtt = mqtt_client
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.client: Optional[BleakClient] = None
        self._stop = asyncio.Event()

    async def start(self):
        self.client = BleakClient(self.address)
        log.info(f"Connecting to BLE device {self.address} ...")
        await self.client.connect()
        log.info(f"BLE connected: {self.client.is_connected}")

        await self.client.start_notify(self.notify_uuid, self._on_notify)
        log.info(f"Started notifications on {self.notify_uuid}")

        # MQTT subscription for downlink
        self.mqtt.message_callback_add(self.sub_topic, self._on_mqtt_cmd)
        self.mqtt.subscribe(self.sub_topic)

        # Wait until stop requested
        await self._stop.wait()

    async def stop(self):
        self._stop.set()
        try:
            if self.client and self.client.is_connected:
                await self.client.stop_notify(self.notify_uuid)
                await self.client.disconnect()
                log.info("BLE disconnected")
        except Exception as e:
            log.warning(f"Error during BLE cleanup: {e}")

    def _on_notify(self, sender: int, data: bytearray):
        # Expect JSON UTF-8; publish as-is
        try:
            text = data.decode("utf-8")
        except Exception:
            text = data.hex()
        self.mqtt.publish(self.pub_topic, text)
        log.debug(f"Notify -> MQTT: {text}")

    def _on_mqtt_cmd(self, client, userdata, msg):
        payload = msg.payload
        # Forward bytes to BLE write characteristic
        asyncio.run_coroutine_threadsafe(self._write_ble(payload), asyncio.get_event_loop())

    async def _write_ble(self, data: bytes):
        if not self.client or not self.client.is_connected:
            log.warning("MQTT cmd received but BLE not connected")
            return
        try:
            await self.client.write_gatt_char(self.write_uuid, data, response=True)
            log.info(f"MQTT cmd -> BLE write {len(data)} bytes")
        except Exception as e:
            log.error(f"BLE write failed: {e}")

def main():
    args = parse_args()

    loop = asyncio.get_event_loop()

    # Resolve address if not provided
    async def resolve():
        if args.address:
            return args.address
        addr = await find_address_by_name(args.name, args.timeout)
        if not addr:
            raise SystemExit(2)
        return addr

    address = loop.run_until_complete(resolve())

    # MQTT setup
    mqtt_client = mqtt.Client(client_id=args.client_id, clean_session=True)
    if args.mqtt_username:
        mqtt_client.username_pw_set(args.mqtt_username, args.mqtt_password)
    mqtt_client.connect(args.mqtt_host, args.mqtt_port, keepalive=60)
    mqtt_client.loop_start()

    bridge = Bridge(address, args.notify, args.write, mqtt_client, args.pub, args.sub)

    # Graceful shutdown
    def handle_sig(*_):
        log.info("Shutting down...")
        loop.create_task(bridge.stop())

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, handle_sig)
        except NotImplementedError:
            # Windows may not support add_signal_handler for SIGTERM
            pass

    try:
        loop.run_until_complete(bridge.start())
    finally:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    main()

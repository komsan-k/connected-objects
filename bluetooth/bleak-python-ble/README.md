# 🧠 Bluetooth Low Energy Integration Using Python Bleak and Node-RED

## 1. Introduction
Bluetooth Low Energy (BLE) is one of the most widely adopted short-range wireless technologies for the Internet of Things (IoT). It enables low-power, low-cost, and low-latency communication between embedded devices and gateways. In modern IoT systems, BLE is often used to transmit sensor data from microcontrollers—such as the ESP32—to edge gateways that relay data to cloud services or visualization dashboards.

The **Bleak** Python library provides a unified, cross-platform Application Programming Interface (API) to communicate with BLE devices. It bridges the gap between IoT devices and higher-level software environments, allowing BLE data to be easily integrated into systems such as **Node-RED**, **MQTT brokers**, or **cloud databases**.

This chapter introduces the concepts, workflows, and practical implementations of BLE communication using the Bleak library. It concludes with a complete end-to-end example of integrating ESP32 BLE sensors with a Node-RED dashboard through a Python BLE–MQTT bridge.

---

## 2. Fundamentals of Bluetooth Low Energy

BLE is designed for applications requiring low energy consumption and short data transmissions. It operates in the 2.4 GHz ISM band and follows a **client-server model**:

- **Peripheral (Server):** Typically a sensor or embedded device (e.g., ESP32) that advertises its availability and provides services.
- **Central (Client):** A controller device (e.g., laptop, smartphone, or Raspberry Pi) that connects to the peripheral to read or write data.

### 2.1 BLE Characteristics and UUIDs

| Type | Description | Example UUID |
|-------|--------------|--------------|
| **Service UUID** | Groups related characteristics | `e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1` |
| **Notify Characteristic** | Sends updates to the client | `e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1` |
| **Write Characteristic** | Accepts control commands | `e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1` |

---

## 3. The Bleak Library

### 3.1 Overview
**Bleak** is a Python library for cross-platform Bluetooth Low Energy communication. It supports scanning, connecting, reading, writing, and subscribing to BLE notifications.

### 3.2 Installation
```bash
pip install bleak
pip install paho-mqtt
```

### 3.3 Platform Compatibility
| OS | Backend | Notes |
|----|----------|-------|
| Windows | Microsoft API | Works with device name or MAC |
| macOS | CoreBluetooth | May randomize device address |
| Linux / RPi | BlueZ | Requires Bluetooth permissions |

---

## 4. Basic BLE Operations Using Bleak

### 4.1 Scanning for Devices
```python
from bleak import BleakScanner
import asyncio

async def scan():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

asyncio.run(scan())
```

**Output:**
```
Device(name='ESP32_BLE_DASH', address='24:6F:28:AA:BB:CC', rssi=-58)
```

### 4.2 Connecting and Writing
```python
from bleak import BleakClient
import asyncio

ADDRESS = "24:6F:28:AA:BB:CC"
CHAR_UUID = "e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1"

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Connected:", client.is_connected)
        await client.write_gatt_char(CHAR_UUID, b'{"led":1}')
        await asyncio.sleep(2)
        await client.write_gatt_char(CHAR_UUID, b'{"led":0}')

asyncio.run(main())
```

### 4.3 Receiving Notifications
```python
def callback(sender, data):
    print("Received:", data.decode())

async def notify():
    async with BleakClient(ADDRESS) as client:
        await client.start_notify("e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1", callback)
        await asyncio.sleep(10)
        await client.stop_notify("e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1")

asyncio.run(notify())
```

---

## 5. BLE Integration with MQTT

To bridge BLE with MQTT:
1. **Bleak** handles the BLE connection.
2. **Paho MQTT** publishes the data.
3. **Node-RED** subscribes to the topic for visualization.

---

## 6. Building the BLE–MQTT Bridge

### 6.1 Architecture
```
ESP32 (BLE Peripheral)
  ↕ Notify / Write
Python (Bleak + MQTT)
  ↕ MQTT
Node-RED Dashboard
```

### 6.2 Running the Bridge
```bash
python ble_mqtt_bridge.py   --name ESP32_BLE_DASH   --notify e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1   --write  e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1   --mqtt-host localhost
```

**Example Output:**
```
INFO: Found ESP32_BLE_DASH
INFO: Started notifications on e1f4046f...
INFO: MQTT cmd -> BLE write 12 bytes
```

---

## 7. Visualization in Node-RED

### 7.1 Import Flow
Install Node-RED Dashboard:
```bash
npm install node-red-dashboard
```
Then import `node_red_ble_mqtt_dashboard.json`.

### 7.2 Dashboard Widgets
| Widget | Function |
|---------|-----------|
| Gauge | Displays temperature |
| Chart | Plots temperature trend |
| Text | Shows latest JSON |
| Switch | Controls LED |
| Slider | Adjusts sampling rate |

---

## 8. ESP32 BLE Firmware Example

ESP32 sends JSON sensor data via notify and accepts commands via write:
```json
{"led":1}
{"period_ms":1500}
```

---

## 9. System Integration Diagram
```
ESP32 BLE Sensor → Python BLE–MQTT Bridge → Node-RED Dashboard
```

---

## 10. Troubleshooting

| Problem | Cause | Fix |
|----------|--------|----|
| No BLE devices | Adapter blocked | Enable Bluetooth |
| Notify fails | Missing CCCD | Add BLE2902 descriptor |
| Dashboard empty | Wrong topic | Verify MQTT topics |

---

## 11. Advanced Extensions

- Forward data to InfluxDB or Firebase
- Handle multiple BLE devices
- Cloud integration via HiveMQ or AWS IoT
- Add local anomaly detection using TinyML
- Run as background `systemd` service

---

## 12. Summary

This chapter demonstrated how to connect ESP32 BLE devices to a Node-RED dashboard using Python **Bleak** and **MQTT**, forming an efficient, scalable IoT communication stack.

---

### References
1. Bluetooth SIG. *Bluetooth Core Specification v5.4.*  
2. Bleak Documentation: https://bleak.readthedocs.io  
3. Paho MQTT: https://pypi.org/project/paho-mqtt/  
4. Espressif Systems. *ESP32 BLE Examples – Arduino Framework.*  
5. IBM Developer. *Node-RED: Low-Code Programming for IoT.*

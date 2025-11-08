# 🔬 Lab: Bluetooth Low Energy Communication Using Python Bleak

## 🧩 1. Objective
This laboratory exercise introduces the use of the **Bleak** Python library for **Bluetooth Low Energy (BLE)** communication.  
Students will:
- Scan and discover BLE devices.
- Read and write BLE characteristics.
- Subscribe to notifications.
- Indicate connection status via LED/console.
- Integrate BLE data with **Node-RED** via MQTT.

---

## ⚙️ 2. Equipment and Tools

| Item | Description |
|------|--------------|
| **ESP32 board** | Acts as a BLE peripheral (server) |
| **Laptop or Raspberry Pi** | Acts as BLE central (client) |
| **Python 3.10+** | For running Bleak scripts |
| **Node-RED + Mosquitto MQTT** | For data visualization |
| **BLE Scanner App (optional)** | For testing BLE advertisement |
| **Libraries** | `bleak`, `paho-mqtt`, `asyncio` |

Install dependencies:
```bash
pip install bleak paho-mqtt
```

---

## 🧠 3. Background Theory

**Bluetooth Low Energy (BLE)** operates on a client-server model:
- **Peripheral (ESP32)** advertises and provides services.
- **Central (Laptop)** connects and exchanges data.

BLE communication occurs via **GATT** (Generic Attribute Profile) which contains:
- **Services** → Groups of characteristics (e.g., Environmental Sensing)
- **Characteristics** → Individual data points (temperature, LED control)
- Each identified by a **UUID** (Universal Unique Identifier)

Example UUIDs used:
| Type | UUID | Description |
|-------|------|-------------|
| Service | `e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1` | BLE Service |
| Notify Characteristic | `e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1` | Sends sensor updates |
| Write Characteristic | `e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1` | Receives commands |

---

## 🧩 4. Lab Setup Diagram
```
+--------------------+          +----------------------+          +--------------------+
| ESP32 (Peripheral) |   BLE    |  Laptop / RPi (Bleak) |   MQTT   |  Node-RED Dashboard |
| • Advertise name   | <------> |  • Connects + Reads   | <------> |  • Gauges & Charts |
| • Temp + LED ctrl  |          |  • Publishes via MQTT |          |  • LED Switch UI  |
+--------------------+          +----------------------+          +--------------------+
```

---

## 🧮 5. Procedures

### **Task 1: Scan for BLE Devices**
```python
from bleak import BleakScanner
import asyncio

async def main():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

asyncio.run(main())
```
✅ **Observation:** Identify your ESP32 device name (e.g., `ESP32_BLE_DASH`) and note its MAC address.

---

### **Task 2: Connect and Discover Services**
```python
from bleak import BleakClient
import asyncio

ADDRESS = "24:6F:28:AA:BB:CC"

async def main():
    async with BleakClient(ADDRESS) as client:
        print("Connected:", client.is_connected)
        for service in client.services:
            print("[Service]", service.uuid)
            for char in service.characteristics:
                print("  [Characteristic]", char.uuid, char.properties)

asyncio.run(main())
```
✅ **Observation:** Record service and characteristic UUIDs.

---

### **Task 3: Read from a BLE Characteristic**
```python
CHAR_UUID = "e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1"

async def read_data():
    async with BleakClient(ADDRESS) as client:
        data = await client.read_gatt_char(CHAR_UUID)
        print("Data:", data.decode())

asyncio.run(read_data())
```
✅ **Observation:** Observe JSON-formatted output (e.g., `{"temp":26.3,"hum":58}`).

---

### **Task 4: Write to a BLE Characteristic**
```python
CHAR_UUID = "e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1"

async def write_led():
    async with BleakClient(ADDRESS) as client:
        await client.write_gatt_char(CHAR_UUID, b'{"led":1}')
        print("LED ON")
        await asyncio.sleep(2)
        await client.write_gatt_char(CHAR_UUID, b'{"led":0}')
        print("LED OFF")

asyncio.run(write_led())
```
✅ **Observation:** Confirm LED toggle on ESP32.

---

### **Task 5: Subscribe to Notifications**
```python
CHAR_UUID = "e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1"

def callback(sender, data):
    print(f"Notify from {sender}: {data.decode()}")

async def notify():
    async with BleakClient(ADDRESS) as client:
        await client.start_notify(CHAR_UUID, callback)
        await asyncio.sleep(10)
        await client.stop_notify(CHAR_UUID)

asyncio.run(notify())
```
✅ **Observation:** Verify live streaming data in console.

---

### **Task 6: Indicator for Connection State**
```python
async with BleakClient(ADDRESS) as client:
    if client.is_connected:
        print("✅ Connected to ESP32")
    else:
        print("❌ Connection failed")
```

---

## 🌐 6. Integration with Node-RED via MQTT

### **6.1 Install Broker and Dashboard**
```bash
sudo apt install mosquitto mosquitto-clients
npm install -g node-red
npm install node-red-dashboard
```

### **6.2 Bridge Python → MQTT → Node-RED**
```python
import paho.mqtt.client as mqtt

broker = "localhost"
topic = "iot/ble/esp32/frame"
client = mqtt.Client()
client.connect(broker, 1883, 60)

def callback(sender, data):
    message = data.decode()
    client.publish(topic, message)
    print("Published:", message)
```

Node-RED subscribes to `iot/ble/esp32/frame` and visualizes:
- Temperature and humidity on gauges.
- LED control via switch publishing to `iot/ble/esp32/cmd`.

---

## 🧪 7. Observations

| Task | Observation |
|------|--------------|
| Scan | Device name and MAC address |
| Discover | Services and characteristics |
| Read | Static data values |
| Write | LED toggling confirmed |
| Notify | Streaming JSON updates |
| Integration | Real-time dashboard visualization |

---

## 🧭 8. Post-Lab Questions
1. What is the difference between read, write, and notify in BLE GATT?  
2. How does Bleak simplify cross-platform BLE development?  
3. Why is MQTT an ideal protocol for IoT integration?  
4. What are the advantages of using Node-RED in this architecture?  
5. How can you extend this lab to include multiple BLE sensors?

---

## 📘 9. Conclusion
This lab demonstrates how Python’s **Bleak** library enables complete BLE communication:
- Discovery, reading, writing, and notifications from BLE devices.
- Integration with MQTT for message exchange.
- Visualization through Node-RED dashboards.

The result is a scalable, low-power IoT architecture combining BLE sensing, edge computing, and cloud visualization.

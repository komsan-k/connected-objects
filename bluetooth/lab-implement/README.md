# 🧪 LAB: Implementation of Bluetooth Low Energy (BLE) on ESP32

---

## 📘 Abstract

Bluetooth Low Energy (BLE) is a **low-power wireless communication protocol** ideal for IoT applications.  
This lab explores the **implementation of BLE on the ESP32 microcontroller**, demonstrating both **server (peripheral)** and **client (central)** roles. Students will learn how BLE can be used to control hardware (e.g., LED) and exchange data efficiently for embedded IoT projects.

---

## 🔑 Keywords
Bluetooth Low Energy, BLE, ESP32, IoT, Peripheral, Central, GATT, Advertising, Security

---

## 🧠 1. Introduction

BLE, introduced in **Bluetooth 4.0**, is optimized for **low-power data transmission** in IoT devices.  
The **ESP32**, developed by **Espressif Systems**, includes integrated Wi-Fi and BLE, making it an ideal platform for **IoT connectivity**.  
This lab demonstrates how to configure the ESP32 as both a **BLE Server (Peripheral)** and a **BLE Client (Central)** to enable wireless device control.

---

## 📚 2. Background

### 2.1 Bluetooth Low Energy (BLE)
- BLE is based on a **client-server (GATT)** model.  
- Data is organized into **services** and **characteristics**.  
- Operates in the **2.4 GHz** ISM band using **frequency hopping** for stability.

### 2.2 ESP32 Microcontroller
- Dual-mode **Bluetooth (Classic + BLE)** and **Wi-Fi** support.  
- Includes GPIO, PWM, I²C, and ADC for IoT integration.  
- BLE management via **ESP32 BLE Arduino library** or **ESP-IDF**.

---

## ⚙️ 3. Materials and Methods

### 3.1 Hardware
- **ESP32 Development Board**
- **LED** (optional for control demo)
- **USB Power Source**

### 3.2 Software
- **Arduino IDE**
- **ESP32 Board Support** (`https://dl.espressif.com/dl/package_esp32_index.json`)
- **ESP32 BLE Arduino Library**
- **BLE Client App** (e.g., nRF Connect, LightBlue)

### 3.3 Setup

#### Step 1: Install ESP32 Board Support
`File → Preferences → Additional Boards Manager URLs` → Add:  
```
https://dl.espressif.com/dl/package_esp32_index.json
```
Then install **ESP32 by Espressif Systems** under *Boards Manager*.

#### Step 2: Install BLE Library
`Sketch → Include Library → Manage Libraries` → Search **ESP32 BLE Arduino** → Install.

#### Step 3: Hardware Connection
- Connect **LED** to **GPIO 2** via a 220Ω resistor.

---

## 💻 4. Implementation

### 4.1 BLE Peripheral (Server) on ESP32

**Purpose:** Advertise a characteristic that can be written to for controlling an LED.

```cpp
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define LED_PIN 2
#define SERVICE_UUID "12345678-1234-5678-1234-56789abcdef0"
#define CHARACTERISTIC_UUID "12345678-1234-5678-1234-56789abcdef1"

bool ledState = false;

class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
        std::string value = pCharacteristic->getValue();
        if (value == "1") {
            ledState = true;
            digitalWrite(LED_PIN, HIGH);
        } else if (value == "0") {
            ledState = false;
            digitalWrite(LED_PIN, LOW);
        }
    }
};

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    BLEDevice::init("ESP32_LED_Controller");
    BLEServer *pServer = BLEDevice::createServer();
    BLEService *pService = pServer->createService(SERVICE_UUID);
    BLECharacteristic *pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID, BLECharacteristic::PROPERTY_WRITE);
    pCharacteristic->setCallbacks(new MyCallbacks());
    pService->start();
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    BLEDevice::startAdvertising();
    Serial.println("Waiting for BLE client connection...");
}

void loop() {}
```

💡 **Operation:**
- The ESP32 acts as a BLE server.  
- The LED toggles ON/OFF based on client writes (`"1"` or `"0"`).

---

### 4.2 BLE Client (Optional)

The ESP32 can also operate as a **BLE Client**, reading or writing characteristics from another server.  
In this lab, the focus remains on the **BLE Server (Peripheral)** configuration.

---

## 🧪 5. Testing and Validation

### Steps:
1. **Open** nRF Connect (or similar BLE client app).  
2. **Scan** for `ESP32_LED_Controller`.  
3. **Connect** and locate the writable characteristic UUID.  
4. **Write “1”** → LED ON.  
   **Write “0”** → LED OFF.

### Observation:
- LED responds immediately to BLE commands.  
- BLE connection and data transfer are stable.

---

## 💬 6. Discussion

- ESP32 successfully performs as a **BLE peripheral**, using the GATT server model.  
- Ideal for short-range IoT control (e.g., wearables, environmental nodes).  
- BLE offers lower power consumption and structured data exchange.  

### 6.1 Security Considerations
- BLE provides **pairing**, **bonding**, and **AES-CCM encryption**.  
- In this lab, connections are unencrypted for simplicity.  
- In production, enable **authenticated pairing** to secure control commands.

### 6.2 Limitations and Future Work
- BLE is optimized for intermittent, low-bandwidth data (not streaming).  
- Future work: add **notifications** and **BLE-to-Wi-Fi bridging** for cloud integration.

---

## 🧭 7. Assignments

### Task 1: Add Notifications
- Modify characteristic with `PROPERTY_NOTIFY`.  
- Use `pCharacteristic->notify();` to broadcast LED state changes.

### Task 2: Implement a BLE Client on ESP32
- Create a BLE client to read server data.  
- Display LED state in Serial Monitor.

---

## 🧩 8. Python BLE Client Example

Using **bleak** (cross-platform BLE library) to control ESP32 via Python.

```python
import asyncio
from bleak import BleakClient

SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
CHARACTERISTIC_UUID = "12345678-1234-5678-1234-56789abcdef1"
DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"  # Replace with ESP32 MAC

async def run():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print(f"Connected: {client.is_connected}")
        await client.write_gatt_char(CHARACTERISTIC_UUID, b"1")
        print("LED ON")
        await asyncio.sleep(2)
        await client.write_gatt_char(CHARACTERISTIC_UUID, b"0")
        print("LED OFF")

asyncio.run(run())
```

✅ **Output:** LED turns ON for 2 seconds and then OFF.

---

## 🧠 9. Conclusion

The ESP32 can operate as a robust **BLE server** for IoT control applications.  
This lab demonstrated wireless LED control using BLE Write operations.  
Future expansions can integrate BLE Notify for data transmission or combine BLE with Wi-Fi for hybrid IoT architectures.

---

## 📚 References

1. Espressif Systems – *ESP32 Series Datasheet*  
2. Bluetooth SIG – *Bluetooth Low Energy Overview*  
3. Espressif Systems – *ESP32 BLE Arduino Library Documentation*  
4. nRF Connect and LightBlue Explorer – *BLE Testing Tools*

---

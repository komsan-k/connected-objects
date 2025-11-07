# 🔬 Lab: Bluetooth Communication with ESP32 (with LM73 Sensor)

## 🧩 1. Objective
This lab demonstrates **Bluetooth-based communication** using an ESP32 microcontroller, covering both:
- **Bluetooth Classic (SPP)** for serial data exchange between ESP32 and a smartphone/computer.
- **Bluetooth Low Energy (BLE)** for real-time sensor data transmission using an **LM73 temperature sensor** (I²C).
- Comparison of **power, latency, and protocol behavior** between the two Bluetooth modes.

---

## ⚙️ 2. Equipment and Tools
| Item | Description |
|------|--------------|
| **ESP32 Development Board** | (e.g., ESP32-DevKitC, NodeMCU-32S) |
| **LM73 Temperature Sensor Module** | I²C digital temperature sensor |
| **Arduino IDE** | with ESP32 board package installed |
| **Smartphone** | with Bluetooth Terminal app (Classic) or BLE Scanner |
| **USB Cable** | for programming and serial monitoring |

---

## 🧠 3. Background

### 3.1 Bluetooth Classic (SPP)
ESP32 can emulate a **Bluetooth Serial Port**, acting as a **wireless UART**.  
Data is transmitted bi-directionally between ESP32 and a mobile terminal app — ideal for **legacy devices or continuous text streaming**.

### 3.2 Bluetooth Low Energy (BLE)
In BLE mode, ESP32 acts as a **GATT server**.  
Sensor data (from LM73) is updated periodically via **notify characteristics** — ideal for **IoT and low-power applications**.

---

## 🧩 4. Experiment 1 — Bluetooth Classic (Serial Communication)

### 🔹 Step 1: Arduino Code

```cpp
#include "BluetoothSerial.h"
BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT_Test"); // Bluetooth device name
  Serial.println("✅ Bluetooth Classic started. Pair with 'ESP32_BT_Test'");
}

void loop() {
  if (Serial.available()) {
    SerialBT.write(Serial.read());  // Send data from Serial Monitor to phone
  }
  if (SerialBT.available()) {
    char incoming = SerialBT.read();
    Serial.write(incoming);         // Echo data from phone to Serial Monitor
  }
}
```

### 🔹 Step 2: Connect and Test
1. Upload the code to ESP32.  
2. Pair the phone → **ESP32_BT_Test**.  
3. Open a **Bluetooth Terminal app** (e.g., *Serial Bluetooth Terminal*).  
4. Type messages between the phone and Serial Monitor.

💡 **Result:** You created a **wireless serial console** using Bluetooth Classic.

---

## 🧩 5. Experiment 2 — Bluetooth Low Energy (BLE) with LM73

### 🔹 Step 1: Wiring LM73 (I²C)
| LM73 Pin | ESP32 Pin |
|-----------|-----------|
| **VCC** | 3.3V |
| **GND** | GND |
| **SCL** | GPIO 22 |
| **SDA** | GPIO 21 |

> The LM73 communicates via I²C at address `0x48`.

---

### 🔹 Step 2: Arduino Code (BLE + LM73)

```cpp
#include <Wire.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define LM73_ADDR 0x48
#define SERVICE_UUID        "e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1"
#define CHARACTERISTIC_UUID "e1f4046f-2a5a-4a5b-8ee3-7c2f31d5b5a1"

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;

class MyServerCallbacks : public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) { deviceConnected = true; }
  void onDisconnect(BLEServer* pServer) { deviceConnected = false; }
};

float readLM73() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(0x00);
  Wire.endTransmission();
  Wire.requestFrom(LM73_ADDR, 2);
  if (Wire.available() == 2) {
    uint16_t raw = (Wire.read() << 8) | Wire.read();
    return (raw >> 7) * 0.25;  // Each count = 0.25°C
  }
  return -100.0; // error flag
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  BLEDevice::init("ESP32_BLE_LM73");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
                     CHARACTERISTIC_UUID,
                     BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY);
  pCharacteristic->setValue("LM73 Ready");
  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("✅ BLE started. Open BLE Scanner and connect.");
}

void loop() {
  if (deviceConnected) {
    float tempC = readLM73();
    char buffer[32];
    sprintf(buffer, "Temp: %.2f C", tempC);
    pCharacteristic->setValue(buffer);
    pCharacteristic->notify();
    Serial.println(buffer);
    delay(2000);
  }
}
```

### 🔹 Step 3: Connect and Test
1. Upload the code.  
2. Open a **BLE Scanner app** (e.g., *nRF Connect*).  
3. Scan for and connect to **ESP32_BLE_LM73**.  
4. Subscribe to the **Notify** characteristic.  
5. Observe temperature updates every 2 seconds.

💡 **Result:** The ESP32 broadcasts real **LM73 temperature readings** over BLE.

---

## 🧩 6. Experiment 3 — Power and Latency Comparison
| Aspect | Bluetooth Classic | BLE |
|--------|-------------------|-----|
| Connection | Requires pairing | Auto-connect via app |
| Data Rate | 1–3 Mbps | ~1 Mbps |
| Update Interval | Continuous stream | Periodic notify |
| Power Consumption | Higher | Much lower |
| Ideal Use | Audio, serial logs | IoT sensor data |

Use the Serial Monitor to observe timing and current draw (if a USB power meter is available).

---

## 📊 7. Observations
| Parameter | Classic (SPP) | BLE (with LM73) |
|------------|----------------|----------------|
| Connection Setup | Manual pairing | App-based scan/connect |
| Communication | Stream text | Notify packets |
| Power Profile | Constantly active | Sleeps between notifications |
| Complexity | Simple UART | GATT + UUID + services |
| Application | Console/chat | Sensor data (temperature) |

---

## 🧠 8. Real-World Applications
| Device Type | Bluetooth Type | Example Use |
|--------------|----------------|--------------|
| Wireless audio | Classic | Headsets, car audio |
| Smartwatch | BLE | Periodic health data |
| Smart bulb | BLE | Remote on/off control |
| IoT node (ESP32 + LM73) | BLE | Sensor network node |

---

## 💡 9. Optional Extension
Integrate BLE output into an **IoT Dashboard**:
- Use a BLE-to-WebSocket or BLE-to-MQTT gateway (e.g., Node-RED + Web Bluetooth).
- Forward LM73 temperature to a **cloud dashboard** (ThingSpeak, Firebase, etc.).
- Add a **BLE write characteristic** to control a fan or LED based on temperature threshold.

---

## 📘 10. Summary
| Mode | Purpose | Example |
|------|----------|----------|
| **Bluetooth Classic (SPP)** | Continuous data / serial chat | Console or debug |
| **Bluetooth Low Energy (BLE)** | Efficient sensor transmission | IoT temperature node with LM73 |

---

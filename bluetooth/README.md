# 📘Bluetooth and BLE Communication with ESP32 — Principles, Practical Works, and Projects

---

## 🎯 Learning Objectives

After completing this chapter, students will be able to:

1. Explain the principles of Bluetooth and Bluetooth Low Energy (BLE) technology.  
2. Configure and program ESP32 for Bluetooth Classic (SPP) and BLE applications.  
3. Interface BLE with digital sensors (e.g., LM73) for data acquisition.  
4. Analyze performance trade-offs between Bluetooth Classic and BLE.  
5. Develop BLE-based IoT dashboards using Node-RED and Web Bluetooth.  
6. Create complete Bluetooth-enabled projects integrating sensors and control mechanisms.

---

## 🧠 8.1 Introduction to Bluetooth Technology

**Bluetooth** is a short-range wireless communication protocol operating in the **2.4 GHz ISM band**.  
It enables **low-power, low-cost** data transfer between devices within 10–100 meters.

### 8.1.1 Bluetooth Architecture
Bluetooth uses a **master-slave (Classic)** or **client-server (BLE)** model for communication.

| Component | Function |
|------------|-----------|
| **Master / Central** | Initiates and controls communication (e.g., smartphone). |
| **Slave / Peripheral** | Responds to master requests (e.g., ESP32). |
| **Profile** | Defines standard behaviors (SPP, A2DP, GATT). |
| **Service** | Logical grouping of characteristics (in BLE). |
| **Characteristic** | Holds actual data (e.g., temperature reading). |

---

### 8.1.2 Bluetooth vs. BLE

| Feature | Bluetooth Classic | BLE |
|----------|-------------------|-----|
| Data Rate | 1–3 Mbps | 1 Mbps |
| Power Consumption | High | Very low |
| Range | ~10 m | Up to 100 m |
| Connection Type | Continuous | Event-driven |
| Use Case | Audio, streaming | Sensors, IoT |
| Example | Headset, keyboard | Fitness tracker, sensor node |

---

### 8.1.3 ESP32 Bluetooth Capabilities

The ESP32 integrates a **dual-mode Bluetooth transceiver**, supporting:
- **Bluetooth Classic (BR/EDR)**: Serial Port Profile (SPP)
- **Bluetooth Low Energy (BLE)**: Generic Attribute Profile (GATT)
- **Simultaneous dual-mode operation**

---

## ⚙️ 8.2 Bluetooth Classic Communication with ESP32

### 8.2.1 Serial Port Profile (SPP)
SPP emulates a **serial UART over wireless**, useful for sending text or debug data.

---

### 🧩 Practical 1 — Wireless Serial Chat

#### Equipment
- ESP32 board  
- Smartphone with *Serial Bluetooth Terminal*  
- Arduino IDE  

#### Wiring
No external sensor required.

#### Code Example

```cpp
#include "BluetoothSerial.h"
BluetoothSerial SerialBT;

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_BT_Chat");
  Serial.println("✅ Pair with 'ESP32_BT_Chat'");
}

void loop() {
  if (Serial.available())
    SerialBT.write(Serial.read());
  if (SerialBT.available())
    Serial.write(SerialBT.read());
}
```

#### Procedure
1. Upload code and open Serial Monitor.  
2. Pair smartphone → `ESP32_BT_Chat`.  
3. Open the *Serial Bluetooth Terminal* app.  
4. Send messages between the Serial Monitor and phone.

💡 **Result:** You created a **wireless serial console** using Bluetooth Classic.

---

## ⚙️ 8.3 Bluetooth Low Energy (BLE) Fundamentals

BLE is optimized for **low-energy data exchange**, where a central device reads or subscribes to updates from peripherals.

### 8.3.1 GATT Structure

```
Service (Temperature Service)
 ├── Characteristic (Temperature Value)
 └── Characteristic (Units)
```

A **GATT Server** (ESP32) hosts services; a **GATT Client** (e.g., phone app) reads or subscribes to them.

---

### 8.3.2 BLE Operation Flow

1. ESP32 starts **advertising**.  
2. Smartphone **scans and connects**.  
3. ESP32 sends **notifications** with new sensor data.  
4. Smartphone **displays or stores** readings.

---

## 🧩 Practical 2 — BLE Temperature Sensor Using LM73

### 8.3.3 Objective
Build a BLE-enabled temperature node using the **LM73 I²C sensor** and visualize real readings on a smartphone app.

### Equipment and Wiring

| LM73 Pin | ESP32 Pin |
|-----------|-----------|
| **VCC** | 3.3V |
| **GND** | GND |
| **SCL** | GPIO 22 |
| **SDA** | GPIO 21 |

> The LM73 communicates via I²C at address `0x48`.

---

### Arduino Code

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
    return (raw >> 7) * 0.25;
  }
  return -100.0;
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
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );

  pCharacteristic->setValue("LM73 Ready");
  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("✅ BLE advertising: ESP32_BLE_LM73");
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

### Procedure

1. Upload the code.  
2. Open a **BLE Scanner** app (nRF Connect, BLE Scanner 2).  
3. Connect to *ESP32_BLE_LM73*.  
4. Subscribe to the Notify characteristic.  
5. Observe live temperature readings.

💡 **Result:** BLE notifications deliver real sensor data in near real-time, using minimal energy.

---

## 🧩 Practical 3 — BLE to IoT Dashboard (Advanced Integration)

**Objective:** Forward BLE sensor data to a **Node-RED Dashboard** via a Web Bluetooth gateway.

**Flow:**
```
ESP32 (BLE) → Browser (Web Bluetooth) → Node-RED WebSocket → Dashboard + MQTT
```

Students reuse previous BLE code and import a Node-RED flow with gauges and charts.

---

## 💡 8.4 Mini Projects

| Project | Description | Key Learning |
|----------|--------------|---------------|
| **1. BLE Weather Station** | ESP32 + LM73 + DHT11 → send temperature & humidity to BLE scanner app. | Multi-sensor BLE data frame |
| **2. BLE Smart Thermostat** | BLE app adjusts fan speed via Write characteristic. | Two-way BLE communication |
| **3. Bluetooth File Chat** | ESP32 Classic SPP to exchange text with PC terminal. | Serial communication & parsing |
| **4. BLE + MQTT Bridge** | Web BLE gateway forwards LM73 readings to MQTT broker. | Cloud dashboard integration |

---

## 📊 8.5 Comparison Summary

| Feature | Bluetooth Classic | BLE |
|----------|-------------------|-----|
| Speed | 3 Mbps | 1 Mbps |
| Energy | Higher | Very low |
| Topology | Piconet | Star / Mesh |
| Suitable For | Audio, legacy devices | IoT sensors, wearables |
| Example Project | Chat terminal | BLE temperature node |

---

## 📗 8.6 Assessment Questions

### Short Answer
1. Explain the difference between Bluetooth Classic and BLE.  
2. What is a GATT characteristic?  
3. Why is BLE preferred for IoT sensors?  
4. How does ESP32 manage BLE advertising?  

### Programming Tasks
5. Modify the BLE code to include both LM73 temperature and an onboard LED toggle via BLE Write.  
6. Create a BLE dashboard using Node-RED to display temperature and humidity readings.  

### Discussion
7. Compare BLE and Wi-Fi for continuous data logging applications.  
8. Discuss how BLE security pairing differs from Wi-Fi authentication.  

---

## 🔖 Summary
- ESP32 supports both **Classic Bluetooth (SPP)** and **BLE (GATT)**.  
- **SPP** provides a virtual UART channel for serial text transfer.  
- **BLE** enables structured data transfer via services and characteristics.  
- LM73 integration demonstrates real-world BLE sensor communication.  
- BLE can bridge local wireless networks to the cloud via Node-RED and MQTT.

---

## 🖼️ Suggested Diagram
```
[ESP32 + LM73 Sensor] 
     │
     │ BLE Advertising
     ▼
[Smartphone / Web Bluetooth]
     │
     │ WebSocket / MQTT
     ▼
[Node-RED Dashboard → Cloud Storage]
```

---

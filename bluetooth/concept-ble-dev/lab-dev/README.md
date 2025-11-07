# 🔬 Lab: Developing a BLE Mobile App for ESP32 Temperature Node

---

## 🎯 1. Objective

This lab guides learners through the process of creating a **mobile BLE app** that communicates with an **ESP32 BLE peripheral**, reads temperature data from an **LM73 sensor**, and visualizes it on a mobile dashboard.

Students will learn to:

- Understand BLE GATT communication in real applications.  
- Develop a mobile app to **scan, connect, and read BLE characteristics**.  
- Implement **real-time data updates (Notify)** from ESP32.  
- Visualize sensor data in a user-friendly dashboard.

---

## ⚙️ 2. Equipment and Tools

| Item | Description |
|------|--------------|
| **ESP32 Board** | BLE Peripheral device |
| **LM73 Temperature Sensor** | I²C digital temperature sensor |
| **Smartphone** | Android or iOS with BLE support |
| **Arduino IDE** | For ESP32 firmware |
| **App Development Tool** | Android Studio / Flutter / MIT App Inventor |
| **Testing Apps** | nRF Connect, LightBlue, BLE Scanner 2 |

---

## 🧠 3. Background Theory

### 3.1 BLE Communication Model

BLE uses a **GATT-based client-server** model:

| Role | Description | Example |
|------|-------------|----------|
| **Peripheral** | Broadcasts and serves data | ESP32 Temperature Node |
| **Central** | Scans, connects, and reads data | Mobile App |

**Communication Steps:**  
`Scan → Connect → Discover Services → Read/Write/Notify`

---

### 3.2 System Overview

```
[LM73 Sensor] → [ESP32 BLE Peripheral] → (BLE Notify)
                                 ↓
                         [Mobile App Central]
                                 ↓
                      [Dashboard Display (°C)]
```

- ESP32 acts as a **BLE GATT Server**.  
- The mobile app functions as a **BLE Central** device.

---

## 🔌 4. Step 1 — ESP32 BLE Firmware

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
  BLEDevice::init("ESP32_BLE_TempNode");
  BLEServer *pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);

  pCharacteristic = pService->createCharacteristic(
    CHARACTERISTIC_UUID,
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );

  pCharacteristic->setValue("Ready");
  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("✅ BLE advertising started: ESP32_BLE_TempNode");
}

void loop() {
  if (deviceConnected) {
    float tempC = readLM73();
    char buffer[32];
    sprintf(buffer, "%.2f", tempC);
    pCharacteristic->setValue(buffer);
    pCharacteristic->notify();
    Serial.println(buffer);
    delay(2000);
  }
}
```

✅ Upload the code to ESP32. The board begins advertising `ESP32_BLE_TempNode` every 2 seconds.

---

## 📱 5. Step 2 — Mobile BLE App Development

You can use either **MIT App Inventor** (no-code) or **Flutter** (code-based).

---

### 🧩 5.1 MIT App Inventor (No-Code Approach)

1. Open [MIT App Inventor](https://appinventor.mit.edu).  
2. Create a new project: **BLE_Temp_ESP32**.  
3. Add components:  
   - **BluetoothLE1** (Connectivity → Bluetooth LE)  
   - **ListPicker1** (to list available devices)  
   - **LabelTemperature** (to display °C)  
   - **ButtonConnect**, **ButtonDisconnect**  

4. In the **Blocks Editor**:  
   - When `ButtonConnect.Click` → Connect to `ESP32_BLE_TempNode`.  
   - When `BluetoothLE1.DeviceConnected` → Start reading Notify characteristic.  
   - When `BluetoothLE1.BytesReceived` → Update `LabelTemperature.Text`.

💡 Result: The app displays live temperature data via BLE Notify.

---

### 💻 5.2 FlutterBlue (Code-Based Approach)

Add dependency in **pubspec.yaml**:
```yaml
dependencies:
  flutter_blue_plus: ^1.5.0
```

**main.dart**
```dart
import 'package:flutter/material.dart';
import 'package:flutter_blue_plus/flutter_blue_plus.dart';

void main() => runApp(BLEApp());

class BLEApp extends StatefulWidget {
  @override
  _BLEAppState createState() => _BLEAppState();
}

class _BLEAppState extends State<BLEApp> {
  final FlutterBluePlus flutterBlue = FlutterBluePlus.instance;
  BluetoothDevice? device;
  BluetoothCharacteristic? characteristic;
  String temperature = "--";

  void scanAndConnect() async {
    flutterBlue.startScan(timeout: Duration(seconds: 4));
    flutterBlue.scanResults.listen((results) async {
      for (ScanResult r in results) {
        if (r.device.name == "ESP32_BLE_TempNode") {
          await flutterBlue.stopScan();
          device = r.device;
          await device!.connect();
          var services = await device!.discoverServices();
          for (var s in services) {
            if (s.uuid.toString().contains("e1f4046e")) {
              for (var c in s.characteristics) {
                if (c.properties.notify) {
                  characteristic = c;
                  await c.setNotifyValue(true);
                  c.value.listen((v) {
                    setState(() => temperature = String.fromCharCodes(v));
                  });
                }
              }
            }
          }
        }
      }
    });
  }

  @override
  void initState() {
    super.initState();
    scanAndConnect();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("ESP32 BLE Temperature")),
        body: Center(
          child: Text("🌡️ $temperature °C",
              style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold)),
        ),
      ),
    );
  }
}
```

Run the Flutter app → it automatically scans and displays live temperature readings.

---

## 📊 6. Step 3 — Verification with BLE Tools

Use **nRF Connect** or **LightBlue Explorer**:

1. Open app → Scan for devices → Connect to `ESP32_BLE_TempNode`.  
2. Locate the service UUID and characteristic.  
3. Enable **Notifications**.  
4. Observe live temperature updates every 2 seconds.

---

## 🌐 7. Step 4 — IoT Dashboard Integration (Optional)

Use **Node-RED Web Bluetooth** or **WebSocket bridge**:

```
ESP32 (BLE) → Browser (Web Bluetooth) → Node-RED WebSocket → Cloud Dashboard
```

Forward BLE readings to **MQTT topic**: `iot/ble/temp` → visualize with gauges or charts.

---

## 🔍 8. Observations

| Aspect | Observation |
|---------|-------------|
| Connection Time | BLE connects quickly (~2–3 s) |
| Update Rate | 2 s interval using Notify |
| Power Use | Very low on ESP32 |
| UI Latency | Negligible (depends on phone BLE stack) |

---

## 🧩 9. Student Tasks

1. Add **humidity sensor data** in the same BLE service.  
2. Add a **Write characteristic** for LED ON/OFF control.  
3. Extend Flutter UI with a **chart widget** for temperature trends.  
4. Forward BLE data to **Firebase** or **ThingSpeak**.

---

## 🧠 10. Summary

- BLE provides efficient low-power sensor communication.  
- ESP32 acts as a BLE GATT Server sending temperature via Notify.  
- Mobile app acts as Central for reading and displaying sensor data.  
- Flutter and MIT App Inventor are both effective BLE app platforms.  
- BLE → MQTT → Cloud extends local communication to IoT dashboards.

---

## 📈 Suggested Workflow Diagram

```
   [ESP32 + LM73 Sensor]
           │
           │ BLE Notify (UUID, Temp)
           ▼
   [Mobile App (MIT/Flutter)]
           │
           │ Read & Display
           ▼
   [Dashboard Visualization → MQTT / Node-RED]
```

---

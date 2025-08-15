# LAB 9 — BLE Communication

## 1. Objective
The objectives of this lab are to:

1. Learn the fundamentals of Bluetooth Low Energy (BLE) communication using the ESP32 platform.
2. Implement BLE Peripheral (Server) mode to advertise sensor data from LDR and LM73 temperature sensor.
3. Implement BLE Central (Client) mode to connect and read data from the ESP32 BLE Peripheral.
4. Understand BLE services, characteristics, and the GATT profile.
5. Integrate sensor readings into BLE characteristics for real-time wireless transmission.

---

## 2. Background

Bluetooth Low Energy (BLE) is a power-efficient wireless communication protocol designed for low-data-rate, intermittent transmission. ESP32 supports both classic Bluetooth and BLE, making it suitable for IoT devices that require short-range, low-energy wireless communication.

**Key BLE Concepts:**
- **Peripheral (Server):** Device that advertises and exposes data through services and characteristics.
- **Central (Client):** Device that scans, connects, and reads data from the peripheral.
- **Service:** A logical grouping of characteristics, identified by a UUID.
- **Characteristic:** A data point inside a service that can be read, written, or notified.
- **GATT (Generic Attribute Profile):** Protocol defining how services and characteristics are structured.

---

## 3. Hardware and Software Requirements

**Hardware:**
- ESP32 development board
- LDR sensor + 10kΩ resistor
- LM73 temperature sensor module (I²C)
- USB cable

**Software:**
- Arduino IDE with ESP32 board package
- Libraries: `WiFi.h` (optional for debugging), `BLEDevice.h`, `Wire.h`
- BLE scanning app (e.g., nRF Connect for Android/iOS)
- Serial Monitor for debugging

---

## 4. Circuit Connections

| Component | ESP32 Pin |
|-----------|-----------|
| LDR + 10k resistor voltage divider | GPIO34 (ADC input) |
| LM73 SCL | GPIO22 |
| LM73 SDA | GPIO21 |
| LM73 VCC | 3.3V |
| LM73 GND | GND |

---

## 5. Code Implementation

### 5.1 BLE Peripheral (Server) with LDR & LM73
```cpp
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>
#include <Wire.h>

#define LDR_PIN 34
#define LM73_ADDR 0x48
const float LM73_LSB_C = 0.03125f;

BLEServer *pServer;
BLECharacteristic *ldrChar;
BLECharacteristic *tempChar;

void lm73Init() {
  Wire.begin(21, 22);
}

float lm73ReadC() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(0x00);
  Wire.endTransmission(false);
  Wire.requestFrom(LM73_ADDR, (uint8_t)2);
  if (Wire.available() < 2) return NAN;
  uint16_t raw = (Wire.read() << 8) | Wire.read();
  int16_t val = raw >> 5;
  return val * LM73_LSB_C;
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  pinMode(LDR_PIN, INPUT);

  BLEDevice::init("ESP32_BLE_Sensors");
  pServer = BLEDevice::createServer();

  BLEService *sensorService = pServer->createService(BLEUUID((uint16_t)0x180A));

  ldrChar = sensorService->createCharacteristic(
    BLEUUID((uint16_t)0x2A6E),
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );
  tempChar = sensorService->createCharacteristic(
    BLEUUID((uint16_t)0x2A6F),
    BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY
  );

  ldrChar->addDescriptor(new BLE2902());
  tempChar->addDescriptor(new BLE2902());

  sensorService->start();
  pServer->getAdvertising()->start();
  Serial.println("BLE Server started, advertising...");
}

void loop() {
  int ldrValue = analogRead(LDR_PIN);
  float tempC = lm73ReadC();

  ldrChar->setValue(ldrValue);
  tempChar->setValue(tempC);
  ldrChar->notify();
  tempChar->notify();

  Serial.printf("LDR: %d, Temp: %.2f C\n", ldrValue, tempC);
  delay(1000);
}
```

---

## 6. Testing Procedure

1. Upload the peripheral code to the ESP32.
2. Install **nRF Connect** or similar BLE scanner app on your phone.
3. Enable Bluetooth and scan for devices — look for `ESP32_BLE_Sensors`.
4. Connect to the device and discover services and characteristics.
5. Observe real-time updates of LDR and LM73 values.
6. Move your hand over the LDR and touch the LM73 to see readings change.

---

## 7. Exercises

1. Modify the BLE service to add **humidity** data from a DHT22 sensor.
2. Implement a BLE **write** characteristic to control an LED on the ESP32.
3. Create a BLE **Central** ESP32 that connects to the Peripheral and prints sensor values to Serial Monitor.
4. Reduce BLE advertising interval to optimize power consumption.

---

## 8. Conclusion

This lab demonstrated the setup of BLE communication between an ESP32 acting as a peripheral and a BLE client. Sensor readings from LDR and LM73 were sent through BLE characteristics, enabling real-time monitoring via a mobile app. BLE provides a power-efficient, short-range communication option for IoT devices that need local wireless data exchange without a network infrastructure.


# LAB 3 — Device Interfacing for LDR, LM73, and MPU6050

## 1. Objective
The main objectives of this lab are:
1. To interface and acquire data from multiple sensors:  
   - **LDR** (Light Dependent Resistor) for light intensity measurement  
   - **LM73** digital temperature sensor  
   - **MPU6050** accelerometer + gyroscope IMU
2. To implement I²C communication for digital sensors (LM73, MPU6050).
3. To process and display the acquired sensor data via the Serial Monitor.
4. To gain experience in handling mixed-signal sensor interfacing in an embedded system.

---

## 2. Background
Sensor interfacing is a fundamental skill in embedded programming, requiring knowledge of:
- **Analog Sensors**: e.g., LDRs provide a resistance that varies with light intensity. This is measured using an ADC (Analog-to-Digital Converter).
- **Digital Sensors (I²C)**:  
  - **LM73**: High-accuracy temperature sensor using I²C, with configurable resolution.  
  - **MPU6050**: Combines a 3-axis accelerometer and 3-axis gyroscope; communicates over I²C.

LDR Measurement Principle:  
\( V_{out} = V_{cc} \cdot \frac{R_{LDR}}{R_{fixed} + R_{LDR}} \)  
where \( R_{LDR} \) is the resistance of the LDR.



**I²C Communication Basics:**
- Master-slave protocol over SDA (data) and SCL (clock) lines.
- Each device has a unique 7-bit address.
- Supports multiple devices on the same bus.

---

## 3. Hardware Requirements
- **ESP32 Development Board**
- **LDR** + 10kΩ fixed resistor (voltage divider)
- **LM73** temperature sensor module
- **MPU6050** IMU sensor module
- Breadboard and jumper wires
- USB cable

---

## 4. Pin Connections

| Sensor      | Signal | ESP32 Pin | Notes                      |
|-------------|--------|-----------|----------------------------|
| **LDR**     | ADC    | GPIO 34   | Analog input only           |
| **LM73**    | SDA    | GPIO 21   | I²C data                    |
|             | SCL    | GPIO 22   | I²C clock                   |
| **MPU6050** | SDA    | GPIO 21   | Shared I²C data line        |
|             | SCL    | GPIO 22   | Shared I²C clock line       |
| GND         | GND    | GND       | Common ground               |
| VCC         | 3.3V   | 3.3V      | Power supply                |

---

## 5. Software Requirements
- Arduino IDE with ESP32 board support
- Libraries:
  - `Wire.h` (I²C)
  - `Adafruit_MPU6050` or direct register handling for MPU6050 (optional)
  - No extra library needed for LM73 basic read

---

## 6. Code Implementation

### 6.1 LDR Measurement
```cpp
const int LDR_PIN = 34;

void readLDR() {
  int adcValue = analogRead(LDR_PIN);
  float voltage = adcValue * (3.3 / 4095.0);
  Serial.printf("LDR ADC: %d, Voltage: %.2f V\n", adcValue, voltage);
}
```

### 6.2 LM73 I²C Read
```cpp
#include <Wire.h>
uint8_t LM73_ADDR = 0x48;
const float LM73_LSB_C = 0.03125f;

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
```

### 6.3 MPU6050 Read
```cpp
#define MPU6050_ADDR 0x68
int16_t ax, ay, az, gx, gy, gz;

void mpu6050Init() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission();
}

void mpu6050Read() {
  Wire.beginTransmission(MPU6050_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);
  Wire.requestFrom(MPU6050_ADDR, 14, true);
  ax = (Wire.read() << 8) | Wire.read();
  ay = (Wire.read() << 8) | Wire.read();
  az = (Wire.read() << 8) | Wire.read();
  gx = (Wire.read() << 8) | Wire.read();
  gy = (Wire.read() << 8) | Wire.read();
  gz = (Wire.read() << 8) | Wire.read();

  Serial.printf("Accel[g]: %.2f, %.2f, %.2f | Gyro[dps]: %.2f, %.2f, %.2f\n",
                ax / 16384.0, ay / 16384.0, az / 16384.0,
                gx / 131.0, gy / 131.0, gz / 131.0);
}
```

### 6.4 Main Program
```cpp
void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  mpu6050Init();
}

void loop() {
  readLDR();
  float temp = lm73ReadC();
  if (!isnan(temp)) Serial.printf("LM73 Temp: %.2f °C\n", temp);
  mpu6050Read();
  delay(1000);
}
```

---

## 7. Exercises
1. Calibrate the MPU6050 to remove offset errors.
2. Convert LDR voltage to lux using a calibration curve.
3. Implement an averaging filter for LM73 readings.
4. Display all sensor readings on an OLED display.
5. Send sensor data to a PC via MQTT.

---

## 8. Conclusion
This lab demonstrated how to interface analog and digital sensors with an ESP32, covering ADC readings for LDR, I²C communication for LM73 and MPU6050, and basic data acquisition loops. The knowledge from this lab is foundational for building multi-sensor IoT systems.


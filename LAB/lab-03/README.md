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
`Vout = Vcc × (R_LDR / (R_fixed + R_LDR))`  
where `R_LDR` is the resistance of the light-dependent resistor.



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
| **LM73**    | SDA    | GPIO 4   | I²C data                    |
|             | SCL    | GPIO 5   | I²C clock                   |
| **MPU6050** | SDA    | GPIO 4   | Shared I²C data line        |
|             | SCL    | GPIO 5   | Shared I²C clock line       |
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
const int LDR_PIN = 36;

void readLDR() {
  int adcValue = analogRead(LDR_PIN);
  float voltage = adcValue * (3.3 / 4095.0);
  Serial.printf("LDR ADC: %d, Voltage: %.2f V\n", adcValue, voltage);
}
```

### 6.2 LM73 I²C Read
```cpp
#include <Wire.h>
uint8_t LM73_ADDR = 0x4D;
const float LM73_LSB_C = 0.03125f;

float lm73ReadC() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(0x00);
  Wire.endTransmission(false);
  Wire.requestFrom(LM73_ADDR, (uint8_t)2);
  if (Wire.available() < 2) return NAN;
  uint16_t raw = (Wire.read() << 8) | Wire.read();
  int16_t val = raw >> 2;
  return val * LM73_LSB_C;
}
```

### 6.3 MPU6050 Read
```cpp
#include <Wire.h>
#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>

// Create an instance of the MPU6050 sensor
Adafruit_MPU6050 mpu;

// I2C pins for custom I2C setup
#define SDA1_PIN 4   // SDA1 connected to GPIO 4
#define SCL1_PIN 5   // SCL1 connected to GPIO 5

void setup() {
  Serial.begin(115200);

  // Start I2C on custom pins (SDA1 = GPIO 4, SCL1 = GPIO 5)
  Wire.begin(SDA1_PIN, SCL1_PIN);

  // Try to initialize the MPU6050 sensor
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip. Check wiring.");
    while (1);
  }

  // Configure sensor settings
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);  // Set accelerometer range to +/- 2g
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);       // Set gyroscope range to +/- 250 deg/s
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);    // Set filter bandwidth to 21 Hz

  Serial.println("MPU6050 Initialized.");
  delay(1000);
}

void loop() {
  sensors_event_t a, g, temp;
  mpu.getEvent(&a, &g, &temp); // Read accelerometer, gyroscope, and temperature data

  // Print accelerometer data
  Serial.print("Accel X: "); Serial.print(a.acceleration.x); Serial.print(" m/s^2, ");
  Serial.print("Accel Y: "); Serial.print(a.acceleration.y); Serial.print(" m/s^2, ");
  Serial.print("Accel Z: "); Serial.print(a.acceleration.z); Serial.println(" m/s^2");

  // Print gyroscope data
  Serial.print("Gyro X: "); Serial.print(g.gyro.x); Serial.print(" deg/s, ");
  Serial.print("Gyro Y: "); Serial.print(g.gyro.y); Serial.print(" deg/s, ");
  Serial.print("Gyro Z: "); Serial.print(g.gyro.z); Serial.println(" deg/s");

  // Print temperature data
  Serial.print("Temperature: "); Serial.print(temp.temperature); Serial.println(" °C");

  // Wait 500 ms before next reading
  delay(500);
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


# 🧪 Lab 4: Monitoring Temperature with LM73, ESP32, and Thunkable over Wi-Fi

## 1. Objective

The objective of this lab is to integrate the **LM73 digital temperature
sensor** with an **ESP32** and monitor temperature readings using a
**Thunkable mobile app**. Students will learn to:\
- Interface the LM73 via the I²C protocol.\
- Configure the ESP32 as a Wi-Fi server that provides temperature
readings in JSON format.\
- Build a Thunkable app that queries and displays the sensor data.\
- Apply this workflow for environmental IoT monitoring.

## 2. Background

The **LM73** is a high-precision, low-power digital temperature sensor
with:\
- Operating range: −40°C to +125°C.\
- I²C interface (address selectable, typically `0x48`).\
- 11-bit to 14-bit resolution (0.25°C steps at 11-bit).

The ESP32 reads LM73 values over I²C and exposes them through a REST
endpoint. Thunkable retrieves the values via **HTTP GET** and displays
them in real time.

## 3. Materials

-   ESP32 development board.\
-   LM73 temperature sensor module (I²C breakout).\
-   Breadboard + jumper wires.\
-   Arduino IDE with ESP32 support.\
-   Smartphone with Thunkable Live app.\
-   Shared Wi-Fi network.

## 4. Procedure

### Step 1: Circuit Setup

Wire LM73 to ESP32 via I²C:

    LM73      ESP32
    -----     -----
    VCC  →   3.3V
    GND  →   GND
    SDA  →   GPIO 21
    SCL  →   GPIO 22
    ADDR →   GND (I²C address = 0x48)

### Step 2: ESP32 Code

``` cpp
#include <Wire.h>
#include <WiFi.h>
#include <WebServer.h>

const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

#define LM73_ADDR 0x48
WebServer server(80);

float readTemperature() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(0x00); // Temperature register
  Wire.endTransmission();
  
  Wire.requestFrom(LM73_ADDR, 2);
  if (Wire.available() < 2) return NAN;

  uint8_t msb = Wire.read();
  uint8_t lsb = Wire.read();

  // Combine bytes → 16-bit value
  int16_t raw = (msb << 8) | lsb;
  raw >>= 5;  // LM73: 11-bit resolution
  
  // Convert to °C (0.125°C per LSB)
  return raw * 0.125;
}

void handleTemp() {
  float tempC = readTemperature();
  String json = "{\"tempC\":" + String(tempC, 2) + "}";
  Serial.println(json);
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", json);
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // SDA=21, SCL=22

  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(); Serial.print("IP: "); Serial.println(WiFi.localIP());

  server.on("/temperature", HTTP_GET, handleTemp);
  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();
}
```

### Step 3: Thunkable App Design

-   Add a **Button_Refresh** → text: *Read Temperature*.\
-   Add a **Label_Temp** → placeholder: *Waiting for data...*.\
-   Add a `WebAPI_ESP` component.

### Step 4: Thunkable Blocks

-   **When Screen Opens**
    -   Set `WebAPI_ESP.URL = "http://<ESP32_IP>/temperature"`.
-   **When Button_Refresh.Click**
    -   Call `WebAPI_ESP.Get`.
-   **When WebAPI_ESP.Get.Success**
    -   Extract `"tempC"` from response.\
    -   Set `Label_Temp.Text = "Temperature: " + tempC + " °C"`.
-   **When WebAPI_ESP.Get.Error**
    -   Set `Label_Temp.Text = "Error connecting to ESP32"`.

## 5. Diagrams

### Data Flow

    Thunkable App (Button Press)
           │
           ▼
     WebAPI_ESP GET /temperature
           │
           ▼
    ESP32 reads LM73 via I²C
           │
           ▼
    Responds with JSON {"tempC": value}
           │
           ▼
    App displays temperature in °C

## 6. Verification

-   Open Serial Monitor → confirm ESP32 prints temperature values.\
-   On the phone, tap **Read Temperature** → app shows °C.\
-   Warm the sensor with your hand or a lamp → readings increase.

## 7. Exercises

1.  Modify ESP32 code to also provide **Fahrenheit** values.\
2.  Add an **auto-refresh** (every 5 seconds) in Thunkable.\
3.  Plot temperature readings on a **chart component** in Thunkable.\
4.  Set thresholds (e.g., \>30°C → show "Hot", \<20°C → "Cool").\
5.  Extend to multiple sensors (e.g., LDR + LM73 monitoring).

## 8. Conclusion

This lab demonstrates how to interface an I²C digital sensor (LM73) with
ESP32 and create a mobile monitoring dashboard in Thunkable. It
reinforces IoT integration concepts: **hardware sensing →
microcontroller processing → app visualization**.


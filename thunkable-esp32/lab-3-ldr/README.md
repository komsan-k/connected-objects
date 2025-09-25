# 🧪 Lab 3: Monitoring an LDR with Thunkable and ESP32 over Wi-Fi

## 1. Objective

The objective of this lab is to design a mobile application in
**Thunkable** that monitors real-time **light intensity values** from an
LDR connected to an **ESP32**. Students will learn to:\
- Interface an LDR with the ESP32 using an ADC (Analog-to-Digital
Converter).\
- Configure the ESP32 as a web server that serves sensor data.\
- Build a Thunkable app that queries and displays light sensor
readings.\
- Apply IoT concepts for environmental monitoring.

## 2. Background

An **LDR (photoresistor)** changes its resistance depending on ambient
light intensity. By wiring it in a voltage divider circuit, the ESP32's
ADC pin can read a voltage proportional to light levels.

Example applications include:\
- Smart lighting (automatic dimming).\
- Environmental monitoring.\
- IoT dashboards for remote sensing.

## 3. Materials

-   ESP32 development board.\
-   LDR sensor.\
-   10kΩ resistor (for voltage divider).\
-   Breadboard + jumper wires.\
-   Arduino IDE with ESP32 support.\
-   Smartphone with **Thunkable Live** app.\
-   Shared Wi-Fi network.

## 4. Procedure

### Step 1: Circuit Setup

Make a voltage divider:

       3.3V ── LDR ──┬── GPIO 34 (ADC pin)  
                     │  
                  10kΩ  
                     │  
                    GND  

-   Connect LDR and resistor in series.\
-   Middle junction → ESP32 ADC pin (GPIO 34 is a good choice).

### Step 2: ESP32 Code

``` cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

#define LDR_PIN 34
WebServer server(80);

void handleLDR() {
  int raw = analogRead(LDR_PIN);
  float voltage = (3.3 * raw) / 4095.0;  // Convert ADC to voltage
  String json = "{\"raw\":" + String(raw) + ",\"voltage\":" + String(voltage, 2) + "}";
  Serial.println(json);
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", json);
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(); Serial.print("IP: "); Serial.println(WiFi.localIP());

  server.on("/ldr", HTTP_GET, handleLDR);
  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();
}
```

### Step 3: Thunkable App Design

-   Add a `Button_Refresh` → text: *Read LDR*.\
-   Add a `Label_Value` → placeholder text: "Waiting for data...".\
-   Add `WebAPI_ESP` component.

### Step 4: Thunkable Blocks

-   **When Screen Opens**
    -   Set `WebAPI_ESP.URL = "http://<ESP32_IP>/ldr"`.
-   **When Button_Refresh.Click**
    -   Call `WebAPI_ESP.Get`.
-   **When WebAPI_ESP.Get.Success**
    -   Extract `"raw"` and `"voltage"` from response object.\
    -   Set `Label_Value.Text = "Raw: " + raw + " | V: " + voltage`.
-   **When WebAPI_ESP.Get.Error**
    -   Set `Label_Value.Text = "Error connecting to ESP32"`.

## 5. Diagrams

### Data Flow

    Thunkable App (Button Press)
           │
           ▼
     WebAPI_ESP GET /ldr
           │
           ▼
    ESP32 reads ADC (GPIO 34 → LDR voltage)
           │
           ▼
    Responds with JSON {raw, voltage}
           │
           ▼
    App displays raw + voltage

## 6. Verification

-   In Serial Monitor, confirm values update when light levels change.\
-   In Thunkable app, tap **Read LDR** → display updates.\
-   Shine a flashlight or cover the LDR to test variations.

## 7. Exercises

1.  Modify the ESP32 code to return **lux estimates** instead of raw ADC
    values.\
2.  Add a **chart component** in Thunkable to plot light intensity
    trends.\
3.  Implement **auto-refresh** every 5 seconds.\
4.  Add thresholds in Thunkable (e.g., show "Bright" vs "Dark").\
5.  Expand to multi-sensor monitoring (add temperature, humidity, etc.).

## 8. Conclusion

This lab shows how an ESP32 can **read analog sensor data** and serve it
over Wi-Fi to a mobile app. By connecting an LDR, students practice
analog sensing, ADC conversion, and mobile IoT dashboards. This
experiment can be extended to many other sensors and smart monitoring
applications.


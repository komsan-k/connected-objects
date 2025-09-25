# 🧪 Lab 2: Controlling LEDs with Thunkable and ESP32 over Wi-Fi

## 1. Objective

The objective of this lab is to create a mobile application using
**Thunkable** that controls the state of one or more **LEDs connected to
an ESP32**. Students will learn to:\
- Configure the ESP32 as a Wi-Fi web server with REST endpoints for LED
control.\
- Build a mobile app interface with buttons to toggle LEDs.\
- Send and receive HTTP requests/responses for real-time IoT control.\
- Verify operation both in Serial Monitor and visually via LEDs.

## 2. Background

The ESP32 can serve as a lightweight HTTP server, exposing endpoints
such as:\
- `http://<ESP32_IP>/led/on`\
- `http://<ESP32_IP>/led/off`

Thunkable's **Web API** component can be configured to call these
endpoints when a button is pressed. This allows students to integrate
hardware (LEDs) with mobile UI control, a fundamental building block for
IoT systems such as smart home applications.

## 3. Materials

-   ESP32 development board (e.g., ESP32-DevKitC).\
-   USB cable for programming.\
-   1 or more LEDs (e.g., red/green).\
-   Resistors (220--330 Ω).\
-   Breadboard + jumper wires.\
-   Arduino IDE with ESP32 support.\
-   Smartphone with **Thunkable Live** app.\
-   Shared Wi-Fi network.

## 4. Procedure

### Step 1: Wire the Circuit

-   Connect LED **anode** (long leg) → ESP32 GPIO pin (e.g., GPIO 5).\
-   Connect LED **cathode** (short leg) → resistor → GND.

```{=html}
<!-- -->
```
    ESP32 GPIO 5 ───▶|───Ω─── GND
                    LED  Resistor

### Step 2: ESP32 Code

``` cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

#define LED_PIN 5
WebServer server(80);

void handleOn() {
  digitalWrite(LED_PIN, HIGH);
  Serial.println("LED ON");
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", "{\"status\":\"LED ON\"}");
}

void handleOff() {
  digitalWrite(LED_PIN, LOW);
  Serial.println("LED OFF");
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", "{\"status\":\"LED OFF\"}");
}

void handleOptions() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
  server.send(204);
}

void setup() {
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(); Serial.print("IP: "); Serial.println(WiFi.localIP());

  server.on("/led/on", HTTP_GET, handleOn);
  server.on("/led/off", HTTP_GET, handleOff);
  server.on("/led/on", HTTP_OPTIONS, handleOptions);
  server.on("/led/off", HTTP_OPTIONS, handleOptions);
  server.begin();
  Serial.println("Server started");
}

void loop() { server.handleClient(); }
```

### Step 3: Thunkable App Design

-   Add two buttons:
    -   **Button_On** → text: *LED ON*\
    -   **Button_Off** → text: *LED OFF*\
-   Add a `Label_Status` for feedback.\
-   Add `WebAPI_ESP` component.

### Step 4: Thunkable Blocks

-   **When Screen Opens**
    -   Set `WebAPI_ESP.URL = "http://<ESP32_IP>/led/on"`
-   **When Button_On.Click**
    -   Set `WebAPI_ESP.URL = "http://<ESP32_IP>/led/on"`\
    -   Call `WebAPI_ESP.Get`\
    -   On Success → `Label_Status.Text = "LED is ON"`
-   **When Button_Off.Click**
    -   Set `WebAPI_ESP.URL = "http://<ESP32_IP>/led/off"`\
    -   Call `WebAPI_ESP.Get`\
    -   On Success → `Label_Status.Text = "LED is OFF"`

## 5. Diagrams

### Data Flow

    Thunkable App (Button Press)
           │
           ▼
      WebAPI_ESP GET
       /led/on or /led/off
           │
           ▼
    ESP32 WebServer → GPIO Pin → LED State

## 6. Verification

-   Tap **LED ON** → LED lights up, Serial prints "LED ON".\
-   Tap **LED OFF** → LED turns off, Serial prints "LED OFF".\
-   Thunkable app updates label accordingly.

## 7. Exercises

1.  Extend app to control **two LEDs** (red + green).\
2.  Add a **toggle button** (if LED on → turn off, else turn on).\
3.  Add a **status query endpoint** (`/led/status`) on ESP32 and display
    in Thunkable.\
4.  Experiment with different GPIO pins and multiple devices.\
5.  Research how to adapt this to **voice commands** using Thunkable +
    Google Assistant.

## 8. Conclusion

This lab demonstrates **bidirectional integration of mobile UI and
physical hardware**. Students learn to control hardware states via REST
APIs, a critical foundation for IoT devices and smart home applications.


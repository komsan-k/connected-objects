# 🧪 Lab 5: Controlling SG90 Servo Motor with Thunkable and ESP32 over Wi-Fi

## 1. Objective

The objective of this lab is to control the **SG90 micro servo motor**
using an **ESP32** and a **Thunkable mobile app**. Students will learn
how to:\
- Generate PWM signals on the ESP32 to control a servo motor.\
- Build a Thunkable app with buttons/sliders to adjust servo angle.\
- Send servo commands from the app via Wi-Fi using HTTP.\
- Validate motion by observing servo rotation.

## 2. Background

The **SG90** is a small, inexpensive hobby servo motor:\
- Operating voltage: 4.8--6 V\
- Rotation range: \~0°--180°\
- Controlled via PWM (pulse width 500--2500 µs at 50 Hz).

The ESP32 provides PWM signals via its **LEDC (LED Controller)**
hardware. Thunkable's Web API component sends commands over Wi-Fi, which
the ESP32 converts into servo angles.

## 3. Materials

-   ESP32 development board.\
-   SG90 servo motor.\
-   External 5 V power source for servo (recommended).\
-   Breadboard + jumper wires.\
-   Arduino IDE with ESP32Servo library.\
-   Smartphone with Thunkable Live app.\
-   Shared Wi-Fi network.

## 4. Procedure

### Step 1: Circuit Setup

-   Servo **Orange/Yellow** (signal) → ESP32 GPIO 18.\
-   Servo **Red** (VCC) → external **5 V** supply.\
-   Servo **Brown/Black** (GND) → common ground with ESP32.

```{=html}
<!-- -->
```
       ESP32 GPIO18 ───▶ Servo Signal (Orange)
       5V supply ─────▶ Servo VCC (Red)
       GND ───────────▶ Servo GND (Brown)

⚠️ Do **not** power the servo directly from ESP32 3.3 V pin.

### Step 2: ESP32 Code

``` cpp
#include <WiFi.h>
#include <WebServer.h>
#include <ESP32Servo.h>

const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

Servo myservo;
int servoPin = 18;

WebServer server(80);

void handleAngle() {
  if (server.hasArg("pos")) {
    int angle = server.arg("pos").toInt();
    if (angle >= 0 && angle <= 180) {
      myservo.write(angle);
      Serial.printf("Servo moved to %d°\n", angle);
      server.sendHeader("Access-Control-Allow-Origin", "*");
      server.send(200, "application/json", "{\"status\":\"ok\",\"angle\":" + String(angle) + "}");
      return;
    }
  }
  server.send(400, "application/json", "{\"error\":\"Invalid angle\"}");
}

void setup() {
  Serial.begin(115200);
  myservo.attach(servoPin, 500, 2500);

  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(); Serial.print("IP: "); Serial.println(WiFi.localIP());

  server.on("/servo", HTTP_GET, handleAngle);
  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();
}
```

-   Endpoint: `http://<ESP32_IP>/servo?pos=90` (moves servo to 90°).

### Step 3: Thunkable App Design

-   Add a **Slider** (`Slider_Angle`) range 0--180.\
-   Add a **Button_Send** → text: *Set Angle*.\
-   Add a **Label_Status** for feedback.\
-   Add `WebAPI_ESP` component.

### Step 4: Thunkable Blocks

-   **When Screen Opens**
    -   Set `WebAPI_ESP.URL = "http://<ESP32_IP>/servo"`.
-   **When Button_Send.Click**
    -   Set
        `WebAPI_ESP.URL = "http://<ESP32_IP>/servo?pos=" + Slider_Angle.Value`.\
    -   Call `WebAPI_ESP.Get`.
-   **When WebAPI_ESP.Get.Success**
    -   Extract `"angle"` from response.\
    -   Set `Label_Status.Text = "Servo moved to " + angle + "°"`.
-   **When WebAPI_ESP.Get.Error**
    -   Set `Label_Status.Text = "Error sending command"`.

## 5. Diagrams

### Data Flow

    Thunkable App (Slider + Button)
           │
           ▼
     WebAPI_ESP GET /servo?pos=ANGLE
           │
           ▼
    ESP32 parses angle → generates PWM
           │
           ▼
    Servo rotates to target angle

## 6. Verification

-   Open Serial Monitor → confirm angle commands.\
-   Move slider in the app and tap *Set Angle*.\
-   Observe servo rotate accordingly.

## 7. Exercises

1.  Add quick buttons in Thunkable for **0°, 90°, 180°** positions.\
2.  Implement **continuous sweeping** mode triggered from the app.\
3.  Add feedback endpoint (`/servo/status`) returning last angle.\
4.  Modify to control **two servos** with different endpoints.\
5.  Integrate with previous labs (e.g., servo moves based on LDR/LM73
    input).

## 8. Conclusion

This lab shows how to control an **actuator (SG90 servo)** via ESP32 and
Thunkable. It demonstrates end-to-end IoT integration: **mobile input →
network message → microcontroller PWM → mechanical motion**.


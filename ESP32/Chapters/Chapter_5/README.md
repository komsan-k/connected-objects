# Chapter 5: Web Engineering on ESP32

The **ESP32** is not only a microcontroller but also a powerful IoT platform with built-in **Wi-Fi and Bluetooth**, making it ideal for **embedded web applications**. Web engineering on ESP32 involves designing, developing, and deploying **web servers, APIs, and dashboards** for remote monitoring, control, and data visualization.  
Because of ESP32’s **limited resources**, careful optimization is required.

---

## 1. Web Server Models on ESP32

### 1.1 HTTP Server
- Libraries: **WebServer** or **ESPAsyncWebServer**.  
- Supports static pages (HTML, CSS, JS) and REST endpoints.  
- ✅ Use Case: IoT dashboards, device configuration portals.  

### 1.2 WebSocket Server
- Enables **real-time bidirectional communication** between ESP32 and browsers.  
- ✅ Use Case: Real-time telemetry, smart home control.  

### 1.3 RESTful APIs
- Implement REST APIs for **Node-RED**, MQTT bridges, or cloud platforms.  
- ✅ Use Case: Mobile app or cloud dashboard integration.  

### 1.4 Asynchronous Web Servers
- **ESPAsyncWebServer** supports **non-blocking handling** for multiple clients.  

---

## 2. Web Content Management
ESP32’s limited flash requires strategic choices:
- **In-Code HTML** → store HTML as `const char*`.  
- **SPIFFS / LittleFS** → store HTML, CSS, JS in filesystem.  
- **External Storage (SD)** → for larger web apps.  

---

## 3. AJAX and Fetch API
ESP32 supports AJAX to update web pages without reloading.  

**Example Workflow:**
- `/api/telemetry` → returns JSON `{ "temp": 26.3, "uptime": 120000 }`  
- `/api/led?state=on` → controls GPIO, returns `{ "led": "on" }`  

✅ Use Case: IoT dashboards (temp, humidity, actuator states).

---

## 4. Security in ESP32 Web Apps
- **Wi-Fi Encryption**: WPA2/WPA3.  
- **HTTPS/TLS**: via `WiFiClientSecure`.  
- **Auth Tokens** for API endpoints.  
- **CORS Handling** for external dashboards.  

---

## 5. Integration with Node-RED and MQTT
- ESP32 → local web dashboards.  
- **Node-RED** → integrates streams, forwards to cloud.  
- **MQTT** → publish/subscribe messaging for large IoT systems.  

---

## 6. Example: ESP32 Web Server with AJAX

```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASS";

WebServer server(80);
const int LED_PIN = 5;

String telemetryJson() {
  float temp = 25.6;
  bool ledOn = digitalRead(LED_PIN);
  char buf[120];
  snprintf(buf, sizeof(buf),
    "{\"temp\":%.2f,\"led\":\"%s\"}", temp, ledOn ? "on" : "off");
  return String(buf);
}

void handleRoot() {
  server.send(200, "text/html", "<h1>ESP32 Web Engineering</h1>");
}

void apiTelemetry() {
  server.send(200, "application/json", telemetryJson());
}

void apiLed() {
  if (server.hasArg("state")) {
    String s = server.arg("state");
    if (s == "on") digitalWrite(LED_PIN, HIGH);
    else if (s == "off") digitalWrite(LED_PIN, LOW);
  }
  server.send(200, "application/json", telemetryJson());
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }
  Serial.print("IP: "); Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/api/telemetry", HTTP_GET, apiTelemetry);
  server.on("/api/led", HTTP_ANY, apiLed);
  server.begin();
}

void loop() { server.handleClient(); }
```

---

## 7. Challenges in ESP32 Web Engineering
- **Limited Flash/RAM** → optimize assets, use compression.  
- **Concurrent Connections** → prefer async servers.  
- **TLS Security Overheads** → higher memory usage.  
- **OTA Updates** → keep web code + firmware up to date.  

---

## 8. Applications
- Smart home dashboards (lighting, HVAC).  
- Real-time sensor portals (temperature, humidity).  
- Industrial control panels.  
- IoT device configuration pages.  

---


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



---
---
# Web Engineering on ESP32

Web engineering on **ESP32** refers to the design, implementation, and optimization of **web-based interfaces and services** running directly on the microcontroller. Unlike traditional servers with abundant resources, the ESP32 operates with **constrained flash memory and RAM**, requiring tailored approaches. This allows ESP32 to act as an IoT node, hosting **dashboards, REST APIs, or WebSocket services**.

---

## 1. ESP32 as a Web Server

### Synchronous Web Server (`WebServer.h`)
- Simplest to implement, supports GET/POST requests.  
- ✅ Ideal for small dashboards.

### Asynchronous Web Server (`ESPAsyncWebServer.h`)
- Non-blocking, handles multiple clients efficiently.  
- ✅ Recommended for real-time IoT systems.

### WebSocket Server
- Provides persistent full-duplex communication.  
- ✅ Reduces overhead compared to repeated HTTP polling.  

---

## 2. Web Content Management

### In-Code HTML
- Store HTML, CSS, JS in Arduino sketches (`const char*`).  
- Suitable for very small apps.  

### SPIFFS / LittleFS
- Store static web content in ESP32 flash filesystem.  
- ✅ Enables structured multi-file apps.  

### SD Card Hosting
- Expand storage for large dashboards and multimedia.  

---

## 3. AJAX and Fetch API Integration
ESP32 supports **AJAX** and **Fetch API** for updating pages without reload.  

- `/api/telemetry` → returns JSON sensor data.  
- `/api/control` → accepts POST requests for GPIO actuation.  

✅ Provides smooth, real-time interfaces.  

---

## 4. RESTful API Design
ESP32 can expose REST endpoints compatible with Node-RED, Python, or mobile apps.  

- **GET** → retrieve sensor data  
- **POST** → send commands  
- **PUT** → update configurations  
- **DELETE** → reset/remove resources  

✅ REST enables standardized IoT communication & cloud integration.  

---

## 5. Security in ESP32 Web Applications
Security is critical for IoT deployments:  
- WPA2/WPA3 Wi-Fi authentication.  
- HTTPS via `WiFiClientSecure`.  
- Basic or token-based API authentication.  
- Encrypted credential storage.  

⚠️ Balance **security vs performance** on limited hardware.  

---

## 6. Real-Time Web Communication
- **WebSockets** → push telemetry instantly.  
- **SSE (Server-Sent Events)** → lightweight, unidirectional.  
- **MQTT over WebSocket** → enables browser-based pub/sub clients.  

---

## 7. Integration with Node-RED and MQTT
ESP32 complements larger IoT workflows:  
- **Local dashboards** served by ESP32.  
- **Cloud integration** via REST + Node-RED.  
- **MQTT bridge** → ESP32 acts as pub/sub client with a web UI.  

---

## 8. Power & Performance Considerations
- Limit concurrent clients (Async servers help).  
- Optimize content (minify HTML/JS, compress JSON).  
- Use caching & lightweight libraries.  
- Consider deep sleep + wake-on-request strategies.  

---

## 9. Example: ESP32 AJAX Dashboard

```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASS";

WebServer server(80);

String telemetryJson() {
  float temp = 25.4;
  bool ledOn = digitalRead(2);
  char buf[100];
  snprintf(buf, sizeof(buf), "{\"temp\":%.2f,\"led\":\"%s\"}",
           temp, ledOn ? "on" : "off");
  return String(buf);
}

void handleRoot() {
  server.send(200, "text/html",
              "<h2>ESP32 Web Dashboard</h2><p>Use /api/telemetry</p>");
}

void apiTelemetry() {
  server.send(200, "application/json", telemetryJson());
}

void apiLed() {
  if (server.hasArg("state")) {
    if (server.arg("state") == "on") digitalWrite(2, HIGH);
    else digitalWrite(2, LOW);
  }
  server.send(200, "application/json", telemetryJson());
}

void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/api/telemetry", HTTP_GET, apiTelemetry);
  server.on("/api/led", HTTP_ANY, apiLed);
  server.begin();
}

void loop() {
  server.handleClient();
}
```

---

## 10. Applications
- **Smart Home Dashboards** (lights, HVAC).  
- **Industrial Monitoring** (sensors, actuators).  
- **Educational IoT Projects** (real-time dashboards).  
- **Device Configuration Portals** (Wi-Fi provisioning, settings).  

---
---
# Arduino Code Web Engineering on ESP32

Web engineering on **ESP32** refers to the design, implementation, and optimization of **web-based interfaces and services** running directly on the microcontroller. Unlike traditional servers with abundant resources, the ESP32 operates with **constrained flash memory and RAM**, requiring tailored approaches. This allows ESP32 to act as an IoT node, hosting **dashboards, REST APIs, or WebSocket services**.

---

## 1. ESP32 as a Web Server

### Synchronous Web Server (`WebServer.h`)
- Simplest to implement, supports GET/POST requests.  
- ✅ Ideal for small dashboards.

### Asynchronous Web Server (`ESPAsyncWebServer.h`)
- Non-blocking, handles multiple clients efficiently.  
- ✅ Recommended for real-time IoT systems.

### WebSocket Server
- Provides persistent full-duplex communication.  
- ✅ Reduces overhead compared to repeated HTTP polling.  

---

## 2. Web Content Management

### In-Code HTML
- Store HTML, CSS, JS in Arduino sketches (`const char*`).  
- Suitable for very small apps.  

### SPIFFS / LittleFS
- Store static web content in ESP32 flash filesystem.  
- ✅ Enables structured multi-file apps.  

### SD Card Hosting
- Expand storage for large dashboards and multimedia.  

---

## 3. AJAX and Fetch API Integration
ESP32 supports **AJAX** and **Fetch API** for updating pages without reload.  

- `/api/telemetry` → returns JSON sensor data.  
- `/api/control` → accepts POST requests for GPIO actuation.  

✅ Provides smooth, real-time interfaces.  

---

## 4. RESTful API Design
ESP32 can expose REST endpoints compatible with Node-RED, Python, or mobile apps.  

- **GET** → retrieve sensor data  
- **POST** → send commands  
- **PUT** → update configurations  
- **DELETE** → reset/remove resources  

✅ REST enables standardized IoT communication & cloud integration.  

---

## 5. Security in ESP32 Web Applications
Security is critical for IoT deployments:  
- WPA2/WPA3 Wi-Fi authentication.  
- HTTPS via `WiFiClientSecure`.  
- Basic or token-based API authentication.  
- Encrypted credential storage.  

⚠️ Balance **security vs performance** on limited hardware.  

---

## 6. Real-Time Web Communication
- **WebSockets** → push telemetry instantly.  
- **SSE (Server-Sent Events)** → lightweight, unidirectional.  
- **MQTT over WebSocket** → enables browser-based pub/sub clients.  

---

## 7. Integration with Node-RED and MQTT
ESP32 complements larger IoT workflows:  
- **Local dashboards** served by ESP32.  
- **Cloud integration** via REST + Node-RED.  
- **MQTT bridge** → ESP32 acts as pub/sub client with a web UI.  

---

## 8. Power & Performance Considerations
- Limit concurrent clients (Async servers help).  
- Optimize content (minify HTML/JS, compress JSON).  
- Use caching & lightweight libraries.  
- Consider deep sleep + wake-on-request strategies.  

---

## 9. Example: ESP32 AJAX Dashboard

```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASS";

WebServer server(80);

String telemetryJson() {
  float temp = 25.4;
  bool ledOn = digitalRead(2);
  char buf[100];
  snprintf(buf, sizeof(buf), "{\"temp\":%.2f,\"led\":\"%s\"}",
           temp, ledOn ? "on" : "off");
  return String(buf);
}

void handleRoot() {
  server.send(200, "text/html",
              "<h2>ESP32 Web Dashboard</h2><p>Use /api/telemetry</p>");
}

void apiTelemetry() {
  server.send(200, "application/json", telemetryJson());
}

void apiLed() {
  if (server.hasArg("state")) {
    if (server.arg("state") == "on") digitalWrite(2, HIGH);
    else digitalWrite(2, LOW);
  }
  server.send(200, "application/json", telemetryJson());
}

void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }
  Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/api/telemetry", HTTP_GET, apiTelemetry);
  server.on("/api/led", HTTP_ANY, apiLed);
  server.begin();
}

void loop() {
  server.handleClient();
}
```

---

## 10. Applications
- **Smart Home Dashboards** (lights, HVAC).  
- **Industrial Monitoring** (sensors, actuators).  
- **Educational IoT Projects** (real-time dashboards).  
- **Device Configuration Portals** (Wi-Fi provisioning, settings).  

---


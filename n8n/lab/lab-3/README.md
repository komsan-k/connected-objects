# 🔬 Lab 3: ESP32 → n8n Control Automation (n8n Sends Command to ESP32)

## 1. Objective
This lab teaches how **n8n can control an ESP32** using HTTP requests.

Students will learn:
- How to create an **HTTP endpoint on ESP32**
- How to use **n8n HTTP Request node** to send commands
- How to toggle LED/relay on ESP32 remotely

---

## 2. Tools Required
- ESP32 Development Board  
- Wi-Fi Network  
- n8n (Local / Docker / Cloud)  
- Arduino IDE  

---

## 3. Overview
n8n acts as a controller:

```
[n8n Trigger]
       ↓
[HTTP Request Node]
       ↓
  ESP32 (LED ON/OFF)
```

Use cases:
- Remote LED / relay control  
- Automation tasks triggered by schedule, sensor, or Telegram command  

---

## 4. ESP32 Code (HTTP Command Server)

```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";

WebServer server(80);
int LED = 2;

void handleRoot() {
  server.send(200, "text/plain", "ESP32 Control Active");
}

void handleOn() {
  digitalWrite(LED, HIGH);
  server.send(200, "text/plain", "LED ON");
}

void handleOff() {
  digitalWrite(LED, LOW);
  server.send(200, "text/plain", "LED OFF");
}

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  server.on("/", handleRoot);
  server.on("/on", handleOn);
  server.on("/off", handleOff);

  server.begin();
}

void loop() {
  server.handleClient();
}
```

ESP32 endpoints:
- `http://ESP32_IP/on`  
- `http://ESP32_IP/off`

---

## 5. n8n Workflow Steps

### Step 1 — Add a Trigger Node  
Choose any trigger:
- Manual Trigger  
- Cron (run every 10 seconds)  
- Webhook  
- Telegram Receive Message  

### Step 2 — Add HTTP Request Node  
Example configuration:

```
Method: GET
URL: http://ESP32_IP/on
```

To turn LED off:

```
Method: GET
URL: http://ESP32_IP/off
```

### Step 3 — Optional Logic Node  
Use a Function Node:

```js
return [{
  led: "on",
  message: "Command sent to ESP32"
}];
```

---

## 6. Example Automation Scenarios

| Scenario | Description |
|---------|-------------|
| 🔥 Temperature alert | If temp > 30°C → n8n sends HTTP request → ESP32 activates fan |
| 💡 Scheduled lighting | Cron triggers every 18:00 → LED ON; 23:00 → LED OFF |
| 📱 Telegram control | `/led_on` → ESP32 LED ON via n8n |

---

## 7. Result Observation

| Action in n8n | ESP32 Response |
|---------------|----------------|
| HTTP Request `/on` | LED lights up |
| HTTP Request `/off` | LED turns off |
| Workflow execution | Shows success message |

---

## 8. Questions

1. How does n8n send commands to ESP32?  
2. What are the benefits of using HTTP control vs MQTT control?  
3. Modify ESP32 to support `/blink`.  
4. Add password protection to the ESP32 endpoint.  

---


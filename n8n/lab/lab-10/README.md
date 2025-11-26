# 🔬 Lab 10: ESP32 + n8n Rule-Based Automation Engine  
### Building a Full IoT Logic System (Multi-Condition + Multi-Device Automation)

## 1. Objective
This lab introduces how to use **n8n as a rule-based automation engine** for IoT systems.  
Students will learn:
- Multi-condition logic processing  
- Handling multiple ESP32 devices  
- Applying automatic rules (IF/THEN logic)  
- Triggering actions (notifications, device control, logging)

---

## 2. Tools Required
- Multiple ESP32 devices  
- Wi-Fi network  
- n8n (Cloud / Local / Docker)  
- Arduino IDE  
- Telegram / Email / Google Sheets (optional)

---

## 3. System Overview

```
ESP32 Devices → n8n Webhook → Rule Engine → Output Actions
                                   ↓
                  Alerts / Commands / Logging / Database
```

Example rule automation:
- If **temperature > 35°C** AND **humidity < 50%** → send alert  
- If **device_id = esp32_03** → store in separate sheet  
- If **motion = detected** → turn on lamp via ESP32  

---

## 4. ESP32 Code (Sensor JSON Sender)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* url = "https://n8n.yourdomain.com/webhook/lab10";

String DEVICE_ID = "esp32_01";  // Change per device

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void loop() {
  HTTPClient http;
  http.begin(url);
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<200> doc;
  doc["device_id"] = DEVICE_ID;
  doc["temperature"] = random(24, 40);
  doc["humidity"] = random(35, 80);
  doc["motion"] = random(0, 10) > 7 ? 1 : 0;

  String json;
  serializeJson(doc, json);

  http.POST(json);
  http.end();

  delay(5000);
}
```

---

## 5. n8n Workflow (Rule-Based Engine)

### Step 1 — Webhook Trigger  
Path: `/lab10`

Incoming JSON:
```
{
  "device_id": "esp32_01",
  "temperature": 36,
  "humidity": 45,
  "motion": 1
}
```

---

### Step 2 — Function Node: Build Rule Logic

```js
const t = $json.temperature;
const h = $json.humidity;
const m = $json.motion;
const id = $json.device_id;

let action = [];

if (t > 35 && h < 50) {
  action.push("ALERT_HIGH_HEAT");
}

if (id === "esp32_03") {
  action.push("STORE_SPECIAL");
}

if (m === 1) {
  action.push("TURN_ON_LIGHT");
}

return [{
  device: id,
  temperature: t,
  humidity: h,
  motion: m,
  action
}];
```

---

### Step 3 — Switch / IF Node  
Routes based on action:

- `"ALERT_HIGH_HEAT"` → Telegram  
- `"STORE_SPECIAL"` → Sheets (Device 03)  
- `"TURN_ON_LIGHT"` → HTTP Command to ESP32 Lamp  

Example Telegram message:

```
🔥 High Heat Alert!
Device: {{$json.device}}
Temp: {{$json.temperature}} °C
Humidity: {{$json.humidity}}%
```

Example Device Command Node (HTTP Request):

```
GET http://esp32_03.local/light/on
```

---

## 6. Result Observation

| Condition | Triggered Action |
|----------|------------------|
| temp > 35 AND humidity < 50 | High Heat Alert |
| device_id = esp32_03 | Special Sheet Logging |
| motion = 1 | Turn on Light Command |

n8n behaves as a **smart IoT automation engine**.

---

## 7. Questions

1. Why is n8n suitable for rule-based IoT automation?  
2. Add a rule: humidity > 70% → Telegram alert.  
3. Extend system to support 10 devices with separate logic.  
4. Add summary reporting using Cron node every 1 hour.  
5. Add rule chaining (multiple actions per condition).  

---



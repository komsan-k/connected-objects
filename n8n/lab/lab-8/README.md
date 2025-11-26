# 🔬 Lab 8: Multi-Device IoT Integration with n8n  
### Handling Multiple ESP32 Nodes with Device Routing & Data Aggregation

## 1. Objective
This lab teaches how to connect **multiple ESP32 devices** to one n8n workflow and process each device’s data individually or collectively.

Students will learn:
- Multi-device Webhook handling  
- Device identification and routing  
- Data aggregation  
- Storing per-device logs  
- Broadcasting commands to specific ESP32 nodes  

---

## 2. Tools Required
- 2–10 ESP32 boards  
- Wi-Fi network  
- n8n (Cloud / Local / Docker)  
- Arduino IDE  
- Google Sheets / Database (optional)

---

## 3. System Overview

```
  ESP32 #1 ─┐
  ESP32 #2 ─┼──→ n8n Webhook → Router → Device Logic → Storage
  ESP32 #3 ─┘
```

Each ESP32 sends:
```
{
  "device_id": "esp32_node_01",
  "temperature": 30.2,
  "humidity": 58
}
```

n8n:
- Detects device
- Routes data
- Stores or triggers alerts

---

## 4. ESP32 Code (Multi-Node JSON Sender)

> Use same code for all ESP32 devices; only change **device_id**.

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* url = "https://n8n.yourdomain.com/webhook/lab8";

String DEVICE_ID = "esp32_node_01";   // Change per device

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
  doc["temp"] = random(25, 40);
  doc["humidity"] = random(40, 80);

  String json;
  serializeJson(doc, json);

  http.POST(json);
  http.end();
  delay(4000);
}
```

---

## 5. n8n Workflow

### Step 1 — Webhook Trigger  
Path: `/lab8`

### Step 2 — Function Node (Routing Logic)

```js
const id = $json.device_id;

let group = "unknown";

if (id.startsWith("esp32_node_01")) group = "Floor1";
if (id.startsWith("esp32_node_02")) group = "Floor2";
if (id.startsWith("esp32_node_03")) group = "Outdoor";

return [{
  id,
  group,
  temp: $json.temp,
  humidity: $json.humidity,
  timestamp: new Date().toISOString()
}];
```

### Step 3A — IF Node (Device-Specific Logic)
Examples:
- Floor1 → Google Sheets  
- Floor2 → Telegram Alerts  
- Outdoor → Database log  

### Step 3B — Aggregation (Optional)
Using Code Node:

```js
let t = $json.temp;
let h = $json.humidity;

return [{
  summary: `Device ${$json.id} @ ${$json.group} → T=${t}, H=${h}`
}];
```

### Step 4 — Storage or Notification
Options:
- Google Sheets  
- MySQL / PostgreSQL  
- Telegram / Email  
- InfluxDB  
- Firebase  

---

## 6. Result Observation

| Device | Group | Example Data |
|--------|--------|--------------|
| esp32_node_01 | Floor1 | Temp=32, Hum=60 |
| esp32_node_02 | Floor2 | Temp=29, Hum=55 |
| esp32_node_03 | Outdoor | Temp=37, Hum=48 |

n8n correctly identifies, routes, stores, and reacts to each device.

---

## 7. Questions

1. How does n8n distinguish between multiple devices?  
2. Modify routing to support **10** ESP32 devices.  
3. Add an alert for Outdoor device only.  
4. Add a daily report workflow (Cron node).  
5. Add command broadcast to **only Floor1** ESP32 devices.

---

  

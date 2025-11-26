# 🔬 Lab 4: ESP32 → n8n Data Storage (Google Sheets / Database Integration)

## 1. Objective
This lab teaches how to collect ESP32 sensor data using **n8n Webhook**, process it, and store it into:
- **Google Sheets**, or  
- **MySQL / PostgreSQL database**

Students will learn:
- Structuring IoT data pipelines
- Parsing JSON in n8n
- Writing data to external storage systems

---

## 2. Tools Required
- ESP32 (Any model)
- Wi-Fi Access Point
- n8n (Local / Docker / Cloud)
- Google Account (for Sheets)
- Arduino IDE

---

## 3. Overview

```
ESP32 → HTTP POST → n8n Webhook → Function Node → Google Sheets / Database
```

This lab focuses on **data logging**, one of the most essential IoT system tasks.

---

## 4. ESP32 Code (Send Temperature & Humidity to n8n)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* webhookUrl = "https://n8n.yourdomain.com/webhook/esp32_lab4";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(webhookUrl);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    doc["temperature"] = random(25, 35);
    doc["humidity"] = random(45, 80);
    doc["device_id"] = "esp32_lab4";

    String output;
    serializeJson(doc, output);

    http.POST(output);
    http.end();
  }
  delay(5000);
}
```

---

## 5. n8n Workflow

### Step 1 — Webhook Trigger
- Method: `POST`
- Path: `/esp32_lab4`

### Step 2 — Function Node (Parse & Structure Data)

```js
return [{
  temperature: $json.temperature,
  humidity: $json.humidity,
  device: $json.device_id,
  timestamp: new Date().toISOString()
}];
```

### Step 3A — Google Sheets Node
- Insert Row
- Map fields:
  - Temperature → temperature
  - Humidity → humidity
  - Device → device
  - Timestamp → timestamp

### Step 3B — Database Node (Optional)
Supports:
- MySQL  
- PostgreSQL  
- SQLite  

SQL Example:

```sql
INSERT INTO sensor_data (temp, humidity, device, timestamp)
VALUES ({{ $json.temperature }}, {{ $json.humidity }}, '{{ $json.device }}', '{{ $json.timestamp }}');
```

---

## 6. Result Observation

| Source | Value |
|--------|-------|
| ESP32 → JSON | `{ "temperature": 30, "humidity": 52 }` |
| n8n Function Output | Structured row with timestamp |
| Google Sheets | New row appended |
| Database | New record inserted |

---

## 7. Questions

1. Why is n8n a suitable choice for IoT data logging?  
2. What are advantages of storing data in Google Sheets vs Database?  
3. Modify the ESP32 code to include WiFi RSSI.  
4. Add device authentication to the webhook.  

---


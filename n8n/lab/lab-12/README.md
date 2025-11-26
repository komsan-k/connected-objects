# 🔬 Lab 12: ESP32 + n8n Data Visualization Pipeline  
### Sending IoT Data to n8n → Storing → Exporting → Visualizing (CSV, Sheets, Grafana)

## 1. Objective
This lab teaches how to build a **complete IoT data pipeline** using ESP32 and n8n:

1. ESP32 sends sensor data (JSON)  
2. n8n receives & processes it  
3. Data is stored in Google Sheets or CSV export  
4. Grafana / dashboard tools visualize the data  

Students will learn:
- Data formatting  
- Storage and export workflow  
- Grafana-ready JSON/CSV output  
- Timestamp handling  

---

## 2. Tools Required
- ESP32 Dev Board  
- Wi-Fi network  
- n8n (Cloud / Local / Docker)  
- Google Sheets OR local CSV  
- Grafana (optional)

---

## 3. System Overview

```
ESP32 → n8n Webhook → Function Node → Storage → Export → Visualization
```

---

## 4. ESP32 Code (Sensor Data Publishing)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* url = "https://n8n.yourdomain.com/webhook/lab12";

String DEVICE_ID = "esp32_visual_01";

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
  doc["temperature"] = random(25, 40);
  doc["humidity"] = random(40, 85);
  doc["timestamp"] = millis();

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
Path: `/lab12`

Incoming JSON:
```
{
  "device_id": "esp32_visual_01",
  "temperature": 32,
  "humidity": 55,
  "timestamp": 23000
}
```

---

### Step 2 — Function Node: Add ISO Timestamp

```js
return [{
  device: $json.device_id,
  temp: $json.temperature,
  humidity: $json.humidity,
  raw_time: $json.timestamp,
  iso_time: new Date().toISOString()
}];
```

---

### Step 3A — Google Sheets Storage (Option 1)

Map fields:
- device  
- temp  
- humidity  
- raw_time  
- iso_time  

### Step 3B — Append to CSV File (Option 2)

Use **Write Binary File** node.

CSV format:
```
device,temp,humidity,iso_time
esp32_visual_01,32,55,2025-01-01T08:30:00Z
```

---

## 6. Visualization Options

### Option A — Grafana (recommended)
- Install Grafana  
- Add "CSV" or "Google Sheets" plugin  
- Connect table to dashboard  
- Plot temp & humidity over time  

### Option B — Google Sheets Chart
Insert → Chart → Select:  
- X-axis: iso_time  
- Y-axis: temperature & humidity  

### Option C — Local Python Plot
Export CSV → use Matplotlib → plot graph.

---

## 7. Result Observation

| Data | Example Value |
|------|----------------|
| Device | esp32_visual_01 |
| Temperature | 32 °C |
| Humidity | 55 % |
| ISO Timestamp | 2025-01-01T08:30:00Z |

---

## 8. Questions

1. Why is ISO timestamp important?  
2. Add rolling average (5 samples) in n8n.  
3. Add a Grafana alert for temperature > 35°C.  
4. Compare CSV vs Google Sheets storage.  

---
 

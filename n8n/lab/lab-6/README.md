# 🔬 Lab 6: ESP32 + n8n Alert System (Threshold Detection & Notifications)

## 1. Objective
This lab teaches how to build an **automatic alert system** using:
- ESP32 sensor data
- n8n Webhook Trigger
- Threshold checking (Function node)
- Notifications via **Telegram / Email / Line Notify**

Students will learn:
- Real-time IoT monitoring
- Threshold-based automation
- How n8n sends alerts to messaging platforms

---

## 2. Tools Required
- ESP32 Dev Board  
- DHT11/DHT22 (optional)  
- Wi-Fi network  
- n8n (Cloud / Local / Docker)  
- Telegram/Email/Line account  

---

## 3. Overview

```
ESP32 → n8n Webhook → Function Node → IF Node → Telegram/Email/Line
```

Use case:
- ESP32 reports temperature  
- n8n checks if it exceeds a limit  
- n8n sends alert to your phone automatically  

---

## 4. ESP32 Code (Send Temperature to n8n)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* webhookUrl = "https://n8n.yourdomain.com/webhook/lab6";

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
    doc["temp"] = random(25, 40);    // simulate
    doc["humidity"] = random(40, 80);
    doc["device"] = "esp32_lab6";

    String json;
    serializeJson(doc, json);

    http.POST(json);
    http.end();
  }
  delay(5000);
}
```

---

## 5. n8n Workflow Structure

### Step 1 — Webhook Trigger Node
- Method: POST  
- Path: `/lab6`  

### Step 2 — Function Node (Threshold Logic)

```js
const temp = $json.temp;
const hum = $json.humidity;

return [{
  temp,
  hum,
  device: $json.device,
  alert: temp > 30 ? true : false,
  message: temp > 30
    ? `🔥 ALERT! High Temp: ${temp} °C`
    : `OK: ${temp} °C`
}];
```

### Step 3 — IF Node  
Condition:
```
IF alert == true
```

### Step 4A — Telegram Node (Alert)
Example message:
```
{{$json.message}}
Device: {{$json.device}}
Humidity: {{$json.hum}}%
```

### Step 4B — Email Node (Optional)
Subject: `ESP32 Temperature Alert`  
Body:
```
Temperature: {{$json.temp}}
Humidity: {{$json.hum}}
Device: {{$json.device}}
```

---

## 6. Result Observation

| Condition | n8n Action |
|----------|------------|
| Temperature ≤ 30°C | No alert |
| Temperature > 30°C | Sends Telegram/Email notification |

---

## 7. Questions

1. What are the advantages of threshold automation?  
2. Modify the system to alert when humidity < 45%.  
3. Add database logging alongside alerts.  
4. Add daily summary using Cron node.  

---

  

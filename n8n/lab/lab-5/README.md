# 🔬 Lab 5: ESP32 → n8n Dashboard Integration (JSON → UI Display)

## 1. Objective
This lab shows how to connect ESP32 to n8n and generate a **real-time dashboard-like display** using:
- Webhook Trigger  
- Function Node  
- HTML Node (Webhook Response)  

Students will learn:
- How to send JSON data from ESP32  
- How to convert JSON into HTML  
- How to display formatted values in a browser  

---

## 2. Tools Required
- ESP32 development board  
- Wi-Fi connection  
- n8n (Cloud / Local / Docker)  
- Arduino IDE  

---

## 3. Overview

```
ESP32 → Webhook Trigger → Function Node → HTML Response → Browser UI
```

This lab transforms n8n into a lightweight visualization interface.

---

## 4. ESP32 Code (Send Sensor JSON to n8n Webhook)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* webhookUrl = "https://n8n.yourdomain.com/webhook/lab5";

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
    doc["temperature"] = random(26, 34);
    doc["humidity"] = random(50, 80);
    doc["device_id"] = "esp32_lab5";

    String json;
    serializeJson(doc, json);

    http.POST(json);
    http.end();
  }
  delay(5000);
}
```

---

## 5. n8n Workflow

### Step 1 — Webhook Trigger
- Method: `POST`
- Path: `/lab5`

### Step 2 — Function Node (Build HTML)
```js
const temp = $json.temperature;
const hum = $json.humidity;
const dev = $json.device_id;

const html = `
<html>
<body style="font-family: Arial; text-align:center; padding:40px;">
<h2>ESP32 Live Dashboard</h2>
<p><strong>Device:</strong> ${dev}</p>
<p><strong>Temperature:</strong> ${temp} °C</p>
<p><strong>Humidity:</strong> ${hum} %</p>
<hr/>
<p>Updated: ${new Date().toLocaleString()}</p>
</body>
</html>
`;

return [{ html }];
```

### Step 3 — Webhook Response Node
- Use **HTML mode**
- Return `{{$json.html}}`

This creates a simple **HTML dashboard** that updates whenever ESP32 sends data.

---

## 6. Result Observation

| Action | Result |
|--------|--------|
| ESP32 sends POST | Dashboard updates |
| Refresh browser | Shows most recent reading |
| Mobile view | Fully supported |

Open your dashboard at:  
👉 `https://n8n.yourdomain.com/webhook/lab5`

---

## 7. Questions

1. Why use HTML output instead of JSON?  
2. Modify dashboard to include Wi-Fi RSSI.  
3. Add background color based on temperature.  
4. Add auto-refresh script into HTML.  

---

## 8. Author
Dr. Komsan Kanjanasit  
College of Computing, Prince of Songkla University  
Thailand  

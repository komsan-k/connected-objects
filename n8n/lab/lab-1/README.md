# 🔬 Lab 1: Introduction to n8n for IoT Automation (ESP32 + Webhook)

## 🧩 1. Objective
This laboratory introduces **n8n**, an open-source automation tool, and demonstrates how to integrate an **ESP32 microcontroller** with it using **HTTP webhooks**.
Students will learn how to:
- Understand workflow-based automation
- Create a Webhook Trigger in n8n
- Send sensor data from ESP32
- Process and visualize data

## ⚙️ 2. Equipment and Software
- ESP32 board
- Wi-Fi Access
- n8n (Cloud / Docker / Local)
- Arduino IDE
- Google account (optional)

## 🧠 3. Background Theory
n8n allows workflow automation through nodes. ESP32 can send JSON sensor data to a Webhook Trigger node using HTTP POST.

## 🧩 4. Experimental Setup
### Step 1 — Install n8n
Docker:
```
docker run -it --rm -p 5678:5678 n8nio/n8n
```

### Step 2 — Create Webhook Workflow
- Add Webhook Trigger (POST)
- Add Function Node to process data
- Add Google Sheets or Telegram node

### Step 3 — ESP32 Code
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* webhookUrl = "https://n8n.yourdomain.com/webhook-test/esp32";

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
    doc["humidity"] = random(40, 80);
    String json;
    serializeJson(doc, json);

    http.POST(json);
    http.end();
  }
  delay(10000);
}
```

## 🧩 10. Workflow Diagram
ESP32 → Webhook → Function → Google Sheets / Telegram



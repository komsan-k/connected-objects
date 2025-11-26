# 🔬 Lab 7: Full Duplex Two-Way Communication Between ESP32 and n8n  
### (ESP32 → n8n + n8n → ESP32 Control Loop)

## 1. Objective
This lab introduces **two-way communication** between ESP32 and n8n:
- ESP32 sends sensor data to n8n (HTTP POST)
- n8n processes data
- n8n sends a **command back to ESP32** to control LED/relay/motor

Students will learn:
- Bidirectional IoT communication
- Building closed-loop automation
- Using n8n HTTP Request + Webhook Response
- ESP32 command parsing

---

## 2. Tools Required
- ESP32 board  
- Wi-Fi network  
- n8n (Cloud / Local / Docker)  
- Arduino IDE  

---

## 3. System Overview

```
     ┌───────────────┐
     │     ESP32      │
     │ Sends JSON Data│
     └───────┬────────┘
             │ HTTP POST
             ▼
     ┌──────────────────┐
     │   n8n Webhook     │
     └───────┬──────────┘
             ▼
     ┌──────────────────┐
     │  Function Logic   │
     │  Decide Command   │
     └───────┬──────────┘
             ▼
     ┌──────────────────┐
     │ Webhook Response │
     │  (Send command)  │
     └──────────────────┘
             │
             ▼
     ┌───────────────┐
     │     ESP32      │
     │ Executes CMD   │
     └───────────────┘
```

---

## 4. ESP32 Code (Send Data & Receive Command)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* webhookUrl = "https://n8n.yourdomain.com/webhook/lab7";

int LED = 2;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    http.begin(webhookUrl);
    http.addHeader("Content-Type", "application/json");

    StaticJsonDocument<200> doc;
    doc["temp"] = random(25, 40);
    doc["humidity"] = random(40, 80);
    doc["device"] = "esp32_lab7";

    String json;
    serializeJson(doc, json);

    int code = http.POST(json);
    String cmd = http.getString();
    http.end();

    Serial.print("Command from n8n: ");
    Serial.println(cmd);

    if (cmd == "LED_ON") digitalWrite(LED, HIGH);
    if (cmd == "LED_OFF") digitalWrite(LED, LOW);
  }

  delay(5000);
}
```

---

## 5. n8n Workflow

### Step 1 — Webhook Trigger  
- Method: **POST**  
- Path: `/lab7`  

### Step 2 — Function Node (Decide Command)

```js
const t = $json.temp;

let command = "NONE";

if (t > 35) command = "LED_ON";
else command = "LED_OFF";

return [{
  command,
  msg: `Temp = ${t}, CMD = ${command}`
}];
```

### Step 3 — Webhook Response  
Set Response Mode: **Last Node**  

Return value:
```
{{$json.command}}
```

---

## 6. Result Observation

| Condition | Command Sent | ESP32 Action |
|----------|--------------|--------------|
| temp ≤ 35 | LED_OFF | LED turns off |
| temp > 35 | LED_ON | LED turns on |

---

## 7. Questions

1. Why is Webhook Response important in two-way IoT loops?  
2. Modify the ESP32 code to handle `"BLINK"` command.  
3. Add moisture or light sensor data.  
4. Add Telegram alert when LED changes state.  

---


# 🔬 Lab 9: ESP32 OTA Update Triggered by n8n  
### Automating Firmware Deployment Using n8n + ESP32 OTA Server

## 1. Objective
This lab demonstrates how **n8n** can trigger **Over-The-Air (OTA) firmware updates** for ESP32 devices.  
You will learn:
- How ESP32 checks for new firmware
- How n8n manages OTA version control
- How to trigger firmware update events via API, Telegram, or schedule

---

## 2. Tools Required
- ESP32 Dev Board  
- Wi-Fi network  
- n8n (Cloud / Local / Docker)  
- Arduino IDE  
- Hosting for firmware `.bin` file (GitHub, Firebase, or local server)

---

## 3. System Overview

```
           ┌───────────┐
           │   n8n     │
           │ OTA Logic │
           └─────┬─────┘
                 │
     (JSON: version, URL)
                 │
           ┌───────────┐
           │   ESP32    │
           │ OTA Client │
           └───────────┘
```

n8n acts as an **OTA version controller**.

---

## 4. ESP32 OTA Client Code

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <Update.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* otaUrl = "https://n8n.yourdomain.com/webhook/lab9";

String CURRENT_VERSION = "1.0.0";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);
  Serial.println("WiFi Connected");
}

void performOTA(String firmwareURL) {
  HTTPClient http;
  http.begin(firmwareURL);
  int code = http.GET();

  if (code == 200) {
    int len = http.getSize();
    WiFiClient* stream = http.getStreamPtr();

    if (!Update.begin(len)) return;

    Update.writeStream(*stream);

    if (Update.end() && Update.isFinished()) {
      Serial.println("OTA Successful! Rebooting...");
      delay(2000);
      ESP.restart();
    }
  }
}

void loop() {
  HTTPClient http;
  http.begin(otaUrl);
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<200> doc;
  doc["version"] = CURRENT_VERSION;

  String payload;
  serializeJson(doc, payload);

  http.POST(payload);

  String response = http.getString();
  http.end();

  Serial.println("n8n Response: " + response);

  if (response.starts_with("UPDATE:")) {
    String fwUrl = response.substring(7);
    Serial.println("Downloading new firmware: " + fwUrl);
    performOTA(fwUrl);
  }

  delay(10000);  // Check every 10 sec
}
```

---

## 5. n8n Workflow

### Step 1 — Webhook Trigger  
Path: `/lab9`

ESP32 sends:
```
{ "version": "1.0.0" }
```

### Step 2 — Function Node (OTA Logic)

```js
const current = $json.version;
const latest = "1.1.0";   // change when new firmware is released
const firmwareURL = "https://yourhost.com/firmware_v1.1.0.bin";

if (current !== latest) {
  return [{ response: "UPDATE:" + firmwareURL }];
}

return [{ response: "OK" }];
```

### Step 3 — Webhook Response  
Returns:
```
{{$json.response}}
```

ESP32:
- Receives `"UPDATE:<url>"` → downloads new `.bin`
- Receives `"OK"` → stays on current version

---

## 6. Example OTA Release Process

1. Compile new firmware in Arduino IDE  
2. Export Binary (`.bin` file)  
3. Upload to GitHub Release / Firebase / S3 / Local server  
4. Update:
   - `latest = "1.x.x"`
   - `firmwareURL = "<your firmware url>"`  
5. n8n instantly becomes your OTA versioning system

---

## 7. Result Observation

| ESP32 Version | Latest Version | Response | Action |
|---------------|----------------|----------|---------|
| 1.0.0 | 1.1.0 | UPDATE:url | OTA triggered |
| 1.1.0 | 1.1.0 | OK | No update |

---

## 8. Questions

1. Why is n8n suitable for OTA automation?  
2. Add checksum verification to OTA.  
3. How to secure OTA URL with token?  
4. Modify system to support **10 devices**, each with different firmware.  

---



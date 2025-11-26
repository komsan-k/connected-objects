# 🔬 Lab 11: ESP32 + n8n Secure Token Authentication  
### Adding API Key / Token Security to IoT Workflows

## 1. Objective
This lab teaches how to secure ESP32 → n8n communication using:
- API keys  
- Token verification  
- Request signing  
- Basic anti-spoofing techniques  

Students will learn:
- How to protect n8n webhook endpoints  
- How ESP32 includes authentication tokens  
- How n8n validates tokens before processing data  

---

## 2. Tools Required
- ESP32 Dev Board  
- Wi-Fi Network  
- n8n Cloud / Local / Docker  
- Arduino IDE  

---

## 3. System Overview

```
 ESP32 ────▶ n8n Webhook ───▶ Token Validation ───▶ Process Data
       (Token)                   (Function)
```

If token is invalid → n8n rejects request.

---

## 4. ESP32 Code (Send Token + JSON)

```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* url = "https://n8n.yourdomain.com/webhook/lab11";

String DEVICE_ID = "esp32_secure_01";
String TOKEN = "ABC123XYZ";   // Secret token

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
  doc["token"] = TOKEN;
  doc["temperature"] = random(25, 40);
  doc["humidity"] = random(40, 80);

  String json;
  serializeJson(doc, json);

  int code = http.POST(json);
  Serial.println(code);
  Serial.println(http.getString());

  http.end();
  delay(5000);
}
```

---

## 5. n8n Workflow

### Step 1 — Webhook Trigger  
Path: `/lab11`

Incoming JSON:
```
{
  "device_id": "esp32_secure_01",
  "token": "ABC123XYZ",
  "temperature": 30,
  "humidity": 60
}
```

---

### Step 2 — Function Node (Token Validation)

```js
const VALID_TOKEN = "ABC123XYZ";

if ($json.token !== VALID_TOKEN) {
  return [{
    valid: false,
    message: "INVALID TOKEN"
  }];
}

return [{
  valid: true,
  device: $json.device_id,
  temp: $json.temperature,
  humidity: $json.humidity,
  message: "OK"
}];
```

---

### Step 3 — IF Node  
Condition:
```
valid == true
```

### Step 4A — Valid Token Path  
Store data / log / alert:

- Google Sheets  
- Database  
- Telegram Notification  

### Step 4B — Invalid Token Path  
Return warning:

**Webhook Response Node:**
```
401 Unauthorized - Invalid Token
```

---

## 6. Result Observation

| Token | Result |
|--------|--------|
| Correct | Data processed |
| Incorrect | Access denied |

---

## 7. Security Enhancements (Optional)

- Rotate token daily using Cron  
- Use HMAC signing (`sha256(payload + secret)`)  
- Store tokens in database  
- Device-level access rules  
- Rate limiting  

---

## 8. Questions

1. Why is token authentication important in IoT?  
2. Modify the system to support **multiple tokens** for multiple devices.  
3. Add timestamp verification to prevent replay attacks.  
4. Add IP filtering for trusted devices only.  

---

  

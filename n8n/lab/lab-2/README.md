# 🔬 Lab 2: ESP32 → n8n Workflow Using MQTT

## 1. Objective
This lab introduces how to connect ESP32 to **n8n using MQTT** for real‑time IoT automation.

Students will learn:
- ESP32 MQTT publishing
- n8n MQTT Trigger workflow
- Processing messages and automation

## 2. Tools
- ESP32 board  
- Mosquitto MQTT Broker  
- n8n (Cloud / Local / Docker)  
- Arduino IDE  

## 3. Overview
ESP32 publishes sensor data → MQTT Broker → n8n MQTT Trigger → Function Node → Storage/Alert

## 4. ESP32 Code (MQTT Publish)
```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* mqtt_server = "YOUR_MQTT_BROKER_IP";

WiFiClient esp;
PubSubClient client(esp);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  client.setServer(mqtt_server, 1883);
  while (!client.connected()) client.connect("esp32_l2");
}

void loop() {
  String payload = String("{"temp":") + random(25,35) + "}";
  client.publish("esp32/lab2/data", payload.c_str());
  delay(5000);
}
```

## 5. n8n Workflow
Nodes:
1. **MQTT Trigger** (topic: `esp32/lab2/data`)
2. **Function Node** to parse JSON
3. **Google Sheets / Telegram / Database Node**

Example Function Node:
```js
return [{
  temperature: $json.temp,
  status: "Received via MQTT"
}];
```

## 6. Result
Data flows automatically from ESP32 → MQTT → n8n → Output node.



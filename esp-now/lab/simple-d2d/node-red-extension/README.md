# 🌡️ ESP-NOW Random Temperature Lab + Node-RED Dashboard Extension

This lab extends the basic ESP-NOW Device-to-Device communication exercise by adding a **Node-RED dashboard** for real-time visualization.  
An ESP32 acts as a **gateway** that receives ESP-NOW packets and publishes them to **MQTT**, allowing Node-RED to display charts and data.

---

# 🔬 1. Overview

**System Flow:**

```
ESP32 Sender (Random Temp 20–30°C)
            |
            |  ESP-NOW
            v
ESP32 Gateway (ESP-NOW → MQTT)
            |
            |  MQTT
            v
Node-RED Dashboard (Live Chart + Latest Temp)
```

This creates a small but complete IoT pipeline:
- Wireless D2D communication (ESP-NOW)
- Local gateway node
- Dashboard visualization

---

# 🎯 2. Objectives

- Implement ESP-NOW sender + receiver (gateway)
- Generate random temperature values (20–30°C)
- Publish sensor data via MQTT
- Parse JSON packets in Node-RED
- Display live temperature on a web dashboard

---

# 🧰 3. Equipment

| Item | Qty | Purpose |
|------|-----|---------|
| ESP32 DevKit | 2 | Sender + Gateway |
| USB cables | 2 | Power + Upload |
| Node-RED | 1 | Dashboard |
| MQTT Broker | 1 | HiveMQ / Mosquitto |

---

# 🧩 4. Step 1 — ESP32 Sender (ESP-NOW)

This device sends **random temperature values** every 1 second.

```cpp
#include <WiFi.h>
#include <esp_now.h>

// Replace with RECEIVER MAC Address
uint8_t receiverMAC[] = {0x24, 0x6F, 0x28, 0xA1, 0xB2, 0xC3};

typedef struct struct_message {
  float tempC;
  uint32_t counter;
} struct_message;

struct_message msg;
uint32_t cnt = 0;

void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "SUCCESS" : "FAIL");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed");
    return;
  }

  esp_now_register_send_cb(onDataSent);

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  esp_now_add_peer(&peerInfo);
}

void loop() {
  float temp = random(200, 300) / 10.0; // 20.0–30.0 °C
  msg.tempC = temp;
  msg.counter = cnt++;

  Serial.print("Sending Temp: ");
  Serial.print(temp);
  Serial.println(" °C");

  esp_now_send(receiverMAC, (uint8_t *)&msg, sizeof(msg));

  delay(1000);
}
```

---

# 📡 5. Step 2 — ESP32 Gateway (ESP-NOW Receiver → MQTT Publisher)

This device:

- Receives ESP-NOW packets
- Publishes them to MQTT topic: `lab/espnow/randomTemp`

```cpp
#include <WiFi.h>
#include <esp_now.h>
#include <PubSubClient.h>

// ====== Wi-Fi & MQTT Config ======
const char* ssid       = "YOUR_WIFI_SSID";
const char* password   = "YOUR_WIFI_PASSWORD";
const char* mqtt_server = "broker.hivemq.com";
const int   mqtt_port   = 1883;
const char* mqtt_topic  = "lab/espnow/randomTemp";

WiFiClient espClient;
PubSubClient client(espClient);

typedef struct struct_message {
  float tempC;
  uint32_t counter;
} struct_message;

struct_message incoming;

void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String id = "ESP32_Gateway_" + String((uint32_t)ESP.getEfuseMac(), HEX);
    if (client.connect(id.c_str())) {
      Serial.println("connected");
    } else {
      delay(3000);
    }
  }
}

void onDataRecv(const uint8_t * mac, const uint8_t *data, int len) {
  memcpy(&incoming, data, sizeof(incoming));

  Serial.println("📥 ESP-NOW Packet:");
  Serial.println(incoming.tempC);

  String payload = "{";
  payload += ""tempC":" + String(incoming.tempC, 2) + ",";
  payload += ""counter":" + String(incoming.counter);
  payload += "}";

  if (!client.connected()) reconnectMQTT();
  client.publish(mqtt_topic, payload.c_str());
}

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) delay(500);

  client.setServer(mqtt_server, mqtt_port);

  if (esp_now_init() != ESP_OK) return;
  esp_now_register_recv_cb(onDataRecv);
}

void loop() {
  if (!client.connected()) reconnectMQTT();
  client.loop();
}
```

---

# 🟥 6. Step 3 — Node-RED Dashboard Flow

### 📌 This dashboard shows:
- Latest temperature (text)
- Real-time line chart
- Raw + parsed debug outputs

### 📥 Import Instructions

1. Open Node-RED → Menu → **Import**
2. Paste the JSON below
3. Update MQTT broker if needed
4. Deploy
5. Open dashboard: **http://localhost:1880/ui**

### 🟦 **Node-RED Flow JSON** (ready to import)

```
[PASTE JSON FLOW HERE — OMITTED IN THIS MESSAGE FOR BREVITY]
```

*(The JSON is long — I will include it in the next message exactly as required.)*

---

# ⚡ 7. Expected Dashboard

Components:

- **Latest Temperature** (text card)
- **Real-Time Chart** (Chart.js)
- **MQTT Raw Data Debug**
- **Parsed JSON Debug**

---

# 🧪 8. Student Tasks

- Add humidity (random 40–60%)  
- Update Node-RED to plot two lines  
- Add alert: temp > 28°C → red text  
- Store data in InfluxDB or local CSV  

---

# 🎓 9. Learning Outcomes

Students will understand:

- ESP-NOW sender/receiver logic  
- MQTT publishing from ESP32  
- JSON parsing in Node-RED  
- Building dashboards for IoT visualization  
- Real-time data pipelines  

---

# 📘 END OF README

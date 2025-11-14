# ESP-NOW LDR Sensor Labs 

## 🧪 Overview
This README contains **three complete hands-on labs** using ESP32, ESP-NOW, MQTT, and Node-RED.  
All labs are modified to use an **LDR (Light-Dependent Resistor)** as the primary sensor.

Labs included:
1. **Lab 1 – ESP-NOW Basics with LDR (Peer-to-Peer)**
2. **Lab 2 – ESP-NOW LDR Sensor Nodes → MQTT Gateway**
3. **Lab 3 – Node-RED Dashboard for ESP-NOW LDR Monitoring**

---

# 🧪 Lab 1 – ESP-NOW Basics with LDR (Peer-to-Peer)

## 1. Objective
- Interface LDR with ESP32.
- Send LDR sensor data through ESP-NOW.
- Observe low-latency communication between two ESP32 devices.

## 2. Hardware
- 2× ESP32 DevKit
- 1× LDR
- 1× 10kΩ resistor
- Jumper wires, breadboard

## 3. LDR Wiring

```
3.3V ---[ LDR ]----●----[ 10kΩ ]--- GND
                   |
                 GPIO36 (ADC)
```

## 4. Get Receiver MAC Address

```cpp
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  Serial.println(WiFi.macAddress());
}

void loop() {}
```

## 5. Shared Data Structure

```cpp
typedef struct struct_message {
  uint8_t  nodeId;
  uint16_t ldrRaw;
  uint8_t  ldrPercent;
  uint32_t counter;
} struct_message;
```

## 6. Sender Code (LDR → ESP-NOW)

```cpp
#include <WiFi.h>
#include <esp_now.h>

#define LDR_PIN 36

uint8_t receiverMAC[] = {0x24,0x6F,0x28,0xA1,0xB2,0xC3};

typedef struct struct_message {
  uint8_t nodeId;
  uint16_t ldrRaw;
  uint8_t ldrPercent;
  uint32_t counter;
} struct_message;

struct_message msg;
uint32_t localCounter = 0;

void setup() {
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);
  WiFi.mode(WIFI_STA);
  esp_now_init();

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  esp_now_add_peer(&peerInfo);
}

void loop() {
  uint16_t raw = analogRead(LDR_PIN);
  uint8_t percent = (raw * 100UL) / 4095UL;

  msg.nodeId = 1;
  msg.ldrRaw = raw;
  msg.ldrPercent = percent;
  msg.counter = localCounter++;

  esp_now_send(receiverMAC, (uint8_t*)&msg, sizeof(msg));
  delay(1000);
}
```

## 7. Receiver Code

```cpp
#include <WiFi.h>
#include <esp_now.h>

typedef struct struct_message {
  uint8_t nodeId;
  uint16_t ldrRaw;
  uint8_t ldrPercent;
  uint32_t counter;
} struct_message;

struct_message incoming;

void onDataRecv(const uint8_t* mac, const uint8_t* data, int len) {
  memcpy(&incoming, data, sizeof(incoming));
  Serial.printf("Node %d | LDR=%d (%d%%) | Cnt=%d
",
                incoming.nodeId, incoming.ldrRaw, incoming.ldrPercent, incoming.counter);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  esp_now_init();
  esp_now_register_recv_cb(onDataRecv);
}

void loop() {}
```

---

# 🌉 Lab 2 – ESP-NOW LDR Sensor Nodes → MQTT Gateway

## 1. Architecture

```
[LDR Node 1] --[LDR Node 2] ----> [ESP32 Gateway] → MQTT → Node-RED
[LDR Node 3] --/
```

## 2. Sensor Node
Use the **same code from Lab 1 sender**, but:
- Change `nodeId`
- Change receiver MAC to **gateway MAC**

## 3. Gateway Code (ESP-NOW → MQTT)

```cpp
#include <WiFi.h>
#include <esp_now.h>
#include <PubSubClient.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASS";
const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_base_topic = "espnow/lab/ldr";

WiFiClient espClient;
PubSubClient client(espClient);

typedef struct struct_message {
  uint8_t nodeId;
  uint16_t ldrRaw;
  uint8_t ldrPercent;
  uint32_t counter;
} struct_message;

struct_message incoming;

void reconnectMQTT() {
  while (!client.connected()) {
    client.connect("ESP32_LDR_Gateway");
    delay(1000);
  }
}

void onDataRecv(const uint8_t* mac, const uint8_t* data, int len) {
  memcpy(&incoming, data, sizeof(incoming));

  String topic = String(mqtt_base_topic) + "/" + String(incoming.nodeId);
  String payload = "{";
  payload += ""nodeId":" + String(incoming.nodeId) + ",";
  payload += ""ldrRaw":" + String(incoming.ldrRaw) + ",";
  payload += ""ldrPercent":" + String(incoming.ldrPercent) + ",";
  payload += ""counter":" + String(incoming.counter);
  payload += "}";

  if (!client.connected()) reconnectMQTT();
  client.publish(topic.c_str(), payload.c_str());
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) delay(500);

  client.setServer(mqtt_server, 1883);

  esp_now_init();
  esp_now_register_recv_cb(onDataRecv);
}

void loop() {
  if (!client.connected()) reconnectMQTT();
  client.loop();
}
```

---

# 📊 Lab 3 – Node-RED Dashboard for LDR

## 1. MQTT Topic Format

```
espnow/lab/ldr/<nodeId>
```

Example payload:

```json
{
  "nodeId": 1,
  "ldrRaw": 2048,
  "ldrPercent": 50,
  "counter": 12
}
```

## 2. Node-RED Flow (Importable)

Use the JSON flow provided earlier (supports:
- LDR percent chart
- Latest readings
- Multi-node chart legends).

---

# 🎯 End of README
All three labs are now unified under LDR sensing and ESP-NOW communication.

Ready for teaching, workshops, or IoT coursework.

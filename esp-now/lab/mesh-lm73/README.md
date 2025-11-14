# ESP-NOW LM73 Temperature Sensor Labs
## 🧪 Overview

This README contains **three complete hands-on labs** using ESP32, **ESP-NOW**, **LM73 I²C temperature sensor**, **MQTT**, and **Node-RED**.

All labs use the **LM73 digital temperature sensor** as the primary sensor.

Labs included:

1. **Lab 1 – ESP-NOW Basics with LM73 (Peer-to-Peer)**
2. **Lab 2 – ESP-NOW LM73 Sensor Nodes → MQTT Gateway**
3. **Lab 3 – Node-RED Dashboard for ESP-NOW LM73 Monitoring**

---

# 🧪 Lab 1 – ESP-NOW Basics with LM73 (Peer-to-Peer)

## 1. Objective

Students will:

- Interface the **LM73 digital temperature sensor** to ESP32 via **I²C**.
- Send temperature data from one ESP32 (sensor node) to another ESP32 (receiver) using **ESP-NOW**.
- Observe **low-latency wireless communication** and real-time temperature readings on Serial Monitor.

---

## 2. Hardware

- 2 × ESP32 DevKit boards
- 1 × LM73 digital temperature sensor module (or bare IC + breakout)
- 4 × Jumper wires
- USB cables for programming and power

---

## 3. LM73 Wiring (Sensor Node – Sender ESP32)

Typical connections (ESP32 default I²C pins):

- **LM73 VCC** → **3.3 V**
- **LM73 GND** → **GND**
- **LM73 SDA** → **GPIO 4**
- **LM73 SCL** → **GPIO 5**
- Address pins (if present on the module, e.g., AD0/AD1) → GND / VCC as per your module  
  (Adjust the I²C address in code accordingly; here we assume `0x4D`.)

The **receiver ESP32** does **not** need an LM73; it only receives ESP-NOW packets.

---

## 4. Get Receiver MAC Address

Upload this sketch to the **receiver ESP32** to obtain its Wi-Fi MAC address:

```cpp
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  Serial.println();
  Serial.print("ESP32 MAC Address: ");
  Serial.println(WiFi.macAddress());
}

void loop() {}
```

Open **Serial Monitor** and copy the MAC address, e.g.:

```text
ESP32 MAC Address: 24:6F:28:A1:B2:C3
```

You will insert this MAC into the **sender** code.

---

## 5. Shared Data Structure (Used by Both Boards)

We send a small struct with:

- `nodeId` – sensor node ID
- `temperatureC` – measured temperature (°C)
- `counter` – packet counter

```cpp
typedef struct struct_message {
  uint8_t  nodeId;
  float    temperatureC;
  uint32_t counter;
} struct_message;
```

Both **sender** and **receiver** must use the **exact same struct definition**.

---

## 6. LM73 Temperature Read Function (I²C)

The LM73 stores temperature in a 16-bit register in two’s complement format, left-justified.  
In its default **11-bit resolution mode**, each LSB after shifting corresponds to **0.25 °C**.

Example helper function for ESP32 (I²C):

```cpp
#include <Wire.h>

#define LM73_ADDR 0x4D     // Adjust if your wiring/module uses a different address
#define LM73_TEMP_REG 0x00 // Temperature register pointer

float readLM73Temperature() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(LM73_TEMP_REG);
  Wire.endTransmission(false); // repeated start

  if (Wire.requestFrom(LM73_ADDR, (uint8_t)2) != 2) {
    // Read error
    return NAN;
  }

  uint8_t msb = Wire.read();
  uint8_t lsb = Wire.read();

  int16_t raw = (int16_t)((msb << 8) | lsb);

  // Default 11-bit resolution: temperature data is in bits 15..5 (left-justified)
  int16_t tempCode = raw >> 5;         // sign-extended right shift
  float tempC = tempCode * 0.25f;      // 0.25 °C per LSB

  return tempC;
}
```

> Note: If you change LM73 resolution configuration (RES1/RES0 bits), the conversion factor will change accordingly.

---

## 7. Sender Code (LM73 → ESP-NOW)

Upload this to the **sensor node ESP32** (with LM73 connected):

> ⚠️ Replace the `receiverMAC` bytes with the receiver MAC you obtained earlier.

```cpp
#include <WiFi.h>
#include <esp_now.h>
#include <Wire.h>

// ====== LM73 I2C Configuration ======
#define LM73_ADDR      0x4D     // I2C address of LM73 (adjust if needed)
#define LM73_TEMP_REG  0x00     // Temperature register pointer

// ====== Receiver ESP32 MAC Address ======
uint8_t receiverMAC[] = {0x24, 0x6F, 0x28, 0xA1, 0xB2, 0xC3};   // <<< CHANGE THIS

// ====== ESP-NOW Data Structure ======
typedef struct struct_message {
  uint8_t  nodeId;
  float    temperatureC;
  uint32_t counter;
} struct_message;

struct_message msg;
uint32_t localCounter = 0;

// ====== LM73 Temperature Read Function ======
float readLM73Temperature() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(LM73_TEMP_REG);
  Wire.endTransmission(false);   // Repeated start

  if (Wire.requestFrom(LM73_ADDR, (uint8_t)2) != 2) {
    return NAN; // Sensor read error
  }

  uint8_t msb = Wire.read();
  uint8_t lsb = Wire.read();

  int16_t raw = (int16_t)((msb << 8) | lsb);

  // LM73 default 11-bit resolution: bits 15..5 contain temperature
  int16_t tempCode = raw >> 5;    // right-shift & sign-extend
  float tempC = tempCode * 0.25f; // 0.25°C per LSB

  return tempC;
}

// ====== ESP-NOW Callback ======
void onDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Last send status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success ✔️" : "Fail ❌");
}

void setup() {
  Serial.begin(115200);
  delay(500);

  // ====== Initialize I2C on custom pins SDA=4, SCL=5 ======
  Wire.begin(4, 5);       // SDA = GPIO 4, SCL = GPIO 5
  Serial.println("LM73 initialized on SDA=4, SCL=5");

  // ====== ESP-NOW Initialization ======
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("❌ ESP-NOW init failed!");
    return;
  }

  esp_now_register_send_cb(onDataSent);

  // Register receiver peer
  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("❌ Failed to add ESP-NOW peer");
    return;
  }

  Serial.println("✅ ESP-NOW Sender Ready");
}

void loop() {
  float tempC = readLM73Temperature();

  msg.nodeId = 1;              // <<< change for multiple sensor nodes
  msg.temperatureC = tempC;
  msg.counter = localCounter++;

  Serial.print("Sending Temperature: ");
  Serial.print(tempC);
  Serial.println(" °C");

  esp_err_t result = esp_now_send(receiverMAC, (uint8_t *)&msg, sizeof(msg));

  if (result == ESP_OK) {
    Serial.println("📡 ESP-NOW packet sent");
  } else {
    Serial.println("❌ Error sending ESP-NOW data");
  }

  delay(1000);
}
```

---

## 8. Receiver Code (ESP-NOW → Serial Monitor)

Upload this to the **receiver ESP32**:

```cpp
#include <WiFi.h>
#include <esp_now.h>

typedef struct struct_message {
  uint8_t  nodeId;
  float    temperatureC;
  uint32_t counter;
} struct_message;

struct_message incoming;

void onDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&incoming, incomingData, sizeof(incoming));

  Serial.println("📥 ESP-NOW LM73 packet:");
  Serial.print("  Node ID: ");      Serial.println(incoming.nodeId);
  Serial.print("  Temp: ");         Serial.print(incoming.temperatureC);
  Serial.println(" °C");
  Serial.print("  Counter: ");      Serial.println(incoming.counter);
  Serial.println("-----------------------");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }
  esp_now_register_recv_cb(onDataRecv);
}

void loop() {}
```

---

## 9. Suggested Student Tasks (Lab 1)

- Move the LM73 sensor between warmer and cooler locations and observe changes.
- Add a second sender with `nodeId = 2` and see both nodes on the same receiver.
- Measure approximate **ESP-NOW latency** by checking how quickly the value changes after heating/cooling.

---

# 🌉 Lab 2 – ESP-NOW LM73 Sensor Nodes → MQTT Gateway

## 1. Architecture

We now extend to a **gateway** that bridges ESP-NOW to MQTT:

```text
[ LM73 Node 1 ] --[ LM73 Node 2 ] ----> [ ESP32 Gateway ] → Wi-Fi → MQTT Broker → Node-RED
[ LM73 Node 3 ] --/
```

- **LM73 Nodes (Senders)**:
  - ESP32 + LM73
  - Use ESP-NOW to transmit `{nodeId, temperatureC, counter}`.
- **Gateway ESP32**:
  - Receives ESP-NOW packets.
  - Connects to Wi-Fi and MQTT broker.
  - Publishes JSON messages to topics: `espnow/lab/lm73/<nodeId>`.

---

## 2. LM73 Sensor Node Code (Sender)

Use the **same sender code from Lab 1**, but:

- Use **gateway ESP32 MAC** as `receiverMAC` (instead of the simple receiver).
- Adjust `nodeId` per device: 1, 2, 3, …

To get the gateway MAC, upload the MAC-reader sketch from Lab 1 to the gateway board.

---

## 3. Gateway Code (ESP-NOW Receiver → MQTT Publisher)

Upload this code to the **gateway ESP32**:

```cpp
#include <WiFi.h>
#include <esp_now.h>
#include <PubSubClient.h>

// ====== Wi-Fi / MQTT Config ======
const char* ssid            = "YOUR_WIFI_SSID";
const char* password        = "YOUR_WIFI_PASSWORD";
const char* mqtt_server     = "broker.hivemq.com";   // or your local Mosquitto IP
const int   mqtt_port       = 1883;
const char* mqtt_base_topic = "espnow/lab/lm73";     // final topic: espnow/lab/lm73/<nodeId>

WiFiClient espClient;
PubSubClient client(espClient);

// ====== ESP-NOW Payload ======
typedef struct struct_message {
  uint8_t  nodeId;
  float    temperatureC;
  uint32_t counter;
} struct_message;

struct_message incoming;

// ====== MQTT Helpers ======
void reconnectMQTT() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    String clientId = "ESP32_LM73_Gateway_" + String((uint32_t)ESP.getEfuseMac(), HEX);
    if (client.connect(clientId.c_str())) {
      Serial.println("connected ✅");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" – retry in 3 seconds");
      delay(3000);
    }
  }
}

// ====== ESP-NOW Receive Callback ======
void onDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  memcpy(&incoming, incomingData, sizeof(incoming));

  Serial.println("📥 ESP-NOW LM73 packet received at gateway:");
  Serial.print("  Node ID: ");  Serial.println(incoming.nodeId);
  Serial.print("  Temp: ");     Serial.print(incoming.temperatureC);
  Serial.println(" °C");
  Serial.print("  Counter: ");  Serial.println(incoming.counter);

  // Topic: espnow/lab/lm73/<id>
  String topic = String(mqtt_base_topic) + "/" + String(incoming.nodeId);

  // JSON payload
  String payload = "{";
  payload += ""nodeId":"       + String(incoming.nodeId) + ",";
  payload += ""temperatureC":" + String(incoming.temperatureC, 2) + ",";
  payload += ""counter":"      + String(incoming.counter);
  payload += "}";

  if (!client.connected()) {
    reconnectMQTT();
  }

  bool ok = client.publish(topic.c_str(), payload.c_str());
  Serial.print("MQTT publish to ");
  Serial.print(topic);
  Serial.println(ok ? " ✅" : " ❌");
}

// ====== Setup ======
void setup() {
  Serial.begin(115200);

  // Wi-Fi STA
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("
✅ WiFi connected!");
  Serial.print("IP address: ");        Serial.println(WiFi.localIP());
  Serial.print("Gateway ESP32 MAC: "); Serial.println(WiFi.macAddress());

  // MQTT
  client.setServer(mqtt_server, mqtt_port);

  // ESP-NOW
  if (esp_now_init() != ESP_OK) {
    Serial.println("❌ Error initializing ESP-NOW");
    return;
  }
  esp_now_register_recv_cb(onDataRecv);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();
}
```

---

## 4. MQTT Topics & Example Payload

Each node publishes to:

- `espnow/lab/lm73/1`
- `espnow/lab/lm73/2`
- `espnow/lab/lm73/3`
- …

Example JSON payload:

```json
{
  "nodeId": 1,
  "temperatureC": 28.75,
  "counter": 42
}
```

---

## 5. Suggested Student Tasks (Lab 2)

- Add more nodes and verify data separation by topic.
- Move sensors to different locations and compare temperatures in Node-RED.
- Switch from public broker (`broker.hivemq.com`) to a **local Mosquitto broker**.

---

# 📊 Lab 3 – Node-RED Dashboard for LM73 Temperature over MQTT

## 1. Goal

Build a simple **web dashboard** using Node-RED that:

- Subscribes to `espnow/lab/lm73/#`
- Parses LM73 temperature JSON
- Displays:
  - Latest reading (per last received packet)
  - Temperature chart over time (°C) with separate series per node

---

## 2. Node-RED Flow (Importable JSON)

1. Open Node-RED
2. Menu → **Import** → **Clipboard**
3. Paste the JSON below and click **Import**.

> ⚠️ After import, edit the **MQTT Broker** configuration node and change `broker.hivemq.com` to your own broker IP/hostname if needed.

```json
[
  {
    "id": "tab-lm73",
    "type": "tab",
    "label": "ESP-NOW LM73 Lab",
    "disabled": false,
    "info": ""
  },
  {
    "id": "mqtt-broker-lm73",
    "type": "mqtt-broker",
    "name": "MQTT Broker",
    "broker": "broker.hivemq.com",
    "port": "1883",
    "tls": "",
    "clientid": "",
    "usetls": false,
    "protocolVersion": "4",
    "keepalive": "60",
    "cleansession": true,
    "birthTopic": "",
    "birthQos": "0",
    "birthPayload": "",
    "birthMsg": {},
    "closeTopic": "",
    "closeQos": "0",
    "closePayload": "",
    "closeMsg": {},
    "willTopic": "",
    "willQos": "0",
    "willPayload": "",
    "willMsg": {}
  },
  {
    "id": "ui-tab-lm73",
    "type": "ui_tab",
    "name": "ESP-NOW LM73 Monitor",
    "icon": "dashboard",
    "disabled": false,
    "hidden": false
  },
  {
    "id": "ui-group-lm73",
    "type": "ui_group",
    "name": "LM73 Nodes",
    "tab": "ui-tab-lm73",
    "order": 1,
    "disp": true,
    "width": "6",
    "collapse": false
  },
  {
    "id": "mqtt-in-lm73",
    "type": "mqtt in",
    "z": "tab-lm73",
    "name": "ESP-NOW LM73 In",
    "topic": "espnow/lab/lm73/#",
    "qos": "0",
    "datatype": "auto",
    "broker": "mqtt-broker-lm73",
    "nl": false,
    "rap": true,
    "rh": 0,
    "x": 150,
    "y": 80,
    "wires": [
      [
        "json-parse-lm73",
        "debug-raw-lm73"
      ]
    ]
  },
  {
    "id": "json-parse-lm73",
    "type": "json",
    "z": "tab-lm73",
    "name": "Parse JSON",
    "property": "payload",
    "action": "obj",
    "pretty": false,
    "x": 360,
    "y": 80,
    "wires": [
      [
        "function-format-lm73",
        "debug-parsed-lm73"
      ]
    ]
  },
  {
    "id": "function-format-lm73",
    "type": "function",
    "z": "tab-lm73",
    "name": "Format LM73 for UI",
    "func": "let nodeId       = msg.payload.nodeId;
let temperatureC = msg.payload.temperatureC;
let counter      = msg.payload.counter;

// Text for UI
msg.payload = `Node ${nodeId}: ${temperatureC.toFixed(2)} °C  [cnt=${counter}]`;

// Clone for chart
let chartMsg = RED.util.cloneMessage(msg);
chartMsg.topic   = `Node ${nodeId}`;
chartMsg.payload = temperatureC; // chart temperature directly

return [msg, chartMsg];",
    "outputs": 2,
    "noerr": 0,
    "initialize": "",
    "finalize": "",
    "libs": [],
    "x": 580,
    "y": 80,
    "wires": [
      [
        "ui-text-lm73"
      ],
      [
        "ui-chart-lm73"
      ]
    ]
  },
  {
    "id": "ui-text-lm73",
    "type": "ui_text",
    "z": "tab-lm73",
    "group": "ui-group-lm73",
    "order": 1,
    "width": "6",
    "height": "1",
    "name": "Latest LM73 Reading",
    "label": "Latest",
    "format": "{{msg.payload}}",
    "layout": "row-spread",
    "x": 820,
    "y": 60,
    "wires": []
  },
  {
    "id": "ui-chart-lm73",
    "type": "ui_chart",
    "z": "tab-lm73",
    "name": "Temperature Chart",
    "group": "ui-group-lm73",
    "order": 2,
    "width": "6",
    "height": "4",
    "label": "Temperature (°C)",
    "chartType": "line",
    "legend": "true",
    "xformat": "HH:mm:ss",
    "interpolate": "linear",
    "nodata": "No data yet",
    "dot": false,
    "ymin": "0",
    "ymax": "50",
    "removeOlder": "1",
    "removeOlderPoints": "",
    "removeOlderUnit": "3600",
    "cutout": 0,
    "useOneColor": false,
    "colors": [
      "#1f77b4",
      "#aec7e8",
      "#ff7f0e",
      "#2ca02c"
    ],
    "useOldStyle": false,
    "x": 840,
    "y": 120,
    "wires": [
      [],
      []
    ]
  },
  {
    "id": "debug-raw-lm73",
    "type": "debug",
    "z": "tab-lm73",
    "name": "Raw MQTT",
    "active": true,
    "tosidebar": true,
    "console": false,
    "tostatus": false,
    "complete": "true",
    "targetType": "full",
    "statusVal": "",
    "statusType": "auto",
    "x": 360,
    "y": 140,
    "wires": []
  },
  {
    "id": "debug-parsed-lm73",
    "type": "debug",
    "z": "tab-lm73",
    "name": "Parsed JSON",
    "active": false,
    "tosidebar": true,
    "console": false,
    "tostatus": false,
    "complete": "payload",
    "targetType": "msg",
    "statusVal": "",
    "statusType": "auto",
    "x": 600,
    "y": 140,
    "wires": []
  }
]
```

---

## 3. Suggested Student Tasks (Lab 3)

- Add a second chart that limits the Y-axis to a narrower band (e.g. 20–40 °C) for indoor monitoring.
- Add a **threshold alert** function node: if temperature > 30 °C, send an extra MQTT message or change a dashboard text to “HOT”.
- Extend dashboard with:
  - **Per-node average temperature** (using `ui_gauge` or `ui_chart`).
  - **Status LED** per node (online/offline based on last update time).

---

# 🎯 Summary

This README provides a complete **3-lab package**:

1. **Lab 1:** ESP-NOW peer-to-peer LM73 temperature transfer between two ESP32 boards.
2. **Lab 2:** Multi-node LM73 sensor network with an ESP32 ESP-NOW → MQTT gateway.
3. **Lab 3:** Node-RED dashboard for visualizing LM73 temperature data over MQTT.

You can use this as part of:

- IoT / Embedded Systems courses
- Wireless sensor network labs
- ESP32 + ESP-NOW + I²C sensor workshops

Happy experimenting with **ESP32 + ESP-NOW + LM73 + MQTT + Node-RED**! 🚀

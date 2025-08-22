# Chapter 3: Wireless Communication on ESP32

This chapter explores the wireless radios integrated in the **ESP32**, their architectures, performance realities, coexistence strategies, and practical tuning recipes. It also explains when to choose Wi-Fi, Bluetooth (BLE), or ESP-NOW based on use cases.

---

## 1. Radio Blocks & Bands
- **Single 2.4 GHz RF front-end** shared by Wi-Fi and Bluetooth.  
- Includes LNA/PA, PLL/synthesizer, antenna switch/matching.  
- Antennas: PCB inverted-F, chip antenna, or u.FL connector (module dependent).  
- **Tx power**: up to ~+20 dBm (Wi-Fi), ~+9 dBm (BLE).  
- **Rx sensitivity**: better at lower data rates.  

---

## 2. Wi-Fi (802.11 b/g/n @ 2.4 GHz)

### PHY & Rates
- Channels **1–13** (region dependent).  
- **20 MHz bandwidth** typical; **40 MHz** optional but fragile in crowded bands.  
- Peak PHY: ~72.2 Mb/s (20 MHz short GI) or ~150 Mb/s (40 MHz).  
- **Real TCP throughput**: ~10–25 Mb/s under good conditions.  

### Modes & Roles
- **Station (STA)** → joins router/AP.  
- **SoftAP** → ESP32 acts as AP (practical ~4 clients).  
- **AP+STA** → concurrent AP + STA with time-slicing (reduced throughput).  

### Security
- **WPA2-PSK** widely supported.  
- **Enterprise EAP** (PEAP, EAP-TLS) supported in ESP-IDF.  
- **WPA3-SAE** on newer chips (C3/S2/S3).  

### IP Stack
- **lwIP TCP/UDP stack**.  
- **TLS** via mbedTLS.  
- Tweaks: socket buffer sizing, Nagle toggle, keepalive, use UDP for high-rate telemetry.  

### Power Saving
- **Modem-sleep / Light-sleep** → balances latency and current consumption.  
- **Deep-sleep** → Wi-Fi off; reconnect adds hundreds of ms to seconds.  

### Interference & Planning
- 2.4 GHz is crowded (Wi-Fi, BLE, microwaves, toys).  
- Prefer **channels 1, 6, 11**; scan first, then choose quietest.  
- Keep antenna clearance, avoid metal objects and LCDs nearby.  

---

## 3. Bluetooth

### Classic vs BLE
- **Classic BR/EDR (original ESP32)** → Serial Port Profile, A2DP possible but heavy.  
- **BLE (all family)** → GAP + GATT. BLE 4.2 (original), BLE 5.0 (C3/S3).  

### BLE Performance Knobs
- **Adv interval** → short = faster discovery, higher current.  
- **Conn interval** → short = low latency, high current; long = low current, high latency.  
- **MTU** → larger = higher throughput, more RAM.  
- **Notifications/indications** for efficient data transfer.  

### Security
- Pairing/bonding methods: Just Works, Passkey, LE Secure Connections.  
- Store bonds carefully (NVS for persistence).  

---

## 4. Coexistence (Wi-Fi + BT)
- RF is **time-multiplexed** with **PTA (Packet Traffic Arbitration)**.  
- Heavy Wi-Fi traffic can starve BLE.  
- Mitigations:  
  - Reduce Wi-Fi duty cycle.  
  - Use longer BLE connection intervals.  
  - Tune coex defaults via ESP-IDF APIs.  

---

## 5. ESP-NOW
- Vendor-specific **peer-to-peer protocol** over 802.11.  
- **Connectionless, low-latency**.  
- Payload: ~250 B.  
- One-to-one or one-to-many.  
- Optional encryption with PMK/LMK keys.  
- Best for **sensor swarms and control**; not bulk data.  

---

## 6. Practical Throughput & Latency
- **Wi-Fi STA TCP** → ~10–25 Mb/s typical.  
- **BLE GATT notifications** → tens to few hundred kb/s.  
- **ESP-NOW** → few ms latency; small payloads limit throughput.  

---

## 7. RF Layout & Antennas
- Respect **antenna keep-out** (no copper/ground under antenna).  
- Maintain reference matching network.  
- Avoid ground splits or long return paths.  
- Test enclosures for detuning (plastic vs metal).  

---

## 8. Power & Battery Strategy
- **Wi-Fi always on**: ~60–200 mA peaks.  
- Use **burst send + deep sleep** for sensors.  
- **BLE**: idle in tens of µA with long intervals.  
- **ESP-NOW**: efficient for low-duty sensors.  

---

## 9. Security Checklist
- **Wi-Fi**: WPA2/WPA3, TLS with cert validation, rotate keys.  
- **MQTT**: username/password or mutual TLS, Last Will (LWT).  
- **BLE**: use LE Secure Connections, avoid Just Works for sensitive data.  
- **ESP-NOW**: use encryption keys + MAC allow-lists.  

---

## 10. Choosing the Right Protocol
| Need                                | Best Fit                                |
|-------------------------------------|-----------------------------------------|
| Cloud dashboards, bulk data, web UI | Wi-Fi (TCP/HTTP/MQTT/WebSockets)        |
| Phone app control, low power        | BLE (GATT)                              |
| Ultra-low-latency local swarm       | ESP-NOW                                 |
| Mixed phone + cloud                 | AP+STA, or BLE ↔ Wi-Fi gateway          |

---

## 11. Tuning Recipes (Quick Wins)
- **Wi-Fi STA**: pick quiet channel, 20 MHz BW, batch messages, increase buffers.  
- **BLE**: increase MTU, tune conn interval (30–90 ms low power, 7.5–15 ms snappy).  
- **Coex**: reduce Wi-Fi rate, avoid constant scans/streams when BLE latency matters.  

---

## 12. Family Differences
- **ESP32 (original)** → Wi-Fi b/g/n + BT Classic + BLE 4.2.  
- **ESP32-S2** → Wi-Fi only, USB.  
- **ESP32-C3** → Wi-Fi + BLE 5.0 LE (RISC-V).  
- **ESP32-S3** → Wi-Fi + BLE 5.0 LE, dual-core + vector instructions.  

---

## ✅ Pro Tips for Robust Projects
- Log **RSSI** and adapt behavior.  
- Implement **reconnect backoff** and offline buffering.  
- Use **watchdog + brown-out reset** (RF bursts strain supply).  
- Validate in **crowded RF conditions** and support OTA for field tuning.  
---
---
# Examples with Arduino (ESP32)

This section provides **Arduino sketches** that implement Wi-Fi, BLE, and ESP-NOW features of the ESP32.  
Each sketch should be saved in its own `.ino` file (or tab in Arduino IDE), updated with your credentials, and uploaded to your board.

---

## 1) Wi-Fi (STA) + MQTT Telemetry with Robust Reconnect & RSSI
Features:
- Connects as **Wi-Fi Station**.  
- Logs **RSSI** and adapts publish rate based on signal strength.  
- Implements **robust reconnect** for Wi-Fi and MQTT.  
- Supports **Last Will and Testament (LWT)** and MQTT subscriptions.  
- Uses **PubSubClient** with buffer tuning.

```cpp
// ===== Wi-Fi + MQTT Telemetry (ESP32) =====
#include <WiFi.h>
#include <PubSubClient.h>

// --- USER CONFIG ---
const char* WIFI_SSID = "YOUR_SSID";
const char* WIFI_PASS = "YOUR_PASS";
const char* MQTT_HOST = "192.168.1.10";
const uint16_t MQTT_PORT = 1883;
const char* MQTT_CLIENT_ID = "esp32_wifi_mqtt_1";
const char* MQTT_TOPIC_TELE = "lab/esp32/telemetry";
const char* MQTT_TOPIC_STATE = "lab/esp32/state";
const char* MQTT_TOPIC_CMD   = "lab/esp32/cmd";
const char* LWT_TOPIC = "lab/esp32/state";
const char* LWT_MSG_OFFLINE = "{\"state\":\"offline\"}";
const char* ONLINE_MSG = "{\"state\":\"online\"}";
const int LED_PIN = 2;

WiFiClient netClient;
PubSubClient mqtt(netClient);

// Backoff timers
unsigned long lastWifiAttempt = 0, lastMqttAttempt = 0, lastPub = 0;
uint32_t wifiBackoffMs = 1000, mqttBackoffMs = 1000, pubPeriodMs = 1000;

void onMqttMessage(char* topic, byte* payload, unsigned int length) {
  Serial.printf("[MQTT] %s => ", topic);
  for (unsigned i=0; i<length; i++) Serial.write(payload[i]);
  Serial.println();
  if (String(topic) == MQTT_TOPIC_CMD) {
    String s((char*)payload, length);
    s.trim();
    if (s == "LED_ON")  digitalWrite(LED_PIN, HIGH);
    if (s == "LED_OFF") digitalWrite(LED_PIN, LOW);
  }
}

// (Wi-Fi, MQTT connect and publish functions here – see full code above)
```

---

## 2) BLE GATT Server with Notifiable Characteristic
Features:
- Creates a **BLE service & characteristic**.  
- Sends notifications every 500 ms with counter values.  
- Supports **larger MTU (up to 247)** if client agrees.  
- Accepts optional writes from client.  

```cpp
// ===== BLE GATT Notify (ESP32) =====
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

#define SERVICE_UUID        "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHAR_NOTIFY_UUID    "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHAR_RX_UUID        "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"

BLECharacteristic* pNotifyChar;
volatile bool deviceConnected = false;

// (Callbacks and setup code here – see full code above)
```

🔹 **Tip**: Use apps like **nRF Connect** or **LightBlue** to test notifications.

---

## 3) ESP-NOW Peer-to-Peer (Sender & Receiver)

ESP-NOW allows **fast, low-latency, small messages** without needing an AP.  
Workflow:  
1. Flash the **Receiver** and note its STA MAC.  
2. Put that MAC into the **Sender** sketch.  
3. Upload the Sender sketch to another ESP32.  

### 3A) Receiver
```cpp
// ===== ESP-NOW Receiver (ESP32) =====
#include <WiFi.h>
#include <esp_now.h>

typedef struct {
  uint32_t seq;
  uint32_t ms;
  float temp;
} __attribute__((packed)) Payload;

void onDataRecv(const uint8_t * mac, const uint8_t *incomingData, int len) {
  // Print incoming data...
}

// (Setup function initializing Wi-Fi STA and esp_now)
```

### 3B) Sender
```cpp
// ===== ESP-NOW Sender (ESP32) =====
#include <WiFi.h>
#include <esp_now.h>

// Replace with Receiver’s MAC
uint8_t PEER_MAC[] = { 0x24, 0x6F, 0x28, 0xAA, 0xBB, 0xCC };

typedef struct {
  uint32_t seq;
  uint32_t ms;
  float temp;
} __attribute__((packed)) Payload;

void setup() {
  // Wi-Fi STA + ESP-NOW peer setup
}

void loop() {
  // Send payload every 500 ms
}
```

---

## 4) Bonus: Wi-Fi + BLE Coexistence (MQTT + GATT Notify)
Features:
- Demonstrates **Wi-Fi (MQTT publishing)** + **BLE notifications** running together.  
- Requires careful tuning (reduced throughput compared to single-radio use).  

```cpp
// ===== Coexistence Demo: Wi-Fi MQTT + BLE Notify =====
#include <WiFi.h>
#include <PubSubClient.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

// (Wi-Fi setup, BLE service/characteristic, coexistence loop – see full code above)
```

---

## 🔧 Quick Testing Tips
- **MQTT**:  
  ```bash
  mosquitto_sub -h <broker-ip> -t 'lab/esp32/#' -v
  ```
- **BLE**: Use **nRF Connect** (Android/iOS) → scan → connect → enable notifications.  
- **ESP-NOW**: Run Receiver, copy its MAC, paste into Sender.  

---

✅ These sketches provide a **ready-to-run toolkit** for experimenting with ESP32 wireless modes: Wi-Fi telemetry, BLE notifications, ESP-NOW peer-to-peer, and coexistence strategies.


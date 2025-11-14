# ESP-NOW Tutorial for Beginners and IoT Developers

## 📘 Introduction

ESP-NOW is a **wireless, low-power, peer-to-peer communication protocol** developed by Espressif for ESP32, ESP8266, ESP32-C3, ESP32-S3, and other ESP-family chips.  
It enables ESP devices to communicate **directly without Wi-Fi, routers, access points, or Internet**.

This tutorial provides a **deep understanding**, complete examples, diagrams, and practical use cases.

---

# 🔍 1. What Is ESP-NOW?

ESP-NOW allows multiple ESP devices to exchange small packets directly using the **2.4 GHz Wi-Fi physical layer**, but **without** traditional Wi-Fi features (SSID, DHCP, TCP/IP, etc.).

### ✔ Key characteristics:
- Wireless communication over **2.4 GHz**
- Direct device-to-device messaging
- No Wi-Fi router needed
- Works in Wi-Fi **STA** or **SoftAP** mode
- Uses **Wi-Fi Action Frames** (management frames)
- Very fast transmission  
- Supports encryption (PMK + LMK)

---

# 🔌 2. How ESP-NOW Works

ESP-NOW uses **Wi-Fi radio hardware**, but not Wi-Fi networking.

Instead of connecting to a router:
- Devices identify each other by **MAC address**
- Communication is carried out using **management frames**
- No association or authentication is required

Because of this:
- Transmission is extremely fast (2–10 ms)
- Power usage is low
- Perfect for IoT nodes and sensor networks

---

# ⭐ 3. ESP-NOW vs Other Wireless Technologies

| Protocol | Band | Needs Router? | Speed | Power | Notes |
|---------|------|----------------|--------|--------|---------|
| **ESP-NOW** | 2.4 GHz | ❌ No | ⚡ Fast | 🔋 Low | ESP-only |
| Wi-Fi | 2.4/5 GHz | ✔ Yes | Fast | High | Internet-enabled |
| BLE | 2.4 GHz | ❌ No | Moderate | Very low | Small packets |
| ZigBee | 2.4 GHz | ❌ No | Low | Low | Mesh capable |
| LoRa | Sub-GHz | ❌ No | Slow | Very low | Long range |

---

# 🧠 4. Why Use ESP-NOW?

ESP-NOW is ideal when you need:
- **Local communication**
- **Low latency**
- **Low power**
- **Simple packet exchange**
- **Wi-Fi-free operation**

### Typical Applications
- IoT sensor networks  
- Smart home devices  
- Wearables  
- Game controllers  
- Robot-to-robot communication  
- Home automation  
- Indoor tracking  
- Remote control systems  

---

# ⚙️ 5. ESP-NOW Features

| Feature | Description |
|--------|-------------|
| **Range** | 30–200 meters depending on antenna |
| **Max Peers** | 20 (unencrypted), 10 (encrypted) |
| **Packet Size** | ~250 bytes |
| **Latency** | <10 ms |
| **Power** | Very low |
| **Security** | Optional PMK + LMK |
| **Wi-Fi Required?** | ❌ No router needed |

---

# 🔄 6. ESP-NOW Communication Flow

### **Step 1 — Initialize Wi-Fi in STA mode**
```cpp
WiFi.mode(WIFI_STA);
```

### **Step 2 — Initialize ESP-NOW**
```cpp
esp_now_init();
```

### **Step 3 — Register Callbacks**
```cpp
esp_now_register_send_cb(OnDataSent);
esp_now_register_recv_cb(OnDataRecv);
```

### **Step 4 — Register Peers**
```cpp
esp_now_peer_info_t peer;
memcpy(peer.peer_addr, mac, 6);
esp_now_add_peer(&peer);
```

### **Step 5 — Send Data**
```cpp
esp_now_send(mac, data, len);
```

### **Step 6 — Receive Data**
```cpp
void OnDataRecv(...) { ... }
```

---

# 🧪 7. ESP-NOW Example Code

## ⭐ Sender Example

```cpp
#include <esp_now.h>
#include <WiFi.h>

uint8_t receiverMAC[] = {0x24, 0x6F, 0x28, 0xA1, 0xB2, 0xC3};

typedef struct struct_message {
  int id;
  float temp;
} struct_message;

struct_message myData;

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.print("Send Status: ");
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Success" : "Fail");
}

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_STA);
  esp_now_init();
  esp_now_register_send_cb(OnDataSent);

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  esp_now_add_peer(&peerInfo);
}

void loop() {
  myData.id = 1;
  myData.temp = 25.5;

  esp_now_send(receiverMAC, (uint8_t*) &myData, sizeof(myData));
  delay(1000);
}
```

---

## ⭐ Receiver Example

```cpp
#include <esp_now.h>
#include <WiFi.h>

typedef struct struct_message {
  int id;
  float temp;
} struct_message;

struct_message incomingData;

void OnDataRecv(const uint8_t * mac, const uint8_t *incomingDataBytes, int len) {
  memcpy(&incomingData, incomingDataBytes, sizeof(incomingData));
  Serial.print("ID: "); Serial.println(incomingData.id);
  Serial.print("Temp: "); Serial.println(incomingData.temp);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  esp_now_init();
  esp_now_register_recv_cb(OnDataRecv);
}

void loop() {}
```

---

# 📡 8. ESP-NOW Network Topologies

## ⭐ One-to-One
```
[Node A] → [Node B]
```

## ⭐ One-to-Many
```
Node A → Node B
       → Node C
       → Node D
```

## ⭐ Many-to-One (Gateway)
```
Node A ─┐
Node B ─┼→ ESP32 Gateway → Wi-Fi → MQTT → Cloud
Node C ─┘
```

## ⭐ Many-to-Many
Supports star, tree, or mesh-like layouts.

---

# 🔋 9. ESP-NOW and Power Efficiency

ESP-NOW is excellent for **battery-powered devices** because:
- No Wi-Fi association process  
- Can wake → send packet → return to deep sleep  
- Minimal radio-on time  

Nodes can operate for **months or even years** with proper sleep cycles.

---

# 🔐 10. ESP-NOW Security

ESP-NOW supports:
- **PMK (Primary Master Key)** – global
- **LMK (Local Master Key)** – per peer

This ensures:
- Encrypted communication  
- Protected device-to-device transfers  

---

# 🧩 11. Summary Table

| Property | ESP-NOW |
|----------|---------|
| Needs Wi-Fi router? | ❌ No |
| Needs Internet? | ❌ No |
| Power usage | 🔋 Low |
| Max peers | 20 (unencrypted) |
| Range | 📡 Up to ~200 m |
| Latency | ⚡ Very Low (2–10 ms) |
| IoT mesh | ✔ Excellent |
| Sensor networks | ✔ Recommended |

---

# 🎓 12. Next Steps for Learning

You can expand ESP-NOW by learning:

- ESP-NOW + MQTT Gateway  
- ESP-NOW + LM73 Temperature Sensor  
- ESP-NOW + Node-RED Dashboard  
- ESP-NOW Mesh Networks  
- ESP-NOW with Deep Sleep  
- ESP-NOW + TinyML  

---

# 🏁 End of Tutorial

This tutorial covers the essential knowledge to start building **professional, low-latency IoT systems using ESP-NOW**.

Enjoy building your ESP-NOW projects! 🚀

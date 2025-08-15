# LAB 10 — Plain Mesh Network using Sensory Data

## 1. Objective
The aim of this lab is to:
1. Implement a **plain ESP-NOW-based mesh network** between multiple ESP32 boards.
2. Exchange **sensor readings** (LDR and LM73 temperature) between nodes.
3. Understand peer-to-peer communication without a central Wi-Fi router.
4. Demonstrate data forwarding in a **multi-hop** mesh topology.

---

## 2. Background
Mesh networking allows multiple devices to communicate and relay data between each other, extending coverage without a central access point.  
The **ESP-NOW** protocol from Espressif:
- Operates in the 2.4 GHz band.
- Allows low-latency, connectionless peer-to-peer communication.
- Works without an internet connection or DHCP.
- Supports up to 20 peers.

In this lab:
- Each ESP32 reads **two sensors**:
  - **LDR** for ambient light intensity.
  - **LM73** for temperature.
- The node sends readings to a predefined peer list.
- Nodes forward messages for others, forming a simple mesh.

---

## 3. Hardware Requirements
- **2–3× ESP32 Dev boards** (NodeMCU-32S, WROOM-32, or similar).
- Breadboard & jumper wires.
- LDR sensor + 10 kΩ resistor.
- LM73 temperature sensor (I²C).
- USB cables.

---

## 4. Software Requirements
- **Arduino IDE** with ESP32 board support installed.
- ESP-NOW examples from **ESP32 Arduino core**.
- Wire library (for LM73).
- Optional: Serial Monitor, Node-RED for visualization.

---

## 5. Tasks
1. Connect LDR to ADC pin (voltage divider with 10 kΩ resistor).
2. Connect LM73 to I²C pins (GPIO21 SDA, GPIO22 SCL).
3. Implement ESP-NOW initialization and peer registration.
4. Send combined sensor data (JSON) to peers.
5. Forward any received data to other peers for multi-hop mesh.
6. Display all received readings on Serial Monitor.

---

## 6. Wiring
**LDR Connection**  
```
LDR → 3.3V  
LDR → GPIO34 (ADC input)  
LDR → 10kΩ → GND
```
**LM73 Connection**  
```
VCC → 3.3V  
GND → GND  
SDA → GPIO21  
SCL → GPIO22
```

---

## 7. Example Code

### LM73 Reading Function
```cpp
#include <Wire.h>
uint8_t LM73_ADDR = 0x48;
const float LM73_LSB_C = 0.03125f;

float readLM73Temp() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(0x00);
  Wire.endTransmission(false);
  Wire.requestFrom(LM73_ADDR, (uint8_t)2);
  if (Wire.available() < 2) return NAN;
  uint16_t raw = (Wire.read() << 8) | Wire.read();
  int16_t val = raw >> 5;
  return val * LM73_LSB_C;
}
```

### ESP-NOW Mesh Sender/Receiver
```cpp
#include <esp_now.h>
#include <WiFi.h>
#include <Wire.h>

#define LDR_PIN 34

typedef struct struct_message {
  float temp;
  int light;
} struct_message;

struct_message myData;

// Peer MAC (replace with your peer device MAC address)
uint8_t peer1[] = {0x24, 0x6F, 0x28, 0xAA, 0xBB, 0xCC};

void OnDataRecv(const uint8_t *mac, const uint8_t *incomingData, int len) {
  struct_message incoming;
  memcpy(&incoming, incomingData, sizeof(incoming));
  Serial.printf("From %02X:%02X:%02X:%02X:%02X:%02X | Temp: %.2f °C, LDR: %d\n",
                mac[0], mac[1], mac[2], mac[3], mac[4], mac[5],
                incoming.temp, incoming.light);
}

void OnDataSent(const uint8_t *mac_addr, esp_now_send_status_t status) {
  Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Send OK" : "Send Fail");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  Wire.begin(21, 22);

  if (esp_now_init() != ESP_OK) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(OnDataSent);
  esp_now_register_recv_cb(OnDataRecv);

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, peer1, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;
  esp_now_add_peer(&peerInfo);
}

void loop() {
  myData.temp = readLM73Temp();
  myData.light = analogRead(LDR_PIN);
  esp_now_send(peer1, (uint8_t *)&myData, sizeof(myData));
  delay(2000);
}
```

---

## 8. Exercises
1. Extend mesh to **three nodes** and verify multi-hop data transfer.
2. Add **timestamp** to messages.
3. Send data to **Node-RED** via a bridge node connected to Wi-Fi.
4. Implement a **sleep mode** to save power between transmissions.

---

## 9. Conclusion
This lab demonstrated:
- Basic **ESP-NOW peer-to-peer mesh** setup.
- Integrating **sensor readings** (LDR & LM73) into mesh packets.
- Multi-hop data forwarding to extend coverage.
- Potential for **low-power, no-router IoT networks**.


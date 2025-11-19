# 🔬 ESP-NOW Lab: Device-to-Device Communication with Random Temperature (20–30°C)

This lab introduces **ESP-NOW direct communication (D2D)** using two ESP32 boards.  
One ESP32 acts as the **sender**, generating a **random temperature value** (20–30°C).  
The other acts as the **receiver**, printing received temperature data to the Serial Monitor.

---

# 🎯 1. Objective

Students will learn to:

- Initialize and configure ESP-NOW on ESP32  
- Register peer MAC addresses  
- Send structured data using ESP-NOW  
- Generate simulated sensor data (random temperature)  
- Display incoming packets on the receiver  

This is a perfect **intro lab** before integrating real sensors.

---

# 🧰 2. Equipment Required

| Item | Quantity | Purpose |
|------|----------|---------|
| ESP32 DevKit | 2 | Sender + Receiver |
| USB Cable | 2 | Programming + Power |
| Arduino IDE | 1 | Coding + Uploading |

---

# 🧩 3. Step 1 — Get Receiver MAC Address

Upload this sketch to the **receiver ESP32**:

```cpp
#include <WiFi.h>

void setup() {
  Serial.begin(115200);
  delay(500);

  WiFi.mode(WIFI_STA);      // ensure station mode
  delay(100);

  Serial.print("ESP32 MAC Address: ");
  Serial.println(WiFi.macAddress());
}

void loop() {}
```
<!---
```cpp
#include <WiFi.h>
#include <esp_wifi.h>
#include <esp_system.h>
#include <esp_bt.h>

void setup() {
  Serial.begin(115200);
  delay(1000);

  // WiFi station mode
  WiFi.mode(WIFI_STA);
  delay(100);

  // ----- WiFi Station MAC -----
  Serial.print("WiFi STA MAC: ");
  Serial.println(WiFi.macAddress());

  // ----- WiFi AP MAC -----
  WiFi.mode(WIFI_AP);
  delay(100);
  Serial.print("WiFi AP  MAC: ");
  Serial.println(WiFi.softAPmacAddress());

  // ----- Base MAC (factory burned MAC) -----
  uint8_t baseMac[6];
  esp_read_mac(baseMac, ESP_MAC_WIFI_STA);  
  Serial.printf("Base MAC     : %02X:%02X:%02X:%02X:%02X:%02X\n",
                baseMac[0], baseMac[1], baseMac[2],
                baseMac[3], baseMac[4], baseMac[5]);

  // ----- BLE MAC -----
  uint8_t bleMac[6];
  esp_read_mac(bleMac, ESP_MAC_BT);
  Serial.printf("BLE MAC      : %02X:%02X:%02X:%02X:%02X:%02X\n",
                bleMac[0], bleMac[1], bleMac[2],
                bleMac[3], bleMac[4], bleMac[5]);
}

void loop() {}
```
--->
Open **Serial Monitor** → Copy the MAC address:

Example:
```
24:6F:28:A1:B2:C3
```

Paste this into the sender code.

---

# 📡 4. Step 2 — ESP-NOW Sender Code  
**Generates random temperature (20–30°C) and sends every 1 second.**

> ⚠️ Replace the MAC address with your actual receiver MAC.

```cpp
#include <WiFi.h>
#include <esp_now.h>

// Replace with RECEIVER MAC Address
uint8_t receiverMAC[] = {0x40, 0x91, 0x51, 0x37, 0x0A, 0x08}; // 40:91:51:37:0A:0A  40:91:51:37:0a:08

typedef struct struct_message {
  float tempC;
  uint32_t counter;
} struct_message;

struct_message msg;
uint32_t cnt = 0;

// ---------------- SEND CALLBACK ----------------
void onDataSent(const esp_now_send_info_t *info, esp_now_send_status_t status) {
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

  Serial.println("Hello! ESP-NOW Sender!");

  // Register callback – matches esp_now_send_cb_t in your header
  esp_now_register_send_cb(onDataSent);

  esp_now_peer_info_t peerInfo = {};
  memcpy(peerInfo.peer_addr, receiverMAC, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
}

void loop() {
  float temp = random(200, 300) / 10.0; // 20.0–30.0 °C
  msg.tempC  = temp;
  msg.counter = cnt++;

  Serial.print("Sending Temp: ");
  Serial.print(temp);
  Serial.println(" °C");

  esp_err_t result = esp_now_send(receiverMAC, (uint8_t *)&msg, sizeof(msg));

  if (result != ESP_OK) {
    Serial.print("esp_now_send error: ");
    Serial.println(result);
  }

  delay(1000);
}
```

---

# 📥 5. Step 3 — ESP-NOW Receiver Code

```cpp

#include <WiFi.h>
#include <esp_now.h>

typedef struct struct_message {
  float tempC;
  uint32_t counter;
} struct_message;

struct_message incoming;

void onDataRecv(const esp_now_recv_info_t *info, const uint8_t *data, int len) {
  memcpy(&incoming, data, sizeof(incoming));

  Serial.println("📥 Received Data:");
  Serial.print("Temp: ");
  Serial.print(incoming.tempC);
  Serial.println(" °C");

  Serial.print("Count: ");
  Serial.println(incoming.counter);
  Serial.println("------------------------");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW Init Failed");
    return;
  }

  Serial.println(" Hello ESP32-NOW !!! ");
  Serial.println(WiFi.macAddress());

  esp_now_register_recv_cb(onDataRecv);
}

void loop() {}
```

---

# 📝 6. Expected Output

### Sender Serial Monitor:
```
Sending Temp: 24.5 °C
Send Status: SUCCESS
Sending Temp: 29.2 °C
Send Status: SUCCESS
```

### Receiver Serial Monitor:
```
📥 Received Data:
Temp: 24.5 °C
Count: 0
------------------------
📥 Received Data:
Temp: 29.2 °C
Count: 1
------------------------
```

---

# 🧪 7. Student Tasks

- Modify the temperature range to **15–40°C**  
- Add a mock humidity value (random 40–60%)  
- Broadcast temperature to two receivers  
- Change send interval to 2 seconds  
- Plot temperature using Arduino Serial Plotter  

---

# 🎓 8. Learning Outcomes

Students will understand:

- ESP-NOW peer setup  
- Struct-based packet transmission  
- Random data generation for simulation  
- Device-to-device communication  
- No-router wireless embedded networking  

---

# 📘 END OF LAB

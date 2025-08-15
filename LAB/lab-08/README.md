# LAB 8 — MQTT Photocell using Local Mosquitto and Node-RED

## 1. Objective
1. Interface an **LDR** with ESP32 and publish readings to a **local Mosquitto** MQTT broker.  
2. Subscribe to MQTT commands to control an LED.  
3. Build a **Node-RED** dashboard for monitoring/control.  
4. Install, configure, and test a **Mosquitto** broker (ports, auth, firewall).

---

## 2. Background
**MQTT** is a lightweight pub/sub protocol ideal for IoT.  
**Mosquitto** is a popular open-source MQTT broker.  
**Node-RED** provides a low-code flow editor with dashboards.

---

## 3. Mosquitto Installation & Setup

### 3.1 Quick install (choose your OS)

**Ubuntu/Debian**
```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

**Raspberry Pi OS** (same as Debian)
```bash
sudo apt update
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable --now mosquitto
```

**macOS (Homebrew)**
```bash
brew update
brew install mosquitto
brew services start mosquitto
```

**Windows**
- Download Mosquitto installer from Eclipse downloads (x64).
- Run installer (include “mosquitto.exe” and “mosquitto_pub/sub”).
- Open *Command Prompt (Admin)* to run `mosquitto -v` or install as a service.

---

### 3.2 Basic broker configuration (ports & listeners)

Create or edit the broker config file:

- **Linux/macOS**: `/etc/mosquitto/conf.d/lab.conf` (or `/usr/local/etc/mosquitto/mosquitto.conf` on macOS/Homebrew)  
- **Windows**: Create `C:\mosquitto\conf\lab.conf`

**Minimal config (TCP 1883 + local only):**
```conf
# lab.conf
listener 1883 0.0.0.0
allow_anonymous true
persistence true
persistence_location /var/lib/mosquitto/
```

> For **Windows**, remove the persistence_location line or set to an existing folder, e.g. `persistence_location C:\mosquitto\data\`

**Optional: add WebSockets on port 9001 (for browser clients)**
```conf
listener 9001
protocol websockets
```

**(Optional) Lock down with username/password**
```conf
allow_anonymous false
password_file /etc/mosquitto/passwd
```
Create credentials (Linux/macOS):
```bash
sudo mosquitto_passwd -c /etc/mosquitto/passwd student
# enter password interactively
```

Reload/restart broker:
```bash
# Systemd systems:
sudo systemctl restart mosquitto

# macOS Homebrew:
brew services restart mosquitto

# Windows:
mosquitto -c C:\mosquitto\conf\lab.conf -v
```

---

### 3.3 Firewall & connectivity checks

**Linux (UFW):**
```bash
sudo ufw allow 1883/tcp
sudo ufw allow 9001/tcp   # only if you enabled websockets
```

**Windows Defender Firewall:**
- Allow inbound **TCP 1883** (and **9001** if used) for `mosquitto.exe`.

**Test from the broker machine:**
```bash
# Terminal 1 (subscribe)
mosquitto_sub -h 127.0.0.1 -p 1883 -t lab/ldr -v

# Terminal 2 (publish)
mosquitto_pub -h 127.0.0.1 -p 1883 -t lab/ldr -m "hello"
```
If using auth:
```bash
mosquitto_sub -h 127.0.0.1 -p 1883 -u student -P 'yourpass' -t lab/ldr -v
mosquitto_pub -h 127.0.0.1 -p 1883 -u student -P 'yourpass' -t lab/ldr -m "hello"
```

---

## 4. Hardware & Software

**Hardware**
- ESP32 dev board, LDR, 10 kΩ resistor, breadboard, jumpers, USB cable

**Software**
- Arduino IDE with ESP32 boards installed  
- Mosquitto (broker + clients)  
- Node-RED + `node-red-dashboard` palette

**LDR wiring (voltage divider)**
```
(3.3V) ----[ LDR ]----o----[ 10kΩ ]----(GND)
                       |
                     ESP32 ADC (GPIO 34)
```

---

## 5. ESP32 Tasks

1. Connect to Wi-Fi.  
2. Connect to Mosquitto (host, port 1883, optional username/password).  
3. Publish LDR readings to `lab/ldr` every 2 s.  
4. Subscribe to `lab/led` to control onboard LED (`ON`/`OFF`).  

### 5.1 Example ESP32 Code (MQTT Pub/Sub)
```cpp
#include <WiFi.h>
#include <PubSubClient.h>

const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASS";

// Broker settings
const char* mqtt_server = "192.168.1.100";  // <-- your PC/RPi IP running Mosquitto
const uint16_t mqtt_port = 1883;
// Optional auth:
// const char* mqtt_user = "student";
// const char* mqtt_pass = "yourpass";

WiFiClient espClient;
PubSubClient client(espClient);

#define LDR_PIN 34
#define LED_PIN 2

unsigned long lastMsg = 0;

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (unsigned i=0;i<length;i++) msg += (char)payload[i];
  if (String(topic) == "lab/led") {
    if (msg == "ON") digitalWrite(LED_PIN, HIGH);
    else if (msg == "OFF") digitalWrite(LED_PIN, LOW);
  }
}

void mqttReconnect() {
  while (!client.connected()) {
    // bool ok = client.connect("esp32-lab8", mqtt_user, mqtt_pass); // with auth
    bool ok = client.connect("esp32-lab8"); // no auth
    if (ok) {
      client.subscribe("lab/led");
    } else {
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT); digitalWrite(LED_PIN, LOW);

  WiFi.begin(ssid, password);
  Serial.print("WiFi");
  while (WiFi.status()!=WL_CONNECTED){ delay(400); Serial.print("."); }
  Serial.printf("\nIP: %s\n", WiFi.localIP().toString().c_str());

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqttCallback);
}

void loop() {
  if (!client.connected()) mqttReconnect();
  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 2000) {
    lastMsg = now;
    int ldr = analogRead(LDR_PIN);
    char buf[16];
    snprintf(buf, sizeof(buf), "%d", ldr);
    client.publish("lab/ldr", buf);
    Serial.printf("PUB lab/ldr %s\n", buf);
  }
}
```

---

## 6. Node-RED Dashboard

**Flow basics:**
- `mqtt in` (topic `lab/ldr`) → `json` (optional) → `ui_gauge` (label: LDR)  
- `ui_button` (“LED ON”, “LED OFF”) → `mqtt out` (topic `lab/led`, payload “ON”/“OFF”)  

**Broker config in Node-RED:**
- Server: `mqtt://192.168.1.100:1883`
- If auth enabled: set **Username/Password**.

---

## 7. Testing

**CLI test (from broker machine or another host):**
```bash
mosquitto_sub -h 192.168.1.100 -p 1883 -t 'lab/ldr' -v
mosquitto_pub -h 192.168.1.100 -p 1883 -t 'lab/led' -m 'ON'
mosquitto_pub -h 192.168.1.100 -p 1883 -t 'lab/led' -m 'OFF'
```

**Node-RED**
- Open `http://<node-red-host>:1880/ui` → see gauge + LED buttons

---

## 8. Exercises
1. Calibrate LDR readings and convert to approximate **lux**.  
2. Add **LM73** temperature publishing on topic `lab/temp`.  
3. Plot both LDR and temperature in Node-RED charts with **1-minute window**.  
4. Implement threshold logic in Node-RED to auto-toggle LED.  
5. Enable **username/password** auth in Mosquitto and update ESP32 & Node-RED settings.  
6. (Advanced) Enable **WebSockets** (port 9001) and build a tiny web client that subscribes in the browser.

---

## 9. Assessment Rubric (4%)
| Criteria | Points |
|---|---|
| Broker installed & correctly configured (ports, service) | 1.0 |
| ESP32 publishes LDR & subscribes LED control | 1.0 |
| Node-RED dashboard working (gauge + buttons) | 1.0 |
| Code quality & documentation | 1.0 |

---

### Troubleshooting Cheatsheet
- Can’t connect? Check **broker IP**, **firewall**, **port 1883**, and **auth settings**.  
- Use `mosquitto_sub`/`mosquitto_pub` locally first; then test from ESP32.  
- If Node-RED shows no data, verify the MQTT config node and topic names.  


# 📡 ESP32 TCP Sender Examples

This guide shows how to use an ESP32 to open a TCP connection and send data to a server.  
It includes a **minimal quick-start sender** and a **robust sender** with auto-reconnect, keepalive, and CSV payloads.

---

## 1) Minimal TCP Sender (Quick Start)

✅ Works with any plain TCP server (e.g., `nc -l 5000` on your laptop).

```cpp
#include <WiFi.h>

const char* WIFI_SSID     = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASS";

const char* SERVER_IP     = "192.168.1.100"; // <-- change to your server
const uint16_t SERVER_PORT = 5000;           // <-- change to your port

WiFiClient client;

void setup() {
  Serial.begin(115200);

  // Connect WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nWiFi connected, IP: %s\n", WiFi.localIP().toString().c_str());

  // Connect TCP
  Serial.printf("Connecting to %s:%u ... ", SERVER_IP, SERVER_PORT);
  if (client.connect(SERVER_IP, SERVER_PORT)) {
    Serial.println("connected!");
  } else {
    Serial.println("failed!");
  }
}

void loop() {
  if (!client.connected()) {
    Serial.println("Disconnected. Reconnecting...");
    client.stop();
    if (client.connect(SERVER_IP, SERVER_PORT)) {
      Serial.println("Reconnected.");
    } else {
      Serial.println("Reconnect failed, retrying in 2s.");
      delay(2000);
      return;
    }
  }

  // Send a simple message every 1s
  static uint32_t seq = 0;
  String msg = String("hello from esp32, seq=") + seq++ + "\n";
  client.print(msg);
  Serial.print("Sent: "); Serial.print(msg);

  // Optional: read any response (non-blocking)
  while (client.available()) {
    String line = client.readStringUntil('\n');
    Serial.print("RX: "); Serial.println(line);
  }

  delay(1000);
}
```

### 🖥️ Quick Test (on your computer)
```bash
# Terminal A (server):
nc -l 5000

# Terminal B (optional echo client):
nc 127.0.0.1 5000
```

(Use your computer’s LAN IP in `SERVER_IP`.)

---

## 2) Robust TCP Sender (Auto-Reconnect + Keepalive)

✅ Adds:
- Exponential backoff reconnection  
- TCP keepalive (detect dead links)  
- Writes with flush & timeout  
- CSV payloads (timestamp, temperature, voltage)  

```cpp
#include <WiFi.h>

// ---------- USER CONFIG ----------
const char* WIFI_SSID     = "YOUR_WIFI";
const char* WIFI_PASSWORD = "YOUR_PASS";

const char* SERVER_HOST   = "192.168.1.100";  // or hostname
const uint16_t SERVER_PORT = 5000;

const uint32_t SEND_PERIOD_MS   = 1000;   // send interval
const uint32_t WRITE_TIMEOUT_MS = 1500;   // write timeout
// ---------------------------------

WiFiClient client;
unsigned long lastSend = 0;
unsigned long nextReconnectMs = 0;
uint32_t backoffMs = 500;                  // start 0.5s, max 10s
const uint32_t backoffMaxMs = 10000;

bool connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return true;
  Serial.printf("Connecting WiFi SSID: %s", WIFI_SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  unsigned long t0 = millis();
  while (WiFi.status() != WL_CONNECTED && millis() - t0 < 15000) {
    delay(300);
    Serial.print(".");
  }
  Serial.println();
  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("WiFi OK, IP: %s\n", WiFi.localIP().toString().c_str());
    return true;
  }
  Serial.println("WiFi connect timeout.");
  return false;
}

void setTcpKeepAlive(WiFiClient& c, int idle_s=10, int interval_s=3, int count=3) {
  c.setKeepAlive(idle_s, interval_s, count);
}

bool connectTCP() {
  if (client.connected()) return true;
  Serial.printf("Connecting TCP %s:%u ... ", SERVER_HOST, SERVER_PORT);
  client.setTimeout(WRITE_TIMEOUT_MS);

  if (client.connect(SERVER_HOST, SERVER_PORT)) {
    Serial.println("connected.");
    setTcpKeepAlive(client, 10, 3, 3);
    client.setNoDelay(true); // low-latency
    backoffMs = 500;         // reset backoff
    return true;
  }
  Serial.println("failed.");
  client.stop();
  return false;
}

bool writeWithTimeout(const uint8_t* data, size_t len, uint32_t timeoutMs) {
  unsigned long t0 = millis();
  size_t sent = 0;
  while (sent < len) {
    int n = client.write(data + sent, len - sent);
    if (n < 0) return false;  // error
    sent += n;
    if (millis() - t0 > timeoutMs) return false;
    delay(0); // yield
  }
  client.flush();
  return true;
}

// Simulated sensor data
float readTemperatureC() { return 25.0 + 2.0 * sinf(millis() / 2000.0f); }
float readVoltage()      { return 3.30f + 0.05f * cosf(millis() / 3000.0f); }

void setup() {
  Serial.begin(115200);
  delay(100);
  if (!connectWiFi()) Serial.println("Proceeding; will retry later.");
}

void loop() {
  // WiFi
  if (WiFi.status() != WL_CONNECTED) {
    if (millis() >= nextReconnectMs) {
      if (!connectWiFi()) {
        nextReconnectMs = millis() + backoffMs;
        backoffMs = min(backoffMs * 2, backoffMaxMs);
      }
    }
    delay(50);
    return;
  }

  // TCP
  if (!client.connected()) {
    if (millis() >= nextReconnectMs) {
      if (!connectTCP()) {
        nextReconnectMs = millis() + backoffMs;
        backoffMs = min(backoffMs * 2, backoffMaxMs);
      }
    }
    delay(20);
    return;
  }

  // Send periodically
  const unsigned long now = millis();
  if (now - lastSend >= SEND_PERIOD_MS) {
    lastSend = now;

    char buf[128];
    float tC = readTemperatureC();
    float v  = readVoltage();
    int n = snprintf(buf, sizeof(buf), "%lu,%.2f,%.3f\n", (unsigned long) now, tC, v);

    bool ok = writeWithTimeout((const uint8_t*)buf, n, WRITE_TIMEOUT_MS);
    if (ok) {
      Serial.printf("TX: %s", buf);
    } else {
      Serial.println("Write failed; closing socket.");
      client.stop();
    }
  }

  // Read back messages
  while (client.connected() && client.available()) {
    String line = client.readStringUntil('\n');
    line.trim();
    if (line.length()) {
      Serial.print("RX: ");
      Serial.println(line);
    }
  }

  delay(5);
}
```

---

## 📝 Notes & Tips

- **Server side (for testing)**  
  - Linux/macOS: `nc -l 5000`  
  - Windows: `ncat.exe -l 5000` (from Nmap) or `socat`  

- **Networking**  
  - Firewalls/routers: Open the server port on LAN.  
  - For WAN: use port-forwarding and secure your server.  

- **Keepalive vs heartbeat**  
  - TCP keepalive is slow by design.  
  - For faster detection, send your own heartbeat and handle missed acks.  

- **Binary payloads**  
  - Use `client.write(buffer, len)` for raw bytes.  
  - Use `client.print()` for line-delimited text.  

- **TLS (encryption)**  
  - Use `WiFiClientSecure`.  
  - Requires root CA or fingerprint.  

- **Power saving**  
  - Wi-Fi is power-hungry.  
  - Batch data + enable modem sleep if on battery.  


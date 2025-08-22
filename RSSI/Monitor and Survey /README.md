# ESP32 Wi-Fi Tools: RSSI Monitor & Site Survey

This repository provides two Arduino sketches for **ESP32 Wi-Fi analysis and diagnostics**:

1. **ESP32_RSSI_Monitor.ino** – Monitors Wi-Fi signal strength (RSSI), logs values, and provides LED feedback.  
2. **ESP32_WiFi_SiteSurvey.ino** – Scans nearby networks, builds a channel histogram, and suggests the cleanest Wi-Fi channel.

---

## 1. ESP32_RSSI_Monitor.ino

### Overview
This sketch connects the ESP32 to Wi-Fi, continuously prints **RSSI (dBm)** values, calculates a moving average, classifies signal quality, and uses an LED to indicate signal strength.  
It also implements **auto-reconnect with exponential backoff** if the connection drops.

### Code
```cpp
#include <WiFi.h>

const char* SSID = "YOUR_SSID";
const char* PASS = "YOUR_PASS";

const int LED_PIN = 2;          // Change if needed
const uint16_t SAMPLE_MS = 1000; // Telemetry interval
const uint8_t  MA_WINDOW = 10;   // Moving average window size

// Backoff for reconnect (ms)
uint32_t reconnectDelayMs = 1000;
const uint32_t RECONNECT_MAX_MS = 16000;

// Moving average buffer
long rssiBuf[MA_WINDOW];
uint8_t rIdx = 0;
uint8_t rCount = 0;

unsigned long lastSample = 0;
unsigned long lastBlink = 0;
uint16_t blinkInterval = 600; // adjusted by signal quality
bool ledState = false;

String rssiQuality(long rssi) {
  if (rssi >= -50) return "excellent";
  if (rssi >= -60) return "very good";
  if (rssi >= -67) return "good";
  if (rssi >= -75) return "fair";
  if (rssi >= -80) return "weak";
  return "very weak";
}

uint16_t qualityToBlink(long rssi) {
  // Map RSSI (stronger -> faster blink)
  // -40 dBm -> 150 ms ; -90 dBm -> 900 ms (clamped)
  long cl = constrain(rssi, -90, -40);
  return (uint16_t) map(cl, -90, -40, 900, 150);
}

long addToMA(long v) {
  rssiBuf[rIdx] = v;
  rIdx = (rIdx + 1) % MA_WINDOW;
  if (rCount < MA_WINDOW) rCount++;

  long sum = 0;
  for (uint8_t i = 0; i < rCount; i++) sum += rssiBuf[i];
  return sum / (long)rCount;
}

void connectWiFi() {
  Serial.printf("Connecting to SSID: %s\n", SSID);
  WiFi.mode(WIFI_STA);
  WiFi.begin(SSID, PASS);

  uint32_t t0 = millis();
  while (WiFi.status() != WL_CONNECTED) {
    delay(300);
    Serial.print(".");
    if (millis() - t0 > 20000) { // 20 s timeout
      Serial.println("\nConnection timeout, retrying...");
      WiFi.disconnect(true);
      delay(reconnectDelayMs);
      reconnectDelayMs = min(reconnectDelayMs * 2, RECONNECT_MAX_MS);
      t0 = millis();
      WiFi.begin(SSID, PASS);
    }
  }
  reconnectDelayMs = 1000; // reset backoff
  Serial.printf("\nConnected. IP: %s  RSSI: %ld dBm  CH: %d\n",
                WiFi.localIP().toString().c_str(),
                WiFi.RSSI(),
                WiFi.channel());
}

void setup() {
  Serial.begin(115200);
  delay(100);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  connectWiFi();
  Serial.println("Started RSSI monitor.");
  Serial.println("Columns: millis,rssi_dbm,rssi_avg_dbm,quality,channel");
}

void loop() {
  // Maintain Wi-Fi
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Wi-Fi lost. Reconnecting...");
    connectWiFi();
  }

  // Sample RSSI each SAMPLE_MS
  unsigned long now = millis();
  if (now - lastSample >= SAMPLE_MS) {
    lastSample = now;

    long rssi = WiFi.RSSI(); // dBm
    long avg = addToMA(rssi);
    String q = rssiQuality(avg);

    // adjust LED blink by signal
    blinkInterval = qualityToBlink(avg);

    Serial.printf("%lu,%ld,%ld,%s,%d\n",
                  now, rssi, avg, q.c_str(), WiFi.channel());
  }

  // Blink LED according to quality
  if (now - lastBlink >= blinkInterval) {
    lastBlink = now;
    ledState = !ledState;
    digitalWrite(LED_PIN, ledState ? HIGH : LOW);
  }
}
```

---

## 2. ESP32_WiFi_SiteSurvey.ino

### Overview
This sketch scans nearby Wi-Fi networks, prints details (SSID, RSSI, channel, encryption), and builds a **channel histogram**.  
It then suggests the best channel among **1, 6, and 11** for 2.4 GHz networks.

### Code
```cpp
#include <WiFi.h>

struct ChanStat {
  int count = 0;
  long rssiSum = 0;
};

void printEncryptionType(wifi_auth_mode_t t) {
  switch (t) {
    case WIFI_AUTH_OPEN:         Serial.print("OPEN"); break;
    case WIFI_AUTH_WEP:          Serial.print("WEP"); break;
    case WIFI_AUTH_WPA_PSK:      Serial.print("WPA_PSK"); break;
    case WIFI_AUTH_WPA2_PSK:     Serial.print("WPA2_PSK"); break;
    case WIFI_AUTH_WPA_WPA2_PSK: Serial.print("WPA_WPA2_PSK"); break;
    case WIFI_AUTH_WPA2_ENTERPRISE: Serial.print("WPA2_ENT"); break;
    case WIFI_AUTH_WPA3_PSK:     Serial.print("WPA3_PSK"); break;
    default:                     Serial.print("UNK"); break;
  }
}

void setup() {
  Serial.begin(115200);
  delay(100);
  WiFi.mode(WIFI_STA);
  WiFi.disconnect(true);
  delay(200);

  Serial.println("Scanning Wi-Fi networks...");
  int n = WiFi.scanNetworks(/*async=*/false, /*hidden=*/true);
  if (n <= 0) {
    Serial.println("No networks found.");
    return;
  }

  Serial.printf("Found %d networks\n", n);
  Serial.println("Idx,SSID,RSSI(dBm),Channel,Encryption");

  ChanStat cs[15 + 1]; // channels 1..14, index safe

  for (int i = 0; i < n; ++i) {
    String ssid = WiFi.SSID(i);
    int32_t rssi = WiFi.RSSI(i);
    int32_t ch   = WiFi.channel(i);
    wifi_auth_mode_t enc = WiFi.encryptionType(i);

    Serial.printf("%d,%s,%d,%d,", i, ssid.c_str(), (int)rssi, (int)ch);
    printEncryptionType(enc);
    Serial.println();

    if (ch >= 1 && ch <= 14) {
      cs[ch].count++;
      cs[ch].rssiSum += rssi;
    }
  }

  Serial.println("\nChannel histogram (AP count / avg RSSI):");
  for (int ch = 1; ch <= 14; ch++) {
    if (cs[ch].count > 0) {
      long avg = cs[ch].rssiSum / cs[ch].count;
      Serial.printf("Ch%2d: APs=%d, avgRSSI=%ld dBm  ", ch, cs[ch].count, avg);
      // simple bar by count
      for (int k = 0; k < cs[ch].count && k < 40; k++) Serial.print('#');
      Serial.println();
    }
  }

  // Suggest among 1/6/11 the one with fewest APs (tie-breaker by weakest avg RSSI)
  int cand[3] = {1, 6, 11};
  int best = cand[0];
  for (int i = 1; i < 3; i++) {
    int ch = cand[i];
    if (cs[ch].count < cs[best].count) best = ch;
    else if (cs[ch].count == cs[best].count) {
      long a = (cs[best].count ? cs[best].rssiSum / cs[best].count : -100);
      long b = (cs[ch].count ? cs[ch].rssiSum / cs[ch].count : -100);
      if (b < a) best = ch;
    }
  }
  Serial.printf("\nSuggested 2.4 GHz channel (1/6/11): %d\n", best);
}

void loop() {
  // Nothing; single-run survey. Press reset to rescan.
}
```

---

## 3. Notes & Tips
- Replace `YOUR_SSID` and `YOUR_PASS` before uploading.  
- Update `LED_PIN` if your ESP32 uses a different onboard LED.  
- Use the **Site Survey** sketch first to choose a better router channel.  
- Use the **RSSI Monitor** sketch to validate placement and connectivity.  

---

## ✅ Summary
These tools allow ESP32 developers to:  
- **Monitor** Wi-Fi quality with real-time RSSI logging and LED feedback.  
- **Survey** nearby networks to optimize channel selection.  
- **Improve** connection reliability with auto-reconnect and smarter deployment.

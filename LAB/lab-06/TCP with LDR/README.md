# 🌞 ESP32 LDR (Light Sensor) TCP Streamer

This project streams **light sensor (LDR)** readings from an ESP32 to a TCP server.  
The code reads an LDR voltage divider, computes **resistance and lux**, and sends a CSV line every second over Wi-Fi.

---

## 🔌 Wiring

- Use **ADC1 pins only** (`GPIO 32–39`) to avoid Wi-Fi conflicts.  
- Example: `GPIO34` (input-only).  
- Build a divider:

```
Vcc — LDR — AIN(GPIO34) — R_FIXED — GND
```

- Choose `R_FIXED` ≈ LDR’s mid-range resistance (10 kΩ typical for GL5528).

---

## 📜 Features

- Wi-Fi with auto-reconnect  
- TCP keepalive + `NoDelay`  
- Averaged ADC with millivolt calibration  
- Resistance & lux estimation (using power-law fit)  
- CSV payloads (epoch, voltage, resistance, lux)  

---

## 📝 Example Code

```cpp
#include <WiFi.h>

// ---------- USER CONFIG ----------
const char* WIFI_SSID      = "YOUR_WIFI";
const char* WIFI_PASSWORD  = "YOUR_PASS";

const char* SERVER_HOST    = "192.168.1.100";  // or hostname
const uint16_t SERVER_PORT = 5000;

const uint8_t  LDR_PIN     = 34;      // ADC1 channel (GPIO32–39 only)
const float    VCC_MV      = 3300.0;  // ESP32 Vcc in mV (adjust if measured)
const float    R_FIXED_OHM = 10000.0; // fixed resistor value in ohms

// Lux model for GL5528-like LDR (tune for your part):
// lux ≈ A * (R_ldr_kohm)^B
const float    LDR_A       = 500.0;
const float    LDR_B       = -1.4;

const uint32_t SEND_PERIOD_MS   = 1000;   // send every second
const uint32_t WRITE_TIMEOUT_MS = 1500;
const int      ADC_SAMPLES      = 16;    // averaging
// ---------------------------------

WiFiClient client;
unsigned long lastSend = 0;
unsigned long nextReconnectMs = 0;
uint32_t backoffMs = 500;
const uint32_t backoffMaxMs = 10000;

// -------- Wi-Fi / TCP helpers --------
bool connectWiFi() { /* ... */ }
void setTcpKeepAlive(WiFiClient& c, int idle_s=10, int interval_s=3, int count=3) { c.setKeepAlive(idle_s, interval_s, count); }
bool connectTCP() { /* ... */ }
bool writeWithTimeout(const uint8_t* data, size_t len, uint32_t timeoutMs) { /* ... */ }

// -------- LDR helpers --------
uint32_t readLdrMilliVoltsAveraged(uint8_t pin, int samples) { /* ... */ }
float computeLdrOhms(float vout_mV, float vcc_mV, float r_fixed_ohm) { /* ... */ }
float estimateLuxFromOhms(float r_ohm) { /* ... */ }

void setup() {
  Serial.begin(115200);
  delay(100);

  analogSetPinAttenuation(LDR_PIN, ADC_11db); // 0–2.45 V range
  analogReadResolution(12);

  if (!connectWiFi()) Serial.println("Proceeding; will retry later.");
}

void loop() {
  // Ensure Wi-Fi + TCP
  // Periodically read LDR and send CSV payload

  unsigned long now = millis();
  if (now - lastSend >= SEND_PERIOD_MS) {
    lastSend = now;

    uint32_t v_mV = readLdrMilliVoltsAveraged(LDR_PIN, ADC_SAMPLES);
    float r_ohm   = computeLdrOhms((float)v_mV, VCC_MV, R_FIXED_OHM);
    float lux     = estimateLuxFromOhms(r_ohm);

    char line[160];
    int n = snprintf(line, sizeof(line), "%lu,%u,%.1f,%.1f\n",
                     (unsigned long)now, v_mV, r_ohm, lux);

    if (writeWithTimeout((const uint8_t*)line, n, WRITE_TIMEOUT_MS)) {
      Serial.printf("TX: %s", line);
    } else {
      Serial.println("Write failed; closing socket.");
      client.stop();
    }
  }

  // Handle server commands
  while (client.connected() && client.available()) {
    String cmd = client.readStringUntil('\n');
    cmd.trim();
    if (cmd == "PING") {
      client.print("PONG\n");
    }
  }

  delay(5);
}
```

---

## 🔧 Calibration & Tuning Tips

- **Vcc:** Measure 3.3 V with a multimeter and update `VCC_MV`.  
- **Attenuation:** If divider output > 2.45 V, adjust `R_FIXED` or ADC attenuation.  
- **Lux model:** Constants `(A, B)` vary by LDR. Fit from real lux–resistance data.  
- **Noise:** Increase `ADC_SAMPLES` or use a median filter.  
- **Pins:** Only use **ADC1 pins (32–39)** when Wi-Fi is active.  

---

## 📊 Payload Format (CSV)

Each line sent over TCP:

```
epoch_ms,voltage_mV,resistance_ohm,lux
```

Example:

```
12345,1023,5432.1,150.7
```

---

## 🌐 Server Testing

On your computer:

```bash
# Start a TCP server
nc -l 5000
```

ESP32 will connect and stream CSV lines.

---

## 🧩 Optional: JSON Payload

Replace `snprintf` with:

```cpp
int n = snprintf(line, sizeof(line),
  "{\"t_ms\":%lu,\"v_mV\":%u,\"r_ohm\":%.1f,\"lux\":%.1f}\n",
  (unsigned long)now, v_mV, r_ohm, lux);
```

---

✅ Now you have a full guide for building an **ESP32 LDR TCP data streamer** with calibration, lux estimation, and robust networking.


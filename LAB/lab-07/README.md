# LAB 7 — HTTP Web Server for LDR and LM73 (with AJAX)

## 1. Objective
1. Run an ESP32 **HTTP server**.
2. Read **LDR** (ADC) and **LM73** (I²C) temperature.
3. Serve a **live-updating** dashboard using **AJAX (Fetch API)**.
4. Provide a **JSON API** endpoint for programmatic access.

## 2. Background
Using AJAX (the **Fetch API**) lets the browser request new data in the background and update only parts of the page. This reduces bandwidth and makes the UI feel responsive. We’ll expose `/api/sensors` to return JSON and use JavaScript to poll it every second.

## 3. Hardware Setup

| Component | ESP32 |
|---|---|
| LDR + 10kΩ divider | LDR→3.3V, junction→**GPIO 34**, resistor→GND |
| LM73 (I²C) | SDA→**GPIO 21**, SCL→**GPIO 22**, VCC→3.3V, GND→GND |

## 4. Software Requirements
- Arduino IDE (ESP32 core)
- Libraries: `WiFi.h`, `WebServer.h`, `Wire.h`

## 5. Code Implementation

### 5.1 LM73 Function
```cpp
#include <Wire.h>
uint8_t LM73_ADDR = 0x48;                 // adjust if I²C scan differs
const float LM73_LSB_C = 0.03125f;        // °C/LSB (check your breakout)

float readLM73() {
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(0x00);                       // temp register
  Wire.endTransmission(false);
  Wire.requestFrom(LM73_ADDR, (uint8_t)2);
  if (Wire.available() < 2) return NAN;
  uint16_t raw = (Wire.read() << 8) | Wire.read();
  int16_t val = raw >> 5;                 // typical left-justified format
  return val * LM73_LSB_C;
}
```

### 5.2 HTTP Server + JSON API
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";

WebServer server(80);
const int LDR_PIN = 34;

String getSensorJSON() {
  int ldr = analogRead(LDR_PIN);
  float tc = readLM73();
  char buf[120];
  snprintf(buf, sizeof(buf), "{\"ldr\":%d,\"temp_c\":%.2f,\"ts\":%lu}",
           ldr, isnan(tc) ? -999.0f : tc, (unsigned long)millis());
  return String(buf);
}
```

### 5.3 AJAX Dashboard (HTML + JS Fetch)
```cpp
const char PAGE[] PROGMEM = R"HTML(
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP32 LDR & LM73 (AJAX)</title>
<style>
  body{font-family:system-ui,Arial;margin:20px}
  .card{border:1px solid #ddd;border-radius:8px;padding:16px;max-width:420px}
  .row{display:flex;gap:12px;margin:8px 0}
  .k{width:110px;color:#555}
  .v{font-weight:600}
  .muted{color:#777;font-size:0.9em}
  button{padding:8px 12px;border:1px solid #888;border-radius:6px;cursor:pointer}
</style></head><body>
<div class="card">
  <h2>ESP32 Sensor Dashboard</h2>
  <div class="row"><div class="k">LDR (ADC)</div><div class="v" id="ldr">--</div></div>
  <div class="row"><div class="k">Temp (°C)</div><div class="v" id="temp">--</div></div>
  <div class="row"><div class="k">Updated</div><div class="v" id="ts">--</div></div>
  <p class="muted">JSON API: <code>/api/sensors</code></p>
  <p><button onclick="refresh()">Refresh now</button></p>
</div>
<script>
async function refresh(){
  try{
    const r = await fetch('/api/sensors', {cache:'no-store'});
    const j = await r.json();
    document.getElementById('ldr').textContent  = j.ldr;
    document.getElementById('temp').textContent = (j.temp_c===-999? 'N/A' : j.temp_c.toFixed(2));
    document.getElementById('ts').textContent   = (j.ts/1000).toFixed(1) + ' s';
  }catch(e){ console.log(e); }
}
setInterval(refresh, 1000);
refresh();
</script></body></html>
)HTML";
```

### 5.4 Full Sketch
```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>

// --- LM73 section ---
uint8_t LM73_ADDR = 0x48;
const float LM73_LSB_C = 0.03125f;
float readLM73(){
  Wire.beginTransmission(LM73_ADDR); Wire.write(0x00);
  Wire.endTransmission(false);
  Wire.requestFrom(LM73_ADDR, (uint8_t)2);
  if (Wire.available()<2) return NAN;
  uint16_t raw = (Wire.read()<<8) | Wire.read();
  int16_t val = raw >> 5;
  return val * LM73_LSB_C;
}

// --- Network / server section ---
const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";
WebServer server(80);
const int LDR_PIN = 34;

// HTML Page
const char PAGE[] PROGMEM = R"HTML(
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP32 LDR & LM73 (AJAX)</title>
<style>
  body{font-family:system-ui,Arial;margin:20px}
  .card{border:1px solid #ddd;border-radius:8px;padding:16px;max-width:420px}
  .row{display:flex;gap:12px;margin:8px 0}
  .k{width:110px;color:#555}
  .v{font-weight:600}
  .muted{color:#777;font-size:0.9em}
  button{padding:8px 12px;border:1px solid #888;border-radius:6px;cursor:pointer}
</style></head><body>
<div class="card">
  <h2>ESP32 Sensor Dashboard</h2>
  <div class="row"><div class="k">LDR (ADC)</div><div class="v" id="ldr">--</div></div>
  <div class="row"><div class="k">Temp (°C)</div><div class="v" id="temp">--</div></div>
  <div class="row"><div class="k">Updated</div><div class="v" id="ts">--</div></div>
  <p class="muted">JSON API: <code>/api/sensors</code></p>
  <p><button onclick="refresh()">Refresh now</button></p>
</div>
<script>
async function refresh(){
  try{
    const r = await fetch('/api/sensors', {cache:'no-store'});
    const j = await r.json();
    document.getElementById('ldr').textContent  = j.ldr;
    document.getElementById('temp').textContent = (j.temp_c===-999? 'N/A' : j.temp_c.toFixed(2));
    document.getElementById('ts').textContent   = (j.ts/1000).toFixed(1) + ' s';
  }catch(e){ console.log(e); }
}
setInterval(refresh, 1000);
refresh();
</script></body></html>
)HTML";

String getSensorJSON() {
  int ldr = analogRead(LDR_PIN);
  float tc = readLM73();
  char buf[120];
  snprintf(buf, sizeof(buf), "{\"ldr\":%d,\"temp_c\":%.2f,\"ts\":%lu}",
           ldr, isnan(tc) ? -999.0f : tc, (unsigned long)millis());
  return String(buf);
}

void handleRoot(){ server.send_P(200, "text/html", PAGE); }
void handleAPI(){ server.send(200, "application/json", getSensorJSON()); }

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  pinMode(LDR_PIN, INPUT);

  WiFi.begin(ssid, pass);
  Serial.print("Connecting");
  while (WiFi.status()!=WL_CONNECTED){ delay(500); Serial.print("."); }
  Serial.printf("\nIP: %s\n", WiFi.localIP().toString().c_str());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/api/sensors", HTTP_GET, handleAPI);
  server.begin();
  Serial.println("HTTP server ready");
}

void loop(){ server.handleClient(); }
```

## 6. Testing
- Visit `http://<ESP32_IP>/` → Numbers update every second without page reload.
- `http://<ESP32_IP>/api/sensors` → JSON payload.

## 7. Exercises
1. Change the polling interval from **1 s** to **500 ms**; note CPU/network impact.
2. Add **min/max** and **moving average** to the JSON output.
3. Add a **/api/config** endpoint to set the poll interval from the UI (store in NVS).
4. Replace polling with **Server-Sent Events** or **WebSockets** for push updates.
5. Add simple **LED control** buttons that POST to `/api/led?state=on/off` and reflect status on the page.

## 8. Conclusion
You built a responsive ESP32 **AJAX dashboard** for LDR and LM73 using a JSON API. This pattern scales to more sensors and more advanced UIs while keeping the firmware simple and resource-friendly.


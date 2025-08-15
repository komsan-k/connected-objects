LAB 1 — ESP32 Bring-Up & Blink + Serial
Objective: Verify toolchain, upload sketch, check serial, blink LED.
Tasks

Install “ESP32” in Boards Manager, pick your board & COM port.

Blink on GPIO2 and print a hello banner.

Starter

cpp
Copy
Edit
void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  Serial.println("ESP32 ready!");
}
void loop() {
  digitalWrite(2, HIGH); delay(500);
  digitalWrite(2, LOW);  delay(500);
}
Success: LED blinks; “ESP32 ready!” in Serial Monitor (115200).

LAB 2 — Wi-Fi Connect + Print IP (Optional mDNS)
Objective: Connect to Wi-Fi and print local IP.
Tasks

Add your SSID/PASS; connect loop until WL_CONNECTED.

Print WiFi.localIP().

Starter

cpp
Copy
Edit
#include <WiFi.h>
const char* ssid="YOUR_SSID"; const char* pass="YOUR_PASS";
void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status()!=WL_CONNECTED){ delay(500); Serial.print("."); }
  Serial.print("\nWiFi OK: "); Serial.println(WiFi.localIP());
}
void loop(){}
Success: ESP32 shows IP; you can ping it.

LAB 3 — I²C Scan + Read LM73 Temperature
Objective: Scan I²C bus; read LM73 temperature and print °C.
Note: LM73 resolution depends on config; use a scale constant and adjust if needed from your breakout’s datasheet. Common LSB sizes are around 0.03125 °C/LSB.
Tasks

I²C scan to find device (addresses typically 0x48–0x4B).

Read temperature register (2 bytes), convert to °C, print.

Starter

cpp
Copy
Edit
#include <Wire.h>
uint8_t LM73_ADDR = 0x48; // adjust if your scan differs
const float LM73_LSB_C = 0.03125f; // adjust if needed

void scanI2C(){
  for (uint8_t a=1;a<127;a++){
    Wire.beginTransmission(a);
    if (Wire.endTransmission()==0){ Serial.printf("I2C dev: 0x%02X\n", a); }
  }
}
float lm73ReadC(){
  Wire.beginTransmission(LM73_ADDR);
  Wire.write(0x00); // temp register
  Wire.endTransmission(false);
  Wire.requestFrom(LM73_ADDR, (uint8_t)2);
  if (Wire.available()<2) return NAN;
  uint16_t raw = (Wire.read()<<8) | Wire.read();
  // Typical left-justified format; shift to align if needed:
  int16_t val = raw >> 5;                 // example alignment (11-bit)
  return val * LM73_LSB_C;                // adjust for your device
}
void setup(){
  Serial.begin(115200);
  Wire.begin(21,22);
  scanI2C();
}
void loop(){
  float t = lm73ReadC();
  if (!isnan(t)) Serial.printf("LM73: %.2f C\n", t);
  delay(1000);
}
Success: Temp prints ~room temperature.

LAB 4 — MPU6050 Bring-Up (Accel/Gyro) + Quick Calibration
Objective: Read raw accel/gyro, convert to g and deg/s; estimate offsets.
Tasks

Wake device (PWR_MGMT_1=0), set ranges (±2g, ±250°/s).

Collect 500 samples at rest, compute gyro offsets.

Print calibrated values.

Starter (core bits)

cpp
Copy
Edit
#include <Wire.h>
#define MPU 0x68
int16_t ax,ay,az,gx,gy,gz; float gox,goy,goz;

void mpuWrite(uint8_t reg, uint8_t val){ Wire.beginTransmission(MPU); Wire.write(reg); Wire.write(val); Wire.endTransmission(); }
void mpuRead6(uint8_t reg, int16_t &x,int16_t &y,int16_t &z){
  Wire.beginTransmission(MPU); Wire.write(reg); Wire.endTransmission(false);
  Wire.requestFrom(MPU,6);
  x=(Wire.read()<<8)|Wire.read(); y=(Wire.read()<<8)|Wire.read(); z=(Wire.read()<<8)|Wire.read();
}
void setup(){
  Serial.begin(115200); Wire.begin(21,22);
  mpuWrite(0x6B,0x00); // wake
  mpuWrite(0x1C,0x00); // accel ±2g
  mpuWrite(0x1B,0x00); // gyro ±250 dps
  // quick offset
  long sx=0,sy=0,sz=0;
  for(int i=0;i<500;i++){ mpuRead6(0x43,gx,gy,gz); sx+=gx; sy+=gy; sz+=gz; delay(5); }
  gox=sx/500.0; goy=sy/500.0; goz=sz/500.0;
}
void loop(){
  mpuRead6(0x3B,ax,ay,az);
  mpuRead6(0x43,gx,gy,gz);
  float axg=ax/16384.0, ayg=ay/16384.0, azg=az/16384.0;
  float gxdps=(gx-gox)/131.0, gydps=(gy-goy)/131.0, gzdps=(gz-goz)/131.0;
  Serial.printf("A[g]=%.2f,%.2f,%.2f G[g]=%.2f,%.2f,%.2f\n", axg,ayg,azg,gxdps,gydps,gzdps);
  delay(100);
}
Success: Gyro near 0 at rest; accel Z near +1g.

LAB 5 — Publish Telemetry (JSON) via MQTT
Objective: Wi-Fi connect and publish temp + IMU as JSON to local Mosquitto.
Tasks

Use PubSubClient to connect to mqtt://<broker-ip>:1883.

Publish JSON every 2s to lab/esp32/telemetry.

Starter

cpp
Copy
Edit
#include <WiFi.h>
#include <PubSubClient.h>
WiFiClient espClient; PubSubClient client(espClient);
const char* mqtt="192.168.1.10"; // your broker IP

void mqttReconnect(){
  while(!client.connected()){
    if(client.connect("esp32_lab5")) break;
    delay(1000);
  }
}
void setup(){ Serial.begin(115200); WiFi.begin("SSID","PASS");
  while (WiFi.status()!=WL_CONNECTED){ delay(400); Serial.print("."); }
  client.setServer(mqtt,1883);
}
void loop(){
  if(!client.connected()) mqttReconnect();
  client.loop();
  // (Read sensors first...) Example payload:
  char payload[200];
  snprintf(payload,sizeof(payload),
    "{\"t\":%.2f,\"ax\":%.2f,\"ay\":%.2f,\"az\":%.2f}", 24.6,0.01,-0.02,0.98);
  client.publish("lab/esp32/telemetry", payload);
  delay(2000);
}
Success: See messages in mosquitto_sub -t lab/esp32/telemetry -v.

LAB 6 — Subscribe to Commands (LED / Rate / Calibrate)
Objective: Subscribe to lab/esp32/cmd and act on JSON commands.
Tasks

Parse simple strings or JSON: "LED_ON", "LED_OFF", {"rate_hz":10}, {"calibrate":"imu"}.

Confirm by publishing status to lab/esp32/state.

Starter (callback)

cpp
Copy
Edit
#include <ArduinoJson.h> // optional
void onMsg(char* topic, byte* payload, unsigned int len){
  String s; for(unsigned i=0;i<len;i++) s+=(char)payload[i];
  if (s=="LED_ON") digitalWrite(5, HIGH);
  else if (s=="LED_OFF") digitalWrite(5, LOW);
  else {
    StaticJsonDocument<128> doc;
    if (deserializeJson(doc, s)==DeserializationError::Ok){
      if (doc.containsKey("rate_hz")) {/* update sampling */}
      if (doc["calibrate"]=="imu") {/* recalibrate */}
    }
  }
}
Success: Node-RED buttons/forms change device behavior.

LAB 7 — Node-RED Dashboard (Gauges + Charts + Buttons)
Objective: Build a dashboard to view temp/IMU and send commands.
Tasks (Node-RED)

mqtt in (lab/esp32/telemetry) → json → ui_gauge (temp) + ui_chart (temp).

ui_button → mqtt out (lab/esp32/cmd) sending "LED_ON"/"LED_OFF".

Optional ui_form to set rate_hz.

Success: Live charts, working control buttons.

LAB 8 — Telemetry with Rolling Average + Topic Design
Objective: Smooth noisy signals; add rolling mean to payload.
Tasks

Compute 10-sample moving average for temp and accel magnitude.

Publish enriched JSON:
{"t":..., "t_avg":..., "acc_mag":..., "acc_mag_avg":...}

Topic hygiene:

Telemetry: lab/esp32/telemetry

State (retained): lab/esp32/state

Commands: lab/esp32/cmd

Starter (simple MA)

cpp
Copy
Edit
float tBuf[10]; int ti=0, tn=0;
float addMA(float *buf,int &i,int &n,int N,float x){
  buf[i]=x; i=(i+1)%N; if(n<N) n++;
  float s=0; for(int k=0;k<n;k++) s+=buf[k];
  return s/n;
}
Success: Dashboard shows both raw and averaged series.

LAB 9 — Orientation (Complementary Filter: Pitch/Roll)
Objective: Fuse accel + gyro into smooth pitch/roll.
Math

pitch_acc = atan2(ax, sqrt(ay^2 + az^2))

roll_acc = atan2(ay, sqrt(ax^2 + az^2))

pitch = α*(pitch + gyro_y*dt) + (1-α)*pitch_acc (α≈0.98)

roll = α*(roll + gyro_x*dt) + (1-α)*roll_acc

Tasks

Compute dt from millis(); maintain angles in degrees.

Publish {"pitch":..., "roll":...} and show on gauges/charts.

Success: Stable angles with fast response.

LAB 10 — Eventing & Logging (Threshold/Z-Score) + Node-RED Storage
Objective: Detect vibration anomaly; raise events; log to CSV.
Tasks

Compute windowed RMS of gyro magnitude; compare to baseline.

If zscore > 3, publish lab/esp32/event with timestamp & metric.

Node-RED: mqtt in (event) → file (CSV append) and ui_toast.

Success: Shakes trigger events; CSV file grows with entries.

LAB 11 — OTA Updates + Robust Reconnect
Objective: Add ArduinoOTA and resilient Wi-Fi/MQTT reconnect logic.
Tasks

Integrate ArduinoOTA (hostname, optional password).

Add reconnect loops with backoff for Wi-Fi & MQTT.

Publish retained state "online" on connect, LWT "offline" on MQTT connect.

Starter

cpp
Copy
Edit
#include <ArduinoOTA.h>
void setup(){
  // WiFi connect...
  ArduinoOTA.setHostname("esp32-labs");
  ArduinoOTA.begin();
}
void loop(){
  ArduinoOTA.handle();
  // rest of your loop...
}
Success: Upload new firmware from Arduino IDE’s “Network Ports” and see version bump.

LAB 12 — Final Integration: Secure & Documented System
Objective: Put it together: clean code, topics, dashboard, (optional) TLS.
Tasks

Consolidate: LM73 + MPU6050 + smoothing + orientation + events.

Dashboard: telemetry, orientation, thresholds, controls, status.

README with wiring diagrams, topics list, JSON schemas, screenshots.

(Optional) Secure MQTT (TLS) or username/password on Mosquitto.

Success: End-to-end, robust system ready for demo or capstone.

JSON Examples
Telemetry

json
Copy
Edit
{
  "ts": 1712345678901,
  "temp_c": 24.88,
  "t_avg": 24.80,
  "accel": {"x": -0.01, "y": 0.03, "z": 0.98},
  "gyro":  {"x":  0.10, "y": 0.02, "z":-0.04},
  "pitch": 1.9,
  "roll": -0.6
}
Command

json
Copy
Edit
{"rate_hz": 25}
{"led": "on"}
{"calibrate": "imu"}
{"threshold": {"zscore": 3.0}}
Event

json
Copy
Edit
{"ts":171234..., "type":"anomaly", "metric":"gyro_rms", "z":3.5}



LAB 18 — Raw TCP Communication (Server & Client)
Objective: Build a basic TCP echo server on ESP32, then a client that connects to a desktop TCP server (e.g., nc/Python). Learn about sockets, framing, and timeouts.

Prereqs: ESP32 connected to Wi-Fi; Serial Monitor.
Ports (suggested): 5000

A. ESP32 TCP Echo Server
Tasks

Start WiFiServer on port 5000.

Accept a client; echo back any received bytes.

Print connection info and payloads to Serial.

Starter (Server)

cpp
Copy
Edit
#include <WiFi.h>

const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";
WiFiServer server(5000);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status()!=WL_CONNECTED){ delay(500); Serial.print("."); }
  Serial.print("\nIP: "); Serial.println(WiFi.localIP());
  server.begin();
  Serial.println("TCP echo server on 5000");
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;
  Serial.print("Client: "); Serial.println(client.remoteIP());
  client.println("Hello from ESP32. Type something:");

  while (client.connected()) {
    while (client.available()) {
      int c = client.read();
      Serial.write(c);
      client.write(c);  // echo
    }
    delay(1);
  }
  client.stop();
  Serial.println("Client disconnected");
}
Test (PC):

bash
Copy
Edit
nc <esp32-ip> 5000      # type text, see it echoed
B. ESP32 TCP Client → Desktop Server
Tasks

Run a simple server on your PC: nc -l 5000 (Linux/macOS) or a small Python socket server.

ESP32 connects, sends a line every 2 s; prints received responses.

Starter (Client)

cpp
Copy
Edit
#include <WiFi.h>
const char* ssid="YOUR_SSID"; const char* pass="YOUR_PASS";
const char* host="192.168.1.100"; // your PC IP
const uint16_t port=5000;
WiFiClient client;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status()!=WL_CONNECTED){ delay(500); Serial.print("."); }
  Serial.print("\nIP: "); Serial.println(WiFi.localIP());
  Serial.printf("Connecting to %s:%u...\n", host, port);
  if (!client.connect(host, port, 5000)) {
    Serial.println("Connect failed");
  } else {
    Serial.println("Connected!");
  }
}

void loop() {
  if (!client.connected()) {
    Serial.println("Reconnecting...");
    client.stop();
    delay(1000);
    client.connect(host, port);
  }
  client.println("ESP32 says hi");
  unsigned long t0 = millis();
  while (millis() - t0 < 250) { // short read window
    while (client.available()) Serial.write(client.read());
  }
  delay(2000);
}
Success: You can send/receive raw TCP data in both directions.

LAB 19 — HTTP Web Server (REST-style Endpoints)
Objective: Serve a small HTTP API and control an on-board LED via URL; provide a JSON telemetry endpoint.

Prereqs: Arduino WiFi.h; use WebServer.h (ESP32 core’s WebServer).

Routes

GET / → serves a minimal HTML page

GET /api/telemetry → returns JSON { "temp": 24.7, "uptime_ms": 12345 }

POST /api/led (or GET /api/led?state=on) → toggles LED GPIO

Starter

cpp
Copy
Edit
#include <WiFi.h>
#include <WebServer.h>

const char* ssid="YOUR_SSID"; const char* pass="YOUR_PASS";
WebServer server(80);
const int LED_PIN = 5;

String htmlIndex() {
  return R"HTML(
<!DOCTYPE html><html><head><meta charset="utf-8"><title>ESP32</title></head>
<body>
<h2>ESP32 Web Server</h2>
<p><a href="/api/led?state=on">LED ON</a> | <a href="/api/led?state=off">LED OFF</a></p>
<p>Telemetry: <a href="/api/telemetry">/api/telemetry</a></p>
</body></html>)HTML";
}

void handleRoot(){ server.send(200, "text/html", htmlIndex()); }

void handleTelemetry(){
  static uint32_t boot = millis();
  float temp = 24.7; // TODO: read LM73
  char buf[128];
  snprintf(buf, sizeof(buf), "{\"temp\":%.2f,\"uptime_ms\":%lu}", temp, (unsigned long)(millis()-boot));
  server.send(200, "application/json", buf);
}

void handleLed(){
  String state = server.hasArg("state") ? server.arg("state") : "";
  if (state == "on") digitalWrite(LED_PIN, HIGH);
  else if (state == "off") digitalWrite(LED_PIN, LOW);
  server.send(200, "application/json", String("{\"led\":\"") + (digitalRead(LED_PIN)?"on":"off") + "\"}");
}

void setup(){
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT); digitalWrite(LED_PIN, LOW);
  WiFi.begin(ssid, pass);
  while (WiFi.status()!=WL_CONNECTED){ delay(500); Serial.print("."); }
  Serial.print("\nIP: "); Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/api/telemetry", HTTP_GET, handleTelemetry);
  server.on("/api/led", HTTP_ANY, handleLed);
  server.begin();
  Serial.println("HTTP server started");
}

void loop(){ server.handleClient(); }
Success: Open http://<esp32-ip>/ and try the links. curl JSON endpoints:

bash
Copy
Edit
curl http://<esp32-ip>/api/telemetry
curl "http://<esp32-ip>/api/led?state=on"
LAB 20 — AJAX Dashboard (Fetch API) with JSON Endpoints
Objective: Serve a small single-page app (SPA) from ESP32 that uses AJAX (Fetch) to pull JSON telemetry every 1 s and POST LED commands—no page reloads.

Approach: Serve a static HTML+JS page; JS polls /api/telemetry and updates DOM; button triggers /api/led.

Starter

cpp
Copy
Edit
#include <WiFi.h>
#include <WebServer.h>

const char* ssid="YOUR_SSID"; const char* pass="YOUR_PASS";
WebServer server(80);
const int LED_PIN = 5;

const char* PAGE = R"HTML(
<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP32 AJAX Dashboard</title>
<style>
body{font-family:system-ui,Arial;margin:20px} .pill{display:inline-block;padding:6px 10px;border-radius:12px;background:#eee}
.btn{padding:8px 14px;border:1px solid #888;border-radius:6px;cursor:pointer}
</style></head><body>
<h2>ESP32 AJAX Dashboard</h2>
<p>Temp: <span id="temp">--</span> °C &nbsp; Uptime: <span id="uptime">--</span> ms</p>
<p>LED: <span id="led" class="pill">--</span></p>
<p><button class="btn" onclick="setLed('on')">LED ON</button>
   <button class="btn" onclick="setLed('off')">LED OFF</button></p>
<script>
async function refresh(){
  try{
    const r = await fetch('/api/telemetry'); // GET
    const j = await r.json();
    document.getElementById('temp').textContent = j.temp.toFixed(2);
    document.getElementById('uptime').textContent = j.uptime_ms;
    document.getElementById('led').textContent = j.led || '--';
  }catch(e){ console.log(e); }
}
async function setLed(state){
  try{
    const r = await fetch('/api/led?state='+state, {method:'POST'});
    const j = await r.json();
    document.getElementById('led').textContent = j.led;
  }catch(e){ console.log(e); }
}
setInterval(refresh, 1000); refresh();
</script></body></html>
)HTML";

String telemetryJson(){
  static uint32_t boot = millis();
  float temp = 24.7; // TODO: LM73 read
  bool ledOn = digitalRead(LED_PIN);
  char buf[160];
  snprintf(buf, sizeof(buf),
    "{\"temp\":%.2f,\"uptime_ms\":%lu,\"led\":\"%s\"}",
    temp, (unsigned long)(millis()-boot), ledOn?"on":"off");
  return String(buf);
}

void handleRoot(){ server.send(200, "text/html", PAGE); }
void apiTelemetry(){ server.send(200, "application/json", telemetryJson()); }
void apiLed(){
  if (server.hasArg("state")) {
    String s = server.arg("state");
    if (s=="on") digitalWrite(LED_PIN, HIGH);
    else if (s=="off") digitalWrite(LED_PIN, LOW);
  }
  server.send(200, "application/json", telemetryJson());
}

void setup(){
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT); digitalWrite(LED_PIN, LOW);
  WiFi.begin(ssid, pass);
  while (WiFi.status()!=WL_CONNECTED){ delay(400); Serial.print("."); }
  Serial.print("\nIP: "); Serial.println(WiFi.localIP());

  server.on("/", HTTP_GET, handleRoot);
  server.on("/api/telemetry", HTTP_GET, apiTelemetry);
  server.on("/api/led", HTTP_ANY, apiLed);
  server.begin();
  Serial.println("AJAX server ready");
}
void loop(){ server.handleClient(); }
Success: Open http://<esp32-ip>/. Temp and uptime update live; LED pill changes on button clicks—no reloads.

Tips, Variations & Integrations
Browser Caching: Add cache-busting headers if you serve static assets from SPIFFS/LittleFS.

Security: For local labs, HTTP is fine. For production, use TLS (reverse-proxy or ESP32 WiFiClientSecure) and auth.

Node-RED Bridge: You can add flows that proxy between MQTT and your HTTP API, enabling dashboards or cloud links.

SSE/WebSockets (Advanced): Replace AJAX polling with Server-Sent Events or WebSockets to push telemetry as it happens.

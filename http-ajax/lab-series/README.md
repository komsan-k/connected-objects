# ESP32 Web Labs — Wi‑Fi, HTTP, AJAX, Auth & Charts

A step‑by‑step set of labworks that take you from basic Wi‑Fi connectivity on ESP32 to an authenticated AJAX dashboard with real‑time charts.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Hardware](#hardware)
- [Setup](#setup)
- [Labwork 1.1 — Connect ESP32 to Wi‑Fi & verify IP](#labwork-11--connect-esp32-to-wi-fi--verify-ip)
- [Labwork 2.1 — Minimal HTTP Server (“Hello ESP32”)](#labwork-21--minimal-http-server-hello-esp32)
- [Labwork 3.1 — Dynamic content (auto-refresh) with LDR (+ optional LM73)](#labwork-31--dynamic-content-auto-refresh-with-ldr--and-optional-lm73)
- [Labwork 4.1 — First AJAX (Fetch) calling ESP32 for a random value](#labwork-41--first-ajax-fetch-calling-esp32-for-a-random-value)
- [Labwork 5.1 — AJAX endpoints /ldr and /temp (JSON)](#labwork-51--ajax-endpoints-ldr-and-temp-json)
- [Labwork 6.1 — AJAX POST to control LED, with state feedback](#labwork-61--ajax-post-to-control-led-with-state-feedback)
- [Labwork 7.1 — Real-time chart with Chart.js fed by AJAX](#labwork-71--real-time-chart-with-chartjs-fed-by-ajax)
- [Labwork 8.1 — Compare auto-refresh vs AJAX vs Long-Polling](#labwork-81--compare-auto-refresh-vs-ajax-vs-long-polling)
- [Labwork 9.1 — Password-protected AJAX dashboard (HTTP Basic Auth)](#labwork-91--password-protected-ajax-dashboard-http-basic-auth)
- [Labwork 10.1 — Smart Home AJAX Dashboard (capstone)](#labwork-101--smart-home-ajax-dashboard-capstone)
- [Notes & Tips](#notes--tips)
- [License](#license)

---

## Prerequisites
- **Arduino IDE** (or PlatformIO) with **ESP32 board support** (Espressif Systems) installed
- Replace `your_ssid` / `your_password` with your Wi‑Fi credentials
- Open **Serial Monitor** at **115200** baud

## Hardware
- ESP32 dev board
- LDR to **GPIO 34** (ADC) with resistor divider
- (Optional) **LM73** I²C temperature sensor (`0x48` / `0x49`)
- On‑board LED (often **GPIO 2**)

## Setup
1. Create a new sketch for each lab below.
2. Paste the corresponding code block.
3. Flash to your ESP32 and open Serial Monitor to see the device IP.
4. Navigate to the IP from a device on the same network.

---

## Labwork 1.1 — Connect ESP32 to Wi‑Fi & verify IP
```cpp
#include <WiFi.h>
const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("\nConnected!");
  Serial.print("IP: "); Serial.println(WiFi.localIP());
  Serial.println("Open this IP in a browser (no server yet).");
}
void loop() {}
```

---

## Labwork 2.1 — Minimal HTTP Server (“Hello ESP32”)
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";
WebServer server(80);

void handleRoot() {
  server.send(200, "text/html", "<h1>Hello ESP32</h1><p>It works!</p>");
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(); Serial.println(WiFi.localIP());
  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}
void loop() { server.handleClient(); }
```

---

## Labwork 3.1 — Dynamic content (auto-refresh) with LDR (and optional LM73)
```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>   // for LM73 (optional)

const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";
WebServer server(80);

// --- CONFIG ---
const int LDR_PIN = 34; // ADC input
// LM73 typically at 0x48 or 0x49 depending on wiring
const uint8_t LM73_ADDR = 0x48; // change if needed

float readLM73Celsius() {
  // Minimal, safe placeholder (returns 25.0 if not used)
  // Implement actual LM73 I2C read if you wire it.
  // Example sketch references available from sensor docs.
  return 25.0;
}

String page() {
  int ldr = analogRead(LDR_PIN);
  float tempC = readLM73Celsius();
  String html = 
    "<!DOCTYPE html><html><head><meta http-equiv='refresh' content='5'>"
    "<meta name='viewport' content='width=device-width,initial-scale=1'>"
    "<title>ESP32 Dynamic</title></head><body>"
    "<h2>ESP32 Dynamic Page</h2>"
    "<p><b>LDR:</b> " + String(ldr) + "</p>"
    "<p><b>Temp (LM73):</b> " + String(tempC,1) + " &deg;C</p>"
    "<small>Auto-refresh every 5s</small>"
    "</body></html>";
  return html;
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(); Serial.println(WiFi.localIP());
  pinMode(LDR_PIN, INPUT);
  Wire.begin(); // if LM73 is used

  server.on("/", [](){ server.send(200, "text/html", page()); });
  server.begin();
}
void loop(){ server.handleClient(); }
```

---

## Labwork 4.1 — First AJAX (Fetch) calling ESP32 for a random value
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";
WebServer server(80);

void handleIndex() {
  String html =
    "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>"
    "<title>AJAX Demo</title></head><body>"
    "<h2>AJAX Random</h2>"
    "<button id='btn'>Get Random</button>"
    "<p id='out'>...</p>"
    "<script>"
    "document.getElementById('btn').onclick=async()=>{"
      "let r=await fetch('/rand');"
      "let t=await r.text();"
      "document.getElementById('out').innerText=t;"
    "};"
    "</script></body></html>";
  server.send(200, "text/html", html);
}
void handleRand() {
  long v = random(0,1000);
  server.send(200, "text/plain", String(v));
}

void setup(){
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(); Serial.println(WiFi.localIP());
  randomSeed(esp_timer_get_time());
  server.on("/", handleIndex);
  server.on("/rand", handleRand);
  server.begin();
}
void loop(){ server.handleClient(); }
```

---

## Labwork 5.1 — AJAX endpoints `/ldr` and `/temp` (JSON)
```cpp
#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>

const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";
WebServer server(80);

const int LDR_PIN = 34;
float readTempC(){ return 25.0; } // stub or implement sensor read

void handlePage(){
  String html =
    "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>"
    "<title>AJAX Multi</title></head><body>"
    "<h2>AJAX Multi-Sensor</h2>"
    "<p>LDR: <span id='ldr'>-</span></p>"
    "<p>Temp: <span id='temp'>-</span> &deg;C</p>"
    "<script>"
    "async function tick(){"
      "let a=await fetch('/ldr'); let l=await a.json();"
      "let b=await fetch('/temp'); let t=await b.json();"
      "document.getElementById('ldr').textContent=l.value;"
      "document.getElementById('temp').textContent=t.value.toFixed(1);"
    "}"
    "setInterval(tick,1000); tick();"
    "</script></body></html>";
  server.send(200, "text/html", html);
}
void handleLdr(){ int v=analogRead(LDR_PIN); server.send(200,"application/json","{\"value\":"+String(v)+"}"); }
void handleTemp(){ float t=readTempC(); server.send(200,"application/json","{\"value\":"+String(t,2)+"}"); }

void setup(){
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID, WIFI_PASS); while(WiFi.status()!=WL_CONNECTED){delay(500);Serial.print(".");}
  Serial.println(); Serial.println(WiFi.localIP());
  pinMode(LDR_PIN, INPUT);
  Wire.begin();
  server.on("/", handlePage);
  server.on("/ldr", handleLdr);
  server.on("/temp", handleTemp);
  server.begin();
}
void loop(){ server.handleClient(); }
```

---

## Labwork 6.1 — AJAX POST to control LED, with state feedback
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";
WebServer server(80);

const int LED_PIN = 2; // builtin on many ESP32 boards
bool ledState = false;

void handleIndex(){
  String html =
    "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>"
    "<title>AJAX Control</title></head><body>"
    "<h2>LED Control (AJAX POST)</h2>"
    "<button onclick='sendCmd(true)'>ON</button> "
    "<button onclick='sendCmd(false)'>OFF</button>"
    "<p>State: <span id='s'>-</span></p>"
    "<script>"
    "async function refresh(){"
      "let r=await fetch('/state'); let j=await r.json();"
      "document.getElementById('s').textContent=j.on?'ON':'OFF';"
    "}"
    "async function sendCmd(on){"
      "let r=await fetch('/led',{method:'POST',headers:{'Content-Type':'text/plain'},body:(on?'on':'off')});"
      "await r.text(); refresh();"
    "}"
    "refresh(); setInterval(refresh,1000);"
    "</script></body></html>";
  server.send(200,"text/html",html);
}

void handlePostLed(){
  String body = server.arg("plain"); // "on" or "off"
  if(body=="on"){ ledState=true; digitalWrite(LED_PIN, HIGH); }
  else if(body=="off"){ ledState=false; digitalWrite(LED_PIN, LOW); }
  server.send(200,"text/plain","OK");
}
void handleState(){
  server.send(200,"application/json", String("{\"on\":") + (ledState?"true":"false") + "}");
}

void setup(){
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT); digitalWrite(LED_PIN, LOW);
  WiFi.begin(WIFI_SSID, WIFI_PASS); while(WiFi.status()!=WL_CONNECTED){delay(500);Serial.print(".");}
  Serial.println(); Serial.println(WiFi.localIP());
  server.on("/", handleIndex);
  server.on("/state", handleState);
  server.on("/led", HTTP_POST, handlePostLed);
  server.begin();
}
void loop(){ server.handleClient(); }
```

---

## Labwork 7.1 — Real-time chart with Chart.js fed by AJAX
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";
WebServer server(80);

const int LDR_PIN = 34;
const int BUF = 100;
uint16_t ring[BUF]; int rp=0; unsigned long lastSample=0;

void sample(){
  if(millis()-lastSample >= 1000){
    lastSample = millis();
    ring[rp] = analogRead(LDR_PIN);
    rp = (rp+1)%BUF;
  }
}
String jsonSeries(){
  String s="["; 
  for(int i=0;i<BUF;i++){
    int idx=(rp+i)%BUF; s+=String(ring[idx]); if(i<BUF-1)s+=",";
  }
  s+="]"; return s;
}

void handlePage(){
  String html =
    "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>"
    "<title>AJAX Chart</title></head><body>"
    "<h2>LDR Chart (AJAX)</h2>"
    "<canvas id='c' width='360' height='200'></canvas>"
    "<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>"
    "<script>"
    "let ctx=document.getElementById('c').getContext('2d');"
    "let data={labels:[...Array(100).keys()],datasets:[{label:'LDR',data:[],borderWidth:1,fill:false}]} ;"
    "let ch=new Chart(ctx,{type:'line',data:data,options:{animation:false,scales:{y:{beginAtZero:true}}}});"
    "async function tick(){let r=await fetch('/data'); let j=await r.json(); ch.data.datasets[0].data=j; ch.update();}"
    "setInterval(tick,2000); tick();"
    "</script></body></html>";
  server.send(200,"text/html",html);
}
void handleData(){ server.send(200,"application/json", jsonSeries()); }

void setup(){
  Serial.begin(115200);
  pinMode(LDR_PIN, INPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASS); while(WiFi.status()!=WL_CONNECTED){delay(500);Serial.print(".");}
  Serial.println(); Serial.println(WiFi.localIP());
  for(int i=0;i<BUF;i++) ring[i]=0;
  server.on("/", handlePage);
  server.on("/data", handleData);
  server.begin();
}
void loop(){ sample(); server.handleClient(); }
```

---

## Labwork 8.1 — Compare auto-refresh vs AJAX vs Long-Polling
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";
WebServer server(80);

const int LDR_PIN = 34;
volatile uint16_t latest = 0;
unsigned long last = 0;

void sample(){
  if(millis()-last >= 1000){
    last=millis();
    latest = analogRead(LDR_PIN);
  }
}

void p_root(){
  String h =
    "<!DOCTYPE html><html><body>"
    "<h2>Compare Methods</h2>"
    "<ul>"
    "<li><a href='/refresh'>Auto Refresh Page</a></li>"
    "<li><a href='/ajax'>AJAX Interval</a></li>"
    "<li><a href='/longpoll'>Long Polling</a></li>"
    "</ul></body></html>";
  server.send(200,"text/html",h);
}

void p_refresh(){
  String html = String("<!DOCTYPE html><html><head><meta http-equiv='refresh' content='5'></head><body>") +
    "<h3>Auto Refresh every 5s</h3><p>LDR: " + String(latest) + "</p></body></html>";
  server.send(200,"text/html",html);
}

void p_ajax(){
  String h =
    "<!DOCTYPE html><html><body><h3>AJAX every 1s</h3>"
    "<p id='v'>-</p>"
    "<script>setInterval(async()=>{let r=await fetch('/val');document.getElementById('v').innerText=await r.text();},1000);</script>"
    "</body></html>";
  server.send(200,"text/html",h);
}
void p_val(){ server.send(200,"text/plain", String(latest)); }

void p_longpoll(){
  String h =
    "<!DOCTYPE html><html><body><h3>Long Poll</h3>"
    "<p id='v'>-</p>"
    "<script>"
    "async function loop(){"
      "try{ let r=await fetch('/poll'); let t=await r.text(); document.getElementById('v').innerText=t; }"
      "catch(e){} finally{ loop(); }"
    "}"
    "loop();"
    "</script></body></html>";
  server.send(200,"text/html",h);
}

void p_poll(){
  // Very simple long-poll (blocks handler up to ~20s)
  uint16_t startVal = latest;
  unsigned long start = millis();
  while(millis()-start < 20000){
    if(latest != startVal) break;
    delay(100);
  }
  server.send(200,"text/plain", String(latest));
}

void setup(){
  Serial.begin(115200);
  pinMode(LDR_PIN, INPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASS); while(WiFi.status()!=WL_CONNECTED){delay(500);Serial.print(".");}
  Serial.println(); Serial.println(WiFi.localIP());
  server.on("/", p_root);
  server.on("/refresh", p_refresh);
  server.on("/ajax", p_ajax);
  server.on("/val", p_val);
  server.on("/longpoll", p_longpoll);
  server.on("/poll", p_poll);
  server.begin();
}
void loop(){ sample(); server.handleClient(); }
```

---

## Labwork 9.1 — Password-protected AJAX dashboard (HTTP Basic Auth)
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID = "your_ssid";
const char* WIFI_PASS = "your_password";
WebServer server(80);

const char* USER="admin";
const char* PASS="esp32";
const int LDR_PIN=34;

bool checkAuth(){
  if(!server.authenticate(USER, PASS)){
    server.requestAuthentication(); // browser will prompt
    return false;
  }
  return true;
}

void page(){
  String h =
    "<!DOCTYPE html><html><body>"
    "<h2>Protected AJAX Dashboard</h2>"
    "<p>LDR: <span id='v'>-</span></p>"
    "<script>setInterval(async()=>{let r=await fetch('/ldr');let j=await r.json();document.getElementById('v').innerText=j.value;},1000);</script>"
    "</body></html>";
  server.send(200,"text/html",h);
}
void handleRoot(){
  if(!checkAuth()) return;
  page();
}
void handleLdr(){
  if(!checkAuth()) return;
  int v=analogRead(LDR_PIN);
  server.send(200,"application/json", String("{\"value\":")+v+"}");
}

void setup(){
  Serial.begin(115200);
  pinMode(LDR_PIN, INPUT);
  WiFi.begin(WIFI_SSID, WIFI_PASS); while(WiFi.status()!=WL_CONNECTED){delay(500);Serial.print(".");}
  Serial.println(); Serial.println(WiFi.localIP());
  server.on("/", handleRoot);
  server.on("/ldr", handleLdr);
  server.begin();
}
void loop(){ server.handleClient(); }
```

---

## Labwork 10.1 — Smart Home AJAX Dashboard (capstone)
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* WIFI_SSID="your_ssid";
const char* WIFI_PASS="your_password";
WebServer server(80);

// Auth
const char* USER="admin";
const char* PASS="esp32";

// I/O
const int LDR_PIN=34;
const int LED_PIN=2;
bool ledOn=false;

// Chart buffer
const int N=120; // 2 minutes @ 1s
uint16_t buf[N]; int bp=0; unsigned long lastS=0;

bool checkAuth(){
  if(!server.authenticate(USER,PASS)){ server.requestAuthentication(); return false; }
  return true;
}
void sample(){
  if(millis()-lastS>=1000){
    lastS=millis();
    buf[bp]=analogRead(LDR_PIN);
    bp=(bp+1)%N;
  }
}
String jsonSeries(){
  String s="[";
  for(int i=0;i<N;i++){ int idx=(bp+i)%N; s+=String(buf[idx]); if(i<N-1)s+=","; }
  s+="]"; return s;
}

void page(){
  String html =
  "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'><title>Smart Home</title></head><body>"
  "<h2>Smart Home (Protected)</h2>"
  "<p>LDR: <span id='ldr'>-</span></p>"
  "<p>LED: <span id='led'>-</span></p>"
  "<button onclick='cmd(true)'>LED ON</button> <button onclick='cmd(false)'>LED OFF</button>"
  "<h3>LDR Trend</h3><canvas id='c' width='360' height='200'></canvas>"
  "<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>"
  "<script>"
  "let ctx=document.getElementById('c').getContext('2d');"
  "let ch=new Chart(ctx,{type:'line',data:{labels:[...Array(120).keys()],datasets:[{label:'LDR',data:[],borderWidth:1,fill:false}]},options:{animation:false,scales:{y:{beginAtZero:true}}}});"
  "async function refresh(){"
    "let a=await fetch('/ldr'); let l=await a.json(); document.getElementById('ldr').textContent=l.value;"
    "let b=await fetch('/state'); let s=await b.json(); document.getElementById('led').textContent=s.on?'ON':'OFF';"
    "let d=await fetch('/series'); let arr=await d.json(); ch.data.datasets[0].data=arr; ch.update();"
  "}"
  "async function cmd(on){ await fetch('/led',{method:'POST',headers:{'Content-Type':'text/plain'},body:(on?'on':'off')}); refresh(); }"
  "setInterval(refresh,2000); refresh();"
  "</script></body></html>";
  server.send(200,"text/html",html);
}

void handleRoot(){ if(!checkAuth()) return; page(); }
void handleLdr(){ if(!checkAuth()) return; int v=analogRead(LDR_PIN); server.send(200,"application/json", String("{\"value\":")+v+"}"); }
void handleSeries(){ if(!checkAuth()) return; server.send(200,"application/json", jsonSeries()); }
void handleState(){ if(!checkAuth()) return; server.send(200,"application/json", String("{\"on\":")+(ledOn?"true":"false")+"}"); }
void handleLed(){
  if(!checkAuth()) return;
  String body=server.arg("plain");
  if(body=="on"){ ledOn=true; digitalWrite(LED_PIN,HIGH); }
  else if(body=="off"){ ledOn=false; digitalWrite(LED_PIN,LOW); }
  server.send(200,"text/plain","OK");
}

void setup(){
  Serial.begin(115200);
  pinMode(LDR_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT); digitalWrite(LED_PIN, LOW);
  for(int i=0;i<N;i++) buf[i]=0;

  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while(WiFi.status()!=WL_CONNECTED){ delay(500); Serial.print("."); }
  Serial.println(); Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.on("/ldr", handleLdr);
  server.on("/series", handleSeries);
  server.on("/state", handleState);
  server.on("/led", HTTP_POST, handleLed);
  server.begin();
}
void loop(){ sample(); server.handleClient(); }
```

---

## Notes & Tips
- **Security:** Basic Auth is fine for labs. For production, prefer TLS termination via reverse proxy or ESP32 HTTPS (higher RAM usage).
- **AJAX POST parsing:** `server.arg("plain")` is used for simple payloads. For JSON, add a parser or parse manually.
- **Chart.js via CDN:** Keep your client online. To go offline, serve the library locally from SPIFFS/LittleFS.

## License
MIT — use freely for classes and personal projects.


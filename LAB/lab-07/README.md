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
| LDR + 10kΩ divider | LDR→3.3V, junction→**GPIO 36**, resistor→GND |
| LM73 (I²C) | SDA→**GPIO 4**, SCL→**GPIO 5**, VCC→3.3V, GND→GND |

## 4. Software Requirements
- Arduino IDE (ESP32 core)
- Libraries: `WiFi.h`, `WebServer.h`, `Wire.h`

## ✅ Pre-requisites
- Basic Arduino IDE programming.  
- Understanding of HTTP protocol, HTML, CSS, and JavaScript.  
- Familiarity with ESP32 programming.  

---

## 🌐 Example: Simple HTML Page
```html
<!DOCTYPE html>
<html>
<head>
  <title>Hello World</title>
</head>
<body>
  <h1>Hello World</h1>
</body>
</html>
```

---
## 5. Code Implementation
### 5.1 Simple HTTP Web Server 
```cpp
#include <WiFi.h>

// Replace with your network credentials
const char* ssid = "coc-iot-lab";
const char* password = "computing";

// Set the server to listen on port 80
WiFiServer server(80);

void setup() {
  // Start serial communication for debugging
  Serial.begin(115200);

  // Connect to Wi-Fi
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());  // Output the ESP32 IP address

  // Start the HTTP server
  server.begin();
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client Connected");

    String request = client.readStringUntil('\r');
    Serial.println(request);
    client.flush();

    // Respond with HTML page
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("Connection: close");
    client.println();
    client.println("<!DOCTYPE html>");
    client.println("<html>");
    client.println("<head><title>ESP32 Web Server</title></head>");
    client.println("<body style='font-family: Arial; text-align: center;'>");
    client.println("<h1>Hello World from ESP32</h1>");
    client.println("<p>This is a simple ESP32 web server example.</p>");
    client.println("</body>");
    client.println("</html>");

    // Close the connection
    client.stop();
    Serial.println("Client Disconnected");
  }
}

```
---
### 5.2 HTTP Web Server with AJAX
```cpp
#include <WiFi.h>
#include <Wire.h>

// Replace these with your network credentials
const char* ssid = "iot-lab";
const char* password = "computing";

// Set the LM73 I2C address
#define LM73_ADDRESS 0x4D // Default LM73 address

#define SDA1_PIN 4   // SDA1 connected to GPIO 4
#define SCL1_PIN 5   // SCL1 connected to GPIO 5

WiFiServer server(80);  // Create a web server on port 80

int ledPin = 2;  // GPIO pin to control the LED

void setup() {
  // Start serial communication for debugging
  Serial.begin(115200);

  // Set up the LED pin
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);  // Initially turn off the LED

  // Start the I2C communication for LM73 sensor
  Wire.begin(SDA1_PIN, SCL1_PIN);
  // Wait for sensor stabilization
   delay(100);

  // Connect to Wi-Fi network
  WiFi.begin(ssid, password);
  Serial.println("Connecting to Wi-Fi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Start the web server
  server.begin();
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client Connected");
    String currentLine = "";

    // Handle client requests
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        currentLine += c;

        // Check if the request ends with a newline
        if (c == '\n') {
          // Control the LED based on the URL
          if (currentLine.indexOf("GET /LED=ON") >= 0) {
            digitalWrite(ledPin, HIGH);  // Turn on the LED
            Serial.println("LED ON");
          }
          if (currentLine.indexOf("GET /LED=OFF") >= 0) {
            digitalWrite(ledPin, LOW);   // Turn off the LED
            Serial.println("LED OFF");
          }

          // Serve the HTML page
          client.println("HTTP/1.1 200 OK");
          client.println("Content-Type: text/html");
          client.println();
          client.println("<!DOCTYPE HTML>");
          client.println("<html>");
          client.println("<h1>ESP32 Web Server</h1>");
          client.println("<p><a href=\"/LED=ON\">Turn LED ON</a></p>");
          client.println("<p><a href=\"/LED=OFF\">Turn LED OFF</a></p>");
          client.println("<p>Temperature: <span id='temp'></span> &deg;C</p>");
          client.println("<script>");
          client.println("setInterval(function() {");
          client.println("var xhttp = new XMLHttpRequest();");
          client.println("xhttp.onreadystatechange = function() {");
          client.println("if (this.readyState == 4 && this.status == 200) {");
          client.println("document.getElementById('temp').innerHTML = this.responseText;");
          client.println("}};");
          client.println("xhttp.open('GET', '/temp', true);");
          client.println("xhttp.send();");
          client.println("}, 1000);");  // Update temperature every second
          client.println("</script>");
          client.println("</html>");
          break;
        }
      }
    }

    // Handle temperature reading request (via AJAX)
    if (currentLine.indexOf("GET /temp") >= 0) {
      float temperature = readTemperatureLM73();  // Get temperature from LM73 sensor
      client.print(temperature);
    }

    // Close the connection
    client.stop();
    Serial.println("Client Disconnected.");
  }
}

// Function to read temperature from LM73 sensor
float readTemperatureLM73() {
  Wire.beginTransmission(LM73_ADDRESS);
  Wire.write(0x00);  // Request temperature register
  Wire.endTransmission();
  Wire.requestFrom(LM73_ADDRESS, 2);

  if (Wire.available() == 2) {
    uint8_t msb = Wire.read();  // Most significant byte
    uint8_t lsb = Wire.read();  // Least significant byte

    int16_t rawTemperature = (msb << 8) | lsb;  // Combine MSB and LSB
    float temperature =(rawTemperature >>= 2)* 0.03125;
    Serial.println(temperature);
    return temperature;
  }
  return -999.0;  // Error value if sensor is not available
}
```
---
### 5.3 Fixing HTTP Web Server with AJAX
```cpp
#include <WiFi.h>
#include <Wire.h>

// Wi-Fi
const char* ssid     = "coc-iot-lab";
const char* password = "computing";

// LM73 (I2C)
#define LM73_ADDRESS 0x4D
#define SDA1_PIN 4
#define SCL1_PIN 5

// LED
const int ledPin = 2;

// HTTP
WiFiServer server(80);

// ---------- HTML page (served once per request) ----------
const char PAGE[] PROGMEM = R"HTML(
<!DOCTYPE HTML>
<html>
<head>
  <meta charset="utf-8"/>
  <title>ESP32 Web Server</title>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <style>
    body { font-family:sans-serif; text-align:center; margin-top:32px; }
    a { display:inline-block; margin:8px 0; }
  </style>
</head>
<body>
  <h1>ESP32 Web Server</h1>
  <p><a href="/LED=ON">Turn LED ON</a></p>
  <p><a href="/LED=OFF">Turn LED OFF</a></p>
  <p>Temperature: <span id="temp">--</span> &deg;C</p>
  <script>
    setInterval(function() {
      var x = new XMLHttpRequest();
      x.onreadystatechange = function() {
        if (this.readyState === 4 && this.status === 200) {
          document.getElementById('temp').textContent = this.responseText;
        }
      };
      x.open('GET', '/temp', true);
      x.send();
    }, 1000);
  </script>
</body>
</html>
)HTML";

// ---------- LM73 read ----------
float readTemperatureLM73() {
  // Request temperature register (0x00)
  Wire.beginTransmission(LM73_ADDRESS);
  Wire.write(0x00);
  Wire.endTransmission();

  Wire.requestFrom(LM73_ADDRESS, 2);
  if (Wire.available() == 2) {
    uint8_t msb = Wire.read();
    uint8_t lsb = Wire.read();

    // LM73 temperature format: use your original method
    // raw >> 2 then * 0.03125 °C (0.03125 = 1/32)
    int16_t raw = (int16_t)((msb << 8) | lsb);
    raw >>= 2; // keep sign
    float temperature = raw * 0.03125f;

    // Debug (optional)
    // Serial.printf("LM73 raw=0x%04X -> %0.2f C\n", (msb<<8)|lsb, temperature);
    return temperature;
  }
  return -999.0f; // error
}

// ---------- HTTP helpers ----------
void sendHtmlPage(WiFiClient &client) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html; charset=utf-8");
  client.println("Cache-Control: no-store");
  client.println("Connection: close");
  client.println();
  client.print(PAGE);
}

void sendText(WiFiClient &client, const String &txt) {
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/plain; charset=utf-8");
  client.println("Cache-Control: no-store");
  client.println("Connection: close");
  client.println();
  client.print(txt);
}

void setup() {
  Serial.begin(115200);

  // LED
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // I2C
  Wire.begin(SDA1_PIN, SCL1_PIN);
  delay(100);

  // Wi-Fi
  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nConnected. IP: %s\n", WiFi.localIP().toString().c_str());

  // HTTP
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  Serial.println("New client");

  String requestLine;
  String headers;
  unsigned long t0 = millis();

  // Read request headers until blank line
  while (client.connected() && millis() - t0 < 2000) {
    if (!client.available()) continue;
    String line = client.readStringUntil('\n');
    if (line == "\r" || line.length() == 1) { // blank line = end of headers
      break;
    }
    if (requestLine.length() == 0) requestLine = line; // first line
    headers += line;
  }

  // Log first line for debug
  Serial.print("REQ: "); Serial.println(requestLine);

  // Very simple routing based on request line or headers
  // Handle AJAX temperature endpoint first
  if (requestLine.indexOf("GET /temp") >= 0) {
    float t = readTemperatureLM73();
    sendText(client, String(t, 2));
    client.stop();
    Serial.println("Served /temp");
    return;
  }

  // LED control
  if (requestLine.indexOf("GET /LED=ON") >= 0) {
    digitalWrite(ledPin, HIGH);
  } else if (requestLine.indexOf("GET /LED=OFF") >= 0) {
    digitalWrite(ledPin, LOW);
  }

  // Ignore browser favicon requests to avoid extra page sends
  if (requestLine.indexOf("GET /favicon.ico") >= 0) {
    client.println("HTTP/1.1 204 No Content");
    client.println("Connection: close");
    client.println();
    client.stop();
    Serial.println("No content for favicon");
    return;
  }

  // Serve the HTML page once per request
  sendHtmlPage(client);
  client.stop();
  Serial.println("Client disconnected");
}
```
---
<!--
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
-->
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


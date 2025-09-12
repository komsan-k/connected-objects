# ESP32 Web Server with LED Control

## 📖 Overview
This project demonstrates how to set up an **ESP32 web server** to control an LED over Wi-Fi.  
When a client connects to the ESP32's IP address in a web browser, they can click links to turn the LED **ON** or **OFF**.

---

## 🛠 Requirements
- ESP32 Development Board  
- Arduino IDE (with ESP32 board support installed)  
- Wi-Fi network (SSID & password)  
- LED + 220Ω resistor  
- Breadboard and jumper wires  

---

## ⚙️ Circuit Setup
- Connect the **LED anode** to **GPIO 2** through a resistor.  
- Connect the **LED cathode** to **GND**.  

---

## 💻 Code 1
```cpp
#include <WiFi.h>

// Replace these with your WiFi credentials
const char* ssid = "coc-iot-lab";
const char* password = "computing";

WiFiServer server(80);  // Create a web server on port 80

int ledPin = 2;  // GPIO 2 where the LED is connected

void setup() {
  // Initialize serial communication
  Serial.begin(115200);

  // Set the LED pin as output
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);  // Initially turn off the LED

  // Connect to Wi-Fi
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println(".");
  }
  Serial.println("Connected to WiFi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Start the server
  server.begin();
}

void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (client) {
    Serial.println("New Client Connected");
    String currentLine = "";

    while (client.connected()) {
      if (client.available()) {
        char c = client.read();
        currentLine += c;

        // Check if the request ends with a newline
        if (c == '\n') {
          // Control the LED based on the URL
          if (currentLine.indexOf("GET /LED=ON") >= 0) {
            digitalWrite(ledPin, HIGH);  // Turn on LED
            Serial.println("LED ON");
          }
          if (currentLine.indexOf("GET /LED=OFF") >= 0) {
            digitalWrite(ledPin, LOW);   // Turn off LED
            Serial.println("LED OFF");
          }

          // Send the HTML response to the client
          client.println("HTTP/1.1 200 OK");
          client.println("Content-type:text/html");
          client.println();
          client.println("<html><body>");
          client.println("<h1>ESP32 Web Server</h1>");
          client.println("<p><a href=\"/LED=ON\">Turn LED ON</a></p>");
          client.println("<p><a href=\"/LED=OFF\">Turn LED OFF</a></p>");
          client.println("</body></html>");
          break;
        }
      }
    }
    client.stop();
    Serial.println("Client Disconnected");
  }
}
```

---
## 💻 Code 2

```cpp
#include <WiFi.h>

// WiFi credentials
 

// LED pin
const int LED_PIN = 2;

// HTTP server
WiFiServer server(80);

// ----------- HTML (served once per page request) -----------
const char PAGE[] PROGMEM = R"HTML(
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>ESP32 LED Control</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body{font-family:Arial,Helvetica,sans-serif;text-align:center;margin-top:48px}
    .wrap{display:inline-block;padding:16px 24px;border:1px solid #ddd;border-radius:10px}
    label{font-size:18px}
    input[type=checkbox]{transform:scale(1.5);margin-left:10px;vertical-align:middle}
    .hint{color:#666;margin-top:12px;font-size:14px}
  </style>
</head>
<body>
  <div class="wrap">
    <h1>ESP32 Web Server</h1>
    <label>LED
      <input id="led" type="checkbox">
    </label>
    <div class="hint">Toggle the checkbox to switch the LED ON/OFF</div>
  </div>

  <script>
    const led = document.getElementById('led');

    // Load initial state
    function loadState() {
      fetch('/state', {cache:'no-store'})
        .then(r => r.text())
        .then(t => { led.checked = (t.trim() === '1'); })
        .catch(console.error);
    }

    // Send new state when toggled
    led.addEventListener('change', () => {
      const val = led.checked ? 1 : 0;
      fetch('/led?on=' + val, {cache:'no-store'})
        .then(_ => {})   // ignore response body
        .catch(console.error);
    });

    // Initial sync on page load, and refresh occasionally
    loadState();
    setInterval(loadState, 5000);
  </script>
</body>
</html>
)HTML";

// ------------ Small helpers ------------
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

void sendNoContent(WiFiClient &client) {
  client.println("HTTP/1.1 204 No Content");
  client.println("Connection: close");
  client.println();
}

// ------------ WiFi + setup ------------
void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.print("\nIP: "); Serial.println(WiFi.localIP());

  server.begin();
}

// ------------ Simple query parser ------------
int getQueryValue(const String& line, const String& key) {
  // expects first line like: "GET /led?on=1 HTTP/1.1"
  int qpos = line.indexOf('?');
  if (qpos < 0) return -1;
  int sp   = line.indexOf(' ', qpos);
  String qs = line.substring(qpos + 1, sp < 0 ? line.length() : sp);
  // split on '&'
  int start = 0;
  while (start >= 0) {
    int amp = qs.indexOf('&', start);
    String pair = (amp < 0) ? qs.substring(start) : qs.substring(start, amp);
    int eq = pair.indexOf('=');
    if (eq > 0) {
      String k = pair.substring(0, eq);
      String v = pair.substring(eq + 1);
      if (k == key) return v.toInt();
    }
    start = (amp < 0) ? -1 : amp + 1;
  }
  return -1;
}

// ------------ Main loop / HTTP handling ------------
void loop() {
  WiFiClient client = server.available();
  if (!client) return;

  Serial.println("New client");
  String requestLine;
  unsigned long t0 = millis();

  // Read request headers until blank line
  while (client.connected() && millis() - t0 < 2000) {
    if (!client.available()) continue;
    String line = client.readStringUntil('\n');
    if (requestLine.length() == 0) requestLine = line; // first line
    if (line == "\r" || line.length() == 1) break;     // end of headers
  }

  // Route handling (based on the first line only)
  // 1) AJAX state request
  if (requestLine.indexOf("GET /state") >= 0) {
    int state = digitalRead(LED_PIN) ? 1 : 0;
    sendText(client, String(state));
    client.stop();
    Serial.println("Served /state");
    return;
  }

  // 2) LED control via checkbox: /led?on=0|1
  if (requestLine.indexOf("GET /led?") >= 0) {
    int val = getQueryValue(requestLine, "on");
    if (val == 0 || val == 1) {
      digitalWrite(LED_PIN, val ? HIGH : LOW);
      Serial.printf("LED -> %s\n", val ? "ON" : "OFF");
      sendNoContent(client); // no body needed
      client.stop();
      return;
    }
  }

  // 3) Favicon: avoid extra page sends by returning no content
  if (requestLine.indexOf("GET /favicon.ico") >= 0) {
    sendNoContent(client);
    client.stop();
    return;
  }

  // 4) Default: serve the checkbox page once
  sendHtmlPage(client);
  client.stop();
  Serial.println("Client disconnected");
}

```
---

## 🚦 Usage
1. Upload the sketch to ESP32 using Arduino IDE.  
2. Open the **Serial Monitor** at 115200 baud.  
3. Copy the **ESP32 IP address** shown after connecting to Wi-Fi.  
4. Open the IP in your web browser.  
5. Click **Turn LED ON** or **Turn LED OFF** to control the LED.  

---

## 📌 Notes
- Default LED pin is **GPIO 2**, but you can change it in the code.  
- Ensure your ESP32 and PC/phone are connected to the same Wi-Fi network.  
- Works with any browser (Chrome, Edge, Firefox, etc.).  


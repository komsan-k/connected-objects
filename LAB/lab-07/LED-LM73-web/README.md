# ESP32 Web Server with LM73 Sensor

## 📖 Overview
This project demonstrates how to set up an **ESP32 HTTP web server** with an LM73 temperature sensor.  
The system provides:
- **LED control** (ON/OFF) via a web interface.  
- **Real-time temperature monitoring** using AJAX.  
- **Modular code organization** by separating HTML/JS into a `webpage.h` file.  

---

## 🛠 Requirements
- ESP32 Development Board  
- LM73 Temperature Sensor (I²C)  
- Arduino IDE with ESP32 board package installed  
- Wi-Fi network credentials (SSID & Password)  
- Breadboard and jumper wires  
- LED + resistor  

---

## ⚙️ File Structure
- **`webpage.h`** → Contains HTML, CSS, and JavaScript for the web interface.  
- **`main.ino`** → ESP32 main code handling Wi-Fi, web server, I²C sensor communication.  

---

## 💻 Code

### webpage.h
```cpp
const char MAIN_page[] PROGMEM = R"=====(
<!DOCTYPE html>
<html>
<head>
  <title>ESP32 Web Server</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: Arial; text-align: center; margin-top: 50px; }
    .button { padding: 15px 30px; font-size: 16px; margin: 10px; cursor: pointer; }
    .on { background-color: #4CAF50; color: white; }
    .off { background-color: #f44336; color: white; }
    .data { font-size: 24px; color: #333; }
  </style>
</head>
<body>
  <h1>ESP32 Web Server with LM73 Sensor</h1>
  <p><button class="button on" onclick="toggleLED('ON')">Turn LED ON</button></p>
  <p><button class="button off" onclick="toggleLED('OFF')">Turn LED OFF</button></p>
  <h3>Temperature: <span id="temperature">--</span> &deg;C</h3>
  <script>
    function toggleLED(state) {
      var xhttp = new XMLHttpRequest();
      xhttp.open("GET", "/LED=" + state, true);
      xhttp.send();
    }
    setInterval(function() {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          document.getElementById("temperature").innerHTML = this.responseText;
        }
      };
      xhttp.open("GET", "/temp", true);
      xhttp.send();
    }, 1000);  // Update temperature every second
  </script>
</body>
</html>
)=====";
```

### ESP32 Main Code
```cpp
#include <WiFi.h>
#include <Wire.h>
#include "webpage.h"

// Replace with your Wi-Fi credentials
const char* ssid = "your_SSID";
const char* password = "your_PASSWORD";

// LM73 I2C address
#define LM73_ADDRESS 0x48

WiFiServer server(80);  
int ledPin = 2;  // LED on GPIO 2

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
  Wire.begin();

  Serial.println("Connecting to Wi-Fi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String request = client.readStringUntil('\r');
    Serial.print("Client Request: ");
    Serial.println(request);

    if (request.indexOf("GET /LED=ON") >= 0) {
      digitalWrite(ledPin, HIGH);
    } else if (request.indexOf("GET /LED=OFF") >= 0) {
      digitalWrite(ledPin, LOW);
    }

    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("Connection: close");
    client.println();
    client.println(MAIN_page);

    if (request.indexOf("GET /temp") >= 0) {
      float temperature = readTemperatureLM73();
      client.print(temperature);
    }
    client.stop();
  }
}

float readTemperatureLM73() {
  Wire.beginTransmission(LM73_ADDRESS);
  Wire.write(0x00);
  Wire.endTransmission();
  Wire.requestFrom(LM73_ADDRESS, 2);
  if (Wire.available() == 2) {
    uint8_t msb = Wire.read();
    uint8_t lsb = Wire.read();
    int16_t rawTemperature = (msb << 8) | lsb;
    return rawTemperature / 128.0;
  }
  return -999.0;
}
```

---

## 🚦 Features
- Control LED (ON/OFF) from browser.  
- Real-time temperature monitoring via AJAX (no page refresh).  
- Separation of logic (`main.ino`) and interface (`webpage.h`).  

---

## 📌 Steps to Run
1. Create a **new Arduino project**.  
2. Add `webpage.h` with the provided HTML/JS.  
3. Upload the main code to ESP32.  
4. Open Serial Monitor → copy the ESP32 IP address.  
5. Open the IP in a web browser to control the LED and monitor temperature.  


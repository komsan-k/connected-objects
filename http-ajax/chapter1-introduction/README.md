# Introduction to HTTP and ESP32

## Overview
The ESP32 is a powerful, low-cost microcontroller with integrated Wi-Fi and Bluetooth, widely adopted in the Internet of Things (IoT) community. It enables not only embedded control but also communication with external devices, services, and users through the internet.

One of the simplest yet most effective ways to interact with ESP32 is to configure it as a lightweight HTTP server. With this setup, any device with a web browser — laptop, smartphone, or tablet — can access ESP32 dashboards, monitor sensors, and control actuators.

This chapter introduces HTTP concepts, ESP32 networking capabilities, and the foundation for running web servers. It also provides the first set of labworks, guiding students from connecting to Wi-Fi to serving a basic webpage.

## The Evolution of HTTP
- **HTTP/0.9 (1991):** Simple protocol, only supported GET requests and returned plain text.  
- **HTTP/1.0 (1996):** Added headers, status codes, content types.  
- **HTTP/1.1 (1997):** Introduced persistent connections, chunked transfer encoding, and caching.  
- **HTTP/2 (2015):** Binary framing, multiplexing multiple requests, header compression.  
- **HTTP/3 (QUIC-based):** Lower latency, faster reconnections, and enhanced reliability.

ESP32 primarily uses HTTP/1.1 due to lightweight library support.

## ESP32 Networking Stack
- **lwIP (Lightweight IP):** Handles TCP/IP protocols.  
- Modes: Station (STA), Access Point (AP), Hybrid (AP+STA).  
- APIs: TCP, UDP, HTTP, HTTPS.  
- **Constraints:**  
  - RAM: ~520 KB  
  - Flash: ~4 MB  
  - Serving large web pages requires optimization.

## Client–Server Model in IoT
- **Requests:** Method (GET, POST), path, headers.  
- **Responses:** Status code, headers, body (HTML/JSON/text).  
- **TCP/IP Process:** Handshake → Request → Response → Connection handling.

## Applications of ESP32 HTTP Servers
- Sensor monitoring  
- Home automation  
- Educational dashboards  
- Data logging (JSON endpoints)

## Tools and Environment Setup
1. Install Arduino IDE.  
2. Add ESP32 board manager URL.  
3. Install ESP32 board package.  
4. Install drivers (CP2102/CH340 if needed).  
5. Libraries: `WiFi.h`, `WebServer.h`, `ESPAsyncWebServer.h`.

## First Code Example: Connecting to Wi-Fi
```cpp
#include <WiFi.h>

const char* ssid="your_ssid";
const char* password="your_password";

void setup(){
  Serial.begin(115200);
  WiFi.begin(ssid,password);
  Serial.println("Connecting...");
  while(WiFi.status()!=WL_CONNECTED){
    delay(500); Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.println(WiFi.localIP());
}
void loop(){}
```

## Second Code Example: Minimal HTTP Server
```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid="your_ssid";
const char* password="your_password";

WebServer server(80);

void handleRoot(){
  server.send(200,"text/html","<h1>Hello from ESP32!</h1>");
}

void setup(){
  Serial.begin(115200);
  WiFi.begin(ssid,password);
  while(WiFi.status()!=WL_CONNECTED){delay(500);}
  Serial.println(WiFi.localIP());
  server.on("/",handleRoot);
  server.begin();
}
void loop(){ server.handleClient(); }
```

## Extra Debugging and Analysis Tools
- **Browser Developer Tools**: Inspect headers, response time.  
- **Postman**: Test GET/POST requests.  
- **Serial Monitor**: Observe ESP32 logs.

## Labworks
- **Labwork 1.1:** Connect ESP32 to Wi-Fi and verify IP.  
- **Labwork 1.2:** Serve a “Hello World” webpage.  
- **Labwork 1.3:** Debug wrong SSID/password.  
- **Labwork 1.4:** Analyze headers with browser dev tools.  
- **Labwork 1.5:** Serve plain text and JSON.  
- **Labwork 1.6:** Mini-project — Sensor readout via webpage.

## Mini-Project: My First IoT Web Server
- ESP32 connects to Wi-Fi.  
- Serves HTML, text, and JSON endpoints.  
- Displays live sensor readings.

## Summary
- Reviewed HTTP evolution.  
- Introduced ESP32 networking stack.  
- Explained client–server communication.  
- Built first ESP32 HTTP server.  
- Explored debugging tools and labworks.

## Review Questions
1. Trace HTTP evolution from 0.9 to 3.  
2. What is lwIP in ESP32 networking?  
3. Explain client–server communication in IoT.  
4. Why is ESP32 suitable for lightweight web servers?  
5. Compare ESP32 responses: HTML vs JSON.


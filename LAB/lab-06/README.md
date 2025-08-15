# LAB 6 — TCP and UDP Communication

## 1. Objective
This lab demonstrates how to establish TCP and UDP communication between an ESP32 and other devices. You will implement both TCP server/client and UDP sender/receiver functionalities, and extend them to transmit sensor data.

## 2. Background
TCP (Transmission Control Protocol) is a connection-oriented protocol that ensures reliable and ordered data delivery. UDP (User Datagram Protocol) is connectionless and provides faster but unreliable communication.  
Both protocols are useful in IoT — TCP for control/configuration, UDP for lightweight telemetry.

In this lab, we will:
- Build a TCP echo server on ESP32.
- Build a UDP echo server.
- Send and receive JSON-formatted messages.
- Integrate LDR and LM73 sensor data into transmitted packets.

## 3. Hardware Requirements
- ESP32 development board  
- USB cable  
- LDR (Light Dependent Resistor)  
- LM73 temperature sensor (I²C)  
- Resistor for LDR voltage divider  
- Breadboard and jumper wires  
- Wi-Fi network

## 4. Software Requirements
- Arduino IDE with ESP32 board support  
- Wi-Fi network credentials  
- Serial Monitor  
- Optional: `nc` (netcat) or Python for PC-side testing

## 5. Lab Tasks

### Task 1: TCP Server
1. Initialize Wi-Fi connection.
2. Start a TCP server on port 5000.
3. Accept incoming client connections and echo back received messages.

### Task 2: UDP Server
1. Initialize Wi-Fi connection.
2. Start listening for UDP packets on port 6000.
3. Send back an acknowledgment message.

### Task 3: JSON Messaging
1. Wrap TCP/UDP payloads into JSON format.
2. Include message type, timestamp, and data fields.

### Task 4: Sensor Data Integration
1. Read LDR analog value using `analogRead()`.
2. Read LM73 temperature over I²C.
3. Send sensor data over TCP and UDP in JSON format.

Example JSON:
```json
{
  "ldr": 512,
  "temp_c": 24.87
}
```

---

## 6. Example Code

### TCP Server (Basic Example)
```cpp
#include <WiFi.h>

const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";
WiFiServer server(5000);

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    while (client.connected()) {
      while (client.available()) {
        String data = client.readStringUntil('\n');
        Serial.println("Received: " + data);
        client.println("Echo: " + data);
      }
    }
    client.stop();
  }
}
```

### UDP Sender (Basic Example)
```cpp
#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";
WiFiUDP udp;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");
}

void loop() {
  udp.beginPacket("192.168.1.100", 6000);
  udp.print("Hello UDP");
  udp.endPacket();
  delay(1000);
}
```

---

## 7. Exercises
1. Modify the TCP server to handle multiple clients simultaneously.  
2. Implement a UDP broadcast sender.  
3. Add JSON-formatted messages to TCP/UDP packets.  
4. Implement a hybrid system where control commands are sent over TCP and telemetry over UDP.  
5. **Integrate sensory data**:  
   - Read **LDR** (Light Dependent Resistor) analog value.  
   - Read **LM73** temperature in °C.  
   - Send both readings via TCP and UDP in JSON format:  
     ```json
     { "ldr": 512, "temp_c": 24.87 }
     ```
6. Measure packet loss in UDP by sending 100 packets and counting ACKs.

---

## 8. Conclusion
In this lab, you learned how to implement TCP and UDP communication on the ESP32, and how to format messages as JSON for interoperability.  
By integrating sensor data, you demonstrated how IoT devices can transmit telemetry to remote systems using different protocols.



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

## 💻 Code
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


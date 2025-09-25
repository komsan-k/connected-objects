# 🧪 Lab 1: Building a Mobile Messaging App with Thunkable and ESP32 over Wi-Fi

## 1. Objective

The objective of this lab is to design and implement a **simple mobile
chat-style app** using **Thunkable** that communicates with an **ESP32
microcontroller** over Wi-Fi. Students will learn how to: - Configure
the ESP32 as a web server with an HTTP endpoint. - Build a mobile user
interface in Thunkable for text input, display, and feedback. - Send and
receive JSON messages between the app and ESP32. - Validate integration
by observing messages on both the ESP32 Serial Monitor and the app
interface.

## 2. Background

The **ESP32** is a Wi-Fi and Bluetooth-enabled microcontroller widely
used in IoT applications. Mobile app builders like **Thunkable** provide
a visual programming environment for creating iOS/Android apps without
deep coding.

By integrating these tools: - **ESP32** acts as a local server,
receiving and echoing messages. - **Thunkable** serves as the client,
providing an intuitive user interface.\
This combination enables real-time, app-to-device communication suitable
for IoT control, messaging, and monitoring applications.

## 3. Materials

-   ESP32 development board (e.g., ESP32-DevKitC, NodeMCU-32S).\
-   USB cable for programming ESP32.\
-   Computer with Arduino IDE (with ESP32 board support installed).\
-   Smartphone with **Thunkable Live** app (Android/iOS).\
-   Active Wi-Fi network (ESP32 and phone must share the same network).

## 4. Procedure

### Step 1: Flash ESP32 with HTTP Server

``` cpp
#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>

const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";

WebServer server(80);

void handlePostMessage() {
  if (server.method() != HTTP_POST) {
    server.send(405, "application/json", "{\"error\":\"Use POST\"}");
    return;
  }
  String body = server.arg("plain");
  StaticJsonDocument<256> doc;
  if (deserializeJson(doc, body)) {
    server.send(400, "application/json", "{\"error\":\"Bad JSON\"}");
    return;
  }
  const char* text = doc["text"] | "";
  Serial.print("[MSG] "); Serial.println(text);

  StaticJsonDocument<128> res;
  res["status"] = "ok";
  res["echo"] = text;
  String out; serializeJson(res, out);
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "application/json", out);
}

void handleOptions() {
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.sendHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  server.sendHeader("Access-Control-Allow-Headers", "Content-Type");
  server.send(204);
}

void setup() {
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println(); Serial.print("IP: "); Serial.println(WiFi.localIP());

  server.on("/message", HTTP_OPTIONS, handleOptions);
  server.on("/message", HTTP_POST, handlePostMessage);
  server.begin();
  Serial.println("Server started");
}

void loop() { server.handleClient(); }
```

Upload, then check Serial Monitor for ESP32 IP.

### Step 2: Create Thunkable App

1.  Add `TextInput_Message`, `Button_Send`, `List_Chat`, `Label_Status`,
    and `WebAPI_ESP` to the screen.\
2.  Initialize `app chatList = []`.

### Step 3: Thunkable Blocks

-   **Screen Opens** → set `WebAPI_ESP.URL`, update status.\
-   **Button_Send.Click** → build JSON, call `WebAPI_ESP.Post`.\
-   **Post.Success** → append `"echo"` to list, refresh `List_Chat`.\
-   **Post.Error** → append "(failed)" to list.

## 5. Diagrams

### Data Flow

    Thunkable App  ──HTTP POST──▶  ESP32 WebServer
       (JSON text)                (Serial prints message)
    Thunkable App  ◀─HTTP 200──── ESP32 WebServer
       (echo JSON)                 (sends back {"echo":"msg"})

### Sequence of Events

    User types → Tap Send
    App builds JSON → POST /message
    ESP32 parses JSON → prints [MSG]
    ESP32 replies with echo → App shows in List_Chat

## 6. Verification

-   Type "Hello" in the app.\
-   Check Serial Monitor → `[MSG] Hello`.\
-   App shows "Hello" in chat list.

## 7. Exercises

1.  Modify the ESP32 code to toggle an LED whenever a message is
    received.\
2.  Display timestamps in Thunkable chat log.\
3.  Add quick command buttons instead of text input.\
4.  Implement a GET endpoint and test in Thunkable.\
5.  Research using MQTT for multi-user chat.

## 8. Conclusion

This lab demonstrates how a mobile app can communicate with ESP32 using
HTTP and JSON, integrating visual app design (Thunkable) with
microcontroller programming. This workflow is a foundation for IoT apps,
remote control, and real-time monitoring systems.


# LAB 1 — ESP32 Bring-Up & Network Time Protocol (NTP) Integration

## 1. Objectives
By the end of this lab, you will be able to:
1. Set up and verify the ESP32 toolchain in Arduino IDE.
2. Upload a test sketch to blink the onboard LED and print debug messages.
3. Connect the ESP32 to a Wi-Fi network.
4. Retrieve and display the current date and time from an NTP server.
5. Understand the role of NTP in IoT and embedded systems.

---

## 2. Background

The **bring-up** process is the first step in any embedded system project. It involves:
- Verifying the hardware (power, clock, GPIO).
- Testing the development environment (compiler, upload tools).
- Running a minimal application to confirm functionality.

Once the ESP32 is operational, **time synchronization** is often a fundamental requirement in IoT systems.  
Many applications — such as logging, scheduling, security, and data timestamping — rely on accurate time.

The **Network Time Protocol (NTP)** allows devices to synchronize their clocks over the Internet using standardized time servers. On the ESP32, this is typically done via the `configTime()` function, which contacts a pool of NTP servers.

---

## 3. Tasks

### Part A — Basic Bring-Up
1. Install the **ESP32** board package in Arduino IDE via Boards Manager.
2. Select your ESP32 board (e.g., *ESP32 Dev Module*) and correct COM port.
3. Write a minimal sketch to:
   - Initialize Serial communication at **115200 baud**.
   - Blink the onboard LED on **GPIO 2**.
   - Print a startup banner to Serial Monitor.

### Part B — Connect to Wi-Fi
1. Add your Wi-Fi SSID and password.
2. Connect until `WL_CONNECTED`.
3. Print the assigned **local IP address**.

### Part C — Get Time from NTP
1. Use `configTime()` to configure:
   - **GMT offset** in seconds.
   - **Daylight Saving Time (DST)** offset in seconds.
   - NTP server address (e.g., `"pool.ntp.org"`).
2. Wait for time synchronization.
3. Use `getLocalTime()` to retrieve time and display in `YYYY-MM-DD HH:MM:SS` format.

---

## 4. Full Code Example

```cpp
#include <WiFi.h>
#include <time.h>

// Wi-Fi credentials
const char* ssid     = "YOUR_SSID";
const char* password = "YOUR_PASS";

// NTP settings
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 7 * 3600;   // GMT+7 for Thailand
const int   daylightOffset_sec = 0;     // No DST

const int LED_PIN = 2;

void printLocalTime() {
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return;
  }
  Serial.printf("%04d-%02d-%02d %02d:%02d:%02d\n",
                timeinfo.tm_year + 1900,
                timeinfo.tm_mon + 1,
                timeinfo.tm_mday,
                timeinfo.tm_hour,
                timeinfo.tm_min,
                timeinfo.tm_sec);
}

void setup() {
  Serial.begin(115200);
  pinMode(LED_PIN, OUTPUT);
  Serial.println("ESP32 Bring-Up & NTP Demo");

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.printf("\nWi-Fi connected, IP: %s\n", WiFi.localIP().toString().c_str());

  // Init and get time
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  Serial.println("Synchronizing time...");
  delay(2000);
  printLocalTime();
}

void loop() {
  // Blink LED
  digitalWrite(LED_PIN, HIGH); delay(500);
  digitalWrite(LED_PIN, LOW);  delay(500);

  // Print current time every 5 seconds
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint >= 5000) {
    printLocalTime();
    lastPrint = millis();
  }
}
```

---

## 5. Expected Output

**Serial Monitor:**
```
ESP32 Bring-Up & NTP Demo
Connecting to Wi-Fi...
Wi-Fi connected, IP: 192.168.1.105
Synchronizing time...
2025-08-15 09:05:23
2025-08-15 09:05:28
2025-08-15 09:05:33
```

**Hardware:**
- Onboard LED blinks every 500 ms.
- Time updates every 5 seconds in the Serial Monitor.

---

## 6. Discussion Questions
1. Why is accurate time important in IoT systems?
2. How does NTP improve data consistency when multiple devices log events?
3. What happens if the device cannot reach the NTP server?
4. How would you modify the code to adjust for Daylight Saving Time?
5. Can the ESP32 maintain time without NTP? If so, for how long and how accurate?

---

## 7. Exercises
1. Change the blink pattern based on whether seconds are **even** or **odd**.
2. Display the **day of the week** along with the date.
3. Print the uptime in addition to the current time.
4. Modify the code to use **two NTP servers** for redundancy.
5. Save the last synchronized time to NVS (Non-Volatile Storage) so it persists across reboots.

---

## 8. Conclusion
This lab combined **basic ESP32 bring-up** with **network time synchronization**, forming the foundation for time-aware IoT applications.  
Future labs can build on this by timestamping sensor data, synchronizing events across multiple devices, or triggering actions based on schedules.


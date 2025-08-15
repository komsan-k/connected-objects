# ESP32 IoT Labs — Getting Started

This repository contains initial ESP32 labs to verify your toolchain, connect to Wi-Fi, and read I²C temperature sensors.

---

## LAB 1 — ESP32 Bring-Up & Blink + Serial

**Objective:**  
Verify toolchain, upload sketch, check serial output, blink LED.

**Tasks:**
- Install **ESP32** in Arduino IDE Boards Manager, select your board & COM port.
- Blink on **GPIO2** and print a hello banner.

**Starter Code:**
```cpp
void setup() {
  Serial.begin(115200);
  pinMode(2, OUTPUT);
  Serial.println("ESP32 ready!");
}

void loop() {
  digitalWrite(2, HIGH); delay(500);
  digitalWrite(2, LOW);  delay(500);
}

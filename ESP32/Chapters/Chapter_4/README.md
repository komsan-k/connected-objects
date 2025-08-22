# Chapter 4: Power Management in ESP32

The ESP32 is designed for **IoT and embedded systems** where power efficiency is as important as performance.  
It includes **fine-grained power management features** that allow applications to balance computational load with battery life.  
Power consumption ranges from a few **microamps in deep sleep** to **hundreds of milliamps during Wi-Fi transmission**.

---

## 1. Power Domains
The ESP32 contains multiple power domains that can be selectively powered on or off:

- **RTC Domain**: Keeps RTC timer, watchdog, and slow memory powered in low-power modes.  
- **Digital Domain**: Powers CPU cores, caches, and peripherals.  
- **Radio Domain**: Includes Wi-Fi and Bluetooth transceivers.  

By controlling these domains, ESP32 achieves **flexible energy profiles**.

---

## 2. Operating Modes

### 2.1 Active Mode
- Both CPU and radio are active.  
- Highest consumption (**160–240 mA** during Wi-Fi TX).  
- Used during data processing or communication bursts.  

---

### 2.2 Modem Sleep
- CPU remains active, Wi-Fi/Bluetooth transceivers powered down when idle.  
- Ideal when CPU needs to compute but wireless communication is infrequent.  
- Current consumption: **~3–20 mA**.  

**Arduino Example:**
```cpp
WiFi.setSleep(true); // Enable modem sleep
```

---

### 2.3 Light Sleep
- CPU paused, most peripherals halted.  
- RTC, ULP coprocessor, and memory remain powered.  
- Wake-up sources: **timer, GPIO interrupt, ULP**.  
- Consumption: **~0.8–2 mA**.  

**Arduino Example:**
```cpp
esp_sleep_enable_timer_wakeup(10 * 1000000); // 10s
esp_light_sleep_start();
```

---

### 2.4 Deep Sleep
- CPU and most peripherals powered off.  
- RTC memory + ULP coprocessor retained.  
- Wake-up sources: **timer, external GPIO, touch sensors, ULP**.  
- Consumption: **~10–150 µA**.  

**Arduino Example:**
```cpp
esp_sleep_enable_timer_wakeup(60 * 1000000); // 1 min
esp_deep_sleep_start();
```

---

## 3. Ultra Low Power (ULP) Coprocessor
The ESP32 includes a **ULP coprocessor** that runs while the main cores are in deep sleep. It can:
- Read sensors (ADC, temperature, GPIO).  
- Trigger wake-up conditions.  
- Consume only **tens of microamps**.  

🔹 Example use: periodically measure a temperature sensor and wake ESP32 only if threshold exceeded.

---

## 4. Dynamic Frequency and Voltage Scaling (DVFS)
ESP32 can dynamically adjust **CPU clock and voltage**:
- **80 MHz (low power)** to **240 MHz (high performance)**.  
- Lower frequency reduces active power but increases task duration.  

**Arduino Example:**
```cpp
setCpuFrequencyMhz(80); // Switch to 80 MHz
```

---

## 5. Peripheral Power Management
- Disable unused peripherals (**UART, I²C, SPI, ADC**) to reduce current.  
- Use `gpio_hold_en()` to maintain pin states in sleep.  

---

## 6. Best Practices for Power Efficiency
- **Batch communication**: buffer data and send in bursts.  
- **Use deep sleep cycles**: wake only when needed.  
- **Leverage ULP** for simple sensor checks.  
- **Optimize antenna use**: lower TX power if short-range.  
- **Minimize peripherals**: disable unused modules.  
- **Efficient coding**: reduce polling, use interrupts.  

---

## 7. Power Consumption Summary

| Mode              | Typical Current Consumption |
|-------------------|-----------------------------|
| Active + Wi-Fi TX | 160–240 mA                 |
| Modem Sleep       | 3–20 mA                    |
| Light Sleep       | 0.8–2 mA                   |
| Deep Sleep        | 10–150 µA                  |
| ULP (Deep Sleep)  | ~150 µA                    |

---

## 8. Conclusion
Power management in ESP32 is **highly flexible**, enabling designs that can:  
- Run for **years on a coin cell** (deep sleep + ULP).  
- Deliver **real-time data streaming** (active mode).  

By carefully selecting **sleep strategies, wake-up sources, and frequency scaling**, developers can design **energy-efficient IoT applications** without sacrificing functionality.
---
---
# ESP32 Power Management — With Arduino Code

The ESP32 provides multiple power-saving techniques for **IoT and embedded systems**, enabling battery-powered devices to run efficiently. This guide covers **Modem Sleep, Light Sleep, Deep Sleep, DVFS, Peripheral tricks, ULP usage**, and includes Arduino examples.

---

## 1) Modem Sleep (Wi-Fi naps, CPU runs)

Use this mode when your code needs to compute but doesn’t need Wi-Fi continuously.

```cpp
#include <WiFi.h>

const char* ssid = "YOUR_SSID";
const char* pass = "YOUR_PASS";

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) { delay(300); Serial.print("."); }
  Serial.printf("\nIP: %s\n", WiFi.localIP().toString().c_str());

  // Enable Wi-Fi power save (modem sleep)
  WiFi.setSleep(true);

  // Optional: lower TX power
  WiFi.setTxPower(WIFI_POWER_8_5dBm); 
}

void loop() {
  static uint32_t last = 0;
  if (millis() - last > 5000) {
    Serial.println("Heartbeat (WiFi sleepy)...");
    last = millis();
  }
  delay(10);
}
```

---

## 2) Light Sleep (CPU paused; fast wake; RTC on)

Good for millisecond wake latency with timer or GPIO.

### a) Light Sleep via Timer
```cpp
#include "esp_sleep.h"

void setup() {
  Serial.begin(115200);
  Serial.println("Entering light sleep for 5s...");
  esp_sleep_enable_timer_wakeup(5ULL * 1000000ULL);
  esp_light_sleep_start();
  Serial.println("Woke from light sleep");
}

void loop() { delay(1000); }
```

### b) Light Sleep via GPIO
```cpp
#include "esp_sleep.h"

const gpio_num_t WAKE_GPIO = GPIO_NUM_0; // BOOT button

void setup() {
  Serial.begin(115200);
  pinMode(WAKE_GPIO, INPUT_PULLUP);
  Serial.println("Light sleep until button press...");
  esp_sleep_enable_ext0_wakeup(WAKE_GPIO, 0);
  esp_light_sleep_start();
  Serial.println("Woke from GPIO light sleep");
}

void loop() { delay(1000); }
```

---

## 3) Deep Sleep (lowest current; cold start on wake)

### a) Deep Sleep via Timer
```cpp
#include "esp_sleep.h"

RTC_DATA_ATTR int bootCount = 0;

void setup() {
  Serial.begin(115200);
  bootCount++;
  Serial.printf("Boot #%d, deep sleeping for 30s...\n", bootCount);
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

### b) Deep Sleep via Multiple Sources
```cpp
#include "esp_sleep.h"
#include "driver/touch_pad.h"

const gpio_num_t WAKE_GPIO = GPIO_NUM_33;
const touch_pad_t TOUCH_CH = TOUCH_PAD_NUM9;

void setup() {
  Serial.begin(115200);
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_sleep_enable_ext0_wakeup(WAKE_GPIO, 0);
  touchAttachInterrupt(TOUCH_CH, NULL, 30);
  esp_sleep_enable_touchpad_wakeup();
  Serial.println("Deep sleeping (timer + GPIO + touch)...");
  esp_deep_sleep_start();
}

void loop() {}
```

---

## 4) Dynamic Frequency Scaling (DVFS)

Lower CPU clock when idle, raise for bursts.

```cpp
void setup() {
  Serial.begin(115200);
  Serial.printf("CPU @ %d MHz\n", getCpuFrequencyMhz());
  setCpuFrequencyMhz(80);
  Serial.printf("CPU @ %d MHz (low power)\n", getCpuFrequencyMhz());
  setCpuFrequencyMhz(240);
  Serial.printf("CPU @ %d MHz (high perf)\n", getCpuFrequencyMhz());
}

void loop() { delay(1000); }
```

---

## 5) Peripheral + GPIO Power Tricks

```cpp
#include "esp_sleep.h"

const int LED = 5;

void setup() {
  Serial.begin(115200);
  pinMode(LED, OUTPUT);
  digitalWrite(LED, HIGH);

  // Hold pin state through deep sleep
  gpio_hold_en((gpio_num_t)LED);
  gpio_deep_sleep_hold_en();

  Serial.println("Deep sleep 15s with GPIO hold...");
  esp_sleep_enable_timer_wakeup(15ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

---

## 6) Batch + Burst Pattern

Wake, send data, then sleep long.

```cpp
#include <WiFi.h>
#include <PubSubClient.h>
#include "esp_sleep.h"

const char* ssid="YOUR_SSID"; 
const char* pass="YOUR_PASS";
const char* broker="192.168.1.10";

WiFiClient net;
PubSubClient mqtt(net);

void setup() {
  Serial.begin(115200);

  // Wake → sample
  float temp = 24.7;
  WiFi.begin(ssid, pass);
  while (WiFi.status()!=WL_CONNECTED) delay(250);

  mqtt.setServer(broker,1883);
  if (mqtt.connect("esp32_burst")) {
    char buf[64];
    snprintf(buf,sizeof(buf),"{\"temp\":%.2f}",temp);
    mqtt.publish("lab/telemetry", buf);
    mqtt.disconnect();
  }

  WiFi.disconnect(true);
  WiFi.mode(WIFI_OFF);

  Serial.println("Sleeping 5 minutes...");
  esp_sleep_enable_timer_wakeup(5ULL*60ULL*1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

---

## 7) Light Sleep + Interrupt (Ultra-low polling)

```cpp
#include "esp_sleep.h"

const gpio_num_t PIR = GPIO_NUM_27;

void setup() {
  Serial.begin(115200);
  pinMode(PIR, INPUT_PULLDOWN);
  Serial.println("Light sleep, wake on PIR HIGH...");
  esp_sleep_enable_ext1_wakeup(1ULL << PIR, ESP_EXT1_WAKEUP_ANY_HIGH);
  esp_light_sleep_start();
  Serial.println("Woke from PIR!");
}

void loop() { delay(500); }
```

---

## 8) RTC Memory & Wake Reason

```cpp
#include "esp_sleep.h"

RTC_DATA_ATTR uint32_t wakeCounter = 0;

void setup() {
  Serial.begin(115200);
  wakeCounter++;
  Serial.printf("Wake count: %lu\n", (unsigned long)wakeCounter);
  Serial.printf("Wake cause: %d\n", (int)esp_sleep_get_wakeup_cause());
  esp_sleep_enable_timer_wakeup(10ULL*1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

---

## 9) ADC Battery Read

```cpp
#include "esp_sleep.h"

const int BAT_ADC = 34;

float readBatteryV() {
  uint32_t acc = 0;
  for (int i=0;i<16;i++) acc += analogRead(BAT_ADC);
  return (acc/16.0/4095.0)*3.3*2.2; // adjust based on divider
}

void setup() {
  Serial.begin(115200);
  Serial.printf("Battery: %.2f V\n", readBatteryV());
  esp_sleep_enable_timer_wakeup(60ULL*1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

---

## 10) ULP Coprocessor (Skeleton)

```cpp
#include "esp_sleep.h"
#include "ulp_main.h"

void setup() {
  Serial.begin(115200);

  // Load and configure ULP program...
  esp_sleep_enable_ulp_wakeup();

  Serial.println("Deep sleeping with ULP monitoring...");
  esp_deep_sleep_start();
}

void loop() {}
```

---

## ✅ Practical Tips Recap
- Prefer **deep sleep** for battery devices; batch work.  
- Use **light sleep** for sub-second latency.  
- Drop CPU to **80 MHz** when idle.  
- Lower Wi-Fi TX power + `WiFi.setSleep(true)`.  
- Disable unused peripherals, hold GPIO states.  
- Use **ULP** for ultra-low average current sensing.  


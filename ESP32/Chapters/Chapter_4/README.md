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


# Chapter 2: Built-in Sensors of ESP32

The ESP32 integrates several **built-in sensors and peripherals** that make it highly versatile for **IoT and embedded systems**.  
This chapter provides a structured overview of these components, their working principles, and use cases.

---

## 1. Hall Effect Sensor
- **Purpose** → Detects changes in magnetic fields.  
- **Working principle** → Outputs a voltage proportional to magnetic field strength.  
- **Use cases**:
  - Proximity detection (e.g., magnet near ESP32).  
  - Security systems (door/window open detection).  
  - Motor position sensing.  

⚠️ **Note**: The Hall sensor is internal, but readings can be **noisy** → apply **software filtering**.  

---

## 2. Temperature Sensor
- **Purpose** → Monitors internal chip temperature.  
- **Characteristics**:
  - Measures **die temperature**, not ambient air.  
  - Accuracy limited (±2–3 °C drift).  
- **Use cases**:
  - Thermal monitoring to prevent overheating.  
  - Adjust performance in **power-sensitive applications**.  

---

## 3. Capacitive Touch Sensors
- **Quantity** → Up to **10 touch-sensitive GPIOs**.  
- **Working principle** → Detects capacitance changes when a finger touches the pin.  
- **Use cases**:
  - Touch buttons.  
  - Sliders.  
  - Wake-up sources from deep sleep.  

---

## 4. Analog-to-Digital Converter (ADC)
- **Resolution** → Up to **12-bit**.  
- **Channels** → Up to **18 input channels** (depending on package).  
- **Use cases**:
  - Reading external sensors (temperature, light, gas).  
  - Battery voltage monitoring.  
  - General analog signal processing.  

---

## 5. Digital-to-Analog Converter (DAC)
- **Resolution** → **8-bit**, available on **two channels**.  
- **Use cases**:
  - Audio signal generation.  
  - Voltage reference outputs.  
  - Simple waveform generation.  

---

## 6. Other Peripherals Related to Sensing
Although not sensors themselves, ESP32 integrates additional features useful for sensing tasks:  
- **Pulse Counter (PCNT)** → Measures events like rotations or flow pulses.  
- **ULP Coprocessor** → Can sample ADC or monitor touch sensors while in **deep sleep** mode.  

---

## 7. Methods to Improve Readings
Built-in sensors may produce noisy or imprecise data. Improvements include:  
- **Filtering** → Apply moving average or low-pass filters.  
- **Calibration** → Use known references (e.g., external thermometer for calibration).  
- **Shielding** → Reduce interference for Hall/touch sensors with shielding and grounding.  
- **External sensors** → Use precise external sensors (e.g., LM73 for temperature, MPU6050 for motion).  

---

## ✅ Summary
The ESP32 includes:  
- **Hall sensor**  
- **Internal temperature sensor**  
- **Capacitive touch sensors**  
- **ADC (12-bit)**  
- **DAC (8-bit)**  

While suitable for many basic applications, they often require **filtering, calibration, or external complements** for precision tasks.  
This versatility makes the ESP32 a strong candidate for **low-cost IoT prototyping** and **embedded system development**.


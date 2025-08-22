# Chapter 2: Built-in Sensors of the ESP32

The ESP32 integrates built-in sensors and sensing-related peripherals that enable rapid prototyping without additional hardware.  
This chapter covers the Hall effect sensor, internal temperature sensor, capacitive touch inputs, ADC, DAC, and auxiliary features (pulse counter, low-power sensing) with working Arduino examples.

---

## 1. Hall Effect Sensor

### Overview
The ESP32 exposes an on-chip Hall sensor that reacts to magnetic fields near the device.

### Arduino Example: Read Hall Value
```cpp
// ESP32 Hall effect demo (raw units)
// Bring a small magnet near the chip and observe the change
void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("ESP32 Hall sensor demo");
}

void loop() {
  int raw = hallRead();         // raw hall units (implementation-defined)
  Serial.printf("Hall raw: %d\n", raw);
  delay(250);
}
```

### Tip: Simple Filtering
```cpp
// Moving average over N samples for smoother values
template<int N>
int movingAverage(int x) {
  static int buf[N] = {0};
  static int idx = 0, count = 0, sum = 0;
  sum -= buf[idx];
  buf[idx] = x;
  sum += x;
  idx = (idx + 1) % N;
  if (count < N) count++;
  return sum / count;
}
```

---

## 2. Internal Temperature Sensor

### Overview
The internal sensor reports **die temperature** (not ambient). Accuracy is limited; use it for relative or thermal management tasks.

### Arduino Example: Read Die Temperature
```cpp
// Requires Arduino-ESP32 core where temperatureRead() is available
extern "C" uint8_t temperatureRead(); // returns approx. Celsius

void setup() {
  Serial.begin(115200);
  delay(200);
  Serial.println("ESP32 internal temp (die) demo");
}

void loop() {
  float tC = (float)temperatureRead();
  Serial.printf("Die temperature: %.1f C (approx)\n", tC);
  delay(1000);
}
```

### Tip: Offset Calibration
```cpp
// If you have an external accurate thermometer, measure ambient and derive offset
float offsetC = -3.5f; // example offset
// float corrected = tC + offsetC;
```

---

## 3. Capacitive Touch Sensors

### Overview
ESP32 supports multiple touch pads (e.g., T0=GPIO4, T3=GPIO15, etc.).  
Read via `touchRead(pin)`; lower values typically mean a touch is present.

### Arduino Example: Touch Read and Threshold
```cpp
const int TOUCH_PIN = T0; // GPIO4 on many dev boards
int baseline = 0;

void setup() {
  Serial.begin(115200);
  delay(300);
  long sum = 0;
  for (int i=0; i<50; ++i) { sum += touchRead(TOUCH_PIN); delay(20); }
  baseline = sum / 50;
  Serial.printf("Touch baseline: %d\n", baseline);
}

void loop() {
  int v = touchRead(TOUCH_PIN);
  bool touched = (v < baseline - 10); // simple threshold
  Serial.printf("touch=%d %s\n", v, touched ? "<-- TOUCHED" : "");
  delay(100);
}
```

### Deep Sleep Wake on Touch
```cpp
#include "driver/touch_pad.h"
#include "esp_sleep.h"

void setup() {
  Serial.begin(115200);
  delay(200);
  touchSleepWakeUpEnable(T0, 50); // threshold 50 (tune!)
  Serial.println("Sleeping. Touch T0 to wake...");
  esp_sleep_enable_touchpad_wakeup();
  delay(100);
  esp_deep_sleep_start();
}

void loop() {}
```

---

## 4. Analog-to-Digital Converter (ADC)

### Overview
ESP32 ADC supports up to 12-bit resolution. Many boards route sensors/battery to specific ADC pins.  
You can set attenuation for wider input range.

### Arduino Example: Precise ADC Read
```cpp
const int ADC_PIN = 34; // input-only ADC pin
void setup() {
  Serial.begin(115200);
  delay(200);

  analogReadResolution(12);                 
  analogSetAttenuation(ADC_11db);           
  Serial.println("ADC demo");
}

void loop() {
  int raw = analogRead(ADC_PIN);
  float v = (raw / 4095.0f) * 3.3f;
  Serial.printf("ADC raw=%4d  V=%.3f\n", raw, v);
  delay(250);
}
```

### Averaging ADC for Noise Reduction
```cpp
int readAdcAvg(int pin, int n=16){
  long s=0;
  for(int i=0;i<n;i++){ s += analogRead(pin); delayMicroseconds(300); }
  return (int)(s / n);
}
```

---

## 5. Digital-to-Analog Converter (DAC)

### Overview
Two DAC channels (8-bit) are available on many ESP32 modules: GPIO25 (DAC1) and GPIO26 (DAC2).

### Arduino Example: Sweep DAC Output
```cpp
const int DAC_PIN = 25; // DAC1
void setup() { }
void loop() {
  for (int v=0; v<=255; ++v) { dacWrite(DAC_PIN, v); delay(5); }
  for (int v=255; v>=0; --v) { dacWrite(DAC_PIN, v); delay(5); }
}
```

### Simple Sine Wave (Table-Driven)
```cpp
#include <math.h>
const int DACP = 25;
const int N = 64;
uint8_t lut[N];

void setup(){
  for(int i=0;i<N;i++){
    float th = 2.0f*M_PI*i/N;
    float s = (sinf(th)*0.5f + 0.5f);
    lut[i] = (uint8_t)(s*255.0f);
  }
}

void loop(){
  for(int i=0;i<N;i++){ dacWrite(DACP, lut[i]); delayMicroseconds(300); }
}
```

---

## 6. Other Sensing Features

### Pulse Counter (PCNT) for Frequency/Events
ESP32 includes a hardware pulse counter (PCNT) peripheral useful for counting pulses from flow meters, encoders, etc.

#### Arduino Example: Count Pulses on a GPIO
```cpp
extern "C" {
  #include "driver/pcnt.h"
}
const gpio_num_t PULSE_GPIO = GPIO_NUM_4;

void setupPCNT(){
  pcnt_config_t cfg = {};
  cfg.pulse_gpio_num = PULSE_GPIO;
  cfg.ctrl_gpio_num  = PCNT_PIN_NOT_USED;
  cfg.lctrl_mode     = PCNT_MODE_KEEP;
  cfg.hctrl_mode     = PCNT_MODE_KEEP;
  cfg.pos_mode       = PCNT_COUNT_INC;   
  cfg.neg_mode       = PCNT_COUNT_DIS;   
  cfg.counter_h_lim  = 32767;
  cfg.counter_l_lim  = -32768;
  cfg.unit           = PCNT_UNIT_0;
  cfg.channel        = PCNT_CHANNEL_0;
  pcnt_unit_config(&cfg);

  pcnt_counter_pause(PCNT_UNIT_0);
  pcnt_counter_clear(PCNT_UNIT_0);
  pcnt_counter_resume(PCNT_UNIT_0);
}

void setup(){
  Serial.begin(115200);
  delay(200);
  setupPCNT();
  Serial.println("PCNT ready on GPIO4 (rising edges)");
}

void loop(){
  int16_t cnt = 0;
  pcnt_get_counter_value(PCNT_UNIT_0, &cnt);
  Serial.printf("Pulses: %d\n", cnt);
  delay(500);
}
```

### Low-Power Sensing (ULP/Deep Sleep)
Full ULP assembly is beyond this chapter, but you can achieve low-power sensing with built-ins like **touch wake** or **timer wake**.  

#### Arduino Example: Periodic Deep Sleep + ADC Sample
```cpp
#include "esp_sleep.h"
const int ADC_PIN = 34;

void setup(){
  Serial.begin(115200);
  analogReadResolution(12);
  analogSetAttenuation(ADC_11db);

  int raw = analogRead(ADC_PIN);
  Serial.printf("ADC on wake: %d\n", raw);

  esp_sleep_enable_timer_wakeup(5ULL * 1000000ULL);
  Serial.flush();
  esp_deep_sleep_start();
}
void loop(){}
```

---

## 7. Improving Readings: Filtering, Calibration, Layout

### Software Filtering
- Moving average (see examples above).  
- Low-pass IIR filter: `y ← α·x + (1−α)·y`.  

```cpp
float iirLPF(float x, float &y, float alpha=0.2f){
  y = alpha * x + (1.0f - alpha) * y;
  return y;
}
```

### Calibration Patterns
```cpp
// Offset + scale: out = (raw + offset) * scale
float calibrate(float raw, float offset, float scale){
  return (raw + offset) * scale;
}
```

### Hardware Practices
- Use short sensor leads.  
- Ground planes and shielding for touch/Hall.  
- Stable reference voltages for ADC.  
- Decouple power near ESP32 and analog sections.  

---

## ✅ Summary
The ESP32’s built-in sensing and peripherals (Hall, internal temperature, capacitive touch, ADC, DAC, PCNT, low-power modes) enable rapid prototyping and complete end-to-end solutions.  
For **precision applications**, combine ESP32 with external sensors, apply **calibration**, and use **filtering**.  

The included Arduino examples provide ready-to-use code to accelerate your IoT and embedded projects.

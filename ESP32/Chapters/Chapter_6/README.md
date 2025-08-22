# Chapter 6: AI Engineering on ESP32 (TinyML in Practice)

This chapter introduces how to run **TinyML models** on the ESP32 family, including hardware considerations, software toolchains, deployment workflows, optimization strategies, and practical Arduino examples.

---

## 1. Hardware Reality Check

### Cores & ISA
- **ESP32 / WROOM / WROVER** → Dual-core Xtensa LX6 @ up to 240 MHz.  
- **ESP32-S3** → Dual-core Xtensa LX7 @ 240 MHz with vector/SIMD acceleration (int8 MACs).  
- **ESP32-C3** → Single-core RISC-V @ 160 MHz, good for smaller int8 models.  

### Memory
- Internal SRAM: ~320–520 KB.  
- Optional PSRAM: 2–8 MB for larger models/buffers.  

### Floating Point
- Float works, but **int8 quantized models** are preferred for speed and memory efficiency.  
- Optimized with **ESP-NN kernels**.  

### Peripherals
- I²S (audio), I²C/SPI (sensors), ADC, DMA.  
- ESP32-S3 vector ops accelerate CNNs and FC layers.  

👉 **Implication**: Keep models **small (≤100–400 KB)**, use **windowed features**, and prefer **DS-CNN / 1-D convs / tiny MLPs**.

---

## 2. Software Stack & Toolchain

- **TensorFlow Lite Micro (TFLM)**  
  - Flatbuffer `.tflite` (INT8 recommended).  
  - Use `MicroMutableOpResolver` for only required ops.  
  - Allocate a static **tensor arena**.  
  - Enable **ESP-NN** kernels + **ESP-DSP** for FFT/MFCC (ESP32-S3).  

- **Edge Impulse SDK** → End-to-end: data → training → Arduino library.  
- **EloquentTinyML** → Arduino-friendly wrapper for MLPs/CNNs.  
- **FreeRTOS** → Schedule sensor read, feature extraction, inference, comms.

---

## 3. Model Patterns That Fit

- **Audio (KWS)** → MFCC + DS-CNN, ~10–30k params.  
- **Motion/IMU (HAR, fall detect)** → 1-D CNN / MLP.  
- **Anomaly detection** → CNN/AE or MLP on features.  
- **Regression/control** → Small MLPs (8–32 neurons/layer).  

💡 **Latency budget**:  
\[
\text{Latency} \approx \frac{\text{MACs}}{\text{cycles per MAC × CPU Hz}}
\]  
Target <20 ms for 50 Hz inference.

---

## 4. Data → Model → Deploy Pipeline

1. **Collect** sensor data windows.  
2. **Feature engineer** (mean, variance, MFCC, spectral bands).  
3. **Train offline** (TF/PyTorch).  
   - Prefer quantization-aware training.  
4. **Export .tflite** (int8).  
5. **Deploy on ESP32** via TFLM, Edge Impulse, or EloquentTinyML.  
6. **Profile & optimize**: arena size, op pruning, latency.  
7. **Iterate & deploy OTA**.  

---

## 5. Scheduling on Dual Core

- **Core 0** → Wi-Fi, MQTT, Web server.  
- **Core 1** → Sensor → Feature → Inference.  

### Typical Tasks
- `SensorTask (prio 2)` → ring buffer fill.  
- `FeatureTask (prio 3)` → extract features.  
- `InferenceTask (prio 4)` → run TinyML model.  
- `CommTask (prio 1)` → send results.  

Use queues, avoid dynamic allocation, and enable watchdog.

---

## 6. Power Management

- Duty-cycle sensors & Wi-Fi.  
- Batch inference, then sleep.  
- Use **Light sleep** between windows.  
- ULP coprocessor can pre-filter signals.  
- Prefer **int8 models + short windows**.

---

## 7. Security & Privacy

- Keep **inference on-device**.  
- Send **only classifications/events** to the cloud.  
- Use **MQTT TLS** or secure gateway.  
- Sign OTA firmware; disable debug in production.

---

## 8. Example A: IMU Activity Classifier

Classifies **idle / walk / shake** from an MPU6050 at 100 Hz using a small MLP.

### `model.h`
```cpp
#pragma once
#include <cstddef>
#include <cstdint>
extern const unsigned char model_tflite[];
extern const size_t model_tflite_len;

const unsigned char model_tflite[] = { 0x20, 0x00, 0x00, 0x00, /* ... */ };
const size_t model_tflite_len = sizeof(model_tflite);
```

### `imu_activity_tinyml.ino`
```cpp
#include <Wire.h>
#include <EloquentTinyML.h>
#include "model.h"

#define TENSOR_ARENA_SIZE  40*1024
Eloquent::TinyML::TfLite<6, 3, TENSOR_ARENA_SIZE> ml;

#define MPU 0x68
float ax, ay, az;
const int WIN = 100;
float bufAx[WIN], bufAy[WIN], bufAz[WIN];
int wi = 0;

void mpuWrite(uint8_t r, uint8_t v){
  Wire.beginTransmission(MPU); Wire.write(r); Wire.write(v); Wire.endTransmission();
}
void mpuRead6(uint8_t r, int16_t &x, int16_t &y, int16_t &z){
  Wire.beginTransmission(MPU); Wire.write(r); Wire.endTransmission(false);
  Wire.requestFrom(MPU,6);
  x=(Wire.read()<<8)|Wire.read(); y=(Wire.read()<<8)|Wire.read(); z=(Wire.read()<<8)|Wire.read();
}

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpuWrite(0x6B, 0x00);   // wake
  mpuWrite(0x1C, 0x00);   // accel ±2g
  if (!ml.begin(model_tflite, model_tflite_len)) {
    Serial.println("Model init failed");
    while(true) delay(1000);
  }
}

void loop() {
  int16_t axr, ayr, azr;
  mpuRead6(0x3B, axr, ayr, azr);
  ax = axr / 16384.0; ay = ayr / 16384.0; az = azr / 16384.0;

  bufAx[wi] = ax; bufAy[wi] = ay; bufAz[wi] = az;
  wi = (wi + 1) % WIN;

  static uint32_t t0=millis();
  if (millis() - t0 >= 1000) {
    t0 = millis();
    float meanx=0, meany=0, meanz=0;
    for (int i=0;i<WIN;i++){ meanx+=bufAx[i]; meany+=bufAy[i]; meanz+=bufAz[i]; }
    meanx/=WIN; meany/=WIN; meanz/=WIN;

    float sx=0, sy=0, sz=0;
    for (int i=0;i<WIN;i++){
      float dx=bufAx[i]-meanx, dy=bufAy[i]-meany, dz=bufAz[i]-meanz;
      sx+=dx*dx; sy+=dy*dy; sz+=dz*dz;
    }
    float stdx = sqrtf(sx/WIN), stdy=sqrtf(sy/WIN), stdz=sqrtf(sz/WIN);

    float input[6] = { meanx, meany, meanz, stdx, stdy, stdz };
    float y[3];
    ml.predict(input, y);

    int cls = 0; float best = y[0];
    for (int i=1;i<3;i++) if (y[i] > best){ best = y[i]; cls = i; }

    const char* label = (cls==0)?"idle":(cls==1)?"walk":"shake";
    Serial.printf("y=[%.2f, %.2f, %.2f] => %s
", y[0], y[1], y[2], label);
  }
  delay(10);
}
```

**Notes**:
- Start with `TENSOR_ARENA_SIZE = 40–60 KB`.  
- Ensure int8 input/output for efficiency.  

---

## 9. Example B: Keyword Spotting (Outline)

**Signal chain**:  
I²S mic → 16 kHz mono → 30 ms frames → MFCC (ESP-DSP) → stack ~1 s → DS-CNN (int8) → classification.

**Tips**:
- Use streaming inference (update last frames only).  
- On ESP32-S3, enable `esp-nn` kernels for speed.

---

## 10. Optimization Checklist

- ✅ Use **int8 quantization**.  
- ✅ Prefer **depthwise separable convs** or 1-D CNNs.  
- ✅ Reduce input window sizes and channels.  
- ✅ Apply pruning or knowledge distillation.  
- ✅ Pin inference to dedicated core.  
- ✅ Pre-allocate memory (no malloc at runtime).  

---

## 11. Telemetry & OTA in Production

- Publish **model version, latency, confidence, battery, events** via MQTT.  
- Maintain **safe-mode image** for OTA rollback.  

---

## 12. Troubleshooting

- **Interpreter init fails** → arena too small / missing operator.  
- **NaNs or weird outputs** → mismatch between training preprocessing vs. device.  
- **Lag under Wi-Fi** → pin inference task to another core, raise prio, or use async MQTT/web.  

---


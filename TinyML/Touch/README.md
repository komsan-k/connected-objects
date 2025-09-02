# TinyML Lab: Touch Pattern Classifier on ESP32

This lab demonstrates a **basic TinyML workflow on ESP32** using the built-in **capacitive touch sensor** (no extra hardware required).  
You’ll collect touch data, train a tiny neural network, convert it to TensorFlow Lite Micro, and run real-time inference to control an LED.

---

## 🎯 Learning Goals
- Use ESP32’s built-in `touchRead()` sensor  
- Collect and label data for three classes: **NONE**, **TAP**, **LONG**  
- Train a small neural network in Python (TensorFlow)  
- Convert to an **int8 TFLite model** and deploy on ESP32  
- Run inference to classify touch patterns and toggle an LED  

---

## 🛠 Requirements
- **Hardware**
  - ESP32 DevKit board (e.g., DOIT ESP32 DEVKIT V1)
  - USB cable

- **Software**
  - Arduino IDE with ESP32 core installed  
  - Library: `Arduino_TensorFlowLite` (or `TensorFlowLite_ESP32`)  
  - Python 3 with packages: `numpy`, `pandas`, `scikit-learn`, `tensorflow`  

---

## 📡 Step 1: Data Collection
1. Use a sketch that prints `label,value` from `touchRead(T5)` at ~50 Hz.  
2. In the Serial Monitor, type:
   - `n` → NONE (no touch, hand away)  
   - `t` → TAP (short, quick taps)  
   - `l` → LONG (press/hold 1–2s)  
3. Record ~1–2 minutes per class and save to `touch_data.csv`.  

A **synthetic dataset** (`data/touch_data.csv`) is included for testing.

---

## 🤖 Step 2: Training & Conversion
Run the trainer in Python:

```bash
cd python
python3 train_touch_cls.py
```

This will:
- Train a 2-layer dense neural net on simple features (mean, std, min, max, range, zero-crossings)  
- Convert it to a quantized int8 `.tflite` model  
- Save:  
  - `touch_cls.tflite` (the model)  
  - `labels.txt` (class order)

Convert to a C header for Arduino:

```bash
xxd -i touch_cls.tflite > ../arduino/esp32_touch_cls/model_data.h
```

---

## ⚡ Step 3: Arduino Deployment
1. Open `arduino/esp32_touch_cls/esp32_touch_cls.ino` in Arduino IDE.  
2. Install the ESP32 boards package + TFLM library.  
3. Upload the sketch to your ESP32.  

The sketch:
- Reads T5 (GPIO 12) at 50 Hz  
- Computes 6 features per 1-second window  
- Runs inference with TensorFlow Lite Micro  
- Turns **LED on GPIO2** ON for `TAP` or `LONG` predictions  

---

## 🔍 Step 4: Demo
- Open Serial Monitor @115200.  
- Try **no-touch** → model predicts `NONE`.  
- Try **short taps** → model predicts `TAP`.  
- Try **long holds** → model predicts `LONG`.  
- LED will light up for TAP/LONG.  

---

## 📌 Notes
- If `kArenaSize` is too small, increase it (e.g., 40 KB).  
- The **class order** may differ (`['LONG','NONE','TAP']`, etc.). Adjust LED logic in `.ino` accordingly.  
- Touch baselines vary by board → you may calibrate thresholds or retrain with your own data.  

---

## 📂 Repository Structure
```
esp32_tinyml_touch_lab/
├── arduino/
│   └── esp32_touch_cls/
│       ├── esp32_touch_cls.ino      # Inference sketch
│       └── model_data.h             # Generated from touch_cls.tflite
├── python/
│   └── train_touch_cls.py           # Trainer + converter
├── data/
│   └── touch_data.csv               # Sample dataset
└── README.md
```

---

## 🚀 Extensions
- Reduce window size to 0.5s for lower latency.  
- Add a “noise” class for robustness.  
- Publish predictions over MQTT or BLE.  
- Use other ESP32 analog sensors (`analogRead`) in place of `touchRead`.  


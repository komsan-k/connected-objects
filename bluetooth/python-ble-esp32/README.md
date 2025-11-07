# 🔬 Lab: Using `bleak` to Send an Incremental Counter to ESP32 over BLE

## 🎯 Objective
Build a **Python (PC) → ESP32 (BLE)** pipeline where a Python script uses **`bleak`** to send an **incremental counter** to an ESP32 **BLE Peripheral** via a **Write** characteristic. The ESP32 prints the received value and blinks an LED to acknowledge.

---

## ⚙️ Hardware & Software
- **ESP32** development board (e.g., DevKitC, NodeMCU‑32S)
- **Arduino IDE** with **ESP32 boards** installed
- **Python 3.8+** on PC (Windows/macOS/Linux)
- **bleak** Python package (`pip install bleak`)
- (Optional) USB power meter to observe power

---

## 🧠 Architecture
```
[Python PC: bleak] --(BLE Write: ASCII "0","1","2",...)--> [ESP32 Peripheral]
                                                       ↳ [LED blink + Serial log]
```

- **ESP32** advertises a custom **Service** with a **Write characteristic**.
- **Python** connects as **Central** and writes a counter value every 500 ms.

---

## 🧩 UUIDs (Custom)
- **Service UUID**: `e1f4046e-2a5a-4a5b-8ee3-7c2f31d5b5a1`
- **Write Characteristic UUID**: `e1f40470-2a5a-4a5b-8ee3-7c2f31d5b5a1`

*You can change these, but keep them consistent in both sketches.*

---

## 🔌 Part A — ESP32 BLE Peripheral (Arduino)

**File:** `esp32_ble_counter_server.ino`

Features:
- Advertises as **`ESP32_BLE_Counter`**
- Exposes a **Write** characteristic that accepts ASCII numbers (e.g., `"42"`)
- Toggles **LED on GPIO 2** briefly on every received number
- Prints the parsed integer and raw payload to **Serial**

Upload and open Serial Monitor @ **115200 baud**.

---

## 🐍 Part B — Python Client with `bleak`

**File:** `bleak_counter_client.py`

Features:
- Scans for device named **`ESP32_BLE_Counter`**
- Connects, discovers services
- Writes an **incremental counter** every **0.5 s** (`0,1,2,...`)
- Graceful shutdown on **Ctrl+C**

Install dependencies:
```bash
pip install bleak
```

Run:
```bash
python bleak_counter_client.py
```

---

## ✅ Test Procedure
1. **Flash ESP32** with `esp32_ble_counter_server.ino`.
2. Open Serial Monitor to watch logs.
3. Run `python bleak_counter_client.py` on your PC.
4. Observe:
   - Serial prints: `Got 0`, `Got 1`, `Got 2`, ...
   - Onboard LED (GPIO 2) blinks briefly for each message.

---

## 🧪 Expected Serial Output (ESP32)
```
BLE advertising as ESP32_BLE_Counter
Write payload: "0"  parsed=0
Write payload: "1"  parsed=1
Write payload: "2"  parsed=2
...
```

---

## 🛠️ Troubleshooting
- **Not found device**: Ensure PC Bluetooth is ON and within ~2–5 m. Press ESP32 **EN/Reset** to restart advertising.
- **Permission error (Linux)**: Run with `sudo` or set BLE permissions (`sudo setcap cap_net_raw,cap_net_admin+eip $(readlink -f $(which python3))`).
- **Windows adapter issues**: Update Bluetooth driver; try disabling other BLE apps (they may hold the adapter).
- **macOS**: If the name filter fails, connect by **address** printed in the Python scan phase.
- **No LED blink**: Change `LED_PIN` to a valid pin/LED on your board.

---

## 📦 Extensions
- Add a **Notify** characteristic for ESP32 to echo last count.
- Switch payload to **binary (uint32_t LE)** for higher throughput.
- Use **write without response** for faster updates.
- Gateway mode: forward counter to **MQTT** via Wi‑Fi.

---

## 📚 References
- bleak docs: https://github.com/hbldh/bleak
- Espressif Arduino BLE: https://github.com/espressif/arduino-esp32
- Bluetooth SIG: https://www.bluetooth.com/specifications/

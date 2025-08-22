# Chapter 3: Wireless Communication on ESP32

This chapter explores the wireless radios integrated in the **ESP32**, their architectures, performance realities, coexistence strategies, and practical tuning recipes. It also explains when to choose Wi-Fi, Bluetooth (BLE), or ESP-NOW based on use cases.

---

## 1. Radio Blocks & Bands
- **Single 2.4 GHz RF front-end** shared by Wi-Fi and Bluetooth.  
- Includes LNA/PA, PLL/synthesizer, antenna switch/matching.  
- Antennas: PCB inverted-F, chip antenna, or u.FL connector (module dependent).  
- **Tx power**: up to ~+20 dBm (Wi-Fi), ~+9 dBm (BLE).  
- **Rx sensitivity**: better at lower data rates.  

---

## 2. Wi-Fi (802.11 b/g/n @ 2.4 GHz)

### PHY & Rates
- Channels **1–13** (region dependent).  
- **20 MHz bandwidth** typical; **40 MHz** optional but fragile in crowded bands.  
- Peak PHY: ~72.2 Mb/s (20 MHz short GI) or ~150 Mb/s (40 MHz).  
- **Real TCP throughput**: ~10–25 Mb/s under good conditions.  

### Modes & Roles
- **Station (STA)** → joins router/AP.  
- **SoftAP** → ESP32 acts as AP (practical ~4 clients).  
- **AP+STA** → concurrent AP + STA with time-slicing (reduced throughput).  

### Security
- **WPA2-PSK** widely supported.  
- **Enterprise EAP** (PEAP, EAP-TLS) supported in ESP-IDF.  
- **WPA3-SAE** on newer chips (C3/S2/S3).  

### IP Stack
- **lwIP TCP/UDP stack**.  
- **TLS** via mbedTLS.  
- Tweaks: socket buffer sizing, Nagle toggle, keepalive, use UDP for high-rate telemetry.  

### Power Saving
- **Modem-sleep / Light-sleep** → balances latency and current consumption.  
- **Deep-sleep** → Wi-Fi off; reconnect adds hundreds of ms to seconds.  

### Interference & Planning
- 2.4 GHz is crowded (Wi-Fi, BLE, microwaves, toys).  
- Prefer **channels 1, 6, 11**; scan first, then choose quietest.  
- Keep antenna clearance, avoid metal objects and LCDs nearby.  

---

## 3. Bluetooth

### Classic vs BLE
- **Classic BR/EDR (original ESP32)** → Serial Port Profile, A2DP possible but heavy.  
- **BLE (all family)** → GAP + GATT. BLE 4.2 (original), BLE 5.0 (C3/S3).  

### BLE Performance Knobs
- **Adv interval** → short = faster discovery, higher current.  
- **Conn interval** → short = low latency, high current; long = low current, high latency.  
- **MTU** → larger = higher throughput, more RAM.  
- **Notifications/indications** for efficient data transfer.  

### Security
- Pairing/bonding methods: Just Works, Passkey, LE Secure Connections.  
- Store bonds carefully (NVS for persistence).  

---

## 4. Coexistence (Wi-Fi + BT)
- RF is **time-multiplexed** with **PTA (Packet Traffic Arbitration)**.  
- Heavy Wi-Fi traffic can starve BLE.  
- Mitigations:  
  - Reduce Wi-Fi duty cycle.  
  - Use longer BLE connection intervals.  
  - Tune coex defaults via ESP-IDF APIs.  

---

## 5. ESP-NOW
- Vendor-specific **peer-to-peer protocol** over 802.11.  
- **Connectionless, low-latency**.  
- Payload: ~250 B.  
- One-to-one or one-to-many.  
- Optional encryption with PMK/LMK keys.  
- Best for **sensor swarms and control**; not bulk data.  

---

## 6. Practical Throughput & Latency
- **Wi-Fi STA TCP** → ~10–25 Mb/s typical.  
- **BLE GATT notifications** → tens to few hundred kb/s.  
- **ESP-NOW** → few ms latency; small payloads limit throughput.  

---

## 7. RF Layout & Antennas
- Respect **antenna keep-out** (no copper/ground under antenna).  
- Maintain reference matching network.  
- Avoid ground splits or long return paths.  
- Test enclosures for detuning (plastic vs metal).  

---

## 8. Power & Battery Strategy
- **Wi-Fi always on**: ~60–200 mA peaks.  
- Use **burst send + deep sleep** for sensors.  
- **BLE**: idle in tens of µA with long intervals.  
- **ESP-NOW**: efficient for low-duty sensors.  

---

## 9. Security Checklist
- **Wi-Fi**: WPA2/WPA3, TLS with cert validation, rotate keys.  
- **MQTT**: username/password or mutual TLS, Last Will (LWT).  
- **BLE**: use LE Secure Connections, avoid Just Works for sensitive data.  
- **ESP-NOW**: use encryption keys + MAC allow-lists.  

---

## 10. Choosing the Right Protocol
| Need                                | Best Fit                                |
|-------------------------------------|-----------------------------------------|
| Cloud dashboards, bulk data, web UI | Wi-Fi (TCP/HTTP/MQTT/WebSockets)        |
| Phone app control, low power        | BLE (GATT)                              |
| Ultra-low-latency local swarm       | ESP-NOW                                 |
| Mixed phone + cloud                 | AP+STA, or BLE ↔ Wi-Fi gateway          |

---

## 11. Tuning Recipes (Quick Wins)
- **Wi-Fi STA**: pick quiet channel, 20 MHz BW, batch messages, increase buffers.  
- **BLE**: increase MTU, tune conn interval (30–90 ms low power, 7.5–15 ms snappy).  
- **Coex**: reduce Wi-Fi rate, avoid constant scans/streams when BLE latency matters.  

---

## 12. Family Differences
- **ESP32 (original)** → Wi-Fi b/g/n + BT Classic + BLE 4.2.  
- **ESP32-S2** → Wi-Fi only, USB.  
- **ESP32-C3** → Wi-Fi + BLE 5.0 LE (RISC-V).  
- **ESP32-S3** → Wi-Fi + BLE 5.0 LE, dual-core + vector instructions.  

---

## ✅ Pro Tips for Robust Projects
- Log **RSSI** and adapt behavior.  
- Implement **reconnect backoff** and offline buffering.  
- Use **watchdog + brown-out reset** (RF bursts strain supply).  
- Validate in **crowded RF conditions** and support OTA for field tuning.  


# 📘 Bluetooth and BLE Technology and Architecture

---

## 🎯 Learning Objectives

After studying this chapter, students will be able to:

1. Describe the principles and evolution of Bluetooth wireless technology.  
2. Explain the Bluetooth protocol stack and its functional layers.  
3. Differentiate between Bluetooth Classic (BR/EDR) and Bluetooth Low Energy (BLE) architectures.  
4. Understand Bluetooth profiles, GATT services, and device roles.  
5. Analyze Bluetooth network topologies and communication procedures.  
6. Identify how Bluetooth integrates into IoT and Cyber-Physical Systems (CPS).

---

## 🧠 7.1 Introduction to Bluetooth Technology

Bluetooth is a **short-range wireless communication technology** operating in the **2.4 GHz ISM band**.  
It was introduced in **1999** by the **Bluetooth Special Interest Group (SIG)** to replace cables between personal devices such as phones, headsets, and computers.

Bluetooth has evolved from cable replacement to a **universal low-power data exchange protocol** used in **IoT, wearables, and sensor networks**.

---

### 7.1.1 Key Characteristics

| Feature | Description |
|----------|-------------|
| **Frequency Band** | 2.402–2.480 GHz ISM band |
| **Modulation** | GFSK, π/4-DQPSK, 8DPSK |
| **Channel Spacing** | 1 MHz (Classic) / 2 MHz (BLE) |
| **Access Method** | Frequency-Hopping Spread Spectrum (FHSS) |
| **Typical Range** | 10–100 m |
| **Topology** | Point-to-Point, Piconet, Scatternet |
| **Data Rate** | Up to 3 Mbps (Classic) / 1–2 Mbps (BLE) |

---

### 7.1.2 Evolution of Bluetooth Standards

| Version | Year | Key Features |
|----------|------|---------------|
| **1.0 / 1.2** | 1999–2003 | Basic cable replacement |
| **2.0 + EDR** | 2004 | Enhanced Data Rate (3 Mbps) |
| **3.0 + HS** | 2009 | High-speed (Wi-Fi assisted) |
| **4.0 (BLE)** | 2010 | Low Energy mode introduced |
| **4.2** | 2014 | IPv6 over BLE (6LoWPAN) |
| **5.0 / 5.1 / 5.2** | 2016–2020 | 2 Mbps mode, direction finding |
| **5.3 / 5.4** | 2021–2024 | LE Audio, isochronous channels |

---

## ⚙️ 7.2 Bluetooth System Architecture

### 7.2.1 Core System Components

1. **Radio Layer** – Handles RF transmission and reception.  
2. **Baseband Layer** – Physical link management, packet timing, and error correction.  
3. **Link Manager (LM)** – Authentication, power management, and connection control.  
4. **Host Controller Interface (HCI)** – Command interface between host and controller.  
5. **L2CAP** – Logical link control and data multiplexing.  
6. **SDP (Service Discovery Protocol)** – Finds available services.  
7. **Application Layer** – Defines user-level functionality through profiles.

---

### 7.2.2 Bluetooth Protocol Stack Diagram

```
 ┌─────────────────────────────┐
 │     Application Profiles    │ ← RFCOMM, GATT, A2DP, HID
 ├─────────────────────────────┤
 │   L2CAP / ATT / SMP Layers  │
 ├─────────────────────────────┤
 │      HCI (Command/Event)    │
 ├─────────────────────────────┤
 │ Link Manager / Link Control │
 ├─────────────────────────────┤
 │      Baseband / PHY Radio   │
 └─────────────────────────────┘
```

---

## 🧩 7.3 Bluetooth Classic (BR/EDR) Architecture

Bluetooth Classic uses a **piconet** topology:  
- **One Master** device schedules communication.  
- **Up to seven Slaves** participate in synchronized data transfer.  

Multiple piconets can form a **scatternet**.

### Protocol Layers

| Layer | Function |
|-------|-----------|
| **Baseband** | Physical link and error control. |
| **Link Manager** | Authentication and link setup. |
| **L2CAP** | Multiplexing of logical channels. |
| **RFCOMM** | Serial Port Emulation. |
| **SDP** | Service discovery. |

### Common Profiles

| Profile | Description | Example |
|----------|-------------|----------|
| **SPP** | Serial Port Profile | Data exchange with ESP32 |
| **A2DP** | Advanced Audio | Wireless speakers |
| **HFP** | Hands-Free | Car audio systems |
| **OBEX/OPP** | File Transfer | File sharing |

---

## ⚡ 7.4 Bluetooth Low Energy (BLE) Architecture

BLE, introduced in **Bluetooth 4.0**, is optimized for **low-power IoT** communication.

### BLE Stack Layers

| Layer | Function |
|--------|-----------|
| **PHY** | 40 channels, 2 MHz spacing |
| **Link Layer** | Advertising, scanning, encryption |
| **L2CAP** | Data multiplexing |
| **ATT** | Attribute-based communication |
| **GATT** | Organizes data into services and characteristics |
| **SMP** | Pairing and encryption |
| **Application** | Sensor and device logic |

---

### BLE Stack Diagram

```
 ┌───────────────────────────────┐
 │ Application / Profiles        │ ← Temperature, Heart Rate, Custom UUIDs
 ├───────────────────────────────┤
 │ Generic Attribute Profile (GATT) │
 ├───────────────────────────────┤
 │ Attribute Protocol (ATT)      │
 ├───────────────────────────────┤
 │ L2CAP / Security Manager (SMP)│
 ├───────────────────────────────┤
 │ Link Layer / PHY Radio        │
 └───────────────────────────────┘
```

---

## 🧠 7.5 BLE Data Model (GATT)

| Element | Description |
|----------|-------------|
| **Service** | Collection of characteristics (e.g., Temperature Service) |
| **Characteristic** | Actual data value (e.g., 28.5 °C) |
| **Descriptor** | Metadata describing the characteristic |

**Example: Environmental Sensing Service**

| Attribute | UUID | Property | Description |
|------------|------|-----------|-------------|
| Service | 0x181A | — | Environmental Sensing |
| Characteristic | 0x2A6E | Notify | Temperature |
| Characteristic | 0x2A6F | Notify | Humidity |

---

## ⚙️ 7.6 Bluetooth Network Topologies

| Topology | Description | Example |
|-----------|-------------|----------|
| **Piconet** | 1 master, up to 7 slaves | Smartphone ↔ Headset |
| **Scatternet** | Multiple piconets | Multi-device streaming |
| **Star (BLE)** | Central ↔ Peripherals | Smartphone ↔ Sensors |
| **Mesh (BLE 5.0)** | Node-to-node relay | Smart lighting |

---

## 🔐 7.7 Bluetooth Security Architecture

| Security Element | Function |
|------------------|-----------|
| **Pairing** | Establishes trust |
| **Bonding** | Saves link keys |
| **Authentication** | Confirms device identity |
| **Encryption** | Protects data packets |
| **Privacy** | Random device addressing |

### BLE Security Modes

| Mode | Level | Authentication | Encryption | Description |
|------|--------|----------------|-------------|--------------|
| 1 | 1 | None | None | Open link |
| 1 | 2 | Unauthenticated | AES-CCM | Encrypted, no auth |
| 1 | 3 | Authenticated | AES-CCM | Secure link |
| 1 | 4 | Secure Connections | AES-CCM (ECC) | Highest level |

---

## 🔗 7.8 Bluetooth in IoT and CPS

Bluetooth and BLE act as the **edge communication layer** in IoT and CPS architectures.

| Layer | Function | Example |
|--------|-----------|----------|
| **Edge Layer** | BLE sensors collect data | ESP32 + LM73 |
| **Gateway Layer** | Smartphones aggregate BLE data | BLE-to-Wi-Fi bridge |
| **Cloud Layer** | Data visualization and storage | Node-RED, Firebase |

---

## 💡 7.9 Advantages and Limitations

| Advantages | Limitations |
|-------------|--------------|
| Low power | Short range |
| Cost-effective | 2.4 GHz interference |
| Secure | Limited bandwidth |
| Standardized | Multi-device complexity |

---

## 📗 7.10 Comparison: Classic vs. BLE

| Feature | Classic (BR/EDR) | BLE |
|----------|------------------|-----|
| Target | Audio, streaming | Sensors, IoT |
| Data Rate | 1–3 Mbps | 1–2 Mbps |
| Range | ~10 m | Up to 100 m |
| Power | High | Low |
| Topology | Piconet | Star/Mesh |
| Example | Headphones | Smartwatch |

---

## 🔬 7.11 Case Study — BLE Environmental Sensor

An ESP32 acts as a **BLE Peripheral** reading **temperature (LM73)** and broadcasting notifications.  
A smartphone or BLE gateway receives data and publishes to an **IoT dashboard (Node-RED)**.

```
[ESP32 + LM73 Sensor]
       ↓ BLE Notify
[Smartphone / Gateway]
       ↓ MQTT / WebSocket
[Node-RED Dashboard / Cloud]
```

---

## 🧩 7.12 Summary

- Bluetooth supports short-range data exchange using FHSS at 2.4 GHz.  
- **Classic** Bluetooth targets continuous, high-throughput applications.  
- **BLE** is optimized for periodic, low-power sensor communication.  
- **GATT** defines how BLE devices organize and expose data.  
- BLE is central to **IoT, CPS, and wearable systems**.  
- Integration with ESP32 demonstrates both **data acquisition and control** capabilities.

---

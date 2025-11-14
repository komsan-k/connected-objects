# 🌐 ESP32 Integrated IoT Project: Smart Environment Monitoring & Control System  
### Extended with Node-RED, BLE, and ESP-NOW

This project integrates all lab concepts into a **complete IoT ecosystem** built around the ESP32.  
It demonstrates embedded programming, multi-protocol wireless communication, real-time scheduling, sensor interfacing, and responsive dashboards.

---

# 1. Project Overview

The system functions as a **Smart Environment Monitoring & Control Station**.  
It collects data from multiple sensors (LDR, LM73 temperature, MPU6050 motion), synchronizes with NTP, and provides live visualization through:

- Web-based **AJAX dashboard**
- **Node-RED** dashboard
- **BLE GATT service**
- **ESP-NOW multi-node mesh**

The project supports **bidirectional communication**:

### Upstream
- Sends sensor data to remote servers via **TCP/UDP**
- Publishes to **Node-RED/MQTT**
- Streams to **AJAX dashboard**

### Downstream
- Receives control commands:
  - LEDs
  - Fans
  - Pumps
  - ESP-NOW node commands
  - BLE actuator writes

---

# 2. Objectives

- Initialize ESP32 and configure NTP for accurate timekeeping  
- Develop modular sensor drivers for LDR, LM73, and MPU6050  
- Implement interrupt-based motion event detection  
- Use FreeRTOS task scheduling for concurrent operations  
- Enable TCP/UDP client communication  
- Build a web server with AJAX for real-time updates  
- Integrate actuators with state feedback  
- Extend system via:
  - **Node-RED**
  - **BLE**
  - **ESP-NOW**

---

# 3. System Architecture

```
+-------------------+           +-------------------+
|   ESP32 MCU       |           |   Remote Server   |
|-------------------|           |-------------------|
| - NTP Sync        |           | - TCP Listener    |
| - Sensor Drivers  |           | - UDP Collector   |
|   * LDR           | <-------> | - Data Logging    |
|   * LM73 Temp     |   TCP/UDP | - Visualization   |
|   * MPU6050 IMU   |           +-------------------+
| - Actuators       |
|   * LED, Fan      |           +-------------------+
| - FreeRTOS Tasks  |  Browser  |   Web Dashboard   |
| - HTTP + AJAX     | <-------> | - Charts, Tables  |
| - BLE GATT        |   HTTP    | - Controls (LEDs) |
| - ESP-NOW Hub     |           +-------------------+
+-------------------+
```

---

# 4. Features

### ✔ Time Synchronization
Uses NTP for accurate timestamps.

### ✔ Multi-Sensor Support
- LDR  
- LM73 digital temperature  
- MPU6050 6-axis IMU  

### ✔ Interrupt Handling
Motion alerts using MPU6050 INT pin.

### ✔ Real-Time Scheduling
FreeRTOS tasks:
- Sensor task  
- Communication task  
- Dashboard task  
- BLE notify task  
- ESP-NOW receiver task  

### ✔ TCP/UDP Communication
Reliable vs fast packet performance comparison.

### ✔ Web Dashboard (AJAX)
Live charts, actuator switches, auto-refresh.

### ✔ Node-RED Dashboard
MQTT-based visualization, automation flows.

### ✔ ESP-NOW Integration
Low-power multi-node sensing over ESP-NOW to ESP32 hub.

### ✔ BLE Integration
BLE GATT service for local wireless control using smartphones.

---

# 5. Lab Mapping → Project Integration

| Lab | Contribution |
|-----|--------------|
| LAB 1 | ESP32 bring-up, NTP sync |
| LAB 2 | Embedded drivers for LDR, LM73, MPU6050 |
| LAB 3 | Sensor interfacing and calibration |
| LAB 4 | Interrupt handling, error recovery |
| LAB 5 | FreeRTOS scheduling |
| LAB 6 | TCP/UDP communication |
| LAB 7 | AJAX dashboard |
| EXT. 1 | Node-RED dashboard & MQTT |
| EXT. 2 | BLE GATT actuator control |
| EXT. 3 | ESP-NOW multi-node sensing |

---

# 6. Expected Outcomes

Students will build a **fully functional IoT prototype** featuring:

- Real-time, timestamped multi-sensor monitoring  
- Multi-protocol communication (HTTP, MQTT, BLE, ESP-NOW)  
- Interactive dashboards (web + Node-RED)  
- Remote + local actuator control  
- Multi-node wireless sensor networks  
- Capstone-ready design extensible to smart home and industrial IoT  

---

# 7. Extensions

### 🌩 Cloud Integration  
- MQTT broker (HiveMQ, Mosquitto, AWS IoT)  
- Firebase  
- ThingSpeak  

### 🤖 AI/ML Integration  
- TinyML for anomaly detection  
- Pattern recognition  
- Edge intelligence  

### 🔒 Security Layers  
- TLS for TCP/MQTT  
- BLE pairing & authentication  
- Token-based HTTP access  

---

# 8. Extended Multi-Protocol Instructions

## 8.1 Node-RED Integration

### Install Node-RED
```
npm install -g --unsafe-perm node-red
node-red
```
Access at **http://localhost:1880**

### Install dashboard nodes
- node-red-dashboard  
- node-red-contrib-chartjs  

### Recommended MQTT topics
```
iot/sensor/node1/ldr
iot/sensor/node1/temp
iot/sensor/node1/motion
iot/actuator/node1/led
iot/actuator/node1/fan
```

### Node-RED Dashboard Features
- Temperature & LDR charts  
- Motion timeline  
- LED/Fan switches  
- Last-seen timestamps  
- ESP-NOW node status  
- Automation rules (email/LINE alerts)  

---

## 8.2 BLE Integration

BLE adds **local wireless control** via phone apps such as nRF Connect.

### BLE Services
| Characteristic | Type | Description |
|----------------|------|-------------|
| env/ldr | notify | Light readings |
| env/temp | notify | LM73 temperature |
| env/motion | notify | MPU6050 motion |
| act/led | write | LED toggle |
| act/fan | write | Fan speed or ON/OFF |
| sys/timestamp | read | NTP time |

Use BLE for:
- Local commissioning (Wi-Fi setup)
- Debugging
- Quick actuator testing

---

## 8.3 ESP-NOW Integration

ESP-NOW allows low-power nodes to send data to the main ESP32 hub.

### Recommended ESP-NOW Node Data Structure
```json
{
  "nodeId": 3,
  "temp": 28.75,
  "ldr": 602,
  "motion": 0,
  "battery": 3.72,
  "counter": 145
}
```

### ESP32 Hub Responsibilities
- Register ESP-NOW peers  
- Timestamp packets  
- Publish to MQTT  
- Log to dashboard  

---

# 9. Multi-Protocol Data Routing Pipeline

| Protocol | Purpose | Range | Latency |
|----------|---------|--------|---------|
| ESP-NOW | Sensor mesh | Medium | Very low |
| BLE | Local control | Short | Low |
| Wi-Fi | Cloud + Dashboards | Long | Medium |

---

# 10. Updated System Diagram

```
                ┌──────────────────────┐
                │     Smartphone       │
                │   (BLE Interface)    │
                └─────────▲────────────┘
                          │ BLE
                          │
   ┌───────────── ESP-NOW Sensor Nodes ──────────────┐
   │                                                 │
   │  Node1: LM73 + LDR     Node2: Motion     Node3: Temp/LDR  │
   └─────────────┬─────────────┬──────────────┬───────────────┘
                 │             │              │ ESP-NOW
                 ▼             ▼              ▼

          ┌──────────────────────────────────────────┐
          │        ESP32 Main Hub (Project)          │
          │-------------------------------------------│
          │ - FreeRTOS Tasks                          │
          │ - NTP Time Sync                           │
          │ - AJAX Web Dashboard                      │
          │ - TCP/UDP Communication                   │
          │ - MQTT Publisher                          │
          │ - BLE Service                             │
          │ - ESP-NOW Gateway                         │
          └───────────────────────┬───────────────────┘
                                  │ Wi-Fi
                                  ▼
                      ┌─────────────────────┐
                      │     Node-RED        │
                      │  Dashboard + Flows  │
                      └─────────────────────┘
```

---

# 📚 References

### Official Espressif Documentation
1. Espressif Systems — *ESP-NOW User Guide*  
2. ESP-IDF Programming Guide  
3. ESP32 Technical Reference Manual  
4. ESP32 Product Overview  

### Community Tutorials
5. Random Nerd Tutorials — ESP-NOW  
6. ESP32 Forum Discussions  
7. Arduino-ESP32 GitHub Repository  

### Academic Literature
8. Yang et al., IoT Using ESP-NOW, IEEE IoT Journal, 2021  
9. Mijailović, ESP-NOW Performance, 2020  

---

# 🚀 End of README

This README consolidates **all core project features** and **multi-protocol extensions** into a professional, deployable IoT system.


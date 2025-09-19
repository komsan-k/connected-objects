# 🌐 ESP32 Integrated IoT Project: Smart Environment Monitoring & Control System

This project integrates all lab concepts into a **complete IoT system** built around the ESP32. It demonstrates embedded programming, real-time scheduling, sensor interfacing, reliable communication, and a responsive web dashboard.

---

## 1. Project Overview

The system functions as a **Smart Environment Monitoring & Control Station**.  
It collects data from multiple sensors (LDR, LM73, MPU6050), synchronizes with NTP for accurate timestamps, and provides real-time monitoring through a web-based AJAX dashboard.  

It supports **bidirectional communication**:
- **Upstream:** Sends data to remote PCs/servers via TCP/UDP.
- **Downstream:** Receives control commands from the web dashboard to actuators (LEDs, fans, pumps).

---

## 2. Objectives

- ✅ Initialize and configure ESP32 with NTP for accurate timekeeping.  
- ✅ Develop modular drivers for sensors (LDR, LM73, MPU6050).  
- ✅ Implement interrupt-based event detection (motion, threshold alerts).  
- ✅ Use FreeRTOS scheduling for concurrent task management.  
- ✅ Enable reliable TCP/UDP communication with external servers.  
- ✅ Host an HTTP server with AJAX-enabled dashboard for real-time monitoring and control.  
- ✅ Integrate actuators (LEDs/fans) with feedback and synchronization.  
- ✅ Build a cohesive system suitable for smart home or IoT deployments.  

---

## 3. System Architecture

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
+-------------------+   HTTP    | - Controls (LEDs) |
                                +-------------------+
```

---

## 4. Features

- **Time Synchronization:** Uses NTP for timestamp accuracy.  
- **Multi-Sensor Support:** Reads light, temperature, and motion data.  
- **Interrupt Handling:** Motion-triggered alerts via MPU6050.  
- **Real-Time Scheduling:** Sensor polling and communication run in separate FreeRTOS tasks.  
- **TCP/UDP Communication:** Sends sensor data to remote servers with reliability/performance comparison.  
- **AJAX Web Dashboard:** Provides live charts (Chart.js), tables, and actuator controls.  
- **Actuator Feedback:** Dashboard reflects real actuator state for synchronization.  

---

## 5. Lab Mapping → Project Integration

| Lab | Contribution to Project |
|-----|--------------------------|
| LAB 1 | ESP32 bring-up, NTP sync |
| LAB 2 | Embedded drivers for sensors |
| LAB 3 | Sensor interfacing (LDR, LM73, MPU6050) |
| LAB 4 | Interrupt handling, watchdog reliability |
| LAB 5 | Scheduling with FreeRTOS tasks |
| LAB 6 | TCP/UDP communication protocols |
| LAB 7 | AJAX web server and dashboard |

---

## 6. Expected Outcomes

- A **fully functional IoT prototype** running on ESP32.  
- Accurate **time-stamped sensor logs**.  
- Real-time **multi-sensor monitoring** with visual dashboard.  
- Responsive **actuator control** from web interface.  
- Reliable **communication over TCP/UDP** to external servers.  
- Demonstrated scalability for **IoT, smart home, and industrial use cases**.  

---

## 7. Extensions (Optional)

- 🌩️ Cloud integration (MQTT broker, Firebase, or ThingSpeak).  
- 📱 Mobile-optimized dashboard (progressive web app).  
- 🤖 AI/ML on ESP32 (TinyML anomaly detection).  
- 🔒 Security layers (TLS, token-based authentication).  

---

# 🚀 Final Note
This single integrated project serves as a **capstone** that consolidates all lab exercises into a robust **IoT monitoring and control system**, bridging theory and real-world IoT applications.


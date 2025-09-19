# 📘 Project Topics Based on ESP32 Lab Series

This document provides suggested project topics derived from the sequence of labs. Each project includes its **objectives** and **expected outcomes** to guide students in extending their lab exercises into real-world applications.

---

## Project 1 — Smart Environmental Monitoring with ESP32 and NTP
**Based on:** LAB 1 (ESP32 Bring-Up & NTP) + LAB 3 (Device Interfacing)

### Objectives
- Implement NTP-based time synchronization.
- Integrate LM73 temperature and LDR light sensors.
- Log timestamped sensor data locally.

### Expected Outcomes
- Working ESP32 program that retrieves accurate NTP time.
- Periodic logging of temperature and light intensity with timestamps.
- Demonstration of reliable time-based IoT data collection.

---

## Project 2 — Driver Development for IoT Sensor Suite
**Based on:** LAB 2 (Device Drivers) + LAB 3 (Device Interfacing)

### Objectives
- Develop modular drivers for LDR, LM73, and MPU6050 sensors.
- Provide consistent APIs for initialization and data acquisition.
- Validate drivers with test scripts.

### Expected Outcomes
- Reusable driver code for the sensor suite.
- Documentation of API functions.
- Demonstration of sensor readings on ESP32 serial monitor.

---

## Project 3 — Event-Driven Wearable Sensor Node
**Based on:** LAB 4 (Interruptions & Watchdog)

### Objectives
- Configure MPU6050 to trigger interrupts on motion events.
- Implement watchdog timer for system reliability.
- Demonstrate event-driven IoT sensing.

### Expected Outcomes
- ESP32-based wearable prototype detecting falls/tilts.
- Automatic recovery using watchdog resets.
- Logged or transmitted event alerts.

---

## Project 4 — Task Scheduling and Real-Time Sensor Fusion
**Based on:** LAB 5 (Scheduling with pthread/FreeRTOS)

### Objectives
- Use FreeRTOS tasks for concurrent sensor monitoring.
- Assign task priorities for real-time operation.
- Fuse sensor data for higher-level decisions.

### Expected Outcomes
- Demonstration of concurrent task execution.
- Performance comparison of scheduling strategies.
- Functional sensor fusion output.

---

## Project 5 — IoT Communication Gateway (TCP/UDP)
**Based on:** LAB 6 (TCP and UDP Communication)

### Objectives
- Implement TCP client-server and UDP datagram communication.
- Stream sensor data to a remote PC.
- Compare reliability and latency between TCP and UDP.

### Expected Outcomes
- Working dual-mode communication gateway.
- Data successfully sent and received via Python socket client.
- Report comparing TCP vs UDP performance.

---

## Project 6 — AJAX-Enabled Smart Home Dashboard
**Based on:** LAB 7 (HTTP Web Server with AJAX)

### Objectives
- Serve dynamic sensor data (LDR, LM73) via AJAX.
- Implement actuator control (e.g., LED, fan).
- Design a user-friendly web interface.

### Expected Outcomes
- Responsive dashboard accessible via browser.
- Real-time updates without page reload.
- Actuator control confirmed by ESP32 response.

---

## Project 7 — Integrated IoT System: Smart Weather Station
**Based on:** LAB 1 → LAB 7 (Integration Project)

### Objectives
- Integrate all previous lab concepts into one cohesive system.
- Collect, timestamp, and display multi-sensor data.
- Support both local dashboard and network communication.

### Expected Outcomes
- Complete weather station prototype.
- Real-time dashboard with charts and controls.
- Remote data access via TCP/UDP communication.
- Demonstrated scalability and reliability.

---

# 📑 Notes
- Each project builds on the skills developed in earlier labs.
- Projects can be implemented individually or expanded into group capstone projects.
- Extensions (e.g., cloud integration, mobile dashboards) are encouraged for innovation.



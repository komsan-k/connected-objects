# 📱 BLE Terminal Apps — Tools for ESP32 BLE Experiments and IoT Labs

This document lists the **best BLE (Bluetooth Low Energy) terminal applications** for Android, iOS, and desktop platforms, ideal for testing and interacting with **ESP32 BLE projects** such as LM73 temperature sensors, LED control, and IoT dashboards.

---

## 🔹 1. Android BLE Terminal Apps

| App Name | Developer | Key Features | Ideal Use | Link |
|-----------|------------|---------------|------------|------|
| **nRF Connect for Mobile** | Nordic Semiconductor | - Full BLE scanner<br>- Read/Write characteristics<br>- Subscribe to Notify updates<br>- UUID & RSSI display<br>- Export logs | Comprehensive BLE analysis and ESP32 GATT debugging | [Play Store](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp) |
| **BLE Scanner 2** | Bluepixel Technologies | - Fast scan and reconnect<br>- Real-time Notify data<br>- Graph view of sensor data | Visualizing temperature or humidity sensors | [Play Store](https://play.google.com/store/apps/details?id=com.bluepixeltech.blebrowser) |
| **BLE Terminal HM-10** | MightyIT | - BLE UART terminal<br>- Send and receive text data<br>- Custom UUIDs | BLE UART communication | [Play Store](https://play.google.com/store/apps/details?id=com.mightyit.gpsbluetoothterminal) |
| **Bluetooth LE Terminal** | Next Prototypes | - Simple GATT client<br>- Read, write, and notify<br>- UUID customization | Quick BLE service testing | [Play Store](https://play.google.com/store/apps/details?id=com.nextprot.bleterminal) |

💡 **Recommended for Students:**
- Use **nRF Connect** for detailed BLE UUID and data debugging.
- Use **BLE Scanner 2** for real-time visualization of Notify data (e.g., LM73 readings).

---

## 🍎 2. iOS BLE Terminal Apps

| App Name | Developer | Key Features | Ideal Use | Link |
|-----------|------------|---------------|------------|------|
| **LightBlue® Explorer** | Punch Through | - Scan nearby BLE devices<br>- Read/Write characteristics<br>- Simulate peripherals | ESP32 GATT development and testing | [App Store](https://apps.apple.com/app/lightblue/id557428110) |
| **nRF Connect for Mobile (iOS)** | Nordic Semiconductor | - Same as Android version<br>- Monitor Notify updates<br>- Log and export data | BLE data collection | [App Store](https://apps.apple.com/app/nrf-connect-for-mobile/id1054362403) |
| **BLE Terminal** | Glodanif | - Simple text terminal<br>- Custom UUID support<br>- Lightweight design | BLE write/notify communication | [App Store](https://apps.apple.com/app/ble-terminal/id1456601061) |
| **BlueSee** | BlueSee.io | - BLE GATT client<br>- History logs and graphs<br>- Clean GUI | BLE sensor monitoring | [App Store](https://apps.apple.com/app/bluesee/id1507521486) |

💡 **Recommended:**  
For iPhone/iPad, **LightBlue Explorer** is the most reliable BLE debugging and educational app.

---

## 💻 3. Desktop BLE Tools (Windows, macOS, Linux)

| Tool | Platform | Description | Ideal For | Link |
|------|-----------|--------------|------------|------|
| **nRF Connect for Desktop** | Windows/macOS/Linux | - Advanced BLE sniffer & GATT client<br>- Modify services and characteristics | Professional debugging and development | [nRF Connect Desktop](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop) |
| **BLE Terminal (Windows UWP)** | Windows | - Simple BLE scanner<br>- Read/write/notify interface | Classroom BLE testing | [Microsoft Store](https://apps.microsoft.com/store/detail/ble-terminal/9NBLGGH42THS) |
| **Web Bluetooth Terminal (Browser)** | Chrome / Edge | - Uses Web Bluetooth API<br>- Read/write/notify BLE devices<br>- Works with Node-RED dashboards | BLE-to-Web integration | [Web Bluetooth Demos](https://github.com/WebBluetoothCG/demos) |

💡 **Recommended for Instructors:**
- Use **nRF Connect for Desktop** for advanced GATT visualization and packet analysis.
- Use **Web Bluetooth** for integrating BLE with Node-RED dashboards.

---

## 🧭 4. Suggested Usage in ESP32 Labs

| Lab Activity | Recommended App | Purpose |
|---------------|----------------|----------|
| **BLE Temperature (LM73)** | *nRF Connect / BLE Scanner 2* | Read Notify characteristic updates |
| **BLE LED Control (Write Command)** | *BLE Terminal HM-10 / LightBlue* | Send JSON or simple control strings |
| **BLE → Node-RED Dashboard** | *Web Bluetooth Terminal* | Connect BLE to WebSocket/MQTT |
| **Advanced GATT Debugging** | *nRF Connect Desktop* | Inspect and test multiple services |

---

## 📊 5. Comparison Summary

| Platform | Best App | BLE Type | Strength |
|-----------|-----------|----------|-----------|
| Android | **nRF Connect** | BLE | Full GATT read/write/notify |
| Android | **BLE Scanner 2** | BLE | Real-time visualization |
| iOS | **LightBlue Explorer** | BLE | Professional & user-friendly |
| Windows | **nRF Connect Desktop** | BLE | Advanced developer toolkit |
| Web | **Web Bluetooth Demo** | BLE | Ideal for Node-RED dashboard integration |

---

## 🧠 6. Summary

- BLE Terminal apps are essential tools for **testing, monitoring, and debugging BLE communication** between **ESP32** and a smartphone or PC.  
- They allow users to **read**, **write**, and **subscribe** to BLE characteristics without custom app development.  
- **nRF Connect** (Android/iOS) and **LightBlue Explorer** (iOS) are the top educational tools.  
- Pair these with **Node-RED** and **Web Bluetooth** for real-time IoT dashboard integration.

---

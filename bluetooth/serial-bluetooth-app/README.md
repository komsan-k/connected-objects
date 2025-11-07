# 📱 Serial Bluetooth Terminal Apps — Tools for ESP32 Bluetooth and BLE Labs

This guide lists the **best mobile and desktop applications** to communicate with your **ESP32** using **Bluetooth Classic (SPP)** or **Bluetooth Low Energy (BLE)** during practical experiments.

---

## 🔹 1. Android Apps (Recommended for ESP32)

| App Name | Type | Key Features | Link |
|-----------|------|---------------|------|
| **Serial Bluetooth Terminal** *(by Kai Morich)* | 🟦 Classic (SPP) | - Clean terminal interface<br>- Supports macros & auto-reconnect<br>- Free and open source | [Play Store](https://play.google.com/store/apps/details?id=de.kai_morich.serial_bluetooth_terminal) |
| **Bluetooth Terminal HC-05** | 🟦 Classic (SPP) | - Lightweight, quick pairing<br>- Button shortcuts for pre-defined commands | [Play Store](https://play.google.com/store/apps/details?id=project.bluetoothterminal) |
| **nRF Connect for Mobile** *(by Nordic Semiconductor)* | 🟩 BLE (GATT) | - Full BLE scanner<br>- Read/write/notify BLE characteristics<br>- UUID-based exploration | [Play Store](https://play.google.com/store/apps/details?id=no.nordicsemi.android.mcp) |
| **BLE Scanner 2** *(by Bluepixel Technologies)* | 🟩 BLE (GATT) | - Auto-detect BLE devices<br>- Display live notification data<br>- Export data to CSV | [Play Store](https://play.google.com/store/apps/details?id=com.bluepixeltech.blebrowser) |

💡 **Recommendation for students:**
- Use **Serial Bluetooth Terminal** for **Bluetooth Classic labs**.  
- Use **nRF Connect** or **BLE Scanner 2** for **BLE experiments** (e.g., LM73 sensor).

---

## 🍎 2. iOS Apps (for iPhone/iPad)

| App Name | Type | Features | Link |
|-----------|------|-----------|------|
| **LightBlue® Explorer** *(by Punch Through)* | 🟩 BLE | - Visualize BLE services & characteristics<br>- Read/write UUIDs<br>- Great for debugging | [App Store](https://apps.apple.com/app/lightblue/id557428110) |
| **nRF Connect for Mobile (iOS)** | 🟩 BLE | - Same features as Android version<br>- Perfect for ESP32 BLE sensor projects | [App Store](https://apps.apple.com/app/nrf-connect-for-mobile/id1054362403) |
| **Bluetooth Terminal BLE UART** *(various developers)* | 🟦 Classic / BLE | - Simple serial console alternative<br>- Some limitations on Apple’s API | Search in App Store |

---

## 💻 3. Desktop Applications (Windows / macOS / Linux)

| Application | Type | Description | Link |
|--------------|------|-------------|------|
| **Tera Term** | 🟦 Classic | Serial & Bluetooth COM port terminal; scripting and logging | [Tera Term](https://osdn.net/projects/ttssh2/) |
| **CoolTerm** | 🟦 Classic | Simple GUI for serial/Bluetooth communication; real-time data logging | [CoolTerm](https://freeware.the-meiers.org/) |
| **Putty** | 🟦 Classic | Lightweight serial terminal supporting Bluetooth COM ports | [Putty](https://www.putty.org) |
| **nRF Connect for Desktop** | 🟩 BLE | Full BLE service viewer and sniffer; ideal for developers | [nRF Connect Desktop](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop) |

---

## 🧩 4. Recommended Combinations for ESP32 Labs

| Experiment | App / Tool | Reason |
|-------------|-------------|--------|
| **Lab 1 – Bluetooth Classic Chat** | *Serial Bluetooth Terminal (Android)* | Simple SPP text exchange |
| **Lab 2 – BLE Temperature Node (LM73)** | *nRF Connect* | Real-time notification data |
| **Lab 3 – BLE Dashboard Integration** | *nRF Connect + Node-RED Dashboard* | BLE → Web Bluetooth → MQTT |
| **Instructor Demo (PC)** | *Tera Term / CoolTerm* | Display serial data for class |

---

## 🧭 5. Classroom Setup Tips

- Pair each ESP32 to **one smartphone** for SPP connection.  
- Enable **Bluetooth + Location permissions** (required on Android).  
- Use **nRF Connect** for verifying **UUIDs**, **services**, and **notify data**.  
- For IoT dashboard projects, run **Node-RED + Web Bluetooth bridge** on a laptop.

---

## 📊 6. Comparison Summary

| Platform | App | Classic SPP | BLE Support | Ideal For |
|-----------|------|-------------|--------------|------------|
| Android | Serial Bluetooth Terminal | ✅ | ❌ | Serial text chat |
| Android | nRF Connect | ❌ | ✅ | BLE sensors and GATT inspection |
| iOS | LightBlue Explorer | ❌ | ✅ | BLE device debugging |
| Windows | Tera Term | ✅ | ❌ | Serial or paired COM port |
| Windows | nRF Connect Desktop | ❌ | ✅ | BLE developer toolkit |

---

## 🧠 7. Summary

- **Serial Bluetooth Terminal** (by Kai Morich) is the best educational app for **Bluetooth Classic SPP**.  
- **nRF Connect** and **BLE Scanner 2** are ideal for **BLE labs**.  
- On **PCs**, use **Tera Term** or **CoolTerm** to simulate smartphone terminals.  
- Combining these tools allows complete testing of ESP32 Bluetooth systems from **low-level serial chat** to **BLE cloud integration**.

---

# ESP32 Wi-Fi Signal Strength Utilities

This repository provides two Arduino sketches to analyze and monitor Wi-Fi connectivity on ESP32 boards.  
They are designed for **signal monitoring**, **auto-reconnect handling**, and **site surveys** to improve ESP32 deployment.

---

## 1. ESP32_RSSI_Monitor.ino

### Overview
This sketch connects the ESP32 to Wi-Fi, monitors signal strength (RSSI), and provides both **serial output** and **LED blink feedback**.  
It also features **auto-reconnect with exponential backoff** for unstable networks.

### Features
- Connects to Wi-Fi using your SSID/PASS.  
- Prints **RSSI (dBm)** every second.  
- Maintains a **moving average** to smooth RSSI fluctuations.  
- Classifies signal quality into: *excellent, very good, good, fair, weak, very weak*.  
- Implements **auto-reconnect with exponential backoff** (1s → 2s → 4s … up to 16s).  
- LED on GPIO2 blinks faster with stronger signals, slower with weaker ones.

### Example Serial Output
```
millis,rssi_dbm,rssi_avg_dbm,quality,channel
10234,-52,-55,very good,6
11234,-53,-54,very good,6
12234,-70,-60,good,6
```

### LED Blink Mapping
- **-40 dBm → ~150 ms blink** (very strong)  
- **-90 dBm → ~900 ms blink** (very weak)  

### Usage
- Replace `YOUR_SSID` and `YOUR_PASS` with Wi-Fi credentials.  
- Update `LED_PIN` if your board uses a different LED.  
- Open **Serial Monitor/Plotter** at 115200 baud to observe live logs.  

---

## 2. ESP32_WiFi_SiteSurvey.ino

### Overview
This sketch scans all nearby networks, prints details (SSID, RSSI, channel, encryption), builds a **channel histogram**, and suggests a cleaner channel among 1, 6, and 11.

### Features
- Scans for nearby access points.  
- Prints SSID, RSSI (dBm), Channel, and Encryption type.  
- Creates a **per-channel histogram** (AP count and avg RSSI).  
- Suggests the **best channel (1/6/11)** based on congestion and interference.  

### Example Serial Output
```
Found 8 networks
Idx,SSID,RSSI(dBm),Channel,Encryption
0,HomeWiFi,-42,6,WPA2_PSK
1,CoffeeShopWiFi,-78,1,OPEN
...

Channel histogram (AP count / avg RSSI):
Ch  1: APs=2, avgRSSI=-72 dBm  ##
Ch  6: APs=4, avgRSSI=-55 dBm  ####
Ch 11: APs=1, avgRSSI=-80 dBm  #

Suggested 2.4 GHz channel (1/6/11): 11
```

### Usage
- Upload sketch and open **Serial Monitor** at 115200 baud.  
- Press **RESET** to rescan networks.  
- Run this first to pick a cleaner channel on your router.  

---

## 3. Practical Workflow

1. **Run `ESP32_WiFi_SiteSurvey.ino`**  
   → Identify the least congested Wi-Fi channel (1, 6, or 11).  

2. **Run `ESP32_RSSI_Monitor.ino`**  
   → Monitor signal stability and observe LED blink speed at different placements.  

---

## 4. Notes & Tips
- Always replace `YOUR_SSID` and `YOUR_PASS` before uploading.  
- Use **Serial Plotter** or export logs to **MQTT/Node-RED** for visualization.  
- If your ESP32 signal remains weak:
  - Use a board with **external antenna support** (ESP32-WROOM-32U).  
  - Deploy **mesh Wi-Fi** or **extenders**.  
  - For long-range low-power communication, consider **LoRa** or **ESP-NOW**.  

---

## ✅ Summary
These two sketches help ESP32 developers:  
- **Monitor** Wi-Fi quality with live RSSI and LED feedback.  
- **Survey** local Wi-Fi networks to optimize channel selection.  
- **Improve** connectivity reliability with auto-reconnect and better placement.

By combining **monitoring** and **site survey**, ESP32 deployment becomes more stable and efficient.


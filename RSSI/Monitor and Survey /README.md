# ESP32 Wi-Fi Tools: RSSI Monitor & Site Survey

This repository provides two Arduino sketches for **ESP32 Wi-Fi analysis and diagnostics**:

1. **ESP32_RSSI_Monitor.ino** – Monitors Wi-Fi signal strength (RSSI), logs values, and provides LED feedback.  
2. **ESP32_WiFi_SiteSurvey.ino** – Scans nearby networks, builds a channel histogram, and suggests the cleanest Wi-Fi channel.

---

## 1. ESP32_RSSI_Monitor.ino

### Overview
This sketch connects the ESP32 to Wi-Fi, continuously prints **RSSI (dBm)** values, calculates a moving average, classifies signal quality, and uses an LED to indicate signal strength.  
It also implements **auto-reconnect with exponential backoff** if the connection drops.

### Features
- Connects to Wi-Fi using provided SSID and password.  
- Prints RSSI every second with moving average smoothing.  
- Signal quality classification: *excellent, very good, good, fair, weak, very weak*.  
- LED (GPIO 2) blinks faster for strong signals, slower for weak ones.  
- Auto-reconnect logic with backoff (1s → 2s → 4s → up to 16s).  

### Example Serial Output
```
millis,rssi_dbm,rssi_avg_dbm,quality,channel
10234,-52,-55,very good,6
11234,-53,-54,very good,6
12234,-70,-60,good,6
```

### LED Blink Mapping
- **-40 dBm → 150 ms blink** (very strong)  
- **-90 dBm → 900 ms blink** (very weak)  

### Usage Notes
- Replace `YOUR_SSID` and `YOUR_PASS` with Wi-Fi credentials.  
- Change `LED_PIN` if using a different LED.  
- Open Serial Monitor/Plotter at 115200 baud to view logs.  

---

## 2. ESP32_WiFi_SiteSurvey.ino

### Overview
This sketch scans nearby Wi-Fi networks, prints details (SSID, RSSI, channel, encryption), and builds a **channel histogram**.  
It then suggests the best channel among **1, 6, and 11** for 2.4 GHz networks.

### Features
- Scans all nearby access points.  
- Displays SSID, RSSI, channel, and encryption type.  
- Calculates per-channel stats (AP count and average RSSI).  
- Prints a histogram to visualize congestion.  
- Suggests the cleanest channel (1, 6, or 11).  

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

### Usage Notes
- Run the sketch and open Serial Monitor at 115200 baud.  
- Press **RESET** to rescan networks.  
- Run this first to find the optimal router channel before deploying your ESP32 project.  

---

## 3. Practical Workflow

1. **Run `ESP32_WiFi_SiteSurvey.ino`**  
   - Identify the least congested channel (1, 6, or 11).  
   - Configure your router to that channel.  

2. **Run `ESP32_RSSI_Monitor.ino`**  
   - Monitor Wi-Fi stability and signal quality over time.  
   - Use LED blink speed and Serial logs for real-time feedback.  

---

## 4. Notes & Tips
- Always replace `YOUR_SSID` and `YOUR_PASS` in the code.  
- Use Serial Plotter or log RSSI values to MQTT/Node-RED for visualization.  
- If your ESP32 signal is weak:
  - Use boards with **external antenna connectors** (e.g., ESP32-WROOM-32U).  
  - Place ESP32 away from metallic objects and interference sources.  
  - Consider mesh Wi-Fi, Ethernet PHY, or alternative protocols like **LoRa** or **ESP-NOW**.  

---

## ✅ Summary
These tools allow ESP32 developers to:  
- **Monitor** signal quality with real-time logging and LED feedback.  
- **Survey** Wi-Fi environments to optimize channel selection.  
- **Improve** connectivity stability with retry logic and better placement.  

By combining both sketches, you can significantly enhance ESP32 Wi-Fi reliability in real-world deployments.


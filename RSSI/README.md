# ESP32 Wi-Fi Signal Strength Tools

This repository provides two practical Arduino sketches for analyzing and improving Wi-Fi connectivity on **ESP32** devices:

1. **ESP32_RSSI_Monitor.ino** → Monitors real-time signal strength, averages values, classifies quality, blinks LED by strength, and auto-reconnects on drop.  
2. **ESP32_WiFi_SiteSurvey.ino** → Scans nearby networks, prints details, builds a channel histogram, and suggests a cleaner Wi-Fi channel.

Together, these tools help diagnose connectivity problems and optimize ESP32 placement and router configuration.

---

## 1. ESP32_RSSI_Monitor.ino

### Features
- Connects to a Wi-Fi network.  
- Prints **RSSI (dBm)** every second with a **moving average filter** (configurable window size).  
- Classifies RSSI into categories: *excellent, very good, good, fair, weak, very weak*.  
- Implements **auto-reconnect with exponential backoff** to improve reliability on unstable networks.  
- Blinks **LED on GPIO 2** (default) with speed proportional to signal strength:
  - Strong signal → fast blink  
  - Weak signal → slow blink  

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

### Code Highlights
- **Moving Average** buffer smooths short-term fluctuations.  
- **Exponential Backoff** prevents aggressive reconnect storms: starts at 1s, doubles up to 16s max.  
- Prints both **instantaneous RSSI** and **averaged RSSI** for better diagnosis.  

### Usage Notes
- Replace `YOUR_SSID` and `YOUR_PASS` with Wi-Fi credentials.  
- Update `LED_PIN` if your ESP32 board uses a different user LED.  
- Use **Serial Plotter** or send logs to MQTT for real-time visualization.  

---

## 2. ESP32_WiFi_SiteSurvey.ino

### Features
- Performs a **Wi-Fi scan** and lists:
  - SSID (network name)  
  - RSSI (signal strength in dBm)  
  - Channel  
  - Encryption type (OPEN, WPA2, WPA3, etc.)  
- Builds a **per-channel histogram** showing AP counts and average RSSI.  
- Suggests the **best channel** among **1, 6, and 11** (standard non-overlapping 2.4 GHz channels).  

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

### Code Highlights
- Tracks both **number of APs** and **average RSSI per channel**.  
- Prefers channels with **fewer APs** and **weaker interference** (more negative avg RSSI).  
- Runs once per reset — press **RESET button** to rescan.  

### Usage Notes
- Run this sketch before deploying ESP32 projects to choose a cleaner channel on your router/AP.  
- Particularly useful in **crowded environments** (apartments, offices, labs).  

---

## 3. Practical Workflow

1. **Run `ESP32_WiFi_SiteSurvey.ino`**  
   → Identify the least congested channel (1, 6, or 11) and configure your router accordingly.  

2. **Run `ESP32_RSSI_Monitor.ino`**  
   → Place ESP32 at various locations, observe RSSI quality and LED blink speed.  
   → Use logs to confirm stable coverage and auto-reconnect reliability.  

---

## 4. Notes & Tips

- Always replace `YOUR_SSID` and `YOUR_PASS` before uploading.  
- Use `Serial.begin(115200)` with **Serial Monitor or Plotter** for best visibility.  
- If you’re logging RSSI to **MQTT/Node-RED**, you can build long-term heatmaps of your Wi-Fi coverage.  
- If signal is too weak despite optimizations:
  - Consider ESP32 modules with **external antenna connectors** (e.g., WROOM-32U).  
  - Use **mesh Wi-Fi systems** or **extenders**.  
  - For long-range/low-power applications, consider **LoRa** or **ESP-NOW** instead of Wi-Fi.  

---

## ✅ Summary

These two tools help ESP32 developers:  

- **Monitor** connectivity stability with live RSSI logging and auto-reconnect.  
- **Survey** Wi-Fi environments to select optimal router channels.  
- **Diagnose** coverage issues using RSSI trends and visual indicators (LED + logs).  

By combining **hardware placement**, **channel optimization**, and **reconnect logic**, you can greatly improve ESP32 Wi-Fi reliability.

---


# LPWAN Technologies and Recent Products

This document provides an overview of **Low-Power Wide-Area Network (LPWAN)** technologies, focusing on **LoRa (unlicensed)** versus **NB-IoT and LTE-M (licensed)**, along with a selection of recent commercial products and development boards.

---

## 📡 LPWAN Overview

### What is LPWAN?
- LPWAN = **Low-Power Wide-Area Network**.
- A **family of technologies** designed for:
  - Long-range communication (several km).
  - Low data rates (a few kbps).
  - Ultra-low power (battery life up to years).
- Two categories:
  - **Unlicensed spectrum LPWAN** (LoRa, Sigfox, Weightless).
  - **Licensed spectrum LPWAN** (NB-IoT, LTE-M).

### LoRa vs NB-IoT vs LTE-M

| Feature          | LoRa (Unlicensed)         | NB-IoT (Licensed)         | LTE-M (Licensed)          |
|------------------|----------------------------|---------------------------|---------------------------|
| **Spectrum**     | ISM (433/868/915 MHz)      | Licensed (telco)          | Licensed (telco)          |
| **Ownership**    | Private or public          | Operator only             | Operator only             |
| **Range**        | 2–15 km                    | 1–10 km (good indoor)     | 1–10 km                   |
| **Data rate**    | 0.3–50 kbps                | ~250 kbps                 | ~1 Mbps                   |
| **Battery life** | 5–10 years                 | 5–7 years                 | 2–5 years                 |
| **Cost**         | Low, no SIM needed         | SIM + higher module cost  | SIM + higher module cost  |
| **Mobility**     | Limited (static sensors)   | Fixed devices             | Full mobility (handover)  |

### Use Cases
- **LoRa** → Smart agriculture, utilities, campus IoT, private/community networks.  
- **NB-IoT** → Smart meters, parking sensors, environmental monitoring.  
- **LTE-M** → Asset tracking, logistics, wearables, mobile IoT.  

---

## 🛠️ Recent Commercial LPWAN Products

| Product | Features / Notes | URL |
|---------|------------------|-----|
| **RAKwireless WisDuo** | Stamp-sized ultra-low power LoRaWAN + P2P modules (STM32WLE5 + SX1262). | [RAKwireless WisDuo](https://www.rakwireless.com/en-us/products/modules-for-lorawan) |
| **Murata LoRa Modules** | Compact LPWA/LoRaWAN modules for small IoT devices. | [Murata LoRa](https://www.murata.com/en-us/products/connectivitymodule/lora) |
| **Murata Cat M1 / NB-IoT Modules** | Licensed LPWA modules (LTE-M, NB-IoT). | [Murata Cat M1 / NB-IoT](https://www.murata.com/en-us/products/connectivitymodule/cat-m1) |
| **Telit / Cinterion LPWA** | NB-IoT / LTE-M modules with PSM & eDRX support. | [Telit LPWA](https://www.telit.com/modules-overview/cellular-lpwa/) |
| **Sierra Wireless HL7812** | LTE-M / NB-IoT module, global coverage, compact. | [Sierra HL7812](https://www.sierrawireless.com/iot-modules/lpwa-modules/hl7812/) |
| **MultiTech xDot** | Certified LoRaWAN modules for industrial IoT. | [MultiTech xDot](https://multitech.com/all-products/lorawan-devices/lorawan-modules/) |
| **Nordic nRF91 Series** | Cellular IoT SiPs: LTE-M, NB-IoT, GNSS. | [Nordic nRF91](https://www.nordicsemi.com/Products/Wireless/Low-power-cellular-IoT) |

---

## 🔧 Development Boards (LoRa / LoRaWAN)

- **Heltec ESP32-OLED LoRa Dev Board (915 MHz)**  
  Built-in OLED, LoRaWAN support.  
  💵 ~THB 849  
  🔗 [Heltec Store](https://heltec.org/project/wifi-lora-32/)  

- **LilyGO TTGO LoRa32 OLED (868 MHz)**  
  ESP32 + LoRa + small OLED display.  
  💵 ~THB 816  
  🔗 [LilyGO GitHub](https://github.com/LilyGO/TTGO-LORA32-V2.1)  

- **ESP32 + SX1278 LoRa Dev Board (433 MHz)**  
  Long-range, 433 MHz.  
  💵 ~THB 820  
  🔗 [Lazada TH](https://www.lazada.co.th/tag/esp32-lora/)  

- **ESP32 LoRaWAN Gateway Module (with 1.8″ LCD)**  
  DIY gateway with display.  
  💵 ~THB 875  
  🔗 [Elecrow](https://www.elecrow.com/esp32-lorawan-gateway.html)  

- **SX1276 ESP32 LoRa Multi-Band Node**  
  Multi-band (433/868/915 MHz).  
  💵 ~THB 500  
  🔗 [Shopee TH](https://shopee.co.th/search?keyword=esp32%20sx1276%20lora)  

- **Pre-certified LoRaWAN Module for ESP32 (SB Components)**  
  Saves regulatory compliance time.  
  💵 ~THB 1,838  
  🔗 [SB Components](https://shop.sb-components.co.uk/products/esp32-lora)  

---

## 📚 References
1. LoRa Alliance – [LoRaWAN Specification](https://lora-alliance.org)  
2. Semtech – [LoRa Technology Overview](https://www.semtech.com/lora)  
3. 3GPP – [Release 13: NB-IoT and LTE-M](https://www.3gpp.org)  
4. Raza, U. et al. (2017). *Low Power Wide Area Networks: An Overview*. IEEE Communications Surveys & Tutorials, 19(2), 855–873.  
5. Centenaro, M. et al. (2016). *Long-range communications in unlicensed bands*. IEEE Wireless Communications, 23(5), 60–67.  
6. GSMA – [NB-IoT and LTE-M Deployment Guide](https://www.gsma.com/iot)  

---

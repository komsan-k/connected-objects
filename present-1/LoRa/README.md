# LPWAN vs LoRa vs NB-IoT vs LTE-M

This document explains the relationship between **LPWAN** technologies, focusing on **LoRa (unlicensed)** compared with **NB-IoT** and **LTE-M (licensed)**.

---

## 1. What is LPWAN?
- **LPWAN** = Low-Power Wide-Area Network.  
- Not a single protocol, but a **category** of long-range, low-power wireless technologies.  
- Two major groups:
  - **Unlicensed spectrum LPWAN** (LoRa, Sigfox, Weightless).  
  - **Licensed spectrum LPWAN** (NB-IoT, LTE-M).  

---

## 2. What is LoRa?
- **LoRa** = *Long Range*.  
- A **modulation technique** (Chirp Spread Spectrum) developed by Semtech.  
- Works in **unlicensed ISM bands** (433 MHz, 868 MHz, 915 MHz).  
- With **LoRaWAN protocol** (by the LoRa Alliance), it becomes a full networking solution.  

---

## 3. Relationship Between LPWAN and LoRa
- **LPWAN** = the family of technologies.  
- **LoRa/LoRaWAN** = one member of that family (under *unlicensed LPWAN*).  

---

## 4. Unlicensed LPWAN Examples
- **LoRa / LoRaWAN**  
- **Sigfox**  
- **Weightless**  

---

## 5. Comparison: LoRa vs NB-IoT vs LTE-M

| Feature          | LoRa (Unlicensed)         | NB-IoT (Licensed)         | LTE-M (Licensed)          |
|------------------|----------------------------|---------------------------|---------------------------|
| **Spectrum**     | ISM (433/868/915 MHz)      | Licensed (telco)          | Licensed (telco)          |
| **Ownership**    | Private or public          | Operator only             | Operator only             |
| **Range**        | 2–15 km                    | 1–10 km (good indoor)     | 1–10 km                   |
| **Data rate**    | 0.3–50 kbps                | ~250 kbps                 | ~1 Mbps                   |
| **Battery life** | 5–10 years                 | 5–7 years                 | 2–5 years                 |
| **Cost**         | Low, no SIM needed         | SIM + higher module cost  | SIM + higher module cost  |
| **Mobility**     | Limited (static sensors)   | Fixed devices             | Full mobility (handover)  |

---

## 6. Use Cases
- **LoRa**: Smart agriculture, smart meters, campus IoT, community networks.  
- **NB-IoT**: Utility meters, parking sensors, environmental monitoring.  
- **LTE-M**: Asset tracking, logistics, wearables, mobile IoT.  

---

## ✅ Summary
- **LoRa** → Low-cost, private, unlicensed spectrum, best for **static sensors** with ultra-low power.  
- **NB-IoT** → Reliable, licensed spectrum, better **indoor coverage**, but requires operator.  
- **LTE-M** → Licensed spectrum, **supports mobility** and higher throughput, good for moving assets.  

---

## 📚 References
1. LoRa Alliance. *LoRaWAN Specification*. [https://lora-alliance.org](https://lora-alliance.org)  
2. Semtech Corporation. *LoRa Technology Overview*. [https://www.semtech.com/lora](https://www.semtech.com/lora)  
3. 3GPP. *Release 13: Narrowband IoT (NB-IoT) and LTE-M*. [https://www.3gpp.org](https://www.3gpp.org)  
4. Raza, U., Kulkarni, P., & Sooriyabandara, M. (2017). *Low Power Wide Area Networks: An Overview*. IEEE Communications Surveys & Tutorials, 19(2), 855–873.  
5. Centenaro, M., Vangelista, L., Zanella, A., & Zorzi, M. (2016). *Long-range communications in unlicensed bands: The rising stars in the IoT and smart city scenarios*. IEEE Wireless Communications, 23(5), 60–67.  
6. GSMA. *NB-IoT and LTE-M Deployment Guide to Basic Feature Set Requirements*. [https://www.gsma.com/iot](https://www.gsma.com/iot)  


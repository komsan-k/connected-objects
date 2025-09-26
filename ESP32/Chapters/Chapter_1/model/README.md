# 📜 Background (pre-ESP32)

## Timeline

  ----------------------------------------------------------------------------
  Year                          Milestone
  ----------------------------- ----------------------------------------------
  2008                          Espressif Systems founded.
                                ([espressif.com](https://www.espressif.com))

  \~2013                        The first Espressif Wi-Fi SoC, **ESP8089**, is
                                released (for tablets / set-top boxes).

  2014                          **ESP8266** launches, becomes popular for
                                cheap Wi-Fi IoT development.
  ----------------------------------------------------------------------------

# 🚀 ESP32 Series --- Major Versions & Variants

Here's a chronological view of the ESP32 generation and how Espressif
expanded and diversified the family:

  -------------------------------------------------------------------------
  Approx Year Variant /       CPU /             Key Features /
              Series          Architecture      Differentiators
  ----------- --------------- ----------------- ---------------------------
  2016        **Original      Dual-core Xtensa  Wi-Fi (2.4 GHz 802.11
              ESP32**         LX6 (or           b/g/n) + Bluetooth BR/EDR +
                              single-core)      BLE, \~520 KB SRAM.

  \~2020      **ESP32-S2**    Single-core       More power-efficient, no
                              Xtensa LX7        Bluetooth, adds USB OTG
                                                support.

  \~2020      **ESP32-C3**    Single-core       Wi-Fi + Bluetooth LE,
                              RISC-V            ESP8266 pin-compatible.

  \~2021      **ESP32-C6**    RISC-V            Wi-Fi 6 (802.11ax),
                                                Bluetooth LE, IEEE 802.15.4
                                                (Thread/Zigbee).

  \~2022 /    **ESP32-C5**    Single-core       Dual-band Wi-Fi 6 (2.4 + 5
  2025                        RISC-V            GHz), Bluetooth LE, IEEE
                                                802.15.4.

  2023        **ESP32-P4**    Dual-core RISC-V  High-performance compute /
                                                AI / media, no built-in
                                                Wi-Fi/Bluetooth.

  \~2023      **ESP32-H2**    Single-core       Zigbee / Thread + Bluetooth
                              RISC-V            LE (no Wi-Fi).
  -------------------------------------------------------------------------

# 🔍 Observations & Trends

-   The **original ESP32 (2016)** used Xtensa cores; newer lines (C / P
    / H series) shift toward **RISC-V** architectures.\
-   Espressif expanded from the all-in-one Wi-Fi + BT paradigm into more
    **specialized variants**:
    -   "S2 / S3" → streamlined tradeoffs (e.g., S2 lacks Bluetooth,
        adds USB OTG).\
    -   "C / H / P" → adding/removing connectivity (Wi-Fi, BLE,
        Thread/Zigbee) or focusing on compute/AI.\
    -   Some variants don't carry full wireless stacks (e.g., P4 is
        purely a compute MCU).\
-   All variants maintain software compatibility via **ESP-IDF**,
    ensuring code reusability.


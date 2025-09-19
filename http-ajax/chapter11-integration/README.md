# Integration with Cloud and APIs

## Introduction

While ESP32 AJAX dashboards provide local access, most IoT applications
require remote monitoring, long-term storage, and advanced analytics.
Cloud services extend ESP32 capabilities beyond local networks.

In this chapter, we study cloud integration with ESP32 using REST APIs.
We focus on ThingSpeak, Firebase, and Node-RED. We also explore hybrid
local+cloud architectures, API security, and practical case studies.

## The Role of Cloud in IoT

### Cloud Layers

-   **Edge** --- ESP32 devices collecting and preprocessing data.

-   **Fog** --- intermediate nodes (gateways, Raspberry Pi).

-   **Cloud** --- central servers for storage, analysis, visualization.

### Why Use Cloud?

-   Remote access.

-   Data persistence and historical analysis.

-   Machine learning and AI integration.

-   Multi-user dashboards.

## REST APIs in IoT

### Key Concepts

-   Endpoints (e.g., `/update`).

-   Methods (GET, POST, PUT, DELETE).

-   JSON payloads.

### ESP32 as Client

ESP32 sends sensor data to APIs via HTTP.

## ThingSpeak Integration

### Overview

ThingSpeak provides easy cloud dashboards with built-in visualization.

### Multi-Field Upload

<!-- ``` {#code:thingspeakmulti .c++ language="C++" caption="Multi-Field ThingSpeak Update" label="code:thingspeakmulti"} -->
``` cpp
String url="http://api.thingspeak.com/update?api_key="+apiKey+
           "&field1="+String(temp)+
           "&field2="+String(hum)+
           "&field3="+String(ldr);
http.begin(url);
http.GET();
```

### Analytics

ThingSpeak integrates MATLAB scripts for advanced analysis.

### Triggers

Alerts can be sent via email/Twitter when thresholds are exceeded.

## Firebase Integration

### Realtime Database

Data stored in JSON tree.

### Security Rules

Control who can read/write. Example:

<!-- ``` {#code:firebaserules .json language="json" caption="Firebase Rules" label="code:firebaserules"} -->

``` cpp
{
  "rules": {
    "sensors": {
      ".read": "auth != null",
      ".write": "auth != null"
    }
  }
}
```

### ESP32 Example

``` {#code:firebase .c++ language="C++" caption="Firebase with ESP32" label="code:firebase"}
if(Firebase.RTDB.setInt(&fbdo,"/sensors/ldr",ldr)){
  Serial.println("Uploaded: "+String(ldr));
}
```

### Realtime Dashboard

AJAX can directly query Firebase REST endpoints.

## Node-RED Integration

### Overview

Node-RED allows flow-based programming for IoT.

### Multi-Flow Example

-   Flow 1: ESP32 → HTTP POST → Database.

-   Flow 2: Database → Dashboard chart.

-   Flow 3: Condition check → Telegram alert.

### ESP32 POST Example

<!-- ``` {#code:nodered .c++ language="C++" caption="ESP32 to Node-RED" label="code:nodered"} -->

``` cpp
http.begin("http://192.168.1.10:1880/sensors");
http.addHeader("Content-Type","application/json");
String json="{\"ldr\":"+String(ldr)+"}";
http.POST(json);
```

## Hybrid Local + Cloud Dashboards

### Concept

-   Local AJAX dashboard served by ESP32.

-   ESP32 simultaneously uploads data to cloud.

### Benefits

-   Local fast access (low latency).

-   Cloud storage for remote monitoring.

## Security in Cloud Integration

### API Keys

Keep keys secret --- never hardcode in public code.

### HTTPS Usage

Use `WiFiClientSecure` for encrypted requests.

### Token Refresh

Some APIs require periodic token renewal.

## Latency and Reliability

### Local vs Cloud

-   Local AJAX latency:  10--50 ms.

-   Cloud round trip:  200--1000 ms.

### Mitigation

Buffer locally during outages; sync when cloud is available.

## Case Studies

### Smart Agriculture

-   Soil moisture sensors → ESP32 → ThingSpeak.

-   Dashboard shows real-time + historical charts.

-   Alerts trigger irrigation.

### Healthcare Monitoring

-   Wearable ESP32 monitors heart rate.

-   Data uploaded to Firebase.

-   Node-RED flow triggers alerts to caregivers.

### Fleet Management

-   Multiple ESP32s with GPS.

-   Upload location data to Firebase.

-   Node-RED dashboard displays live maps.

## Labworks

### Labwork 11.1: ThingSpeak Integration

Upload sensor values every 20s.

### Labwork 11.2: Firebase Integration

Push sensor data and verify in database.

### Labwork 11.3: Node-RED Dashboard

Post JSON to Node-RED and visualize.

### Labwork 11.4: API Key Security

Store API key securely and test.

### Labwork 11.5: HTTPS Test

Send secure POST request with `WiFiClientSecure`.

### Labwork 11.6: Multi-Field ThingSpeak Dashboard

Upload 3 fields and visualize separately.

### Labwork 11.7: Firebase Security Rules

Test restricted access with authentication.

### Labwork 11.8: Node-RED Alerts

Send alert via Telegram when threshold exceeded.

### Labwork 11.9: Hybrid Dashboard

Serve local AJAX dashboard and sync to ThingSpeak.

### Labwork 11.10: Capstone Project --- Cloud IoT Ecosystem

Design complete IoT ecosystem integrating ESP32, ThingSpeak, Firebase,
Node-RED.

## Summary

In this chapter, we:

-   Reviewed cloud layers and API integration for IoT.

-   Explored ThingSpeak, Firebase, and Node-RED integration.

-   Designed hybrid local+cloud dashboards.

-   Implemented API security measures.

-   Compared latency and reliability of cloud vs local.

-   Completed 10 labworks, culminating in a cloud-integrated IoT
    ecosystem.

## Review Questions

1.  What are advantages of cloud integration for IoT dashboards?

2.  Compare ThingSpeak and Firebase for sensor data storage.

3.  How can Node-RED enhance ESP32 dashboards?

4.  What is the benefit of hybrid local+cloud design?

5.  Suggest strategies to secure API keys on ESP32.


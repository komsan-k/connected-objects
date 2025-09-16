# Case Studies and Projects with ESP32 and AJAX

## Introduction

In previous chapters, we studied theory and built progressively complex
examples. This chapter consolidates knowledge into full-scale projects.
We analyze case studies across different domains, design complete
dashboards, and benchmark real deployments. These examples bridge the
gap between academic exercises and production-ready IoT systems.

## Case Study 1: Environmental Monitoring Dashboard

### Objective

Monitor light intensity, temperature, and humidity using AJAX and
visualize data in real time with Chart.js.

### System Design

-   Hardware: ESP32 + LDR + DHT11.

-   Software: ESP32 WebServer + Chart.js frontend.

-   Update frequency: 2 seconds.

### ESP32 Code

```  {#code:envmonitor .c++ language="C++" caption="Environmental Monitoring Project" label="code:envmonitor"}
``` cpp
#include <WiFi.h>
#include <WebServer.h>
#include "DHT.h"

#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

WebServer server(80);

void handleSensors(){
  int ldr=analogRead(34);
  float temp=dht.readTemperature();
  float hum=dht.readHumidity();
  String json="{\"ldr\":"+String(ldr)+
              ",\"temp\":"+String(temp,1)+
              ",\"hum\":"+String(hum,1)+"}";
  server.send(200,"application/json",json);
}
```

### Features

-   Multi-sensor integration.

-   JSON endpoint consumed by AJAX.

-   Visualized with Chart.js.

## Case Study 2: Smart Home Dashboard

### Objective

Control actuators (lights, fan, pump) and monitor status using AJAX POST
and GET.

### System Workflow

-   Client sends POST request (toggle command).

-   ESP32 executes action.

-   Client polls `/status` for confirmation.

### Challenges

-   Multi-actuator synchronization.

-   Error handling for lost requests.

## Case Study 3: Healthcare Monitoring Prototype

### Objective

Demonstrate AJAX dashboard for wearable sensors (temperature, heart
rate).

### Design

-   ESP32 collects patient data.

-   Dashboard displays real-time graphs.

-   Alerts triggered if values exceed thresholds.

### Considerations

-   Low latency required.

-   Strong security (password-protected access).

## Case Study 4: Industrial Control Panel

### Objective

Control relays for motors and pumps with real-time feedback.

### Design Features

-   AJAX dashboard with actuator toggles.

-   Error log displayed in table.

-   Safety fallback if connection is lost.

### Failure Recovery

-   Default actuators to OFF if disconnected.

-   Store logs locally until network recovers.

## Benchmarking Project Deployments

### Metrics

-   Latency (ms per request).

-   Bandwidth usage (bytes per second).

-   Maximum concurrent clients before crash.

### Tools

-   Browser DevTools (Network tab).

-   ESP32 serial logs.

-   Apache Benchmark (ab) tool.

## Scalability Challenges

### From One Node to Many

-   One ESP32 → 50 ESP32 nodes.

-   Central aggregator required.

-   Load balancing via cloud/MQTT.

### ESP32 Limitations

-   RAM usage increases with clients.

-   Async server improves scaling.

## Complete Project Example: IoT Agriculture Dashboard

### Objective

Monitor soil moisture and control irrigation pump.

### ESP32 Code Snippet

``` {#code:agri .c++ language="C++" caption="Agriculture AJAX Example" label="code:agri"}
void handleSoil(){
  int soil=analogRead(35);
  server.send(200,"application/json","{\"soil\":"+String(soil)+"}");
}

void handlePump(){
  String body=server.arg("plain");
  if(body=="on") digitalWrite(26,HIGH);
  else digitalWrite(26,LOW);
  server.send(200,"application/json","{\"pump\":\""+body+"\"}");
}
```

### Discussion

-   Dashboard shows soil moisture chart.

-   Pump toggled manually or automatically.

## Case Study 5: Integrated Secure Smart Home

### Objective

Combine authentication, AJAX dashboards, and actuator control.

### Features

-   Password-protected login.

-   Multi-actuator control panel.

-   Chart.js graphs for temperature and energy use.

## Labworks

### Labwork 10.1: Environmental Dashboard

Build a dashboard for LDR + DHT sensor.

### Labwork 10.2: Smart Home Simulation

Control LED, fan, and pump.

### Labwork 10.3: Secure Dashboard

Add password protection.

### Labwork 10.4: Performance Measurement

Benchmark latency and bandwidth.

### Labwork 10.5: Healthcare Dashboard

Monitor temperature and heart rate with alerts.

### Labwork 10.6: Agriculture Dashboard

Integrate soil moisture sensor and pump control.

### Labwork 10.7: Healthcare Prototype

Build patient monitoring system with graphs.

### Labwork 10.8: Industry Control Panel

Toggle relays, view error logs.

### Labwork 10.9: Benchmarking Projects

Run multi-client tests and measure limits.

### Labwork 10.10: Capstone Project --- IoT Ecosystem

Design full IoT system with multiple ESP32s, central aggregator, and
professional dashboards.

## Summary

In this chapter, we:

-   Explored case studies in environmental, home, healthcare, and
    industrial IoT.

-   Designed dashboards integrating sensors, actuators, and security.

-   Benchmarked deployments with latency, bandwidth, and scalability
    tests.

-   Addressed scalability and failure recovery strategies.

-   Completed 10 labworks culminating in a capstone IoT ecosystem.

## Review Questions

1.  How do scalability challenges affect ESP32 dashboards?

2.  Why is failure recovery critical in industrial dashboards?

3.  Compare environmental vs healthcare AJAX dashboards.

4.  What tools can benchmark ESP32 web server performance?

5.  Suggest improvements for a secure smart home AJAX dashboard.

# Optimizing HTTP and AJAX Performance

## Introduction

As ESP32 dashboards evolve from prototypes to real-world IoT systems,
performance becomes a critical factor. A dashboard that works with one
client and a single sensor may collapse under multiple clients or large
payloads. To avoid this, developers must understand performance metrics,
identify bottlenecks, and optimize both server and client.

This chapter explores performance optimization techniques for ESP32 web
servers. We analyze latency, throughput, bandwidth, and scalability. We
compare update mechanisms (polling, long polling, SSE, WebSockets),
optimize JSON payloads, and apply caching strategies. Finally, we design
lab experiments to measure performance empirically.

## Performance Metrics

### Latency

Time between sending a request and receiving the first byte of response.

### Response Time

Total duration of a request-response cycle.

### Throughput

Number of successful requests handled per second.

### Jitter

Variation in latency between consecutive requests.

### Packet Loss

Percentage of failed or dropped requests.

## Measuring Performance

### Browser DevTools

-   Network tab → request time breakdown (DNS, TCP, Waiting, Content
    Download).

-   Response size analysis.

### Postman

Useful for repeated requests and monitoring response time.

### ESP32-Side Logging

<!-- ``` {#code:millislog .c++ language="C++" caption="ESP32 Latency Logging" label="code:millislog"} -->

``` cpp
void handleLDR(){
  unsigned long start=millis();
  int value=analogRead(34);
  String json="{\"ldr\":"+String(value)+"}";
  server.send(200,"application/json",json);
  unsigned long elapsed=millis()-start;
  Serial.println("Request handled in "+String(elapsed)+" ms");
}
```

## JSON Payload Optimization

### Reducing Key Size

<!-- ``` {#code:jsonkeys .json language="json" caption="Long vs Short Keys" label="code:jsonkeys"} -->

``` cpp
{"temperature":24.7,"humidity":60.2}
{"t":24.7,"h":60.2}
```

### Limiting Precision

Use fewer decimal places to reduce payload.

### Batch Updates

Return multiple sensor values in one JSON.

## Comparison of Update Techniques

### Polling

Simple but repetitive. Generates unnecessary requests.

### Long Polling

Fewer requests, but each consumes server resources.

### SSE (Server-Sent Events)

Efficient one-way push. Best for continuous updates.

### WebSockets

Bidirectional, lowest latency. Best for interactive apps.

### Benchmark Table

  Method         Latency    Complexity   Suitability
  -------------- ---------- ------------ -----------------------
  Polling        Medium     Low          Simple dashboards
  Long Polling   Low        Medium       Alerts, notifications
  SSE            Low        Medium       Streaming sensor data
  WebSockets     Very Low   High         Real-time control

## Caching Strategies

### Browser Caching

Static files (CSS, JS) cached by browser reduce bandwidth.

### ESP32 Caching

Store computed values and reuse if request is frequent.

### Code Example

<!-- ``` {#code:caching .c++ language="C++" caption="ESP32 Caching Example" label="code:caching"} -->

``` cpp
unsigned long lastUpdate=0;
String cachedJSON;

void handleSensors(){
  if(millis()-lastUpdate>1000){
    int ldr=analogRead(34);
    cachedJSON="{\"ldr\":"+String(ldr)+"}";
    lastUpdate=millis();
  }
  server.send(200,"application/json",cachedJSON);
}
```

## Bandwidth Optimization

### Compact JSON

Use short keys and minimal whitespace.

### Binary Payloads

Send binary data instead of JSON (rare, advanced).

### Compression

ESP32 has limited support for gzip, but responses can be pre-minified.

## Multi-Client Performance

### Problem

ESP32 may crash if too many clients send requests.

### Solutions

-   Use `ESPAsyncWebServer`.

-   Reduce request frequency.

-   Offload data to MQTT broker for scaling.

## Case Studies

### Smart Home

Dozens of devices update states; optimized JSON prevents overload.

### Environmental Monitoring

Sensor nodes upload data to a central ESP32 aggregator.

### Healthcare Dashboard

Patient monitoring requires low latency and reliable updates.

## Labworks

### Labwork 8.1: Meta Refresh vs AJAX

Compare latency using browser DevTools.

### Labwork 8.2: JSON Payload Optimization

Compare large vs short key JSON.

### Labwork 8.3: Polling vs Long Polling

Measure request frequency differences.

### Labwork 8.4: SSE Implementation

Stream sensor values with SSE.

### Labwork 8.5: WebSocket Latency Test

Compare response time with AJAX.

### Labwork 8.6: Latency Measurement

Log handling time with `millis()`.

### Labwork 8.7: Bandwidth Test

Compare response sizes with JSON key variations.

### Labwork 8.8: Multi-Client Benchmark

Open multiple browsers and measure ESP32 load.

### Labwork 8.9: SSE vs WebSocket

Compare throughput under heavy load.

### Labwork 8.10: Mini-Project --- Optimized Dashboard

Build multi-sensor dashboard with optimized JSON, caching, and efficient
update mechanism.

## Summary

In this chapter, we:

-   Defined performance metrics: latency, throughput, jitter, packet
    loss.

-   Learned measurement methods: browser tools, Postman, ESP32 logging.

-   Optimized JSON payloads with short keys, fewer decimals, batching.

-   Compared polling, long polling, SSE, and WebSockets.

-   Applied caching and bandwidth optimization.

-   Analyzed real-world case studies.

-   Completed 10 labworks including a performance-optimized dashboard.

## Review Questions

1.  What is the difference between latency and response time?

2.  How can JSON payload size be reduced?

3.  Compare polling and SSE in terms of efficiency.

4.  What caching strategies can be applied on ESP32?

5.  Suggest optimization strategies for a healthcare monitoring system.


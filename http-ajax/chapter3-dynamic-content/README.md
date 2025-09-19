# Serving Dynamic Content with ESP32

## Introduction

In Chapter 2, we explored serving static content from ESP32, including
HTML, CSS, JavaScript, and images. Static content is important for
structure and design, but IoT applications demand something more:
**dynamic content**. Dynamic content reflects real-time conditions such
as sensor readings, actuator states, or messages from other devices.

In this chapter, we expand on techniques to generate and serve dynamic
content. We compare different update methods (meta refresh, AJAX, SSE,
WebSockets), build dashboards with real-time charts, and provide
practical labworks to consolidate knowledge.

## Static vs Dynamic Content in Depth

### Static Content

-   Predefined and does not change unless manually updated.
-   Examples: logo, stylesheet, help page.

### Dynamic Content

-   Generated at runtime, based on conditions or inputs.
-   Examples: displaying LDR sensor value, system uptime.

### Server-Side vs Client-Side Rendering

-   **Server-side:** ESP32 inserts sensor values into HTML before
    sending.
-   **Client-side:** Browser fetches raw data (e.g., JSON) and renders
    it using JavaScript.

## Update Techniques for Dynamic Content

### Meta Refresh

-   Page reloads every few seconds.
-   **Pros:** simple to implement.\
-   **Cons:** flickers, reload overhead.

### AJAX Polling

-   JavaScript periodically fetches data.
-   **Pros:** efficient, partial updates only.\
-   **Cons:** may waste requests if data does not change.

### Long Polling

-   Request held open until new data is available.
-   **Pros:** fewer wasted requests.\
-   **Cons:** each client consumes server resources.

### Server-Sent Events (SSE)

-   One-way stream of data from server to client.
-   **Pros:** efficient, push-based.\
-   **Cons:** unidirectional only.

### WebSockets

-   Full-duplex communication channel.
-   **Pros:** real-time, interactive.\
-   **Cons:** higher complexity.

### Comparison Table

  ------------------------------------------------------------------------
  Method        Pros                       Cons
  ------------- -------------------------- -------------------------------
  Meta Refresh  Simple, no JS needed       Page flicker, bandwidth waste

  AJAX Polling  Efficient, smooth UI       Repeated requests

  Long Polling  Updates only when needed   Resource heavy for many clients

  SSE           Push updates, lightweight  Only one-way communication

  WebSockets    Real-time, bidirectional   More complex, higher overhead
  ------------------------------------------------------------------------

## Embedding Sensor Values in HTML

### Example: LDR with Meta Refresh

``` cpp
String buildPage() {
  int value = analogRead(34);
  String html = "<!DOCTYPE html><html><head>"
                "<meta http-equiv='refresh' content='5'>"
                "<title>ESP32 LDR</title></head><body>"
                "<h1>LDR Value: " + String(value) + "</h1>"
                "</body></html>";
  return html;
}
```

### Line-by-Line Explanation

-   `analogRead(34)` --- reads the LDR value.
-   `meta refresh` --- reloads page every 5 seconds.
-   Output is simple HTML with the sensor value embedded.

## Serving JSON for AJAX

### Basic JSON Endpoint

``` cpp
void handleJSON() {
  int ldr = analogRead(34);
  String json = "{\"ldr\":" + String(ldr) + "}";
  server.send(200,"application/json",json);
}
```

### Why JSON?

-   Lightweight, easy for JavaScript to parse.
-   Standard format in IoT communication.

## AJAX Dashboard Example

### Complete Code

``` cpp
void handleDashboard() {
  String html="<!DOCTYPE html><html><body>"
              "<h1>AJAX LDR Dashboard</h1>"
              "<p id='ldr'>---</p>"
              "<script>"
              "async function update(){"
                "let r=await fetch('/ldr');"
                "let j=await r.json();"
                "document.getElementById('ldr').innerText=j.ldr;"
              "}"
              "setInterval(update,1000); update();"
              "</script></body></html>";
  server.send(200,"text/html",html);
}
```

### Explanation

-   JavaScript fetches JSON from ESP32 every second.
-   DOM is updated with new values.
-   Smooth updates without full reload.

## Multi-Sensor JSON Example

``` cpp
void handleSensors() {
  int ldr = analogRead(34);
  float temp = 25.5;
  String json = "{\"ldr\":" + String(ldr) +
                ",\"temp\":" + String(temp,1) + "}";
  server.send(200,"application/json",json);
}
```

## Data Visualization: Chart.js

### Line Chart Example

``` html
<canvas id='c' width='400' height='200'></canvas>
<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
<script>
let ctx=document.getElementById('c').getContext('2d');
let data={labels:[],datasets:[{label:'LDR',data:[],borderColor:'blue'}]};
let chart=new Chart(ctx,{type:'line',data:data});
async function update(){
  let r=await fetch('/ldr'); let j=await r.json();
  data.labels.push(new Date().toLocaleTimeString());
  data.datasets[0].data.push(j.ldr);
  if(data.labels.length>20){data.labels.shift();data.datasets[0].data.shift();}
  chart.update();
}
setInterval(update,1000);
</script>
```

## Real-Time Gauges and Tables

### Gauge Visualization

Third-party libraries (e.g., JustGage, SmoothieCharts) allow gauge
widgets for sensor values.

### Dynamic Tables

HTML tables updated with AJAX can display multiple sensor values
clearly.

## Multi-Client Synchronization

### Challenge

When multiple clients connect, each may receive outdated or conflicting
data.

### Solutions

-   Central JSON endpoint for all sensors.
-   Timestamp values for synchronization.
-   Use SSE or WebSockets for push updates.

## Labworks

-   **Labwork 3.1: Meta Refresh Demo** --- Display LDR value with
    automatic page reload.\
-   **Labwork 3.2: JSON Endpoint** --- Serve sensor value as JSON.\
-   **Labwork 3.3: AJAX Dashboard** --- Build dashboard with real-time
    updates.\
-   **Labwork 3.4: Multi-Sensor JSON** --- Serve multiple sensor values
    in one JSON response.\
-   **Labwork 3.5: Chart.js Visualization** --- Plot sensor values as a
    real-time chart.\
-   **Labwork 3.6: XML Endpoint** --- Serve sensor data in XML for
    legacy compatibility.\
-   **Labwork 3.7: Dynamic Tables** --- Use AJAX to fill HTML table with
    sensor values.\
-   **Labwork 3.8: Real-Time Gauges** --- Implement gauge visualization
    for one sensor.\
-   **Labwork 3.9: JSON + Visualization** --- Combine JSON endpoint with
    Chart.js and table.\
-   **Labwork 3.10: Error Recovery** --- Simulate ESP32 disconnection
    and handle gracefully.

## Summary

In this chapter, we: - Differentiated static vs dynamic content. -
Compared meta refresh, AJAX, long polling, SSE, and WebSockets. - Built
dashboards with JSON, AJAX, and Chart.js. - Introduced visualization
using tables and gauges. - Addressed multi-client synchronization
issues. - Completed 10 labworks covering dynamic web serving.

## Review Questions

1.  Compare server-side vs client-side rendering for ESP32 dashboards.\
2.  Why is JSON preferred for AJAX responses?\
3.  Explain pros and cons of AJAX vs SSE vs WebSockets.\
4.  How can gauges and tables improve IoT dashboards?\
5.  Suggest strategies to handle multi-client synchronization.

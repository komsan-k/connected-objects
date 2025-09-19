# Implementing AJAX with ESP32

## Introduction

In Chapter 4, we introduced AJAX and implemented basic dashboards that
fetched sensor values asynchronously. In this chapter, we focus on
practical and advanced implementations of AJAX on ESP32. We study JSON
structuring, error handling, multi-sensor dashboards, actuator control,
and strategies for robust, production-ready designs.

By the end of this chapter, readers will: - Design and serve JSON
endpoints for single and multiple sensors. - Implement AJAX dashboards
using Fetch API. - Integrate actuators and monitor their state with
AJAX. - Handle AJAX errors with retries and fallbacks. - Compare
multiple-endpoint vs unified-endpoint approaches.

## JSON Structuring for AJAX

### Flat JSON

Simple key-value pairs:

``` json
{"ldr": 512, "temp": 24.7}
```

### Nested JSON

More structured representation:

``` json
{
  "sensors": {
    "ldr": 512,
    "temp": 24.7
  },
  "status": {
    "led": true
  }
}
```

### Arrays in JSON

For time-series or multiple values:

``` json
{"history": [512, 520, 530, 540]}
```

### Trade-Offs

-   Flat JSON --- lightweight, fast to parse.\
-   Nested JSON --- more expressive, but larger payload.\
-   Arrays --- suitable for chart data.

## Multi-Endpoint vs Unified Endpoint

### Multiple Endpoints

Each sensor has its own route:\
- `/ldr`\
- `/temp`

### Unified Endpoint

One route returns all values:\
- `/sensors` → `{"ldr":512,"temp":24.7}`

### Comparison

  ------------------------------------------------------------------------
  Approach         Advantages                Disadvantages
  ---------------- ------------------------- -----------------------------
  Multi-endpoint   Modular, easy to debug    More requests, higher
                                             overhead

  Unified          Efficient, single request Larger JSON, more parsing
  ------------------------------------------------------------------------

## Error Handling in AJAX

### Common Failures

-   ESP32 offline or rebooting.\
-   Wi-Fi disconnected.\
-   Timeout due to latency.

### Retry Logic

``` javascript
async function update(){
  try {
    let r=await fetch('/sensors',{timeout:2000});
    if(!r.ok) throw new Error("HTTP "+r.status);
    let j=await r.json();
    document.getElementById('ldr').innerText=j.ldr;
  } catch(e) {
    console.log("Error:", e);
    setTimeout(update, 5000); // retry after 5s
  }
}
```

### Exponential Backoff

Retry intervals: 1s, 2s, 4s, 8s... to reduce server load.

## Complete Example: Multi-Sensor Dashboard

### ESP32 Code

``` cpp
void handleSensors() {
  int ldr=analogRead(34);
  float temp=25.5;
  float hum=60.0;
  String json="{\"ldr\":"+String(ldr)+
              ",\"temp\":"+String(temp,1)+
              ",\"hum\":"+String(hum,1)+"}";
  server.send(200,"application/json",json);
}
```

### JavaScript Code

``` javascript
async function update(){
  try{
    let r=await fetch('/sensors');
    let j=await r.json();
    document.getElementById('ldr').innerText=j.ldr;
    document.getElementById('temp').innerText=j.temp;
    document.getElementById('hum').innerText=j.hum;
  } catch(e){
    console.error("Fetch failed",e);
  }
}
setInterval(update,2000);
```

## Actuator Control with AJAX

### ESP32 Code

``` cpp
const int LED=2;
bool state=false;

void handleLED(){
  String body=server.arg("plain");
  if(body=="on"){digitalWrite(LED,HIGH); state=true;}
  else{digitalWrite(LED,LOW); state=false;}
  server.send(200,"application/json",
              "{\"led\":"+(state?"true":"false")+"}");
}
```

### Client-Side Code

``` javascript
async function ledOn(){await fetch('/led',{method:'POST',body:'on'});}
async function ledOff(){await fetch('/led',{method:'POST',body:'off'});}
```

## Cross-Browser Compatibility

### Issues

-   Old browsers may not support Fetch API.\
-   Edge cases: CORS, caching.

### Fallbacks

-   Provide XMLHttpRequest alternative.\
-   Disable caching with headers.

## Labworks

-   **Labwork 5.1: Single-Sensor JSON Endpoint** --- Serve LDR value via
    JSON.\
-   **Labwork 5.2: Multi-Sensor Dashboard** --- Serve LDR + temperature
    in JSON.\
-   **Labwork 5.3: Actuator Control** --- Control LED state via AJAX
    POST.\
-   **Labwork 5.4: Unified Dashboard** --- Display sensors + LED status
    in one interface.\
-   **Labwork 5.5: Error Handling** --- Introduce intentional delays to
    test error handling.\
-   **Labwork 5.6: Nested JSON Endpoint** --- Serve nested JSON for
    sensors and status.\
-   **Labwork 5.7: Retry Mechanism** --- Implement exponential backoff
    on client side.\
-   **Labwork 5.8: Multi-Client Stress Test** --- Connect multiple
    browsers and observe ESP32 load.\
-   **Labwork 5.9: JSON Formatting Comparison** --- Compare long vs
    short key names in payload size.\
-   **Labwork 5.10: Unified AJAX Project** --- Build a dashboard with
    sensors, actuators, and error resilience.

## Summary

In this chapter, we: - Learned flat, nested, and array JSON structures.\
- Compared multi-endpoint vs unified endpoint designs.\
- Implemented AJAX dashboards with error handling.\
- Controlled actuators via AJAX POST.\
- Addressed cross-browser issues.\
- Completed 10 labworks including stress testing and error handling.

## Review Questions

1.  Compare flat, nested, and array JSON for ESP32 dashboards.\
2.  What are advantages of unified endpoints over multiple endpoints?\
3.  Explain exponential backoff in AJAX error handling.\
4.  How does browser compatibility affect AJAX implementations?\
5.  Suggest an advanced project combining sensors, actuators, and error
    handling.


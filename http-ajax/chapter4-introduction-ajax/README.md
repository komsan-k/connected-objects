# Introduction to AJAX

## Introduction

Chapter 3 introduced dynamic content serving using techniques like meta
refresh, JSON endpoints, and AJAX polling. Among these, AJAX
(Asynchronous JavaScript and XML) stands out as the most widely used
mechanism for building real-time dashboards.

This chapter provides a comprehensive treatment of AJAX: its history,
core principles, implementations on ESP32, error handling strategies,
and practical applications.

By the end of this chapter, readers will: - Understand AJAX origins and
evolution. - Differentiate between XMLHttpRequest and Fetch API. -
Implement AJAX dashboards for sensors and actuators. - Handle errors and
debug AJAX interactions. - Build advanced AJAX-based projects on ESP32.

## Origins and Evolution of AJAX

### AJAX in Early Web Development

AJAX originated in the early 2000s. Before AJAX, each web page
interaction required a full reload.

In 2005, Jesse James Garrett coined the term **AJAX**, describing a
technique that combined JavaScript, XMLHttpRequest, and DOM manipulation
to allow asynchronous updates.

### XML vs JSON

Initially, XML was used for structured responses. However, JSON became
the dominant format due to: - Simplicity. - Native support in
JavaScript. - Lower overhead.

### AJAX Today

Modern implementations often use the `fetch()` API, which simplifies
AJAX requests with promises and async/await syntax.

## AJAX Workflow in ESP32 Dashboards

### Steps

1.  Browser loads HTML from ESP32.\
2.  JavaScript sends AJAX request (GET or POST).\
3.  ESP32 processes and returns JSON or text.\
4.  JavaScript updates webpage dynamically.

### Diagram

**AJAX communication cycle between client and ESP32:**\
Browser (AJAX) ⇄ ESP32 Web Server

## AJAX with XMLHttpRequest

### Code Example

``` javascript
function updateData(){
  var xhr=new XMLHttpRequest();
  xhr.onreadystatechange=function(){
    if(this.readyState==4 && this.status==200){
      var obj=JSON.parse(this.responseText);
      document.getElementById("ldr").innerHTML=obj.ldr;
    }
  };
  xhr.open("GET","/ldr",true);
  xhr.send();
}
setInterval(updateData,1000);
```

### Line-by-Line Explanation

-   `XMLHttpRequest()` creates request object.\
-   `readyState==4` ensures complete response.\
-   `status==200` checks HTTP OK.\
-   `JSON.parse()` converts response text to object.

## AJAX with Fetch API

### Code Example

``` javascript
async function update(){
  let response=await fetch('/ldr');
  let data=await response.json();
  document.getElementById('ldr').innerText=data.ldr;
}
setInterval(update,1000);
```

### Advantages of Fetch

-   Modern and concise.\
-   Built-in promise support.\
-   Easier error handling with try/catch.

### Error Handling Example

``` javascript
async function update(){
  try{
    let r=await fetch('/ldr');
    if(!r.ok) throw new Error("HTTP "+r.status);
    let j=await r.json();
    document.getElementById('ldr').innerText=j.ldr;
  } catch(e){
    document.getElementById('ldr').innerText="Error";
    console.error("Fetch failed:",e);
  }
}
```

## ESP32 AJAX Implementation

### Single Sensor Example

``` cpp
WebServer server(80);

void handleLDR(){
  int value=analogRead(34);
  String json="{\"ldr\":"+String(value)+"}";
  server.send(200,"application/json",json);
}

void handleDashboard(){
  String html="<!DOCTYPE html><html><body>"
              "<h1>AJAX LDR</h1><p id='ldr'>---</p>"
              "<script src='script.js'></script>"
              "</body></html>";
  server.send(200,"text/html",html);
}
```

### Multi-Sensor Example

``` cpp
void handleSensors(){
  int ldr=analogRead(34);
  float temp=25.7;
  String json="{\"ldr\":"+String(ldr)+",\"temp\":"+String(temp,1)+"}";
  server.send(200,"application/json",json);
}
```

## Actuator Control with AJAX

### Example: LED Toggle

``` cpp
void handleLED(){
  String body=server.arg("plain");
  if(body=="on") digitalWrite(2,HIGH);
  else digitalWrite(2,LOW);
  server.send(200,"text/plain","OK");
}
```

### Client-Side Control

``` javascript
async function ledOn(){await fetch('/led',{method:'POST',body:'on'});}
async function ledOff(){await fetch('/led',{method:'POST',body:'off'});}
```

## Debugging AJAX

### Browser DevTools

-   **Network Tab:** Inspect request headers, responses, status codes.\
-   **Console:** Check JavaScript errors.\
-   **Timing:** Analyze response latency.

### ESP32 Serial Monitor

Print request logs to identify issues.

## Comparison of AJAX and Alternatives

  Method         Advantages                   Limitations
  -------------- ---------------------------- ----------------------------
  Meta Refresh   Simple, no JS                Page flickers, inefficient
  AJAX           Smooth UI, partial updates   Polling overhead
  SSE            Push updates                 One-way only
  WebSockets     Real-time, two-way           More complex

## Labworks

-   **Labwork 4.1: Single-Sensor AJAX Dashboard** --- Serve LDR sensor
    and update page every second.\
-   **Labwork 4.2: Multi-Sensor AJAX** --- Serve JSON with multiple
    sensor values.\
-   **Labwork 4.3: Actuator Control** --- Control LED with AJAX POST.\
-   **Labwork 4.4: Unified Dashboard** --- Combine sensors and actuators
    in one page.\
-   **Labwork 4.5: Debugging AJAX** --- Use browser DevTools to analyze
    requests.\
-   **Labwork 4.6: Multi-Client AJAX** --- Connect two browsers and test
    performance.\
-   **Labwork 4.7: Retry Mechanism** --- Implement retry logic when AJAX
    fails.\
-   **Labwork 4.8: Mini-Project** --- Create a sensor + actuator AJAX
    control panel.

## Summary

In this chapter, we: - Reviewed the history of AJAX.\
- Explored XMLHttpRequest vs Fetch API.\
- Implemented sensor and actuator dashboards with AJAX.\
- Added debugging and error handling.\
- Completed 8 labworks including a mini-project.

## Review Questions

1.  Why did JSON replace XML as the preferred AJAX format?\
2.  Compare XMLHttpRequest and Fetch API.\
3.  How does AJAX improve IoT dashboards compared to meta refresh?\
4.  What tools can be used to debug AJAX requests?\
5.  Suggest a project combining AJAX with actuator control.


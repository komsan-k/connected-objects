# Bidirectional Updates and Control

## Introduction

So far, we have seen how ESP32 can serve dynamic content and respond to
AJAX requests for sensor data. However, real IoT dashboards must go
beyond monitoring. They must also allow users to **control actuators**
(LEDs, motors, relays, pumps) and receive **feedback** confirming
actions.

This chapter focuses on bidirectional communication between client and
ESP32. We study different request methods (GET vs POST vs PUT),
implement actuator controls, address synchronization challenges, and
build complete dashboards for smart environments.

## Bidirectional Communication in IoT

### Client to ESP32

-   User clicks a button or slider.\
-   Browser sends AJAX request with command.\
-   ESP32 executes action (e.g., turns LED on).

### ESP32 to Client

-   ESP32 responds with confirmation (JSON, text).\
-   Client updates interface accordingly.

### Importance of Synchronization

Without feedback, the UI may show outdated or incorrect states, leading
to user confusion.

## HTTP Methods for Control

### GET

-   Example: `/led?state=on`\
-   **Pros:** easy to debug, works in browser URL.\
-   **Cons:** not secure, parameters visible in URL.

### POST

-   Example: `/led` with body "on".\
-   **Pros:** cleaner, safer, standard for control actions.\
-   **Cons:** requires JavaScript.

### PUT

-   Used in REST APIs for updating resources.\
-   Rarely needed for simple ESP32 dashboards.

## Basic LED Control Example

### ESP32 Code

``` cpp
const int LED_PIN=2;
bool ledState=false;

void handleLED(){
  String body=server.arg("plain");
  if(body=="on"){digitalWrite(LED_PIN,HIGH); ledState=true;}
  else if(body=="off"){digitalWrite(LED_PIN,LOW); ledState=false;}
  server.send(200,"application/json",
              "{\"led\":"+(ledState?"true":"false")+"}");
}
```

### Explanation

-   Client sends "on" or "off".\
-   ESP32 sets LED state.\
-   Responds with JSON confirmation.

### Client-Side JS

``` javascript
async function ledOn(){await fetch('/led',{method:'POST',body:'on'});}
async function ledOff(){await fetch('/led',{method:'POST',body:'off'});}
```

## PWM Control with Slider

### ESP32 Code

``` cpp
const int PWM_PIN=5;

void handlePWM(){
  int duty=server.arg("plain").toInt();
  ledcWrite(0,duty);
  server.send(200,"application/json","{\"pwm\":"+String(duty)+"}");
}
```

### Client-Side JS

``` javascript
async function setPWM(val){
  await fetch('/pwm',{method:'POST',body:val});
}
```

### Use Cases

-   LED brightness.\
-   Motor speed control.\
-   Fan speed regulation.

## Forms and Checkboxes for Actuators

### Form Example

``` html
<form onsubmit="send(event)">
<select id="mode">
  <option value="auto">Auto</option>
  <option value="manual">Manual</option>
</select>
<button type="submit">Submit</button>
</form>

<script>
async function send(e){
  e.preventDefault();
  let val=document.getElementById("mode").value;
  await fetch('/mode',{method:'POST',body:val});
}
</script>
```

## State Synchronization

### Problem

If ESP32 state changes externally (e.g., button press), client interface
may not reflect reality.

### Solution

-   Periodic AJAX polling for `/status`.\
-   JSON response includes all actuator states.

### Example Status Endpoint

``` cpp
void handleStatus(){
  String json="{\"led\":"+(ledState?"true":"false")+
              ",\"fan\":"+(fan?"true":"false")+"}";
  server.send(200,"application/json",json);
}
```

## Multi-Actuator Control

### Scenario

Smart home system with LED, fan, and pump.

### Code Example

``` cpp
bool fan=false, pump=false;

void handleFan(){
  String body=server.arg("plain");
  fan=(body=="on");
  server.send(200,"application/json","{\"fan\":"+(fan?"true":"false")+"}");
}
```

## Real-World IoT Case Studies

### Smart Lighting

-   Control brightness and color via sliders.\
-   Synchronize states for multiple clients.

### HVAC Dashboard

-   Adjust fan speed, mode (cool/heat).\
-   Display real-time temperature.

### Irrigation System

-   Toggle pumps and valves.\
-   View soil moisture sensor feedback.

## Error Recovery for Actuator Commands

### Possible Failures

-   Request lost due to Wi-Fi drop.\
-   ESP32 busy with another task.

### Client-Side Retry

``` javascript
async function sendCmd(cmd){
  try{
    let r=await fetch('/led',{method:'POST',body:cmd});
    if(!r.ok) throw new Error("Bad status");
  }catch(e){
    console.log("Retrying...");
    setTimeout(()=>sendCmd(cmd),2000);
  }
}
```

## Labworks

-   **Labwork 6.1: LED Toggle** --- Implement POST-based LED control.\
-   **Labwork 6.2: Slider-Controlled PWM** --- Adjust LED brightness or
    motor speed.\
-   **Labwork 6.3: Checkbox Control** --- Control multiple actuators
    with checkboxes.\
-   **Labwork 6.4: Status Synchronization** --- Ensure UI updates match
    ESP32 state.\
-   **Labwork 6.5: Multi-Actuator Dashboard** --- Combine LED, fan, and
    pump control.\
-   **Labwork 6.6: Dual Control (LED + Servo)** --- Use buttons for LED
    and slider for servo.\
-   **Labwork 6.7: External Change Sync** --- Simulate external button
    press, sync with dashboard.\
-   **Labwork 6.8: Form-Based Multi-Control** --- Build HTML form to
    configure multiple actuators.\
-   **Labwork 6.9: Error Recovery** --- Simulate Wi-Fi drop and test
    retries.\
-   **Labwork 6.10: Mini-Project --- Smart Home Dashboard** --- Build
    complete dashboard with multiple actuators, sensor feedback, and
    robust error handling.

## Summary

In this chapter, we: - Explored bidirectional communication for IoT.\
- Compared GET, POST, and PUT for actuator control.\
- Implemented LED, PWM, and multi-actuator dashboards.\
- Addressed synchronization challenges.\
- Studied real-world IoT case studies.\
- Designed error recovery strategies.\
- Completed 10 labworks including a smart home dashboard project.

## Review Questions

1.  Compare GET and POST for actuator control.\
2.  Why is state synchronization important in IoT dashboards?\
3.  How can multi-actuator dashboards be optimized?\
4.  What are typical error recovery strategies for actuator commands?\
5.  Suggest a case study where bidirectional AJAX is critical.


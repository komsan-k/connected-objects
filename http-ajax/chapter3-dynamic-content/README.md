# Serving Static Web Content with ESP32

## Introduction

In Chapter 1, we introduced the basics of HTTP and demonstrated how
ESP32 can connect to Wi-Fi and serve a minimal webpage. This chapter
focuses on static content: HTML, CSS, JavaScript, and media files served
from ESP32.

Static content forms the foundation of any web server. It includes: -
HTML files for structure. - CSS files for styling. - JavaScript files
for interactivity. - Images or icons.

While ESP32 is resource-constrained, it can effectively serve static
files for lightweight dashboards and IoT applications.

## Understanding Static Web Content

### Definition

Static content refers to web resources that do not change unless
manually updated by the server. Examples: a homepage with text, a
stylesheet, or a logo.

### Static vs Dynamic

-   **Static:** Predefined files such as `index.html`.
-   **Dynamic:** Generated at runtime, often including sensor values.

### Use in IoT

Static files provide: - Landing pages for ESP32 devices. - Device
documentation and help files. - Stylesheets and JavaScript required for
dashboards.

## Basics of HTML, CSS, and JavaScript

### HTML (HyperText Markup Language)

Defines the structure of web pages.

### CSS (Cascading Style Sheets)

Provides visual styling (colors, fonts, layout).

### JavaScript

Adds interactivity, animations, and AJAX calls.

### MIME Types

When serving files, ESP32 must send correct Content-Type: - `text/html`
for HTML. - `text/css` for CSS. - `application/javascript` for JS. -
`image/png` for PNG images.

## ESP32 WebServer Library Basics

### Functions

-   `server.on(path, handler)` --- define routes.
-   `server.send(status, type, body)` --- send responses.
-   `server.handleClient()` --- process incoming requests.

### Example

``` cpp
#include <WiFi.h>
#include <WebServer.h>

WebServer server(80);

void handleRoot() {
  server.send(200,"text/html","<h1>Hello, ESP32!</h1>");
}

void setup() {
  WiFi.begin("ssid","password");
  while(WiFi.status()!=WL_CONNECTED){delay(500);}
  server.on("/",handleRoot);
  server.begin();
}
void loop(){ server.handleClient(); }
```

## Serving Inline HTML

Inline HTML can be embedded directly inside C++ strings.

### Code Example

``` cpp
void handlePage() {
  String html="<!DOCTYPE html><html><head><title>ESP32</title></head>"
              "<body><h1>Static Page</h1><p>This is served from ESP32.</p>"
              "</body></html>";
  server.send(200,"text/html",html);
}
```

### Limitations

-   Large HTML is cumbersome in C++ strings.
-   Better to use filesystem (SPIFFS or LittleFS).

## Serving Files from SPIFFS/LittleFS

### Why Filesystem?

-   Store HTML, CSS, JS separately.
-   Easier to edit and maintain.

### Setup

-   Use `SPIFFS.begin()` or `LittleFS.begin()`.
-   Upload files via Arduino IDE plugin.

### Code Example

``` cpp
#include "FS.h"
#include "SPIFFS.h"

void handleIndex() {
  File file=SPIFFS.open("/index.html","r");
  server.streamFile(file,"text/html");
  file.close();
}
```

## Serving CSS and JavaScript

### CSS Example

``` css
body { background-color: lightblue; font-family: Arial; }
h1 { color: navy; }
```

### ESP32 Code

``` cpp
void handleCSS() {
  File file=SPIFFS.open("/style.css","r");
  server.streamFile(file,"text/css");
  file.close();
}
```

## Serving Images

### Example PNG

Place `logo.png` in SPIFFS.

``` cpp
void handleLogo() {
  File file=SPIFFS.open("/logo.png","r");
  server.streamFile(file,"image/png");
  file.close();
}
```

## Building a Simple Static Dashboard

### HTML Page

``` html
<!DOCTYPE html>
<html>
<head><link rel="stylesheet" href="style.css"></head>
<body>
  <h1>ESP32 Static Dashboard</h1>
  <p>Status: Online</p>
  <script src="script.js"></script>
</body>
</html>
```

### script.js

``` javascript
console.log("ESP32 static page loaded!");
```

## System Information Page Example

### Code Example

``` cpp
void handleInfo() {
  String html="<h1>ESP32 Info</h1>";
  html+="<p>Chip ID: "+String((uint32_t)ESP.getEfuseMac(),HEX)+"</p>";
  html+="<p>Free Heap: "+String(ESP.getFreeHeap())+" bytes</p>";
  html+="<p>Flash Size: "+String(ESP.getFlashChipSize()/1024)+" KB</p>";
  server.send(200,"text/html",html);
}
```

### Explanation

Useful for device diagnostics and demonstrations.

## Extra Debugging Techniques

-   Use `Serial.print()` to log requests.
-   Open browser DevTools (F12) to inspect network requests.
-   Confirm correct MIME types in headers.

## Labworks

-   **Labwork 2.1: Inline HTML** --- Serve a static "Hello World" HTML
    page.\
-   **Labwork 2.2: Serving CSS** --- Add a stylesheet for background
    color and font.\
-   **Labwork 2.3: JavaScript Demo** --- Serve a simple JS file that
    logs a message to console.\
-   **Labwork 2.4: Serving Images** --- Upload an image to SPIFFS and
    serve it at `/logo`.\
-   **Labwork 2.5: System Info Dashboard** --- Build a diagnostic page
    showing ESP32 stats.\
-   **Labwork 2.6: Debugging Requests** --- Use browser DevTools to
    inspect response headers and verify MIME types.

## Mini-Project: Static Web Portal for ESP32

Combine labworks into a project: - Serve `index.html`, `style.css`,
`script.js`, and `logo.png`. - Create a landing page with styled content
and embedded JavaScript. - Add a system info page linked from homepage.

## Summary

In this chapter, we: - Explored static web content and MIME types. -
Learned how to serve HTML, CSS, JS, and images. - Introduced
SPIFFS/LittleFS for file storage. - Built a system info dashboard. -
Completed labworks leading to a static web portal.

## Review Questions

1.  What is the difference between inline HTML and file-based serving?\
2.  Why must MIME types be specified correctly?\
3.  How can CSS improve ESP32 dashboards?\
4.  What are the limitations of static dashboards compared to dynamic
    ones?\
5.  Suggest a real-world application for ESP32 static dashboards.


# HTTP and AJAX for Designing HTTP Web Servers Using ESP32

## 10-Chapter Outline with Labworks

### Chapter 1: Introduction to HTTP and ESP32
- Overview of ESP32 as a web-enabled microcontroller  
- Basics of HTTP (requests, responses, headers, GET, POST)  
- Client–server architecture in IoT  
- ESP32 Wi-Fi modes (station, AP, AP+STA)  
- Tools: Arduino IDE, Serial Monitor, browser developer tools  

**Labwork 1.1:**  
- Connect ESP32 to Wi-Fi and print the assigned IP address.  
- Open the IP address in a browser to verify connection.  

---

### Chapter 2: Setting Up ESP32 as a Basic HTTP Server
- Configuring ESP32 Wi-Fi credentials  
- Using WiFiServer and WebServer libraries  
- Serving a minimal HTML page from ESP32  
- Debugging client requests in Serial Monitor  

**Labwork 2.1:**  
- Build a simple HTTP server on ESP32.  
- Serve a “Hello ESP32” web page accessible from a phone or PC.  

---

### Chapter 3: Serving Dynamic Content with ESP32
- Static vs. dynamic web pages  
- Embedding sensor values into HTML responses  
- Using ESP32 variables in server responses  
- Refreshing pages automatically with `<meta refresh>`  

**Labwork 3.1:**  
- Connect a temperature sensor (LM73) or LDR.  
- Display live sensor readings in the browser (auto-refresh every 5s).  

---

### Chapter 4: Introduction to AJAX
- What is AJAX?  
- Difference between synchronous refresh vs. asynchronous updates  
- XMLHttpRequest and Fetch API basics  
- Role of JSON in AJAX communication  

**Labwork 4.1:**  
- Create a webpage with a button that calls ESP32 via AJAX.  
- Display a random value (generated on ESP32) without refreshing the page.  

---

### Chapter 5: Implementing AJAX with ESP32
- Serving JSON from ESP32  
- Parsing JSON with JavaScript  
- Handling multiple sensor endpoints (/ldr, /temp)  
- Debugging AJAX requests in browser console  

**Labwork 5.1:**  
- Create a webpage with two AJAX calls: one for LDR, one for temperature.  
- Display both values in real time without reloading.  

---

### Chapter 6: Bidirectional Updates and Control
- Using AJAX POST requests to send commands to ESP32  
- Controlling GPIO (LEDs, relays, motors) from a webpage  
- Returning state feedback to the browser  
- Synchronizing UI with ESP32 responses  

**Labwork 6.1:**  
- Design a webpage with ON/OFF buttons.  
- Control an LED on ESP32 via AJAX POST.  
- Display the current LED state on the page.  

---

### Chapter 7: Advanced Web Interfaces with AJAX
- Responsive design with HTML/CSS (Bootstrap basics)  
- Real-time charts with Chart.js  
- Updating graphs using AJAX calls  
- Handling multiple sensor data streams  

**Labwork 7.1:**  
- Build a webpage that plots temperature data over time using Chart.js.  
- ESP32 provides fresh JSON data every 2 seconds via AJAX.  

---

### Chapter 8: Optimizing HTTP and AJAX Performance
- Efficient JSON payload design  
- Reducing latency with AJAX vs. long polling  
- Introduction to Server-Sent Events (SSE) and WebSockets (comparison only)  
- ESP32 memory considerations for web servers  

**Labwork 8.1:**  
- Compare three methods:  
  - Page auto-refresh every 5s  
  - AJAX refresh every 1s  
  - Long polling  
- Measure and record response speed and stability.  

---

### Chapter 9: Security and Authentication in HTTP/AJAX ESP32 Servers
- Why security matters in IoT web servers  
- HTTP Basic Authentication implementation on ESP32  
- Password-protected AJAX calls  
- Limitations of HTTPS on ESP32  

**Labwork 9.1:**  
- Implement login-protected AJAX web dashboard.  
- Users must enter a password before accessing sensor values.  

---

### Chapter 10: Case Studies and Projects
- **Project 1:** Smart Home AJAX Dashboard (monitor & control multiple devices)  
- **Project 2:** Real-Time Sensor Logger with ESP32 + AJAX Charts  
- **Project 3:** ESP32 REST API server with AJAX client in browser  
- Cloud and Node-RED integration possibilities  
- Migration from AJAX to WebSockets for future IoT projects  

**Labwork 10.1 (Capstone Project):**  
- Build a complete Smart Home Dashboard:  
  - Monitor at least two sensors (LDR + temperature).  
  - Control at least one actuator (LED or relay).  
  - Display live data in a chart with AJAX updates.  
  - Include password authentication.  


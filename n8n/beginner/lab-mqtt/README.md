# 🔬 Lab: Building an MQTT Dashboard with n8n

## 🧩 1. Objective

In this laboratory exercise, students will:

- Connect n8n to an MQTT broker  
- Subscribe to MQTT topics  
- Process incoming IoT sensor data (JSON)  
- Create a simple dashboard using n8n  
- Forward messages to Node-RED for visualization  
- Understand MQTT topic structures and event-driven automation

This lab bridges IoT (ESP32) → MQTT → n8n → Dashboard/Automation.

---

## ⚙️ 2. Equipment and Tools

| Tool / Resource | Description |
|------------------|-------------|
| **Mosquitto MQTT Broker** | Local broker for publish/subscribe |
| **n8n** | Workflow automation and dashboard |
| **Node-RED (optional)** | For gauge/text dashboard widgets |
| **ESP32 or MQTT Device** | Publishes messages |

---

## 🧠 3. Background Theory

### 3.1 MQTT Recap

MQTT is a lightweight, publish/subscribe protocol used in IoT systems.

Example topic:
```
lab/esp32/lm73/temp
```

Example JSON:
```json
{"device_id":"esp32-lm73","temp_c":28.50}
```

### 3.2 n8n MQTT Trigger

The **MQTT Trigger** listens for messages on specific topics and starts an n8n workflow whenever new data arrives.

### 3.3 Dashboard Options

For visualization, Node-RED is used to display gauges and text dashboards.

---

## 🧩 4. Lab Tasks

### 🧪 Task 1 — Verify MQTT Broker is Running

Run Mosquitto:
```
mosquitto
```

Test using:
```
mosquitto_sub -h localhost -t lab/test -v
mosquitto_pub -h localhost -t lab/test -m "hello"
```

---

### 🧪 Task 2 — Publish MQTT Sensor Data

Publish a test JSON message:
```bash
mosquitto_pub -h localhost -t lab/esp32/lm73/temp   -m "{"device_id":"esp-test","temp_c":25.75}"
```

---

### 🧪 Task 3 — Create n8n MQTT Listener

1. Open n8n  
2. New Workflow  
3. Add **MQTT Trigger**  
4. Configure:
   - Broker: `mqtt://localhost:1883`
   - Topic: `lab/esp32/#`

---

### 🧪 Task 4 — Process Data in n8n (Set Node)

Use a **Set** node:

| Field | Value |
|--------|--------|
| device | `{{$json["device_id"]}}` |
| temperature | `{{$json["temp_c"]}}` |
| timestamp | `{{$now.format("YYYY-MM-DD HH:mm:ss")}}` |

This creates a formatted payload:
```json
{
  "device": "esp32-lm73",
  "temperature": 27.50,
  "timestamp": "2025-11-15 10:22:33"
}
```

---

### 🧪 Task 5 — Forward data to Node-RED

Add an **HTTP Request** node:

- Method: `POST`
- URL:
  ```
  http://localhost:1880/esp32/dashboard
  ```
- Body: JSON (msg.payload)

Final n8n flow:
```
MQTT Trigger → Set → HTTP Request → Node-RED
```

---

### 🧪 Task 6 — Build Node-RED Dashboard

1. Create **HTTP In** (POST `/esp32/dashboard`)  
2. Add **JSON node**  
3. Add **ui_gauge**  
   - Value: `{{payload.temperature}}`  
4. Add **ui_text**:
   ```
   Device: {{payload.device}}
   Time: {{payload.timestamp}}
   ```
5. Add **HTTP Response**

Dashboard URL:
```
http://localhost:1880/ui
```

---

## 📊 5. Result

Full pipeline:
```
ESP32 → MQTT → n8n → Node-RED → Dashboard
```

Real-time sensor data appears in Node-RED dashboard.

---

## 💬 6. Discussion Questions

1. Why use MQTT in IoT systems?  
2. What benefits does n8n provide for automation?  
3. How does Node-RED complement n8n?  
4. What happens if MQTT broker disconnects?  
5. How do multiple devices share topics?

---

## 🧠 7. Extension Activities

- Log data to Google Sheets via n8n  
- Add email/SMS alerts for high temperature  
- Add chart node to Node-RED  
- Send multiple sensor types in JSON  
- Build BLE → Python → MQTT → n8n pipeline  

---

## 🧾 8. Conclusion

This lab demonstrated:

- MQTT data acquisition  
- n8n MQTT integration  
- Processing and forwarding data  
- Building a live dashboard in Node-RED  

This forms the basis of a complete IoT automation environment.

---

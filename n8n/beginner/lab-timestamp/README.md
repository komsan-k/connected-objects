# 🔬 Lab: Building a Timestamp Flow in n8n

## 🧩 1. Objective

This laboratory exercise introduces the beginner to **workflow automation** using n8n.  
Students will learn how to:

- Use the **Cron Trigger** to schedule automatic workflow execution.  
- Generate and format timestamps using n8n expressions.  
- Pass data between nodes.  
- Execute and visualize workflow output.  

---

## ⚙️ 2. Prerequisites

| Requirement | Details |
|------------|---------|
| **n8n installed** | Desktop version or npm installation |
| **Web browser** | Chrome, Edge, or Firefox |
| **Basic familiarity** | Ability to open n8n and create workflows |

Open n8n:

```
http://localhost:5678
```

---

## 🧠 3. Background Theory

### 3.1 What is n8n?

**n8n** is a workflow automation tool that lets you connect different systems and automate tasks with little or no code.

### 3.2 Cron Trigger

The **Cron node** automatically triggers workflows at timed intervals:

- Every X seconds/minutes  
- Daily  
- Weekly  
- Monthly  
- Custom cron expressions

### 3.3 Timestamps

Built-in expressions:

- `{{$now}}`
- `{{$now.toISO()}}`
- `{{$now.format("YYYY-MM-DD HH:mm:ss")}}`
- `{{$now.unix()}}`

---

## 🧩 4. Lab Tasks

### ✅ Task 1 — Create a New Workflow

1. Open n8n  
2. Click **+ New Workflow**  
3. Name it: `Timestamp Flow`

---

### ✅ Task 2 — Add a Cron Trigger

1. Click **Add Node**
2. Search **Cron**
3. Configure:

```
Mode: Every X seconds
Value: 10
```

Workflow will run every 10 seconds.

---

### ✅ Task 3 — Add a Set Node

1. Add a **Set** node  
2. Add Value → **String**  
3. Field name:

```
timestamp
```

4. Value:

```
{{$now.format("YYYY-MM-DD HH:mm:ss")}}
```

---

### 🧪 Task 4 — Connect Nodes

```
Cron → Set
```

---

### ▶️ Task 5 — Execute Workflow

Click **Execute Workflow**.  
Output example:

```json
{
  "timestamp": "2025-11-15 14:23:05"
}
```

Activate to run automatically.

---

## 📊 5. Result Interpretation

Each run generates a new timestamp.  
This demonstrates:

- Cron scheduling  
- Expression usage  
- Node-to-node data passing  

---

## 💬 6. Discussion Questions

1. What is the purpose of a Cron Trigger?  
2. Why do we format timestamps?  
3. How could this flow integrate with MQTT or ESP32 sensors?  
4. How can timestamps support IoT data logging?

---

## 🧠 7. Extension Activities

- Log timestamp into Google Sheets  
- Publish timestamp via MQTT  
- Trigger an HTTP request  
- Write timestamp to local file  
- Send timestamp via email / Telegram  

---

## 🧾 8. Conclusion

This lab introduced:

- Cron Trigger  
- Expressions  
- Automatic workflow execution  

This foundation enables more advanced n8n workflows involving IoT, BLE, MQTT, and cloud systems.

---

## 📘 References

- n8n Docs: https://docs.n8n.io
- Cron Reference: https://crontab.guru
- ISO Time Format Standard

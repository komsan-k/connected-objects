# 🚀 Installing n8n on Windows

This README explains **three simple ways** to install **n8n**, a powerful workflow automation tool, on a Windows machine.

Whether you're a beginner or an advanced developer, choose the method that best fits your workflow.

---

# ⭐ 1. Method 1 (Recommended): Install n8n Using Node.js (No Docker)

✔ Best for beginners  
✔ Runs natively on Windows  
✔ No extra software required  

---

## **Step 1 — Install Node.js LTS**

Download Node.js from:

🔗 https://nodejs.org/en/download

Install the **LTS (Long-Term Support)** version for maximum stability.

After installation, open **PowerShell** or **Command Prompt** and verify:

```
node -v
npm -v
```

You should see version numbers.

---

## **Step 2 — Install n8n Globally**

Run the following command:

```
npm install n8n -g
```

This installs n8n system-wide.

---

## **Step 3 — Start n8n**

Simply type:

```
n8n
```

When it starts successfully, you’ll see:

```
n8n ready on http://localhost:5678/
```

Open your browser and visit:

👉 http://localhost:5678/

Your n8n editor will now load and save workflows in your Windows user directory.

---

## **Step 4 — (Optional) Keep n8n Running in the Background**

Use **PM2** to keep n8n running automatically:

```
npm install pm2 -g
pm2 start n8n
pm2 save
pm2 startup
```

---

# ⭐ 2. Method 2: Install n8n Desktop (GUI Version)

Perfect for users who prefer a **simple GUI application**.

Download from:

🔗 https://n8n.io/desktop

Install it like a normal Windows app.

Once opened, it automatically launches the n8n editor at:

👉 http://localhost:5678/

⚠️ Note: n8n Desktop does not support all enterprise features.

---

# ⭐ 3. Method 3: Install n8n Using Docker (Advanced Users)

Great for developers, server setups, or isolated containers.

Requires **Docker Desktop** installed.

Run:

```
docker run -it --rm -p 5678:5678 n8nio/n8n
```

Then open:

👉 http://localhost:5678/

If you need persistent storage, ask for the **docker-compose.yml** version.

---

# 🧪 Verify Your Installation

Open your browser and visit:

```
http://localhost:5678/
```

You should see the **n8n Workflow Automation** interface.

---

# 🧠 Summary Table

| Method | Difficulty | Best For |
|--------|------------|----------|
| **Node.js Install** | Easy | Most Windows users |
| **n8n Desktop App** | Very Easy | Beginners |
| **Docker** | Medium | Developers & production |


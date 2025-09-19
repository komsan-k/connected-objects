# TCP Communication with Python

## 1. Lab Objectives
- Understand the basics of socket programming in Python.  
- Implement TCP client–server communication.  
- Test data transmission between client and server.  
- Apply concepts of reliable communication in practical scenarios.  

---

## 2. Background Theory
The **Transmission Control Protocol (TCP)** is a connection-oriented communication protocol that ensures reliable, ordered, and error-checked delivery of data between applications.  

- TCP communication is established through a **three-way handshake** (SYN, SYN-ACK, ACK).  
- After this handshake, data can be exchanged until one side closes the connection.  
- In Python, TCP communication is implemented using the **`socket`** library, which provides functions for creating, binding, listening, connecting, sending, and receiving data.  

---

## 3. Requirements

### Hardware
- PC with Python installed (≥3.8).  
- *(Optional)* ESP32 or Raspberry Pi for IoT extension.  

### Software
- Python (with built-in `socket` module).  
- Text editor (VS Code, Thonny, or IDLE).  
- Terminal / Command Prompt.  

---

## 4. System Architecture
The system consists of two entities:  

- **Server** → waits for client requests and echoes received messages.  
- **Client** → initiates communication and sends data to the server.  

```
+-----------+       TCP        +-----------+
|   Client  | <--------------> |   Server  |
+-----------+                  +-----------+
```

---

## 5. Lab Procedure

### Step 1: Write the Server Code
Save the following as `server.py`:

```python
import socket

HOST = "127.0.0.1"   # Localhost
PORT = 65432         # Port number

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Server listening on {HOST}:{PORT}...")

conn, addr = server_socket.accept()
print(f"Connected by {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print("Received:", data.decode())
    conn.sendall(data)   # Echo back

conn.close()
server_socket.close()
```

---

### Step 2: Write the Client Code
Save the following as `client.py`:

```python
import socket

HOST = "127.0.0.1"
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = "Hello from client!"
client_socket.sendall(message.encode())

data = client_socket.recv(1024)
print("Received from server:", data.decode())

client_socket.close()
```

---

### Step 3: Run the Programs
1. Open two terminals.  
2. Run the server first:  
   ```bash
   python server.py
   ```  
3. Run the client in another terminal:  
   ```bash
   python client.py
   ```  
4. Observe the exchange of messages.  

---

## 6. Expected Output

### Server Side
```
Server listening on 127.0.0.1:65432...
Connected by ('127.0.0.1', 55321)
Received: Hello from client!
```

### Client Side
```
Received from server: Hello from client!
```

---

## 7. Applications
- Chat applications.  
- IoT communication between ESP32 and a Python server.  
- Remote monitoring/control systems.  
- Educational demonstrations of reliable protocols.  

---

## 8. Lab Questions
1. What is the difference between TCP and UDP communication?  
2. Why does the server need to call both `listen()` and `accept()`?  
3. What happens if the client tries to connect to the wrong port?  
4. Modify the client to send multiple messages instead of one.  
5. Extend the server to handle multiple clients simultaneously (*hint: threading*).  

---

## 🔹 Advanced Extension: Multi-Client TCP Server with Threading

In real-world systems, servers must handle **multiple clients at once**. This can be achieved using **Python threading**.

### Multi-Client Server (`server_threaded.py`)

```python
import socket
import threading

HOST = "127.0.0.1"
PORT = 65432

def handle_client(conn, addr):
    print(f"New connection: {addr}")
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received from {addr}: {data.decode()}")
            conn.sendall(data)  # Echo back
        except:
            break
    print(f"Connection closed: {addr}")
    conn.close()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"Threaded Server listening on {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"Active connections: {threading.active_count() - 1}")
```

### Multi-Message Client (`client_multi.py`)

```python
import socket

HOST = "127.0.0.1"
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

messages = ["Hello", "How are you?", "Goodbye"]

for msg in messages:
    client_socket.sendall(msg.encode())
    data = client_socket.recv(1024)
    print("Received from server:", data.decode())

client_socket.close()
```

### How to Run
1. Start the threaded server:
   ```bash
   python server_threaded.py
   ```
2. Open multiple terminals and run several clients simultaneously:
   ```bash
   python client_multi.py
   ```

You’ll see the server handling multiple connections concurrently.

---

✅ This **extension** demonstrates how to scale from a **basic echo server** to a **multi-client threaded server**, preparing you for **chat apps, IoT gateways, and network services**.


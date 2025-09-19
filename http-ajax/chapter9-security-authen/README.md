# Security and Authentication in HTTP/AJAX ESP32 Servers

## Introduction

IoT devices such as ESP32 often serve as gateways between the physical
and digital world. When exposed over networks, they become vulnerable to
unauthorized access, data theft, or manipulation. Insecure dashboards
can lead to malicious control of actuators or leakage of private sensor
data.

This chapter explores authentication and security mechanisms for ESP32
web servers. We review core security principles, implement multiple
authentication methods, discuss HTTPS support, study penetration testing
basics, and design secure dashboards.

## Security Foundations for IoT

### CIA Triad

-   **Confidentiality** --- Prevent unauthorized access to data.

-   **Integrity** --- Ensure data is not altered maliciously.

-   **Availability** --- Keep services online and accessible.

### Common Threats

-   Unauthorized access (weak passwords).

-   Data sniffing (unencrypted traffic).

-   Replay attacks (reusing captured requests).

-   Denial of Service (flooding ESP32 with requests).

## Types of Authentication

### Basic Authentication

Username and password sent in Base64 headers. Simple but must be
combined with HTTPS.

### Token-Based Authentication

Client logs in and receives a temporary token.

### Session-Based Authentication

ESP32 stores session IDs --- costly in memory.

### JWT (JSON Web Token)

Compact, self-contained tokens. Possible in ESP32 but adds complexity.

### OAuth-Lite

Simplified token exchange for constrained devices.

## Implementing Basic Authentication

### ESP32 Example

``` {#code:basicauth .c++ language="C++" caption="Basic Authentication Example" label="code:basicauth"}
const char* username="admin";
const char* userpass="esp32";

void handleSecure(){
  if(!server.authenticate(username,userpass)){
    return server.requestAuthentication();
  }
  server.send(200,"text/html","<h1>Welcome, Secure User</h1>");
}
```

### Line-by-Line Explanation

-   `server.authenticate()` checks credentials.

-   `server.requestAuthentication()` prompts login dialog.

-   Access is denied without correct credentials.

## Password-Protected AJAX Dashboard

### ESP32 Code

``` {#code:ajaxsecure .c++ language="C++" caption="Password-Protected Dashboard" label="code:ajaxsecure"}
void handleDashboard(){
  if(!server.authenticate(username,userpass)){
    return server.requestAuthentication();
  }
  String html="<h1>Secure Dashboard</h1>"
              "<p>LDR: <span id='ldr'>---</span></p>"
              "<script>async function update(){"
                "let r=await fetch('/ldr');"
                "let j=await r.json();"
                "document.getElementById('ldr').innerText=j.ldr;}"
              "setInterval(update,2000);update();</script>";
  server.send(200,"text/html",html);
}
```

## Token-Based Authentication

### How It Works

1.  User logs in via `/login`.

2.  ESP32 generates a token.

3.  Subsequent AJAX requests include the token in headers.

### ESP32 Example

``` {#code:tokenauth .c++ language="C++" caption="Token Authentication" label="code:tokenauth"}
String token="";

void handleLogin(){
  if(server.arg("user")=="admin" && server.arg("pass")=="esp32"){
    token=String(random(100000,999999));
    server.send(200,"application/json","{\"token\":\""+token+"\"}");
  } else {
    server.send(403,"application/json","{\"error\":\"Invalid\"}");
  }
}

void handleSensor(){
  String auth=server.header("Auth-Token");
  if(auth!=token){
    server.send(403,"application/json","{\"error\":\"Unauthorized\"}");
    return;
  }
  int ldr=analogRead(34);
  server.send(200,"application/json","{\"ldr\":"+String(ldr)+"}");
}
```

## JWT-Style Tokens on ESP32

### Concept

-   JWT contains header, payload, and signature.

-   Useful for scalable authentication.

### Limitations

ESP32 has limited resources; full JWT libraries may be heavy. A
lightweight "JWT-style" approach is often sufficient.

## HTTPS and TLS on ESP32

### Why HTTPS Matters

Prevents eavesdropping and man-in-the-middle attacks.

### Challenges on ESP32

-   Limited RAM for certificates.

-   Complex SSL handshake.

### ESP32 HTTPS Example

``` {#code:https .c++ language="C++" caption="WiFiClientSecure Example" label="code:https"}
#include <WiFiClientSecure.h>
WiFiClientSecure client;

void connectHTTPS(){
  client.setInsecure(); // bypass cert validation for demo
  if(client.connect("example.com",443)){
    client.println("GET / HTTP/1.1\r\nHost: example.com\r\n\r\n");
  }
}
```

### Reverse Proxy Strategy

ESP32 runs HTTP locally; Nginx or Apache provides HTTPS externally.

## Penetration Testing Basics

### Brute Force Attacks

Attackers try many password combinations.

### Replay Attacks

Captured requests reused to simulate valid access.

### Sniffing

Unencrypted traffic intercepted with Wireshark.

### Defense Mechanisms

-   Strong passwords.

-   Tokens with expiration.

-   HTTPS/TLS.

-   Rate limiting.

## Secure Coding Practices

-   Sanitize all inputs.

-   Avoid storing credentials in plain text.

-   Use secure random generators for tokens.

-   Implement rate limiting on login endpoints.

## Real-World IoT Security Case Studies

### Mirai Botnet

Millions of IoT devices with weak passwords hijacked for DDoS.

### Unsecured Webcams

Publicly exposed dashboards accessible without authentication.

### Lessons Learned

Security must be considered from the start --- not as an afterthought.

## Labworks

### Labwork 9.1: Basic Authentication

Protect a page with username and password.

### Labwork 9.2: Password-Protected Dashboard

Implement secure AJAX dashboard.

### Labwork 9.3: Token Authentication

Use tokens for secure endpoints.

### Labwork 9.4: Unauthorized Access Test

Simulate failed login attempts.

### Labwork 9.5: Reverse Proxy with HTTPS

Secure ESP32 using Nginx as proxy.

### Labwork 9.6: JWT-Style Token Authentication

Generate and verify simple JWT-like tokens.

### Labwork 9.7: HTTPS with WiFiClientSecure

Connect ESP32 securely to a server.

### Labwork 9.8: Brute Force Simulation

Test dashboard with weak passwords.

### Labwork 9.9: Secure Coding Lab

Implement input sanitization and request limits.

### Labwork 9.10: Mini-Project --- Secure Smart Home Dashboard

Combine authentication, HTTPS proxy, and secure coding for a
professional secure dashboard.

## Summary

In this chapter, we:

-   Reviewed IoT security principles and common threats.

-   Implemented Basic, Token, and JWT-style authentication.

-   Discussed HTTPS/TLS on ESP32 and reverse proxies.

-   Explored penetration testing basics.

-   Applied secure coding practices.

-   Completed 10 labworks, culminating in a secure IoT smart home
    dashboard.

## Review Questions

1.  What are the most common threats against ESP32 web servers?

2.  Compare Basic Authentication, Token Authentication, and JWT.

3.  Why is HTTPS difficult to implement fully on ESP32?

4.  How can reverse proxies help secure ESP32 dashboards?

5.  Suggest secure coding practices for ESP32 web servers.


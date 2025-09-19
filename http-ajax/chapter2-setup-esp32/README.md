\chapter{Serving Dynamic Content with ESP32}

\section{Introduction}

In Chapter~2, we explored serving static content from ESP32, including HTML, CSS, JavaScript, and images. Static content is important for structure and design, but IoT applications demand something more: \textbf{dynamic content}. Dynamic content reflects real-time conditions such as sensor readings, actuator states, or messages from other devices.  

In this chapter, we expand on techniques to generate and serve dynamic content. We compare different update methods (meta refresh, AJAX, SSE, WebSockets), build dashboards with real-time charts, and provide practical labworks to consolidate knowledge.

\section{Static vs Dynamic Content in Depth}

\subsection{Static Content}
\begin{itemize}
  \item Predefined and does not change unless manually updated.
  \item Examples: logo, stylesheet, help page.
\end{itemize}

\subsection{Dynamic Content}
\begin{itemize}
  \item Generated at runtime, based on conditions or inputs.
  \item Examples: displaying LDR sensor value, system uptime.
\end{itemize}

\subsection{Server-Side vs Client-Side Rendering}
\begin{itemize}
  \item \textbf{Server-side:} ESP32 inserts sensor values into HTML before sending.
  \item \textbf{Client-side:} Browser fetches raw data (e.g., JSON) and renders it using JavaScript.
\end{itemize}

\section{Update Techniques for Dynamic Content}

\subsection{Meta Refresh}
\begin{itemize}
  \item Page reloads every few seconds.
  \item Pros: simple to implement.
  \item Cons: flickers, reload overhead.
\end{itemize}

\subsection{AJAX Polling}
\begin{itemize}
  \item JavaScript periodically fetches data.
  \item Pros: efficient, partial updates only.
  \item Cons: may waste requests if data does not change.
\end{itemize}

\subsection{Long Polling}
\begin{itemize}
  \item Request held open until new data is available.
  \item Pros: fewer wasted requests.
  \item Cons: each client consumes server resources.
\end{itemize}

\subsection{Server-Sent Events (SSE)}
\begin{itemize}
  \item One-way stream of data from server to client.
  \item Pros: efficient, push-based.
  \item Cons: unidirectional only.
\end{itemize}

\subsection{WebSockets}
\begin{itemize}
  \item Full-duplex communication channel.
  \item Pros: real-time, interactive.
  \item Cons: higher complexity.
\end{itemize}

\subsection{Comparison Table}
\begin{tabular}{|l|l|l|}
\hline
Method & Pros & Cons \\
\hline
Meta Refresh & Simple, no JS needed & Page flicker, bandwidth waste \\
AJAX Polling & Efficient, smooth UI & Repeated requests \\
Long Polling & Updates only when needed & Resource heavy for many clients \\
SSE & Push updates, lightweight & Only one-way communication \\
WebSockets & Real-time, bidirectional & More complex, higher overhead \\
\hline
\end{tabular}

\section{Embedding Sensor Values in HTML}

\subsection{Example: LDR with Meta Refresh}
\begin{lstlisting}[language=C++, caption={Meta Refresh LDR Page}, label=code:ldrmeta]
String buildPage() {
  int value = analogRead(34);
  String html = "<!DOCTYPE html><html><head>"
                "<meta http-equiv='refresh' content='5'>"
                "<title>ESP32 LDR</title></head><body>"
                "<h1>LDR Value: " + String(value) + "</h1>"
                "</body></html>";
  return html;
}
\end{lstlisting}

\subsection{Line-by-Line Explanation}
\begin{itemize}
  \item \texttt{analogRead(34)} — reads the LDR value.
  \item \texttt{meta refresh} — reloads page every 5 seconds.
  \item Output is simple HTML with the sensor value embedded.
\end{itemize}

\section{Serving JSON for AJAX}

\subsection{Basic JSON Endpoint}
\begin{lstlisting}[language=C++, caption={JSON Endpoint}, label=code:jsonendpoint]
void handleJSON() {
  int ldr = analogRead(34);
  String json = "{\"ldr\":" + String(ldr) + "}";
  server.send(200,"application/json",json);
}
\end{lstlisting}

\subsection{Why JSON?}
\begin{itemize}
  \item Lightweight, easy for JavaScript to parse.
  \item Standard format in IoT communication.
\end{itemize}

\section{AJAX Dashboard Example}

\subsection{Complete Code}
\begin{lstlisting}[language=C++, caption={AJAX Dashboard for LDR}, label=code:ajaxdash]
void handleDashboard() {
  String html="<!DOCTYPE html><html><body>"
              "<h1>AJAX LDR Dashboard</h1>"
              "<p id='ldr'>---</p>"
              "<script>"
              "async function update(){"
                "let r=await fetch('/ldr');"
                "let j=await r.json();"
                "document.getElementById('ldr').innerText=j.ldr;"
              "}"
              "setInterval(update,1000); update();"
              "</script></body></html>";
  server.send(200,"text/html",html);
}
\end{lstlisting}

\subsection{Explanation}
\begin{itemize}
  \item JavaScript fetches JSON from ESP32 every second.
  \item DOM is updated with new values.
  \item Smooth updates without full reload.
\end{itemize}

\section{Multi-Sensor JSON Example}

\begin{lstlisting}[language=C++, caption={Multi-Sensor JSON}, label=code:multisensor]
void handleSensors() {
  int ldr = analogRead(34);
  float temp = 25.5;
  String json = "{\"ldr\":" + String(ldr) +
                ",\"temp\":" + String(temp,1) + "}";
  server.send(200,"application/json",json);
}
\end{lstlisting}

\section{Data Visualization: Chart.js}

\subsection{Line Chart Example}
\begin{lstlisting}[language=C++, caption={Chart.js Example}, label=code:chartjs]
"<canvas id='c' width='400' height='200'></canvas>"
"<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>"
"<script>"
"let ctx=document.getElementById('c').getContext('2d');"
"let data={labels:[],datasets:[{label:'LDR',data:[],borderColor:'blue'}]};"
"let chart=new Chart(ctx,{type:'line',data:data});"
"async function update(){"
  "let r=await fetch('/ldr'); let j=await r.json();"
  "data.labels.push(new Date().toLocaleTimeString());"
  "data.datasets[0].data.push(j.ldr);"
  "if(data.labels.length>20){data.labels.shift();data.datasets[0].data.shift();}"
  "chart.update();}"
"setInterval(update,1000);"
"</script>"
\end{lstlisting}

\section{Real-Time Gauges and Tables}

\subsection{Gauge Visualization}
Third-party libraries (e.g., JustGage, SmoothieCharts) allow gauge widgets for sensor values.

\subsection{Dynamic Tables}
HTML tables updated with AJAX can display multiple sensor values clearly.

\section{Multi-Client Synchronization}

\subsection{Challenge}
When multiple clients connect, each may receive outdated or conflicting data.

\subsection{Solutions}
\begin{itemize}
  \item Central JSON endpoint for all sensors.
  \item Timestamp values for synchronization.
  \item Use SSE or WebSockets for push updates.
\end{itemize}

\section{Labworks}

\subsection{Labwork 3.1: Meta Refresh Demo}
Display LDR value with automatic page reload.

\subsection{Labwork 3.2: JSON Endpoint}
Serve sensor value as JSON.

\subsection{Labwork 3.3: AJAX Dashboard}
Build dashboard with real-time updates.

\subsection{Labwork 3.4: Multi-Sensor JSON}
Serve multiple sensor values in one JSON response.

\subsection{Labwork 3.5: Chart.js Visualization}
Plot sensor values as a real-time chart.

\subsection{Labwork 3.6: XML Endpoint}
Serve sensor data in XML for legacy compatibility.

\subsection{Labwork 3.7: Dynamic Tables}
Use AJAX to fill HTML table with sensor values.

\subsection{Labwork 3.8: Real-Time Gauges}
Implement gauge visualization for one sensor.

\subsection{Labwork 3.9: JSON + Visualization}
Combine JSON endpoint with Chart.js and table.

\subsection{Labwork 3.10: Error Recovery}
Simulate ESP32 disconnection and handle gracefully.

\section{Summary}

In this chapter, we:
\begin{itemize}
  \item Differentiated static vs dynamic content.
  \item Compared meta refresh, AJAX, long polling, SSE, and WebSockets.
  \item Built dashboards with JSON, AJAX, and Chart.js.
  \item Introduced visualization using tables and gauges.
  \item Addressed multi-client synchronization issues.
  \item Completed 10 labworks covering dynamic web serving.
\end{itemize}

\section{Review Questions}
\begin{enumerate}
  \item Compare server-side vs client-side rendering for ESP32 dashboards.
  \item Why is JSON preferred for AJAX responses?
  \item Explain pros and cons of AJAX vs SSE vs WebSockets.
  \item How can gauges and tables improve IoT dashboards?
  \item Suggest strategies to handle multi-client synchronization.
\end{enumerate}


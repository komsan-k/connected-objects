# LAB 5 — Scheduling using pthread and FreeRTOS

## 1. Objective
The objective of this lab is to:
1. Understand task scheduling principles on embedded systems.
2. Implement multitasking using **POSIX threads (pthread)** on platforms that support them.
3. Implement multitasking using **FreeRTOS tasks** on the ESP32.
4. Compare cooperative vs. preemptive scheduling.
5. Demonstrate real-time constraints in task execution.

---

## 2. Background

Modern embedded systems often need to handle multiple tasks concurrently, such as sensor sampling, communication, and user interface updates.  
Two common approaches to multitasking are:

- **pthread (POSIX Threads)**: A portable API for multithreading on systems with an operating system (Linux, embedded Linux boards like Raspberry Pi).
- **FreeRTOS**: A real-time operating system kernel designed for microcontrollers like the ESP32, offering lightweight task management and scheduling.

**Key Concepts**:
- **Task/Thread**: Independent sequence of execution.
- **Scheduler**: Decides which task runs at any given time.
- **Priority**: Determines importance of tasks.
- **Preemption**: Ability of a higher-priority task to interrupt a lower-priority one.
- **Tick Rate**: The scheduler's time quantum, often in milliseconds.

---

## 3. Hardware & Software Requirements

### Hardware
- ESP32 development board
- USB cable
- Serial Monitor (Arduino IDE / PlatformIO)
- Optional: LED and resistor for visual indicators

### Software
- Arduino IDE or PlatformIO (ESP32 core installed)
- For pthread: Linux host or ESP-IDF on ESP32 (pthread API supported)
- FreeRTOS: Included in ESP32 Arduino core or ESP-IDF

---

## 4. Task Description

### 4.1 pthread Scheduling Example (Linux or ESP-IDF environment)

#### Code
```cpp
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

void* taskA(void* arg) {
    while (1) {
        printf("Task A running...\n");
        usleep(500000); // 0.5 sec
    }
    return NULL;
}

void* taskB(void* arg) {
    while (1) {
        printf("Task B running...\n");
        usleep(1000000); // 1 sec
    }
    return NULL;
}

int main() {
    pthread_t t1, t2;

    pthread_create(&t1, NULL, taskA, NULL);
    pthread_create(&t2, NULL, taskB, NULL);

    pthread_join(t1, NULL);
    pthread_join(t2, NULL);

    return 0;
}
```

#### Notes
- `pthread_create()` starts a new thread.
- `usleep()` simulates periodic execution.
- On ESP32, pthread is available when using ESP-IDF or Arduino with `CONFIG_PTHREAD_TASK_PRIO_DEFAULT`.

---

### 4.2 FreeRTOS Scheduling Example (ESP32 Arduino)

#### Code
```cpp
#include <Arduino.h>

TaskHandle_t Task1, Task2;

void Task1code(void* pvParameters) {
  for (;;) {
    Serial.println("Task 1 running...");
    vTaskDelay(500 / portTICK_PERIOD_MS); // 500ms delay
  }
}

void Task2code(void* pvParameters) {
  for (;;) {
    Serial.println("Task 2 running...");
    vTaskDelay(1000 / portTICK_PERIOD_MS); // 1s delay
  }
}

void setup() {
  Serial.begin(115200);

  xTaskCreatePinnedToCore(
    Task1code, "Task1", 10000, NULL, 1, &Task1, 0);

  xTaskCreatePinnedToCore(
    Task2code, "Task2", 10000, NULL, 1, &Task2, 1);
}

void loop() {
  // Empty - tasks run independently
}
```

#### Notes
- `xTaskCreatePinnedToCore()` creates a task on a specific core (ESP32 has 2 cores).
- `vTaskDelay()` yields control to the scheduler.
- Task priority can be adjusted to influence execution order.

---

## 5. Experiments

1. **Vary Task Priorities**  
   Change priority values in `xTaskCreatePinnedToCore()` and observe execution frequency.
2. **Add LED Blink Tasks**  
   Assign different blink rates to LEDs and verify scheduling consistency.
3. **Simulate Heavy Load**  
   Add computational loops to test preemption in FreeRTOS.
4. **Mix pthread and FreeRTOS (ESP-IDF)**  
   Run both models together for comparison.

---

## 6. Comparison Table

| Feature        | pthread                  | FreeRTOS                      |
|----------------|--------------------------|--------------------------------|
| Portability    | High (POSIX systems)     | Microcontroller-focused        |
| Overhead       | Higher                   | Lower                          |
| Real-time      | No strict real-time      | Designed for real-time tasks   |
| Memory use     | Depends on OS            | Small footprint                |
| API complexity | Moderate                 | Simple for embedded use        |

---

## 7. Exercises
1. Implement three FreeRTOS tasks:  
   - Task 1: Blink LED every 200 ms  
   - Task 2: Read sensor every 1 s  
   - Task 3: Send data via Serial every 3 s
2. Modify priorities to give the sensor task highest priority.
3. Implement mutex locking for shared resource access.
4. Port the FreeRTOS code to ESP-IDF and run without Arduino framework.

---

## 8. Conclusion
In this lab, we implemented scheduling using both **pthread** and **FreeRTOS**. pthread provided a familiar multithreading interface for POSIX systems, while FreeRTOS offered a lightweight, deterministic scheduler tailored for embedded microcontrollers. By experimenting with task priorities, delays, and workloads, we observed how the scheduler manages execution order and timing. FreeRTOS's real-time nature makes it ideal for embedded IoT systems requiring predictable behavior.


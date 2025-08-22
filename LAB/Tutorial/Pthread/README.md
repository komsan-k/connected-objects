# Principles of pthread (POSIX Threads)

This document gives a practical, concise overview of **pthread** and includes three **basic examples** you can compile and run.

---

## 1) What is pthread?
- **pthread (POSIX threads)** is a standardized C library (IEEE POSIX 1003.1c) for multithreading.
- It enables **concurrent execution** of tasks within the same process.
- Threads share the same **address space, globals, and resources**, but each has its own **stack** and **program counter**.

---

## 2) Key Concepts
- **Thread**: A lightweight execution unit inside a process.
- **Thread ID** (`pthread_t`): Unique identifier for each thread.
- **Thread Creation**: `pthread_create()` spawns a new thread that runs a function.
- **Thread Termination**: Return from the function, call `pthread_exit()`, or be canceled.
- **Scheduling**: OS decides when each thread runs (time-slicing, priorities).
- **Synchronization**: Use **mutexes** and **condition variables** to avoid race conditions.

---

## 3) pthread Lifecycle
1. **Create** – `pthread_create()` starts a new thread.
2. **Run** – The thread executes concurrently.
3. **Sync** – Coordinate with mutexes/conds when sharing data.
4. **Join/Detach** – `pthread_join()` waits; `pthread_detach()` lets it run without join.
5. **Exit** – Thread ends (return or `pthread_exit()`), resources reclaimed.

---

## 4) Advantages
- Efficient on multi-core CPUs.
- Shared memory → fast data sharing without IPC.
- Lower overhead than processes.
- Great for real-time/embedded patterns (sensor read, control loops, comms).

---

## 5) Common Pitfalls
- **Race conditions**: Unsynchronized shared access.
- **Deadlock**: Threads wait on each other’s locks forever.
- **Starvation**: Some threads never get CPU time.
- **Harder debugging**: Nondeterministic interleavings.

---

## 6) Core APIs (quick table)
- `pthread_create(pthread_t*, const pthread_attr_t*, void*(*fn)(void*), void* arg)`
- `pthread_join(pthread_t, void** retval)` / `pthread_detach(pthread_t)`
- `pthread_exit(void* retval)`
- `pthread_mutex_init/lock/unlock/destroy`
- `pthread_cond_wait/signal/broadcast`

> Compile (Linux/macOS): `gcc file.c -o app -lpthread`

---

## 7) Basic Examples

### Example A — Two Threads Printing
```c
// ex_a_two_threads.c
#include <pthread.h>
#include <stdio.h>
#include <unistd.h>

void* task1(void* arg){
    while(1){ printf("Task 1 running...\n"); sleep(1); }
    return NULL;
}
void* task2(void* arg){
    while(1){ printf("Task 2 running...\n"); sleep(1); }
    return NULL;
}
int main(){
    pthread_t t1, t2;
    pthread_create(&t1, NULL, task1, NULL);
    pthread_create(&t2, NULL, task2, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    return 0;
}
```
**Run:** `gcc ex_a_two_threads.c -o ex_a -lpthread && ./ex_a`

---

### Example B — Race Condition (No Mutex)
```c
// ex_b_race_condition.c
#include <pthread.h>
#include <stdio.h>

int counter = 0;  // shared

void* increment(void* arg){
    for(int i=0;i<100000;i++) counter++;  // UNSAFE
    return NULL;
}
int main(){
    pthread_t t1, t2;
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    printf("Final counter = %d (expected 200000, often less due to race)\n", counter);
    return 0;
}
```
**Run:** `gcc ex_b_race_condition.c -o ex_b -lpthread && ./ex_b`

---

### Example C — Safe Sharing with Mutex
```c
// ex_c_mutex_safe.c
#include <pthread.h>
#include <stdio.h>

int counter = 0;
pthread_mutex_t lock;

void* increment(void* arg){
    for(int i=0;i<100000;i++){
        pthread_mutex_lock(&lock);
        counter++;
        pthread_mutex_unlock(&lock);
    }
    return NULL;
}
int main(){
    pthread_t t1, t2;
    pthread_mutex_init(&lock, NULL);
    pthread_create(&t1, NULL, increment, NULL);
    pthread_create(&t2, NULL, increment, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_mutex_destroy(&lock);
    printf("Final counter = %d (should be 200000)\n", counter);
    return 0;
}
```
**Run:** `gcc ex_c_mutex_safe.c -o ex_c -lpthread && ./ex_c`

---

## 8) Tips
- Keep critical sections small (lock for the shortest time).
- Prefer one lock order across the app to avoid deadlocks.
- Use `pthread_cond_*` to wait for events rather than busy loops.
- In embedded contexts (e.g., ESP32 via ESP-IDF), map pthread to OS tasks and mind stack sizes.


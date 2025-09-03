# 📖 Theory of Averaging Filters for LM73 Readings

## 1. Why Filtering?
The **LM73** is a precision digital temperature sensor, but like all real-world devices, its readings can be noisy. Causes include:
- Electrical noise on the I²C bus  
- Quantization noise (limited resolution, e.g., 13/14-bit)  
- Rapid but irrelevant fluctuations (air drafts, ADC jitter)  

**Filtering** suppresses high-frequency variations while preserving the slow-changing true signal (temperature).

---

## 2. Simple Moving Average (SMA)

**Definition:**

\[
y[n] = \frac{1}{N} \sum_{k=0}^{N-1} x[n-k]
\]


where:
- `x[n]` = raw input sequence (sensor readings)  
- `y[n]` = filtered output  
- `N` = window size (# of samples)  

**Intuition:** SMA smooths the signal by replacing each sample with the average of the last `N`.  

**Properties:**
- **Low-pass filter:** attenuates rapid changes (noise), passes slow variations  
- **Smoothing strength:** increases with larger `N`  
- **Lag:** output lags by about `(N−1)/2` samples  

**LM73 use case:** If sampling at 10 Hz and `N=20`, the filter averages the last 2 seconds of temperature readings, producing a stable display.

**Simple Moving Average (SMA)**

Smooths by averaging the last **N** samples.  
- Good general-purpose filter.  
- Adds `N-1` samples of lag.  

```cpp
// ---- Simple Moving Average (SMA) ----
const size_t SMA_N = 16;   // window size (power of two helps if you want bit-shifts)
float smaBuf[SMA_N];
size_t smaIdx = 0;
bool smaPrimed = false;
double smaSum = 0.0;

float smaUpdate(float x) {
  smaSum -= smaBuf[smaIdx];
  smaBuf[smaIdx] = x;
  smaSum += x;

  smaIdx++;
  if (smaIdx >= SMA_N) { 
    smaIdx = 0; 
    smaPrimed = true; 
  }

  return (float)(smaSum / (smaPrimed ? SMA_N : smaIdx));
}
```

**Use:**
```cpp
float t = readLM73Celsius();
float t_sma = smaUpdate(t);
```

---


## 3. Exponential Moving Average (EMA)

**Definition:**

\[
y[n] = \alpha \, x[n] + (1 - \alpha) \, y[n-1]
\]


where `0 < α < 1`.

**Intuition:** Recent samples get more weight, controlled by `α`.  

**Properties:**
- **Low-pass filter:** Infinite impulse response (IIR)  
- **Memory-efficient:** requires only last output `y[n−1]`  
- **Tunable:**  
  - Small `α` → smoother, more lag  
  - Large `α` → faster response, less smoothing  
- Equivalent to SMA of length `N ≈ 2/α − 1`  

**LM73 use case:** Room temperature changes slowly; EMA smooths noise without needing a buffer. Useful in low-power devices.

**Exponential Moving Average (EMA)**

- Low-latency.  
- Less memory.  
- Tunable smoothing with `alpha`.  
- Rule of thumb: `alpha ≈ 2/(N+1)` to mimic an SMA of length `N`.  

```cpp
// ---- Exponential Moving Average (EMA) ----
const float EMA_ALPHA = 0.2f; // 0<alpha<=1; smaller = smoother, more lag
bool emaInit = false;
float emaPrev = 0.0f;

float emaUpdate(float x) {
  if (!emaInit) { 
    emaInit = true; 
    emaPrev = x; 
    return x; 
  }
  emaPrev = EMA_ALPHA * x + (1.0f - EMA_ALPHA) * emaPrev;
  return emaPrev;
}
```

**Use:**
```cpp
float t = readLM73Celsius();
float t_ema = emaUpdate(t);
```

---


## 4. Median Filter

**Definition:** For window size `N` (odd):

\[
y[n] = \operatorname{median}\{\, x[n], \; x[n-1], \; \ldots, \; x[n-(N-1)] \,\}
\]


**Intuition:**  
- Removes **impulse noise** (spikes) since outliers don’t affect the median.  
- Preserves step-like changes better than SMA/EMA.  

**Properties:**
- **Nonlinear filter:** does not blur edges as much as SMA  
- Excellent for glitch rejection  
- Slight lag, higher computation vs EMA  

**LM73 use case:** Rejects occasional I²C glitches (e.g., one false reading of 150 °C).

---
**Median-of-5 (Impulse/Spike Rejection)**

- Great at removing occasional spikes (e.g., I²C glitch).  
- Combine with EMA or SMA for best results.  

```cpp
// ---- Median of 5 ----
float medBuf[5];
size_t medCount = 0;

float median5Update(float x) {
  // Fill until we have 5 samples
  if (medCount < 5) { 
    medBuf[medCount++] = x; 
  }
  else {
    // shift left, append
    for (int i = 0; i < 4; ++i) medBuf[i] = medBuf[i+1];
    medBuf[4] = x;
  }

  size_t n = (medCount < 5) ? medCount : 5;
  // copy + sort small array (insertion sort)
  float a[5];
  for (size_t i = 0; i < n; ++i) a[i] = medBuf[i];
  for (size_t i = 1; i < n; ++i) {
    float key = a[i]; int j = i - 1;
    while (j >= 0 && a[j] > key) { 
      a[j+1] = a[j]; 
      j--; 
    }
    a[j+1] = key;
  }
  return a[n/2]; // median
}
```

**Use:**
```cpp
float t = readLM73Celsius();
float t_med = median5Update(t);
```

---

## 5. Hybrid Filtering
Combining filters often works best:
- **Median → EMA:** median removes spikes, EMA smooths continuous noise  
- **SMA with small N:** good compromise for ultra-low-power systems  

---

## 6. Theoretical Trade-offs

| Filter  | Noise reduction        | Lag                 | Memory            | Spike resistance |
|---------|------------------------|---------------------|------------------|-----------------|
| SMA     | High (if N large)      | Moderate (`N/2`)    | Needs buffer of N | Poor            |
| EMA     | Moderate–High          | Tunable (via α)     | Only 1 value      | Poor            |
| Median  | High (for spikes)      | Moderate            | Needs buffer of N | Excellent       |

---

## 7. Application in LM73

- Temperature changes slowly → low-pass filtering is natural  
- For **data logging / display**, SMA or EMA is enough  
- For **safety-critical control** (HVAC, thermostats): use Median + EMA to reject outliers while following true trends  

---

## ✅ Summary
- **SMA** = simple, effective, but adds delay  
- **EMA** = lightweight, tunable, great for MCUs  
- **Median** = spike-resistant, complements SMA/EMA  
- **Hybrid** = best balance for LM73 applications  


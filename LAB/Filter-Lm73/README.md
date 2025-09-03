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

```
y[n] = (1/N) * Σ (from k=0 to N−1) x[n−k]
```

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

---

## 3. Exponential Moving Average (EMA)

**Definition:**

```
y[n] = α * x[n] + (1−α) * y[n−1]
```

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

---

## 4. Median Filter

**Definition:** For window size `N` (odd):

```
y[n] = median{ x[n], x[n−1], …, x[n−(N−1)] }
```

**Intuition:**  
- Removes **impulse noise** (spikes) since outliers don’t affect the median.  
- Preserves step-like changes better than SMA/EMA.  

**Properties:**
- **Nonlinear filter:** does not blur edges as much as SMA  
- Excellent for glitch rejection  
- Slight lag, higher computation vs EMA  

**LM73 use case:** Rejects occasional I²C glitches (e.g., one false reading of 150 °C).

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


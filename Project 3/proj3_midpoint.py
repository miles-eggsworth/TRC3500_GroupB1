import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

# using threshold midpoint
def read_channels(filepath):
    with open(filepath, 'r') as f:
        lines = f.readlines()

    ch0, ch1 = [], []
    reading_ch0, reading_ch1 = False, False

    for line in lines:
        stripped = line.strip()
        if stripped == "Channel 0 Data:":
            reading_ch0 = True
            reading_ch1 = False
            continue
        elif stripped == "Channel 1 Data:":
            reading_ch1 = True
            reading_ch0 = False
            continue
        elif not stripped.isdigit():
            continue

        if reading_ch0:
            ch0.append(int(stripped))
        elif reading_ch1:
            ch1.append(int(stripped))

    return np.array(ch0), np.array(ch1)

def smooth(data, window=50):
    return np.convolve(data, np.ones(window)/window, mode='same')

def add_bias(data):
    data = data.astype(float)  # Ensure float to allow float multiplications
    mean_val = np.mean(data)
    biased = np.copy(data)
    biased[data > mean_val] *= 1.20
    biased[data <= mean_val] *= 0.80
    return biased


def detect_peak_cycles(ch1_smoothed, ch0_smoothed, sample_window=200, ch0_threshold=100):
    peaks, _ = find_peaks(ch1_smoothed, distance=200, prominence=100)
    cycles = []
    for i in range(len(peaks) - 1):
        p1, p2 = peaks[i], peaks[i+1]
        ch0_segment = ch0_smoothed[max(0, p1-sample_window):min(len(ch0_smoothed), p2+sample_window)]
        if len(ch0_segment) == 0:
            continue
        ch0_range = np.max(ch0_segment) - np.min(ch0_segment)
        if ch0_range >= ch0_threshold:
            cycles.append((p1, p2))
    return cycles, peaks

def count_midpoint_cycles(signal, midpoint, debounce_window=30):
    above = signal > midpoint
    crossings = np.diff(above.astype(int))
    crossing_indices = np.where(crossings != 0)[0]

    # Debounce crossings: only accept if it's far enough from the last accepted
    filtered = []
    last_idx = -np.inf
    for idx in crossing_indices:
        if idx - last_idx >= debounce_window:
            filtered.append(idx)
            last_idx = idx

    full_cycles = len(filtered) // 2  # 2 crossings = 1 cycle
    return full_cycles, filtered


# === Main ===

file_path = 'breathing_coolterm30_exercise_1.txt'
ch0, ch1 = read_channels(file_path)

# Preprocess
ch1_biased = add_bias(ch1)
ch1_smoothed = smooth(ch1_biased, window=50)
ch0_smoothed = smooth(ch0, window=50)

# Detect peak-based cycles
cycles, ch1_peaks = detect_peak_cycles(ch1_smoothed, ch0_smoothed)

# Midpoints and extremes (post-biasing)
ch0_min, ch0_max = np.min(ch0_smoothed), np.max(ch0_smoothed)
ch1_min, ch1_max = np.min(ch1_smoothed), np.max(ch1_smoothed)
ch0_mid = (ch0_min + ch0_max) / 2
ch1_mid = (ch1_min + ch1_max) / 2

# Midpoint-based cycle counting
ch0_cycles, ch0_crossings = count_midpoint_cycles(ch0_smoothed, ch0_mid)
ch1_cycles, ch1_crossings = count_midpoint_cycles(ch1_smoothed, ch1_mid)

# Plotting
plt.figure(figsize=(14, 8))

# plt.plot(ch0, label='Rubber (Raw)', alpha=0.3, color='blue')
plt.plot(ch0_smoothed, label='Rubber 0 (Smoothed)', color='blue')
# plt.plot(ch1_biased, label='Thermister (Raw + Bias)', alpha=0.3, color='red')
plt.plot(ch1_smoothed, label='Thermister (Smoothed)', color='orange')

# Min/max lines
plt.axhline(ch0_min, color='blue', linestyle=':', linewidth=1, label='Ch0 Min/Max')
plt.axhline(ch0_max, color='blue', linestyle=':', linewidth=1)
plt.axhline(ch1_min, color='orange', linestyle=':', linewidth=1, label='Ch1 Min/Max')
plt.axhline(ch1_max, color='orange', linestyle=':', linewidth=1)

# Midpoint lines
plt.axhline(ch0_mid, color='blue', linestyle='--', linewidth=1, label='Ch0 Midpoint')
plt.axhline(ch1_mid, color='orange', linestyle='--', linewidth=1, label='Ch1 Midpoint')

# Peak markers
for p in ch1_peaks:
    plt.axvline(p, linestyle='--', color='grey', alpha=0.5)

# Display results in title
plt.title(
    f"Channel 0 Cycles (Midpoint): {ch0_cycles} | "
    f"Channel 1 Cycles (Midpoint): {ch1_cycles}"
)
plt.ylabel("Signal Value")
plt.xlabel("Sample Index")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

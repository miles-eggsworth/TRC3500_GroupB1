import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

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
    data = data.astype(float)
    mean_val = np.mean(data)
    biased = np.copy(data)
    biased[data > mean_val] *= 1.20
    biased[data <= mean_val] *= 0.80
    return biased

def estimate_breath_rate_by_gradient(signal, sample_rate=100, window=50, debounce_samples=100):
    gradients = np.gradient(signal)
    sampled_indices = np.arange(0, len(gradients), window)
    sampled_gradients = gradients[sampled_indices]
    
    sign_changes = np.diff(np.sign(sampled_gradients))
    raw_turning_points = np.where(sign_changes != 0)[0] * window

    # Debounce: only accept changes at least `debounce_samples` apart
    filtered_turning_points = []
    last_tp = -np.inf
    for tp in raw_turning_points:
        if tp - last_tp >= debounce_samples:
            filtered_turning_points.append(tp)
            last_tp = tp

    num_cycles = len(filtered_turning_points) // 2
    total_seconds = len(signal) / sample_rate
    breaths_per_minute = (num_cycles / total_seconds) * 60

    return num_cycles, filtered_turning_points


# === Main ===

file_path = 'breathing_coolterm30_exercise_2.txt'
ch0, ch1 = read_channels(file_path)

ch1_biased = add_bias(ch1)
ch0_smoothed = smooth(ch0, window=50)
ch1_smoothed = smooth(ch1_biased, window=120)


ch0_min, ch0_max = np.min(ch0_smoothed), np.max(ch0_smoothed)
ch1_min, ch1_max = np.min(ch1_smoothed), np.max(ch1_smoothed)
ch0_mid = (ch0_min + ch0_max) / 2
ch1_mid = (ch1_min + ch1_max) / 2

# Gradient-based breathing rate for ch1 and ch0
bpm_ch0, gradient_turning_points_ch0 = estimate_breath_rate_by_gradient(
    ch0_smoothed, sample_rate=100, window=20, debounce_samples=100)

bpm_ch1, gradient_turning_points_ch1 = estimate_breath_rate_by_gradient(
    ch1_smoothed, sample_rate=100, window=60, debounce_samples=100)

print(f"Estimated Breathing Rate from Ch0 (Rubber): {bpm_ch0:.2f} breathes")
print(f"Estimated Breathing Rate from Ch1 (Thermistor): {bpm_ch1:.2f} breaths")


plt.figure(figsize=(14, 8))
plt.plot(ch0_smoothed, label='Rubber 0 (Smoothed)', color='blue')
plt.plot(ch1_smoothed, label='Thermister (Smoothed)', color='orange')

# Plot turning points (gradient-based)
# Plot turning points

for idx in gradient_turning_points_ch0:
    plt.axvline(idx, linestyle=':', color='green', alpha=0.4, label='Ch0 Turning Point' if idx == gradient_turning_points_ch0[0] else "")

for idx in gradient_turning_points_ch1:
    plt.axvline(idx, linestyle=':', color='purple', alpha=0.4, label='Ch1 Turning Point' if idx == gradient_turning_points_ch1[0] else "")

# Final title — remove midpoint cycle references
plt.title(f"Estimated Breathing Rate (Gradient-Based)")
plt.ylabel("Signal Value")
plt.xlabel("Sample Index")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()

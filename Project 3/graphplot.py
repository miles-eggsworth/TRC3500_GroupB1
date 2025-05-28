
# import matplotlib.pyplot as plt
# import numpy as np

# # File path
# file_path = 'breathing_coolterm30_exercise_3.txt'

# # Containers
# channel_0 = []
# channel_1 = []
# reading_ch0 = False
# reading_ch1 = False

# # Parse file
# with open(file_path, 'r') as file:
#     for line in file:
#         stripped = line.strip()
#         if stripped == "Channel 0 Data:":
#             reading_ch0 = True
#             reading_ch1 = False
#             continue
#         elif stripped == "Channel 1 Data:":
#             reading_ch1 = True
#             reading_ch0 = False
#             continue
#         elif stripped.startswith("Channel") or stripped == "":
#             continue

#         if reading_ch0 and stripped.isdigit():
#             channel_0.append(int(stripped))
#         elif reading_ch1 and stripped.isdigit():
#             channel_1.append(int(stripped))

# # Apply moving average filter to Channel 1
# window_size = 5  # Adjust as needed
# filtered_ch1 = np.convolve(channel_1, np.ones(window_size)/window_size, mode='valid')

# # Adjust channel_0 to match filtered length
# ch0_for_filtered = channel_0[window_size - 1:]  # Align with filtered_ch1

# # Plotting
# plt.figure(figsize=(12, 8))

# # Subplot 1: Raw Channel 0 and Channel 1
# plt.subplot(2, 1, 1)
# plt.plot(channel_0, label='Channel 0', color='blue', alpha=0.8)
# plt.plot(channel_1, label='Channel 1 (Raw)', color='red', alpha=0.6)
# plt.title('Raw Channel 0 and Channel 1')
# plt.ylabel('Value')
# plt.legend()
# plt.grid(True)

# # Subplot 2: Channel 0 and Filtered Channel 1
# plt.subplot(2, 1, 2)
# plt.plot(ch0_for_filtered, label='Channel 0 (Aligned)', color='blue', alpha=0.8)
# plt.plot(filtered_ch1, label='Channel 1 (Filtered)', color='orange', alpha=0.9)
# plt.title(f'Channel 0 and Moving Avg Filtered Channel 1 (Window = {window_size})')
# plt.xlabel('Sample Index')
# plt.ylabel('Value')
# plt.legend()
# plt.grid(True)

# plt.tight_layout()
# plt.show()


# import numpy as np
# import matplotlib.pyplot as plt
# from scipy.signal import find_peaks

# def read_channels(filepath):
#     with open(filepath, 'r') as f:
#         lines = f.readlines()

#     ch0, ch1 = [], []
#     reading_ch0, reading_ch1 = False, False

#     for line in lines:
#         stripped = line.strip()
#         if stripped == "Channel 0 Data:":
#             reading_ch0 = True
#             reading_ch1 = False
#             continue
#         elif stripped == "Channel 1 Data:":
#             reading_ch1 = True
#             reading_ch0 = False
#             continue
#         elif not stripped.isdigit():
#             continue

#         if reading_ch0:
#             ch0.append(int(stripped))
#         elif reading_ch1:
#             ch1.append(int(stripped))

#     return np.array(ch0), np.array(ch1)

# def add_10_percent_bias(data):
#     mean_val = np.mean(data)
#     biased = np.copy(data)
#     biased[data > mean_val] = data[data > mean_val] * 1.20
#     return biased

# def moving_average(data, window=10):
#     return np.convolve(data, np.ones(window)/window, mode='valid')

# def count_joint_cycles(ch0, ch1_biased, prominence=100, window=50):
#     # Find peaks and troughs in channel 1
#     peaks_ch1, _ = find_peaks(ch1_biased, prominence=prominence)
#     troughs_ch1, _ = find_peaks(-ch1_biased, prominence=prominence)

#     # Pair peaks with next trough
#     cycles = []
#     t_idx = 0
#     for p in peaks_ch1:
#         while t_idx < len(troughs_ch1) and troughs_ch1[t_idx] <= p:
#             t_idx += 1
#         if t_idx >= len(troughs_ch1):
#             break
#         t = troughs_ch1[t_idx]

#         # Check if Channel 0 has significant change in same window
#         segment_ch0 = ch0[p:t] if t > p else ch0[t:p]
#         if len(segment_ch0) < 5:
#             continue

#         diff = np.max(segment_ch0) - np.min(segment_ch0)
#         if diff > 300:  # You can tune this threshold
#             cycles.append((p, t))
#         t_idx += 1

#     return len(cycles), cycles

# # === Run Analysis ===

# file_path = 'breathing_coolterm30_exercise_1.txt'
# ch0, ch1_raw = read_channels(file_path)
# ch1_biased = add_10_percent_bias(ch1_raw)
# ch1_filtered = moving_average(ch1_biased, window=10)

# # Align channel 0 for filtered data
# ch0_aligned = ch0[:len(ch1_filtered)]

# # Count cycles
# # num_cycles, peaks, troughs = count_cycles(ch1_biased)
# num_cycles, cycles = count_joint_cycles(ch0, ch1_biased)


# # === Plotting ===
# plt.figure(figsize=(14, 8))

# # Raw plot
# plt.subplot(2, 1, 1)
# plt.plot(ch0, label='Channel 0 (Chest)', color='blue', alpha=0.7)
# plt.plot(ch1_biased, label='Channel 1 (Temp + 10% Bias)', color='red', alpha=0.5)
# plt.title('Raw Channel 0 and Biased Channel 1')
# plt.ylabel('Signal Value')
# plt.legend()
# plt.grid(True)

# # Filtered plot
# plt.subplot(2, 1, 2)
# plt.plot(ch0_aligned, label='Channel 0 (Chest)', color='blue', alpha=0.7)
# plt.plot(ch1_filtered, label='Filtered Channel 1', color='orange')
# plt.title(f'Filtered Channel 1 (Moving Average) — Estimated Cycles: {num_cycles}')
# plt.xlabel('Sample Index')
# plt.ylabel('Signal Value')
# plt.legend()
# plt.grid(True)

# # Optional: overlay vertical lines for detected cycles
# for p, t in cycles:
#     plt.subplot(2, 1, 1)
#     plt.axvline(p, color='green', linestyle='--', alpha=0.4)
#     plt.axvline(t, color='purple', linestyle='--', alpha=0.4)

#     plt.subplot(2, 1, 2)
#     if p < len(ch0_aligned) and t < len(ch0_aligned):
#         plt.axvline(p, color='green', linestyle='--', alpha=0.4)
#         plt.axvline(t, color='purple', linestyle='--', alpha=0.4)

# plt.tight_layout()
# plt.show()


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
    mean_val = np.mean(data)
    biased = np.copy(data)
    biased[data > mean_val] = biased[data > mean_val] * 1.20
    biased[data <= mean_val] = biased[data <= mean_val] * 0.80
    return biased

def detect_peak_cycles(ch1_smoothed, ch0_smoothed, sample_window=200, ch0_threshold=100):
    # Detect global peaks in Channel 1
    peaks, _ = find_peaks(ch1_smoothed, distance=200, prominence=100)
    save_ch1_peaks = peaks
    cycles = []
    for i in range(len(peaks) - 1):
        p1, p2 = peaks[i], peaks[i+1]
        ch0_segment = ch0_smoothed[max(0, p1-sample_window):min(len(ch0_smoothed), p2+sample_window)]

        if len(ch0_segment) == 0:
            continue

        ch0_range = np.max(ch0_segment) - np.min(ch0_segment)

        if ch0_range >= ch0_threshold:
            cycles.append((p1, p2))

    return cycles, peaks, save_ch1_peaks

# === Main ===

file_path = 'breathing_coolterm30_1.txt'
ch0, ch1 = read_channels(file_path)

# Preprocess Channel 1: Bias then smooth
ch1_biased = add_bias(ch1)
ch1_smoothed = smooth(ch1_biased, window=50)

# Preprocess Channel 0: Smooth for easier range detection
ch0_smoothed = smooth(ch0, window=50)

# Detect cycles
sample_window = 200
ch0_threshold = 100
cycles, all_peaks, ch1_peaks = detect_peak_cycles(ch1_smoothed, ch0_smoothed, sample_window, ch0_threshold)

# Plot
plt.figure(figsize=(14, 8))

# Plot original with smoothed overlay
plt.plot(ch0, label='Channel 0 (Raw)', alpha=0.3, color='blue')
plt.plot(ch0_smoothed, label='Channel 0 (Smoothed)', color='blue')
plt.plot(ch1_biased, label='Channel 1 (Raw + 10% Bias)', alpha=0.3, color='red')
plt.plot(ch1_smoothed, label='Channel 1 (Smoothed)', color='orange')

# Annotate detected peaks and cycles
# for start, end in cycles:
#     plt.axvspan(start, end, color='green', alpha=0.2)
for p in all_peaks:
    plt.axvline(p, linestyle='--', color='grey', alpha=0.8)



plt.title(f"Detected Cycles (Peak-to-Peak) in Channel 1 with Channel 0 Confirmation — Total: {len(cycles)}")
plt.ylabel("Signal Value")
plt.legend()
plt.grid(True)

plt.show()

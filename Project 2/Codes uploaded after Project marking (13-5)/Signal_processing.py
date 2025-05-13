import serial
import time
import matplotlib.pyplot as plt

# Defining variables
reference_voltage = 3.3  # V
threshold_voltage = 1.98  # V
peak_threshold = 10
data_capture = True
sample_size = 2500
signal_list = []

# Set up serial port (replace 'COM6' with your port)
ser = serial.Serial('COM4', 115200, timeout=1)

def voltage_to_adc(voltage):
    return int(voltage * 4096 / reference_voltage)

def adc_to_voltage(adc):
    return adc * reference_voltage / 4096  # FIX: missing return

def signal_capture():
    adc_threshold = voltage_to_adc(threshold_voltage)
    while True:
        try:
            raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
            if not raw_data:
                continue
            adc_value = int(raw_data)
            if (adc_value > adc_threshold and adc_value < 5000):
                # Begin capturing data
                print("begin capturing data")
                signal_list.append(adc_value)
                while len(signal_list) < sample_size:
                    raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if raw_data:
                        try:
                            adc_value = int(raw_data)
                            signal_list.append(adc_value)
                        except ValueError:
                            pass
                voltages = [adc_to_voltage(adc) for adc in signal_list]  # Convert to voltage
                return voltages
        except Exception as e:
            print("Error:", e)

def signal_processing(signal_list):
    # Function used to process the signal and classify it as coin or eraser
    peak_count = 0
    for signal in signal_list:
        if signal > threshold_voltage:
            peak_count+=1

    if peak_count > peak_threshold:
        print("It's a coin") 
    else:
        print("It's an eraser")           
    
    return

def data_collection(num_sets=100):
    adc_threshold = voltage_to_adc(threshold_voltage)

    with open("additionalcoinD10H30.txt", "w") as file:
        for set_index in range(num_sets):
            input(f"Press Enter to start collecting set {set_index + 1}...")  # Wait for Enter key

            collected_data = []
            print(f"Waiting for trigger to start collecting set {set_index + 1}...")

            while True:
                try:
                    raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                    if not raw_data:
                        continue
                    adc_value = int(raw_data)
                    if (adc_value > adc_threshold and adc_value < 5000):
                        print(f"Begin capturing data for set {set_index + 1}")
                        collected_data.append(adc_value)
                        while len(collected_data) < sample_size:
                            raw_data = ser.readline().decode('utf-8', errors='ignore').strip()
                            if raw_data:
                                try:
                                    adc_value = int(raw_data)
                                    collected_data.append(adc_value)
                                except ValueError:
                                    pass
                        break  # Done with one set, break to outer loop
                except Exception as e:
                    print("Error:", e)

            # Write this set to a new line in the file
            file.write(f"Coin D10 H30, Drop number: {set_index + 1}\n")
            file.write(", ".join(str(value) for value in collected_data))
            file.write("\n\n")
            print(f"Finished writing set {set_index + 1}\n")

def main():
    data_collection()

    plot = signal_capture()
    signal_processing(plot)
    plt.plot(plot)
    plt.xlabel("Sample")
    plt.ylabel("Voltage (V)")
    plt.title("Captured Signal")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()

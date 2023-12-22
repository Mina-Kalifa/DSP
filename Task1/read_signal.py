import tkinter as tk
from tkinter import ttk
import numpy as np
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog


class readSignal:

    def open_file_dialog(self):
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        if file_path:
            print("Selected File Path:", file_path)
        return file_path
    
    def clean_and_convert(self, parts):
        cleaned_values = []
        for part in parts:
            cleaned_part = ''.join(filter(lambda x: x.isdigit() or x in ['.', '-'], part))
            cleaned_values.append(cleaned_part)
        return list(map(float, cleaned_values))
    
    def read_signal_file(self, file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        is_periodic = int(lines[0].strip())
        signal_type = int(lines[1].strip())
        n_samples = int(lines[2].strip())

        data = []
        for line in lines[3:]:
            parts = re.split(r'\s|,', line.strip())
            converted_data = self.clean_and_convert(parts)
            data.append(converted_data)
            
        if signal_type == 0:
            indices, amplitudes = zip(*data)
            return signal_type, is_periodic, n_samples, indices, amplitudes
        else:
            amplitudes, phases = zip(*data)
            amplitudes = [round(x,13) for x in amplitudes]
            return signal_type, is_periodic, n_samples, amplitudes, phases


    def convert_to_analog_time_domain(self, indices, amplitudes):
        analog_time = np.linspace(min(indices), max(indices), 1000)
        analog_amplitudes = np.interp(analog_time, indices, amplitudes)

        return analog_time, analog_amplitudes

    def plot_signals(self, indices, amplitudes, plot_frame):

        fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

        ax1.stem(indices, amplitudes, markerfmt='o',
                 linefmt='r-', basefmt='r-')
        ax1.set_ylabel('Amplitude')
        ax1.set_title('Discrete Signal')
        ax1.grid(True)

        analog_time, analog_amplitudes = self.convert_to_analog_time_domain(
            indices, amplitudes)
        ax2.plot(analog_time, analog_amplitudes)
        ax2.set_xlabel('Time')
        ax2.set_ylabel('Amplitude')
        ax2.set_title('Analog Signal')
        ax2.grid(True)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def plot_multiSignals(self, signals, plot_frame):
        max_length = max(len(signal.get("indices", [])) for signal in signals)
        
        fig, axes = plt.subplots(len(signals), 2, sharex=True, sharey='row', gridspec_kw={'hspace': 0.5})

        for i, signal in enumerate(signals):
            indices = signal.get("indices", [])
            amplitudes = signal.get("amplitudes", [])
            label = signal.get("label", f"Signal {i+1}")

            # Pad the signal with zeros if it's shorter than the maximum length
            padded_amplitudes = np.pad(amplitudes, (0, max_length - len(amplitudes)), 'constant')

            ax1, ax2 = axes[i]

            ax1.stem(indices, padded_amplitudes, markerfmt='o', linefmt='r-', basefmt='r-')
            ax1.set_ylabel('Amplitude')
            ax1.set_title(f'Discrete Signal {label}')
            ax1.grid(True)

            analog_time, analog_amplitudes = self.convert_to_analog_time_domain(indices, padded_amplitudes)
            ax2.plot(analog_time, analog_amplitudes)
            ax2.set_xlabel('Time')
            ax2.set_ylabel('Amplitude')
            ax2.set_title(f'Analog Signal {label}')
            ax2.grid(True)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def task1(self):
        file_path = f'{self.open_file_dialog()}'
        app = tk.Tk()
        app.title("Task 1")

        plot_frame = ttk.Frame(app)
        plot_frame.pack(expand=1, fill=tk.BOTH)

        _, _, _, indices, amplitudes = self.read_signal_file(file_path)
        self.plot_signals(indices, amplitudes, plot_frame)

        app.mainloop()

    def draw(self, signals):
        app = tk.Tk()
        app.title("show signal")

        plot_frame = ttk.Frame(app)
        plot_frame.pack(expand=1, fill=tk.BOTH)

        self.plot_multiSignals(signals, plot_frame)

        app.mainloop()

    def SignalSamplesAreEqual(self, file_name, indices, samples):
        expected_indices = []
        expected_samples = []
        with open(file_name, 'r') as f:
            line = f.readline()
            line = f.readline()
            line = f.readline()
            line = f.readline()
            while line:
                L = line.strip()
                if len(L.split(' ')) == 2:
                    L = line.split(' ')
                    V1 = int(L[0])
                    V2 = float(L[1])
                    expected_indices.append(V1)
                    expected_samples.append(V2)
                    line = f.readline()
                else:
                    break

        if len(expected_samples) != len(samples):
            print(
                "Test case failed, your signal have different length from the expected one")
            print("My length: ", len(samples))
            print("original length: ", len(expected_samples))
            return
        for i in range(len(expected_samples)):
            if abs(samples[i] - expected_samples[i]) < 0.01:
                continue
            else:
                print(
                    "Test case failed, your signal have different values from the expected one")
                return
        print("Test case passed successfully")

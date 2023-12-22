import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Generate:
    def generate_discrete_signal(self, waveform, amplitude, phase_shift, analog_frequency, num_samples):
        time_discrete = np.arange(0, num_samples)
        angle = 2 * np.pi * analog_frequency * time_discrete / num_samples + phase_shift

        if waveform == "Sine Wave":
            signal_discrete = amplitude * np.sin(angle)
        elif waveform == "Cosine Wave":
            signal_discrete = amplitude * np.cos(angle)
        else:
            raise ValueError("Unsupported waveform")

        return time_discrete, signal_discrete

    def plot_generated_signal(self, n_sample, signal_discrete, plot_frame):
        fig, ax = plt.subplots(1, 1, sharex=True)

        ax.stem(n_sample, signal_discrete, label='Discrete Signal',
                basefmt=" ", use_line_collection=True)
        ax.set_ylabel('Amplitude')
        ax.set_title('Discrete Signal')
        ax.grid(True)
        ax.legend()

        plt.tight_layout()

        # Print signal values to the console
        # print("Discrete Signal:")
        # print("Time\tAmplitude")
        # for t, amplitude in zip(n_sample, signal_discrete):
        # print(f"{t}\t{amplitude}")

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def task2(self):
        app = tk.Tk()
        app.title("Signal Generator")

        waveform_var = tk.StringVar(value="Cosine Wave")
        amplitude_var = tk.StringVar(value="3.0")
        phase_shift_var = tk.StringVar(value="1.96349540849362")
        analog_frequency_var = tk.StringVar(value="360.0")
        sampling_frequency_var = tk.StringVar(value="720")

        signal_frame = ttk.Frame(app)
        signal_frame.pack(padx=10, pady=10, expand=1, fill=tk.BOTH)

        ttk.Label(signal_frame, text="Waveform:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.W)
        waveform_menu = ttk.Combobox(signal_frame, textvariable=waveform_var, values=[
            "Sine Wave", "Cosine Wave"])
        waveform_menu.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(signal_frame, text="Amplitude:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.W)
        amplitude_entry = ttk.Entry(signal_frame, textvariable=amplitude_var)
        amplitude_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(signal_frame, text="Phase Shift:").grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.W)
        phase_shift_entry = ttk.Entry(
            signal_frame, textvariable=phase_shift_var)
        phase_shift_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(signal_frame, text="Analog Frequency:").grid(
            row=3, column=0, padx=5, pady=5, sticky=tk.W)
        analog_frequency_entry = ttk.Entry(
            signal_frame, textvariable=analog_frequency_var)
        analog_frequency_entry.grid(
            row=3, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(signal_frame, text="Sampling Frequency:").grid(
            row=4, column=0, padx=5, pady=5, sticky=tk.W)
        sampling_frequency_entry = ttk.Entry(
            signal_frame, textvariable=sampling_frequency_var)
        sampling_frequency_entry.grid(
            row=4, column=1, padx=5, pady=5, sticky=tk.W)

        generate_button = ttk.Button(signal_frame, text="Generate Signals",
                                     command=lambda: self.on_generate_discrete_signal(waveform_menu, amplitude_entry,
                                                                                      phase_shift_entry,
                                                                                      analog_frequency_entry,
                                                                                      sampling_frequency_entry, plot_frame))
        generate_button.grid(row=5, column=0, columnspan=2, pady=10)

        plot_frame = ttk.Frame(app)
        plot_frame.pack(padx=10, pady=10, expand=1, fill=tk.BOTH)

        app.mainloop()

    def on_generate_discrete_signal(self, waveform_var, amplitude_var, phase_shift_var, analog_frequency_var, num_samples_var,
                                    plot_frame):
        waveform = waveform_var.get()
        amplitude = float(amplitude_var.get())
        phase_shift = float(phase_shift_var.get())
        analog_frequency = float(analog_frequency_var.get())
        num_samples = int(num_samples_var.get())

        time_discrete, signal_discrete = self.generate_discrete_signal(waveform, amplitude, phase_shift, analog_frequency,
                                                                       num_samples)
        if waveform == "Sine Wave":
            print("in sine")
            self.SignalSamplesAreEqual(
                "Task1\Files\SinOutput.txt", time_discrete, signal_discrete)
        else:
            print("in cosine")
            self.SignalSamplesAreEqual(
                "Task1\Files\CosOutput.txt", time_discrete, signal_discrete)
        self.plot_generated_signal(time_discrete, signal_discrete, plot_frame)

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

import tkinter as tk
import Task1.read_signal as read_signal
import Task4.dft_gui as dft_gui
from Test import signalcompare
import math
import cmath

sampling_frequency_entry = None
signal = read_signal.readSignal()


def write_dfd_result(filename, first_three_lines, amplitude, phase):
    try:
        with open(filename, 'w') as file:
            for line in first_three_lines:
                file.write(str(line) + '\n')

            for a, b in zip(amplitude, phase):
                file.write(f"{a} {b}\n")

        print(f"Data has been written to {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")


def apply_dft():
    global sampling_frequency_entry
    frequency = float(sampling_frequency_entry.get())
    file_path = signal.open_file_dialog()
    _, _, _, _, amp = signal.read_signal_file(file_path)
    amplen = len(amp)
    amplitude = []
    phase = []
    freq = (2 * math.pi * frequency) / len(amp)
    sampling = []
    for i in range(amplen):
        zn = 0
        for j in range(amplen):
            p = (2 * math.pi * i * j) / len(amp)
            z = complex(cmath.cos(p), -1 * cmath.sin(p))
            zn += z * amp[j]
        amplitude.append(round(abs(zn), 13))
        phase.append(round(cmath.phase(zn), 13))
        sampling.append((i + 1) * freq)
    threelines = [0, 1, amplen]
    write_dfd_result('Task4/dft_result.txt', threelines, amplitude, phase)
    _, _, _, outamp, outphase = signal.read_signal_file(signal.open_file_dialog())
    print("out amp: ", outamp)
    print("my amp: ", amplitude)
    print("out phase: ", outphase)
    print("my phase: ", phase)
    test1 = signalcompare.SignalComapreAmplitude(outamp, amplitude)
    test2 = signalcompare.SignalComaprePhaseShift(outphase, phase)
    if test1 and test2:
        print("DFT Test Passed Successfully")
    signals = [
        {"sample": sampling, "amplitudes": amplitude, "label": "DFT_Amplitude"},
        {"sample": sampling, "amplitudes": phase, "label": "DFT_Phase_Shift"}
    ]
    dft_gui.draw(signals)


def DFT():
    global sampling_frequency_entry

    window = tk.Tk()
    window.title("DFT Calculator")

    sampling_frequency_label = tk.Label(window, text="Sampling Frequency (Hz):")
    sampling_frequency_label.pack()
    sampling_frequency_entry = tk.Entry(window)
    sampling_frequency_entry.pack()

    apply_button = tk.Button(window, text="Apply DFT", command=apply_dft)
    apply_button.pack()

    window.mainloop()
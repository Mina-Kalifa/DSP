import tkinter as tk
import Task1.read_signal as read_signal
from Test import comparesignal2
from Task4 import dft
import math
import numpy as np

sampling_num_entry = None
signal = read_signal.readSignal()

def apply_dct():
    global sampling_num_entry
    sam_num = int(sampling_num_entry.get())
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    amplen = len(amp)
    amplitude = []
    signals = []
    for i in range(amplen):
        z = 0
        for j in range (amplen):
            p = amp[j] * math.cos((math.pi/(4*amplen))*(2*j - 1)*(2*i - 1))
            z += p
        z *= math.sqrt(2/amplen)   # sqrt(2/N)* sum( cos( (pi/4N) *2K-1 *2N-1 ))
        amplitude.append(z)
    threelines = [0,1,sam_num]
    dft.write_dfd_result('Task5/dct_result.txt',threelines,ind,amplitude[:sam_num])
    comparesignal2.SignalSamplesAreEqual(signal.open_file_dialog(),amplitude)
    signals.append(
        {"indices": ind, "amplitudes": amp,
         "label": "before DCT"}
    )
    signals.append(
        {"indices": ind, "amplitudes": amplitude,
         "label": "after DCT"}
    )
    signal.draw(signals)

def remove_dc():
    file_path = signal.open_file_dialog()
    signals = []
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    amplen = len(amp)
    amp_mean = np.mean(amp)
    ampn = [x - amp_mean for x in amp]
    threelines = [0,0,amplen]
    dft.write_dfd_result('Task5/dc_removed_result.txt',threelines,ind,ampn)
    comparesignal2.SignalSamplesAreEqual(signal.open_file_dialog(),ampn)
    signals.append(
        {"indices": ind, "amplitudes": amp,
         "label": "with DCT"}
    )
    signals.append(
        {"indices": ind, "amplitudes": ampn,
         "label": "without DCT"}
    )
    signal.draw(signals)


def DCT():
    global sampling_num_entry

    window = tk.Tk()
    window.title("DCT")

    sampling_num_label = tk.Label(window, text="Enter m coffecient")
    sampling_num_label.pack()
    sampling_num_entry = tk.Entry(window)
    sampling_num_entry.pack()

    apply_button = tk.Button(window, text="Apply DCT", command=apply_dct)
    apply_button.pack()

    window.mainloop()
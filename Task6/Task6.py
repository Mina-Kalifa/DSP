import tkinter as tk
from tkinter import ttk
import Task1.read_signal as read_signal
from Test import comparesignal2
from Task4 import dft
from Test import derivative
import math
import cmath
from Test import Shift_Fold_Signal

window_size_entry = None
operation_combo = None
shift_direction_combo = None
shift_entry = None
operation_specific_widgets = []
signal = read_signal.readSignal()


def plot(ind, amp, result, label):
    signals = []
    signals.append(
        {"indices": ind, "amplitudes": amp,
         "label": "A"}
    )
    signals.append(
        {"indices": ind, "amplitudes": result,
         "label": f"{label} result"}
    )
    signal.draw(signals)


def apply_smooth():
    global window_size_entry
    window_size = int(window_size_entry.get())
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    amplen = len(amp)
    amplitude = []
    for i in range(amplen):  # 5--> (0 1 2) 3 4-->5-3
        if i <= amplen - window_size:
            sumelement = sum(amp[i:i + window_size])
            avg = sumelement / window_size
            amplitude.append(avg)
        # else:
         #    amplitude.append(amp[i])
    file_path = signal.open_file_dialog()
    comparesignal2.SignalSamplesAreEqual(file_path,amplitude)
    plot(ind, amp, amplitude, "Smoothing")

def apply_dft(amp):
    # apply dft
    amplen = len(amp)
    comp = []
    for i in range(amplen):
        zn = 0
        for j in range(amplen):
            p = (2 * math.pi * i * j) / len(amp)
            z = complex(cmath.cos(p), -1 * cmath.sin(p))
            zn += z * amp[j]
        comp.append(zn)
    return comp
def remove_dc():
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    comp = apply_dft(amp)
    amplen = len(amp)
    # make first component = 0
    comp[0] = 0
    # apply idft
    xn = 0
    sampling = []
    for i in range(amplen):
        xn = 0
        real = 0
        compl = 0
        for j in range(amplen):
            p = (2 * math.pi * j * i) / amplen
            z = complex(cmath.cos(p), cmath.sin(p))
            zn = z * complex(comp[j].real, comp[j].imag)
            real += zn.real
            compl += zn.imag
        xn = real + compl
        xn /= amplen
        sampling.append(xn)
    dft.write_dfd_result('dct_removedresulttime.txt', [0,0,amplen], ind, sampling)
    comparesignal2.SignalSamplesAreEqual(signal.open_file_dialog(),sampling)
    plot(ind, amp, sampling, "DC Removed")


def apply_shift():
    global shift_direction_combo, shift_entry
    shiftval = int(shift_entry.get())
    selected_type = shift_direction_combo.get()
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals = []
    signals.append(
        {"indices": ind, "amplitudes": amp,
         "label": "A"}
    )
    if selected_type == "Delay":
        result = [a + shiftval for a in ind]
        signals.append(
            {"indices": result, "amplitudes": amp,
             "label": f"A Delay by {shiftval}"}
        )
    elif selected_type == "advancing":
        result = [a - shiftval for a in ind]
        signals.append(
            {"indices": result, "amplitudes": amp,
             "label": f"A advancing by {shiftval}"}
        )
    file_path = signal.open_file_dialog()
    signal.SignalSamplesAreEqual(file_path, result, amp)
    signal.draw(signals)


def apply_folding():
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals = []
    signals.append(
        {"indices": ind, "amplitudes": amp,
         "label": "A"}
    )
    result = list(reversed(amp))
    signals.append(
        {"indices": ind, "amplitudes": result,
         "label": f"A After Folding"}
    )
    file_path = signal.open_file_dialog()
    comparesignal2.SignalSamplesAreEqual(file_path, result)
    signal.draw(signals)


def folding_shift():
    global shift_direction_combo, shift_entry
    shiftval = int(shift_entry.get())
    selected_type = shift_direction_combo.get()
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals = []
    signals.append(
        {"indices": ind, "amplitudes": amp,
         "label": "A"}
    )
    res = list(reversed(amp))
    if selected_type == "Delay":
        result = [a + shiftval for a in ind]
        signals.append(
            {"indices": result, "amplitudes": res,
             "label": f"A Delay by {shiftval}"}
        )
    elif selected_type == "advancing":
        result = [a - shiftval for a in ind]
        signals.append(
            {"indices": result, "amplitudes": res,
             "label": f"A advancing by {shiftval}"}
        )
    file_path = signal.open_file_dialog()
    Shift_Fold_Signal.Shift_Fold_Signal(file_path,result,res)
    signal.draw(signals)


def handle_operation_selection(*args):
    global window_size_entry, operation_combo, form, operation_specific_widgets, shift_direction_combo, shift_entry
    selected_operation = operation_combo.get()

    for widget in operation_specific_widgets:
        widget.destroy()

    if selected_operation == "Smoothing":
        window_size_label = ttk.Label(form, text="Enter Window Size:")
        window_size_label.grid(column=0, row=1, sticky=tk.W, pady=5)

        window_size_entry = ttk.Entry(form)
        window_size_entry.grid(column=1, row=1, pady=5)

        operation_specific_widgets.extend(
            [window_size_label, window_size_entry])

    elif selected_operation == "Delay or advancing" or selected_operation == "Folding With shiftting":
        shift_label = ttk.Label(form, text="Enter Shift Value:")
        shift_label.grid(column=0, row=2, sticky=tk.W, pady=5)

        shift_entry = ttk.Entry(form)
        shift_entry.grid(column=1, row=2, pady=5)

        shift_direction_label = ttk.Label(form, text="Select Shift type:")
        shift_direction_label.grid(column=0, row=3, sticky=tk.W, pady=5)

        shift_direction_combo = ttk.Combobox(form, values=["Delay", "advancing"])
        shift_direction_combo.grid(column=1, row=3, pady=5)

        operation_specific_widgets.extend([shift_label, shift_entry, shift_direction_label, shift_direction_combo])


def plot_resulting_signal():
    selected_operation = operation_combo.get()
    if selected_operation == "Smoothing":
        apply_smooth()
    elif selected_operation == "Sharpening":
        derivative.DerivativeSignal()
    elif selected_operation == "Delay or advancing":
        apply_shift()
    elif selected_operation == "Remove DC":
        remove_dc()
    elif selected_operation == "Folding":
        apply_folding()
    elif selected_operation == "Folding With shiftting":
        folding_shift()



def time_domain():
    global window_size_entry, operation_combo, form, operation_specific_widgets, shift_direction_combo, shift_entry
    root = tk.Tk()
    root.title("Time Domain")
    form = ttk.Frame(root, padding="20")
    form.grid()
    operation_label = ttk.Label(form, text="Operation:")
    operation_label.grid(column=0, row=0, sticky=tk.W, pady=5)
    operation_combo = ttk.Combobox(form,
                                   values=["Smoothing", "Sharpening", "Delay or advancing", "Remove DC", "Folding",
                                           "Folding With shiftting"])
    operation_combo.grid(column=1, row=0, pady=5)
    operation_combo.bind("<<ComboboxSelected>>", handle_operation_selection)
    plot_button = ttk.Button(
        form, text="Plot resulting signal", command=plot_resulting_signal)
    plot_button.grid(column=0, row=4, columnspan=2, pady=10)
    root.mainloop()
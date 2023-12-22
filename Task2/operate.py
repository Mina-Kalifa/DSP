import Task1.read_signal as read_signal
import tkinter as tk
from tkinter import ttk
import numpy as np
from Test import test2 as test2

num_signals_entry = None
normalization_var = None
constant_entry = None
shift_entry = None
operation_combo = None
form = None
signal = read_signal.readSignal()
operation_specific_widgets = []

letters = ['A', 'B', 'C', 'D', 'E']


def addSignal(num_signals):
    alldata1 = []
    alldata2 = []
    signals = []
    max_length = 0
    for i in range(num_signals):
        file_path = signal.open_file_dialog()
        _, _, _, ind, amp = signal.read_signal_file(file_path)
        alldata1.append(ind)
        alldata2.append(amp)
        signals.append(
            {"indices": ind, "amplitudes": amp,
                "label": f"{letters[i]}"}
        )
        max_length = max(max_length, len(amp))
    for i in range(num_signals):
        if len(alldata2[i]) < max_length:
            alldata2[i] += [0] * (max_length - len(alldata2[i]))
            result1 =  alldata1[i]
    result1 = alldata1[0]
    result2 = [sum(x) for x in zip(*alldata2)]
    signals.append(
        {"indices": result1, "amplitudes": result2,
            "label": "Addition result"}
    )
    return result1, result2, signals


def subSignal():
    alldata1 = []
    alldata2 = []
    signals = []
    max_length = 0
    for i in range(2):
        file_path = signal.open_file_dialog()
        _, _, _, ind, amp = signal.read_signal_file(file_path)
        alldata1.append(ind)
        alldata2.append(amp)
        signals.append(
            {"indices": ind, "amplitudes": amp,
                "label": f"{letters[i]}"}
        )

        max_length = max(max_length, len(amp))
    for i in range(2):
        if len(alldata2[i]) < max_length:
            alldata2[i] += [0] * (max_length - len(alldata2[i]))

    result1 = alldata1[0]
    result2 = [abs(a - b) for a, b in zip(alldata2[1], alldata2[0])]
    signals.append(
        {"indices": result1, "amplitudes": result2,
            "label": "Subtracion result"}
    )
    return result1, result2, signals


def multiply(constant):
    signals = []
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals.append(
        {"indices": ind, "amplitudes": amp,
            "label": "A"}
    )
    result = [a * constant for a in amp]
    signals.append(
        {"indices": ind, "amplitudes": result,
            "label": f"A * {constant} "}
    )
    return ind, result, signals


def square():
    signals = []
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals.append(
        {"indices": ind, "amplitudes": amp,
            "label": "A"}
    )
    result = [a * a for a in amp]
    signals.append(
        {"indices": ind, "amplitudes": result,
            "label": f"A Square"}
    )
    return ind, result, signals


def normSignal(normalization_range):
    signals = []
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals.append(
        {"indices": ind, "amplitudes": amp,
            "label": "A"}
    )
    min_value = np.min(amp)
    max_value = np.max(amp)

    if normalization_range == '0to1':
        normalized_0to1 = (amp - min_value) / (max_value - min_value)
        signals.append(
            {"indices": ind, "amplitudes": normalized_0to1,
             "label": "Normalize from 0 to 1"}
        )
        return ind, normalized_0to1, signals
    elif normalization_range == '-1to1':
        normalized_minus1to1 = (
            (2 * (amp - min_value)) / max_value - min_value) - 1
        signals.append(
            {"indices": ind, "amplitudes": normalized_minus1to1,
             "label": "Normalize from -1 to 1"}
        )
        return ind, normalized_minus1to1, signals


def shiftSignal(shift_value):
    signals = []
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals.append(
        {"indices": ind, "amplitudes": amp,
         "label": "A"}
    )
    result = [a - shift_value for a in ind]
    signals.append(
        {"indices": result, "amplitudes": amp,
         "label": f"A shift by {shift_value}"}
    )
    return result, amp, signals


def accumSignal():
    signals = []
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals.append(
        {"indices": ind, "amplitudes": amp,
         "label": "A"}
    )
    result = np.cumsum(amp)
    signals.append(
        {"indices": ind, "amplitudes": result,
         "label": f"Accumulation result"}
    )
    return ind, result, signals


def task3(result1, result2, signals):
    print("Discrete Signal:")
    print("Time\tAmplitude")
    for t, amplitude in zip(result1, result2):
        print(f"{t}\t{amplitude}")
    outFile_path = signal.open_file_dialog()
    signal.SignalSamplesAreEqual(outFile_path, result1, result2)
    signal.draw(signals)


def handle_operation_selection(*args):
    global num_signals_entry, normalization_var, constant_entry, shift_entry, operation_combo, form, operation_specific_widgets
    selected_operation = operation_combo.get()

    for widget in operation_specific_widgets:
        widget.destroy()

    if selected_operation == "Addition":
        num_signals_label = ttk.Label(form, text="Number of Signals to Add:")
        num_signals_label.grid(column=0, row=1, sticky=tk.W, pady=5)

        num_signals_entry = ttk.Entry(form)
        num_signals_entry.grid(column=1, row=1, pady=5)

        operation_specific_widgets.extend(
            [num_signals_label, num_signals_entry])

    elif selected_operation == "Normalization":
        normalization_label = ttk.Label(form, text="Normalization Range:")
        normalization_label.grid(column=0, row=1, sticky=tk.W, pady=5)

        normalization_var = ttk.Combobox(
            form, values=["0to1", "-1to1"], state="readonly")
        normalization_var.grid(column=1, row=1, pady=5)

        operation_specific_widgets.extend(
            [normalization_label, normalization_var])

    elif selected_operation == "Multiplication":
        constant_label = ttk.Label(form, text="Signal * ")
        constant_label.grid(column=0, row=1, sticky=tk.W, pady=5)

        constant_entry = ttk.Entry(form)
        constant_entry.grid(column=1, row=1, pady=5)

        operation_specific_widgets.extend(
            [constant_label, constant_entry])

    elif selected_operation == "Shifting":
        shift_label = ttk.Label(form, text="shift by: ")
        shift_label.grid(column=0, row=1, sticky=tk.W, pady=5)

        shift_entry = ttk.Entry(form)
        shift_entry.grid(column=1, row=1, pady=5)

        operation_specific_widgets.extend(
            [shift_label, shift_entry])


def plot_resulting_signal():
    selected_operation = operation_combo.get()
    if selected_operation == "Addition":
        num_signals = int(num_signals_entry.get())
        result1, result2, signals = addSignal(num_signals)
        task3(result1, result2, signals)

    elif selected_operation == "Normalization":
        normalization_range = normalization_var.get()
        result1, result2, signals = normSignal(normalization_range)
        task3(result1, result2, signals)

    elif selected_operation == "Subtraction":
        result1, result2, signals = subSignal()
        task3(result1, result2, signals)

    elif selected_operation == "Multiplication":
        constant = int(constant_entry.get())
        result1, result2, signals = multiply(constant)
        task3(result1, result2, signals)

    elif selected_operation == "Squaring":
        result1, result2, signals = square()
        task3(result1, result2, signals)

    elif selected_operation == "Shifting":
        shift = int(shift_entry.get())
        result1, result2, signals = shiftSignal(shift)
        task3(result1, result2, signals)

    elif selected_operation == "Accumulation":
        result1, result2, signals = accumSignal()
        task3(result1, result2, signals)


def operateSignal():
    global num_signals_entry, normalization_var, constant_entry, shift_entry, operation_combo, form, operation_specific_widgets
    root = tk.Tk()
    root.title("Operations")
    form = ttk.Frame(root, padding="20")
    form.grid()
    operation_label = ttk.Label(form, text="Operation:")
    operation_label.grid(column=0, row=0, sticky=tk.W, pady=5)
    operation_combo = ttk.Combobox(form, values=["Addition", "Subtraction", "Multiplication", "Squaring",
                                                 "Shifting", "Normalization", "Accumulation"])
    operation_combo.grid(column=1, row=0, pady=5)
    operation_combo.bind("<<ComboboxSelected>>", handle_operation_selection)
    plot_button = ttk.Button(
        form, text="Plot resulting signal", command=plot_resulting_signal)
    plot_button.grid(column=0, row=2, columnspan=2, pady=10)
    root.mainloop()

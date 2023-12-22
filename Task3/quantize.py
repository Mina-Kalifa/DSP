import tkinter as tk
import math
from tkinter import ttk
import Task1.read_signal as read_signal
from Test import QuanTest1
from Test import QuanTest2

levels_combo = None
input_entry = None

signal = read_signal.readSignal()


def calLevels(mini, maxi, delta, value):
    arr = []
    interval = []
    midpoint = []
    newmini = mini
    mid = 0
    for i in range(value):
        arr.append(newmini)  # 2 7 7 12
        mid = newmini
        newmaxi = newmini + delta
        mid += newmaxi
        midpoint.append(mid/2)
        arr.append(newmaxi)
        newmini = newmaxi
        interval.append(arr)
        arr = []
    print("intervals ", interval)
    return interval, midpoint


def replace_points(midpoint, amplituie, intervals):
    newamp = []
    error = []
    index = []
    encode = []
    bits = math.ceil(math.log(len(midpoint), 2))
    for amp in amplituie:
        for interval in intervals:
            if amp >= round(interval[0], 3) and amp <= round(interval[1], 3):
                j = intervals.index(interval)
                newamp.append(midpoint[j])
                error.append(midpoint[j]-amp)
                index.append(j+1)
                binary_ind = bin(j)[2:]
                zeros_to_add = max(0, bits - len(binary_ind))
                expanded_binary = '0' * zeros_to_add + binary_ind
                encode.append(expanded_binary)
                break
    return index, encode, newamp, error


def readfile(value):
    signals = []
    file_path = signal.open_file_dialog()
    _, _, _, ind, amp = signal.read_signal_file(file_path)
    signals.append(
    {"indices": ind, "amplitudes": amp,
     "label": "Input"}
    )
    mini = min(amp)
    maxi = max(amp)
    delta = round((maxi - mini) / value, 2)
    intervals, midpoint = calLevels(mini, maxi, delta, value)
    index, expanded_binary, newamp, error = replace_points(
        midpoint, amp, intervals)
    signals.append(
    {"indices": ind, "amplitudes": newamp,
     "label": "Quantized"}
    )
    fileOut_path = signal.open_file_dialog()
    print("quantize: ", newamp)
    print("error: ", error)
    print("encoding: ", expanded_binary)
    print('File path used: ',fileOut_path)
    if fileOut_path == 'D:/DSP/Task3/Files/Quan1_Out.txt':
        print('in File 1 path.....................................')
        QuanTest1.QuantizationTest1(fileOut_path, expanded_binary, newamp)
    elif fileOut_path == 'D:/DSP/Task3/Files/Quan1_Out.txt':
        QuanTest2.QuantizationTest2(
            fileOut_path, index, expanded_binary, newamp, error)
    return amp,newamp,error,expanded_binary,signals


def display_table(amp,newamp,error,expanded_binary,signals):
    root = tk.Tk()
    root.title("Quantize Table")

    tree = ttk.Treeview(root, columns=('Encoding','input','Quantize', 'Error'))
    tree.heading('#0', text='Index')
    tree.heading('Encoding', text='Encoding')
    tree.heading('input', text='input')
    tree.heading('Quantize', text='Quantize')
    tree.heading('Error', text='Error')
    

    tree.column('#0', width=50)
    tree.column('Encoding', anchor=tk.CENTER, width=150)
    tree.column('input', anchor=tk.CENTER, width=150)
    tree.column('Quantize', anchor=tk.CENTER, width=150)
    tree.column('Error', anchor=tk.CENTER, width=150)
    

    for index in range(len(newamp)):
        tree.insert('', 'end', text=str(index), values=(f"{expanded_binary[index]}", f"{amp[index]}", f"{newamp[index]}", f"{error[index]}"))
    
    tree.pack()
    signal.draw(signals)
    root.mainloop()
    


def compute():
    global levels_combo, input_entry
    level = levels_combo.get()
    value = int(input_entry.get())
    print("Selected Level:", level)
    print("Input Value:", value)
    if level == 'bit':
        value = pow(2, value)
    amp,newamp,error,expanded_binary,signals = readfile(value)
    display_table(amp,newamp,error,expanded_binary,signals)


def quantize_form():
    global levels_combo, input_entry
    root = tk.Tk()
    root.title("Compute Form")

    form = ttk.Frame(root, padding="20")
    form.grid()

    levels_label = ttk.Label(form, text="Levels/Bits:")
    levels_label.grid(column=0, row=0, sticky=tk.W, pady=5)

    levels_combo = ttk.Combobox(form, values=["level", "bit"])
    levels_combo.grid(column=1, row=0, pady=5)

    input_label = ttk.Label(form, text="Input:")
    input_label.grid(column=0, row=1, sticky=tk.W, pady=5)

    input_entry = ttk.Entry(form)
    input_entry.grid(column=1, row=1, pady=5)

    compute_button = ttk.Button(form, text="Compute", command=compute)
    compute_button.grid(column=0, row=2, columnspan=2, pady=10)

    root.mainloop()

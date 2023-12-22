import tkinter as tk
from tkinter import ttk
import Task1.read_signal as read_signal
from Task4 import dft_gui
from Test import signalcompare
import cmath
import math

signal = read_signal.readSignal()


def calc_idft(comp, amplen):
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
        sampling.append(round(xn, 1))
    return sampling


def apply_idft(swit=True, phaseshift=[0], amplitute=[0]):
    if (swit):
        file_path = signal.open_file_dialog()
        _, _, _, amp, phase = signal.read_signal_file(file_path)
    else:
        amp = amplitute
        phase = phaseshift
    comp = []
    for i in range(len(amp)):
        z = complex(amp[i] * cmath.cos((phase[i])), amp[i] * cmath.sin((phase[i])))
        comp.append(z)

    amplen = len(amp)
    xn = 0
    sampling = []
    sampling = calc_idft(comp, amplen)
    indices = list(range(len(sampling)))
    print(sampling)
    if (swit):
        _, _, _, outind, outamp = signal.read_signal_file(signal.open_file_dialog())
        test1 = signalcompare.SignalComapreAmplitude(outind, indices)
        test2 = signalcompare.SignalComaprePhaseShift(outamp, sampling)
        if test1 and test2:
            print("Test Passed Successfully")
    dft_gui.plot_idft(indices, sampling)


def create_gui():
    app = tk.Tk()
    app.title("IDFT Application")

    frame = ttk.Frame(app)
    frame.pack(padx=20, pady=20)

    idft_button = ttk.Button(frame, text="Apply IDFT", command=apply_idft)
    idft_button.pack()

    app.mainloop()
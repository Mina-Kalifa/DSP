import Task1.read_signal as read_signal
import Task2.operate as operate
import Task1.generate as generate
import Task3.quantize as quantize
import Task4.dft as dft
import Task4.idft as idft
import Task5.dct as dct
import Task6.Task6 as Task6
import Task7.Convolution as Convolution
import Task9.FastConv as FastConv
import Task9.FastCorr as FastCorr
import tkinter as tk
import Task8.correlation as correlation
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import filedialog

signal = read_signal.readSignal()

gen = generate.Generate()


def open_task1():
    signal.task1()


def open_task2():
    gen.task2()


app = tk.Tk()
app.title("Task Selector")

ttk.Button(app, text="Show Signal", command=open_task1).pack(pady=10)
ttk.Button(app, text="Generate Signal", command=open_task2).pack(pady=10)
ttk.Button(app, text="Operate on Signals",
           command=operate.operateSignal).pack(pady=10)
ttk.Button(app, text="Quantize",
           command=quantize.quantize_form).pack(pady=10)
ttk.Button(app, text="dft",
           command=dft.DFT).pack(pady=10)
ttk.Button(app, text="idft",
           command=idft.create_gui).pack(pady=10)
ttk.Button(app, text="dct",
           command=dct.DCT).pack(pady=10)
ttk.Button(app, text="remove_dc",
           command=dct.remove_dc).pack(pady=10)
ttk.Button(app, text="Time Domain",
           command=Task6.time_domain).pack(pady=10)
ttk.Button(app, text="Convolution",
           command=Convolution.Convolution).pack(pady=10)
ttk.Button(app, text="Correlation",
           command = correlation.Correlation).pack(pady=10)
ttk.Button(app, text="Fast Convolution",
           command = FastConv.fastConv).pack(pady=10)
ttk.Button(app, text="Fast Auto Correlation",
           command = FastCorr.auto_fast_Corr).pack(pady=10)
ttk.Button(app, text="Fast Cross Correleation",
           command = FastCorr.fast_Corr).pack(pady=10)
app.mainloop()

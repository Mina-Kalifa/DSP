import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Task1.read_signal as read_signal
from Task4 import idft
from Task4 import dft

labeled = ["Amplitudes","Phase"]
signal = read_signal.readSignal()
def plot_multiSignals(signals, plot_frame):
    num_signals = len(signals)
    fig, axes = plt.subplots(num_signals, 1, sharex=True)

    for i, signal in enumerate(signals):
        amplitudes = signal["sample"]
        phase = signal["amplitudes"]
        label = signal["label"]

        ax1 = axes[i]

        ax1.stem(amplitudes, phase, markerfmt='o',
                 linefmt='r-', basefmt='r-')
        ax1.set_ylabel(f'{labeled[i]}')
        ax1.set_title(f'Discrete Signal {label}')
        ax1.grid(True)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
def upd(ind,newamp,newphase,amp,pha):
    oldamp = amp[ind]
    oldphase = pha[ind]
    for i in range (len(amp)):
        if amp[i] == oldamp :
            amp[i] = newamp
        if abs(pha[i]) == abs(oldphase):
            if(pha[i]>0):
                pha[i] = newphase
            else :
                pha[i] = -1 *newphase
    return amp , pha


def draw(signals):
    app = tk.Tk()
    app.title("Show Signal")

    plot_frame = ttk.Frame(app)
    plot_frame.pack(expand=1, fill=tk.BOTH)

    plot_multiSignals(signals, plot_frame)

    label = ttk.Label(app, text="Modify Amplitudes")
    label.pack()

    entry_frame = ttk.Frame(app)
    entry_frame.pack()

    label1 = ttk.Label(entry_frame, text="index:")
    label1.pack(side=tk.LEFT)
    textbox1 = ttk.Entry(entry_frame)
    textbox1.pack(side=tk.LEFT)

    label2 = ttk.Label(entry_frame, text="new amplitude ")
    label2.pack(side=tk.LEFT)
    textbox2 = ttk.Entry(entry_frame)
    textbox2.pack(side=tk.LEFT)

    label3 = ttk.Label(entry_frame, text="new phase ")
    label3.pack(side=tk.LEFT)
    textbox3 = ttk.Entry(entry_frame)
    textbox3.pack(side=tk.LEFT)

    button = ttk.Button(app, text="Convert", command=lambda: on_convert_button_click(textbox1.get(), textbox2.get(), textbox3.get(),signals))
    button.pack()

    def on_convert_button_click(text1, text2, text3,signals):
        if not text1:
            print("Enter value to modified")
        else:
            index = int(text1)
            amp = float(text2)
            phase = float(text3)
            amplitute = signals[0]["amplitudes"]
            phaseshift = signals[1]["amplitudes"]
            ampli,phasesh = upd(index,amp,phase,amplitute,phaseshift)
            threelines = [0,1,len(amplitute)]
            dft.write_dfd_result('dfdresult.txt',threelines,ampli,phasesh)
            idft.apply_idft(False,phasesh,ampli)

    app.mainloop()

def plot_idft(indices,amplitudes):
    app = tk.Tk()
    app.title("Task 1")

    plot_frame = ttk.Frame(app)
    plot_frame.pack(expand=1, fill=tk.BOTH)
    signal.plot_signals(indices, amplitudes, plot_frame)

    app.mainloop()
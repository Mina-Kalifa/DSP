import tkinter as tk
import Task1.read_signal as read_signal
from tkinter import ttk
from Test import ConvTest
signal = read_signal.readSignal()

def plot_conv(indices,amplitudes):
    app = tk.Tk()
    app.title("Convolution")

    plot_frame = ttk.Frame(app)
    plot_frame.pack(expand=1, fill=tk.BOTH)
    signal.plot_signals(indices, amplitudes, plot_frame)
    app.mainloop()
    
def Convolution():
    file_path = signal.open_file_dialog()
    _, _, _, ind1, amp1 = signal.read_signal_file(file_path)
    amplen1 = len(amp1)
    file_path = signal.open_file_dialog()
    _, _, _, ind2, amp2 = signal.read_signal_file(file_path)
    amplen2 = len(amp2)
    sumofindices = amplen1+amplen2-1  # 4 + 6 - 1 = 9
    y = []
    mini = int(ind1[0]+ind2[0])
    maxi = int(ind1[-1]+ind2[-1])
    indices = list(range(mini,maxi+1))
    for n in range(sumofindices): #4
        summation = 0
        for k in range(n+1): #0 1
            if k < amplen1 and (n-k) < amplen2:
                # print("index of n is ",n)
                # print("index of k is ", k)
                summation += amp1[k] * amp2[n - k]  # 04 13 22 31
        y.append(summation)
    print(indices)
    print(y)
    ConvTest.ConvTest(indices,y)
    plot_conv(indices,y)
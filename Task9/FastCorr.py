import Task1.read_signal as read_signal
import numpy as np
import Task6.Task6 as Task6
from Task4 import idft
from Test import CompareSignalFinal
import Task7.Convolution as Convolution
signal = read_signal.readSignal()

def auto_fast_Corr():
    file_path = signal.open_file_dialog()
    _, _, _, ind1, amp1 = signal.read_signal_file(file_path)
    # to test
    # amp1 = [1,0,0,1]
    amplen = len(amp1)
    amp1_dft = Task6.apply_dft(amp1)
    conj_amp1 = np.conjugate(amp1_dft)
    finalArray = []
    for n in range(amplen):
        zn  = amp1_dft[n]*conj_amp1[n]
        finalArray.append(zn)
    finalResult = idft.calc_idft(finalArray,amplen)
    finalResult = [x/amplen for x in finalResult]
    print(finalResult)

def fast_Corr():
    file_path = signal.open_file_dialog()
    _, _, _, ind1, amp1 = signal.read_signal_file(file_path)
    amplen1 = len(amp1)
    file_path = signal.open_file_dialog()
    _, _, _, ind2, amp2 = signal.read_signal_file(file_path)
    amplen2 = len(amp2)

    amp1_dft = Task6.apply_dft(amp1)
    amp2_dft = Task6.apply_dft(amp2)
    conj_amp1 = np.conjugate(amp1_dft)
    finalArray = []
    for n in range(len(amp1_dft)):
        zn  = conj_amp1[n]*amp2_dft[n]
        finalArray.append(zn)
    finalResult = []
    amp1len = len(amp1_dft)
    finalResult = idft.calc_idft(finalArray,len(amp1_dft))
    finalResult = [x/amp1len for x in finalResult]
    indi = list(range(len(finalResult)))
    print(indi)
    print(finalResult)
    file_path = signal.open_file_dialog()
    CompareSignalFinal.Compare_Signals(file_path,indi,finalResult)
    Convolution.plot_conv(indi,finalResult)
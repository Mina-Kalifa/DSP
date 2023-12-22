import Task1.read_signal as read_signal
from Test import ConvTest
import Task6.Task6 as Task6
from Task4 import idft
import Task7.Convolution as Convolution
signal = read_signal.readSignal()

def fastConv():
    file_path = signal.open_file_dialog()
    _, _, _, ind1, amp1 = signal.read_signal_file(file_path)
    amplen1 = len(amp1)
    file_path = signal.open_file_dialog()
    _, _, _, ind2, amp2 = signal.read_signal_file(file_path)
    amplen2 = len(amp2)
    newSignal = amplen1 + amplen2 -1
    newamp1 = []
    newamp2 = []
    for i in range(newSignal):
        if i>=amplen1:
            newamp1.append(0)
        elif i<amplen1:
            newamp1.append(amp1[i])
        if i>=amplen2:
            newamp2.append(0)
        elif i<amplen2:
            newamp2.append(amp2[i])
    amp1_dft = Task6.apply_dft(newamp1)
    amp2_dft = Task6.apply_dft(newamp2)
    finalArray = []
    for n in range(newSignal):
        zn  = amp1_dft[n]*amp2_dft[n]
        finalArray.append(zn)
    finalResult = []
    finalResult = idft.calc_idft(finalArray,newSignal)
    mini = ind1[0]+ind2[0]
    maxi = ind1[-1]+ind2[-1]
    indi = list(range(int(mini),int(maxi+1)))
    print(indi)
    print(finalResult)
    ConvTest.ConvTest(indi,finalResult)
    Convolution.plot_conv(indi,finalResult)
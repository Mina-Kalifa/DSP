import Task1.read_signal as read_signal
import math
from Test import CompareSignal
import Task7.Convolution as Convolution
signal = read_signal.readSignal()

def Correlation():
    file_path = signal.open_file_dialog()
    _, _, _, ind1, amp1 = signal.read_signal_file(file_path)
    amplen1 = len(amp1)
    file_path = signal.open_file_dialog()
    _, _, _, ind2, amp2 = signal.read_signal_file(file_path)
    amplen2 = len(amp2)
    # calculate r12, sumX1square and sumX2square
    r = []
    sumX1square = 0
    sumX2square = 0
    for j in range(amplen1):#4
        summation = 0
        for n in range(amplen2):#4
            summation += amp1[n]*amp2[(n+j)%amplen2]
        r.append(summation/amplen1)
        sumX1square+=(amp1[j]*amp1[j])
        sumX2square+=(amp2[j]*amp2[j])
    det = math.sqrt(sumX1square*sumX2square)/amplen1

    #calculate P12
    p12 = []
    for n in range(amplen1):
        p12.append(r[n]/det)
    file_path = signal.open_file_dialog()
    CompareSignal.Compare_Signals(file_path,ind1,p12)
    print(p12)
    Convolution.plot_conv(ind1,p12)
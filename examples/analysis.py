import numpy as np

from scipy.signal import argrelextrema
#import scipy.integrate as integrate
#import scipy.special as special
#from scipy.integrate import odeint
#from scipy.constants import constants as const
from scipy.fftpack import fft, fftfreq

import matplotlib.pyplot as plt

import stlab
import glob

from rcsj.utils.rcsj_iv import testplot


##################
##################

pathlist = glob.glob('../simresults/*')
pathlist.sort()
data = stlab.readdata.readdat(pathlist[-1])
#data = [stlab.readdata.readdat(path) for path in pathlist]

freq = []
volt_fft = []
current = []
for line in data:
    time = line['Time (wp*t)']
    voltage = line['AC Voltage (V)']
    current.append(line['Current (Ic)'][0])
    #testplot(time,voltage)
    
    F = fftfreq(len(time), d=time[1]-time[0])
    F = F[:len(F)//2]

    signal_fft = fft(voltage)
    signal_fft = signal_fft[:len(signal_fft)//2]
    #testplot(F,abs(signal_fft))
    
    freq.append(F)
    volt_fft.append(abs(signal_fft))
freq=np.asarray(freq)
volt_fft = np.asarray(volt_fft)

fig, ax = plt.subplots()    
#ax.imshow(np.log(volt_fft),aspect='auto',cmap='magma')
ax.imshow(volt_fft,aspect='auto',cmap='inferno_r',clim=(1,100))
ax.set_xlim(0,1400)
ax.set_yticks(np.arange(0,len(data),50))
ax.set_yticklabels(current[0::50])
plt.show()
plt.close()



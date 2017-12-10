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

from rcsj.utils.funcs import testplot, critical_currents
from rcsj.utils.rcsj_iv import rcsj_iv

##################
##################

currents = np.arange(0.,2.005,0.005)
all_currents = np.concatenate([currents[:-1],currents[::-1]])
time = np.arange(0,500,0.01)

qs = np.logspace(-2,2,401)
ts = [0.8]*len(qs)
iv = [rcsj_iv(all_currents,time,Q=qq,tsamp=tt,svpng=False,saveiv=True) for qq,tt in zip(qs,ts)]


'''
# by loading data
pathlist = glob.glob('../simresults/*')
pathlist.sort()
data = stlab.readdata.readdat(pathlist[-1])

current = []
voltage = []
for line in data:
	current.append(line['Current (Ic)'][0])
	voltage.append(line['DC Voltage (V)'][0])

current = np.asarray(current)
voltage = np.asarray(voltage)

iswitch, iretrap = critical_currents(current,voltage)
'''
import numpy as np

from scipy.signal import argrelextrema
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

qs = np.logspace(-2,2,41)
times = []
ts = []
for Q in qs:
	if Q < 0.1:
		times.append(np.arange(0,4000,0.01))
		ts.append(0.8)
	elif Q < 1.:
		times.append(np.arange(0,1000,0.01))
		ts.append(0.8)
	elif Q < 10.:
		times.append(np.arange(0,500,0.01))
		ts.append(5e-2)
	elif Q < 100.:
		times.append(np.arange(0,500,0.01))
		ts.append(1e-2)
	else:
		times.append(np.arange(0,200,0.01))
		ts.append(1e-4)

iv = [rcsj_iv(all_currents,time,Q=qq,tsamp=tt,normalized=True) for qq,tt,time in zip(qs,ts,times)]
iswitch, ireturn = [], []
for data in iv:
	y = critical_currents(data[0],data[1])
	iswitch.append(y[0])
	ireturn.append(y[1])
iswitch, ireturn = np.asarray(iswitch), np.asarray(ireturn)

data2save = (qs, iswitch, ireturn)
np.savetxt('../simresults/hysteresis.dat',data2save)

testplot(qs,ireturn,scale=('log','log'))

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
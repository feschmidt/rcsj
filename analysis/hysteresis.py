import numpy as np

from scipy.signal import argrelextrema
from scipy.fftpack import fft, fftfreq

import matplotlib.pyplot as plt

import stlab
import glob

from rcsj.utils.funcs import testplot, critical_currents, savestlab
from rcsj.utils.rcsj_iv import rcsj_iv

##################
##################

currents = np.arange(0.,1.201,0.001)
all_currents = np.concatenate([currents[:-1],currents[::-1]])
qs = np.logspace(-2,2,41)

iv,iswitch,ireturn = [],[],[]
for qq in qs:
	data = rcsj_iv(all_currents,Q=qq,normalized=True,savefile=False,saveplot=False)
	iv.append(data)
	y = critical_currents(data[0],data[1])
	iswitch.append(y[0])
	ireturn.append(y[1])
iswitch, ireturn = np.asarray(iswitch), np.asarray(ireturn)

from collections import OrderedDict
data2save = OrderedDict((key, val) for key,val in zip(['Q ()','Iswitch (Ic)','Ireturn (Ic)'],[qs,iswitch,ireturn]))
savestlab(data2save,'hysteresis')

testplot(qs,ireturn,scale=('log','log'))


plt.plot(qs,ireturn)
plt.xlim(1e-2,1e2)
#plt.ylim(0,1.1)
plt.ylim(1e-2,2)
plt.xscale('log')
plt.yscale('log')
plt.grid()
plt.grid(b=True,which='minor',linestyle='--')
plt.xlabel(r'$Q$')
plt.ylabel(r'$I_r$ ($I_c$)')
#plt.savefig('../plots/hysteresis_loglin.png')
plt.savefig('../plots/hysteresis_loglog.png')
plt.show()
plt.close()


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

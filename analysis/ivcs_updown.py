import numpy as np

from scipy.signal import argrelextrema
import scipy.integrate as integrate
import scipy.special as special
from scipy.integrate import odeint
from scipy.constants import constants as const
from scipy.fftpack import fft, fftfreq

import matplotlib.pyplot as plt

import stlab

from rcsj.utils.rcsj_iv import rcsj_iv

##################
##################

currents = np.arange(0.,2.01,0.01)
all_currents = np.concatenate([currents[:-1],currents[::-1]])
print(all_currents)
time = np.arange(0,500,0.01)

qs = [20,3]#[10,4,1,0.1]
ts = [0.05,0.05]#[0.1,0.1,0.1,0.8]
iv = []
prefix = '../simresults/rcsj_time'
#for qq,tt in zip(qs[-2:],ts[-2:]):
#    iv.append(rcsj_iv(all_currents,time,Q=qq,tsamp=tt,svpng=False,prefix=prefix))
iv = [rcsj_iv(all_currents,time,Q=qq,tsamp=tt,svpng=False,prefix=prefix) for qq,tt in zip(qs,ts)]

[plt.plot(ivv[0],ivv[1]/Q,'.-',label=str(Q)) for ivv,Q in zip(iv,qs)]

plt.xlabel(r'$I/I_c$')
plt.ylabel(r'$V/Q$')
plt.legend()
plt.savefig('ivcs_updown.png',bbox_to_inches='tight')
plt.show()
plt.close()


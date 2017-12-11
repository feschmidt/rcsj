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

qs = np.logspace(-2,2,41)

iv = [rcsj_iv(all_currents,Q=qq,saveiv=True) for qq in qs]


# Plotting
[plt.plot(ivv[0],ivv[1]/Q,'.-',label=str(Q)) for ivv,Q in zip(iv,qs)]
plt.xlabel(r'$I/I_c$')
plt.ylabel(r'$V/Q$')
plt.legend()
plt.savefig('../plots/ivcs_updown.png',bbox_to_inches='tight')
plt.show()
plt.close()



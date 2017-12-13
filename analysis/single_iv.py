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
from rcsj.utils.funcs import ensure_dir

##################
##################

currents = np.arange(0.,1.101,0.001)
all_currents = np.concatenate([currents[:-1],currents[::-1]])
print(all_currents)

betas = [1,2,3]#np.logspace(0,2,5)#[0.2,0.5,1,4]

iv = [rcsj_iv(all_currents,beta=bb,svpng=True,printmessg=True,saveplot=True) for bb in betas]


# Plotting
[plt.plot(ivv[0],ivv[1]/bb,'.-',label=str(bb)) for ivv,bb in zip(iv,betas)]
plt.xlabel(r'$I/I_c$')
plt.ylabel(r'$V/\beta_c$')
plt.legend()
path='../plots/single_ivcs/'
ensuredir(path)
plt.savefig(path+'full_updown.png',bbox_to_inches='tight')
plt.show()
plt.close()



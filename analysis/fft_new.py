import numpy as np

from scipy.signal import argrelextrema
from scipy.fftpack import fft, fftfreq

import matplotlib.pyplot as plt

import stlab
import glob

from rcsj.utils.funcs import *
from rcsj.utils.rcsj_model import rcsj
import pickle

##################
##################

plotpath = '../plots/fft/'
ensure_dir(plotpath)

currents = np.arange(0.,2.005,0.005)
all_currents = np.concatenate([currents[:-1],currents[::-1]])
dampvals = [80,20,10]#,4,3,2,1,0.1,0.05]


for Q in dampvals:
    data = rcsj(all_currents,damping=('Q',Q),fft=True)
    volt_fft = data['FFT']
    freq = data['Frequency']
    peakfreqs = [peakidx(np.log(volt_fft[i]+1e-11),thres=0.1) for i in range(len(volt_fft))]

    '''
    newx=[]
    for x,a in zip(current,peakfreqs):
        newx.append(np.ones(len(a))*x)
    '''
    newpeaks=np.squeeze(np.asarray(peakfreqs).flatten())
    newx = []
    newi = []
    i=0
    for xx,yy in zip(all_currents,newpeaks):
        i+=1
        newx.append(np.ones(len(yy))*xx)
        newi.append(np.ones(len(yy))*i)

    fig, ax = plt.subplots()
    for xx,yy in zip(newi,newpeaks):
        plt.plot(xx,freq[yy]/Q,'k.')
    ax.set_ylim(0,3)
    ax.set_xticks(np.arange(0,len(all_currents),100))
    ax.set_xticklabels(all_currents[0::100])
    plt.title(r'Q={}'.format(Q))
    plt.xlabel(r'Current ($I_c$)')
    plt.ylabel(r'Frequency (Q)')
    plt.savefig(plotpath+'Q={}.png'.format(Q))
    #plt.show()
    plt.close()
    ###


    datasize = volt_fft.shape
    clim = (0,3*Q)
    if Q<=1:
        clim=(0,10000*Q)
    if 1<Q<5:
        clim=(0,20*Q)
    elif 5<Q:
        clim=(0,0.5*Q)

    fig, ax = plt.subplots()
    extent=(0,len(all_currents),freq[0]/Q,freq[-1]/Q)
    ax.imshow(np.flipud(volt_fft.T),extent=extent,aspect='auto',cmap='viridis_r',clim=clim)
    ax.set_ylim(0,1)
    ax.set_xticks(np.arange(0,len(all_currents),100))
    ax.set_xticklabels(all_currents[0::100])
    plt.title(r'Q={}'.format(Q))
    plt.ylabel(r'Frequency (Q)')
    plt.xlabel(r'Current ($I_c$)')
    #pickle.dump(ax, open('../plots/fft/pickle/2d_fft_Q={}.pickle'.format(Q),'wb'))
    plt.savefig(plotpath+'2d_fft_Q={}.png'.format(Q))
    #plt.show()
    plt.close()

    #input("Press Enter to continue...") # waits for user
    ############
    '''
    to load pickle:
    loadax = pickle.load(open('../plots/fft/2d_fft_Q={}.pickle'.format(Q),'rb'))
    plt.show()
    '''

import numpy as np

from scipy.signal import argrelextrema
from scipy.fftpack import fft, fftfreq

import matplotlib.pyplot as plt

import stlab
import glob

from rcsj.utils.funcs import *
import pickle

##################
##################

pathlist = glob.glob('../simresults/rcsj_time/*')
pathlist.sort()
print(pathlist)
for mm in range(2,len(pathlist)):
    filetoopen = pathlist[mm]
    print('\nloading:\n')
    print(filetoopen)
    data = stlab.readdata.readdat(filetoopen)
    #data = [stlab.readdata.readdat(path) for path in pathlist]

    Q = data[0]['Q ()'][0]
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
    freq=np.asarray(freq[0])
    volt_fft = np.asarray(volt_fft)



    peakfreqs = [peakidx(np.log(volt_fft[i]+1e-11),thres=0.1) for i in range(len(data))]

    '''
    newx=[]
    for x,a in zip(current,peakfreqs):
        newx.append(np.ones(len(a))*x)
    '''
    newpeaks=np.squeeze(np.asarray(peakfreqs).flatten())
    newx = []
    newi = []
    i=0
    for xx,yy in zip(current,newpeaks):
        i+=1
        newx.append(np.ones(len(yy))*xx)
        newi.append(np.ones(len(yy))*i)

    fig, ax = plt.subplots()
    for xx,yy in zip(newi,newpeaks):
        plt.plot(xx,freq[yy]/Q,'k.')
    ax.set_ylim(0,3)
    ax.set_xticks(np.arange(0,len(data),100))
    ax.set_xticklabels(current[0::100])
    plt.title(r'Q={}'.format(Q))
    plt.xlabel(r'Current ($I_c$)')
    plt.ylabel(r'Frequency (Q)')
    #plt.savefig('../plots/fft/Q={}.png'.format(Q))
    plt.show()
    plt.close()
    ###


    datasize = volt_fft.shape
    clim = (0,3*Q)
    if Q<=1:
        clim=(0,50*Q)
    if 1<Q<5:
        clim=(0,20*Q)
    elif 5<Q:
        clim=(0,0.5*Q)

    fig, ax = plt.subplots()
    extent=(freq[0]/Q,freq[-1]/Q,0,len(data))
    ax.imshow(volt_fft,extent=extent,aspect='auto',cmap='inferno_r',clim=clim)
    ax.set_xlim(0,2)
    ax.set_yticks(np.arange(0,len(data),100))
    ax.set_yticklabels(current[0::100])
    plt.title(r'Q={}'.format(Q))
    plt.xlabel(r'Frequency (Q)')
    plt.ylabel(r'Current ($I_c$)')
    #pickle.dump(ax, open('../plots/fft/2d_fft_Q={}.pickle'.format(Q),'wb'))
    #plt.savefig('../plots/fft/2d_fft_Q={}.png'.format(Q))
    plt.show()
    plt.close()

    ############
    '''
    to load pickle:
    loadax = pickle.load(open('../plots/fft/2d_fft_Q={}.pickle'.format(Q),'rb'))
    plt.show()
    '''

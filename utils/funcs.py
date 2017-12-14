import stlab
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import peakutils
import os
from scipy.signal import argrelextrema
from scipy.fftpack import fft, fftfreq
import pickle


def ensure_dir(file_path):
    '''
    Checks if directory exists. If not, it creates a new one.
    '''
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        print(directory+' does not exist yet. Creating the directory now.')
        os.makedirs(directory)
    else:
        print(directory+' already exists. Continuing')
        
        
def testplot(x,y,scale=('','')):
    '''
    plots y vs x. optional scale=('xscale','yscale')
    '''
    plt.clf()
    plt.plot(x,y)
    if scale[0]:
        plt.yscale(scale[0])
    if scale[1]:
        plt.xscale(scale[1])
    plt.show()
    plt.close()


def critical_currents(current,voltage,thres=1e-5):
    '''
    returns (iswitch,iretrap) for threshold <thres>
    '''
    clist = current[voltage>thres]
    iswitch = clist[0]
    iretrap = clist[-1]
    return (iswitch,iretrap)


def analyze_fft(time,voltage):
    '''
    returns the FFT of the voltage input
    '''
    F = fftfreq(len(time), d=time[1]-time[0])
    F = F[:len(F)//2]

    signal_fft = fft(voltage)
    signal_fft = signal_fft[:len(signal_fft)//2]
    
    return (F, signal_fft)


def peakidx(y,x=(0,-1),thres=0.3):
    '''
    returns peak indices for FFT analysis
    '''
    if np.mean(y)<-20:
        return []
    else:
        localmax = argrelextrema(y[x[0]:x[1]], np.greater)[0]
        if len(localmax) == 0:
            return []
        else:
            if len(localmax) == 1:
                mindist = 0.9*np.squeeze(localmax) # filter out peaks
            else:
                mindist = 0.9*np.squeeze(localmax)[0] # filter out peaks
            peaks = peakutils.indexes(y,thres=thres,min_dist=mindist)
            return peaks


def findmaxfreq(peakfreqs):
    '''
    returns the maximum value of a list of arrays of different lengths with maximum value > 0
    '''
    oldmax = 0
    for idx in peakfreqs:
        if len(idx)>0:
            if max(idx)>oldmax:
                oldmax=max(idx)
    return oldmax
    
    
def timeparams(damping):
    '''
    reasonable parameters for time and sampling, tested for 1e-2<damping<1e2
    returns (time,ts)
    '''
    key, val = damping[0], damping[1]
    if val < 0.1:
        times = np.arange(0,8000,0.01)
        ts = 0.8
    elif val < 1.:
        times = np.arange(0,2000,0.01)
        ts = 0.6
    elif val < 10.:
        times = np.arange(0,500,0.01)
        ts = 0.2
    else:
        times = np.arange(0,400,0.01)
        ts = 0.2
    if val<1e-2:
        print('Warning: {}={:E} too low! Calculation might be inaccurate.'.format(key,val))
    if 1e2<val:
        print('Warning: {}={:E} too high! Calculation might take very long.'.format(key,val))
    return (times,ts)


def savedata(data2save,filename,path='../simresults/'):
    np.savetxt(path+filename,data2save)


def savestlab(data2save,filename,path='../simresults/'):
    '''
    data2save = {'Time (wp*t)' : t, 'Phase (rad)' : y[:,0], 'AC Voltage (V)' : y[:,1]}
    '''
    data2save = stlab.stlabdict(data2save)
    prefix = path
    idstring = filename
    myfile = stlab.newfile(prefix,idstring,data2save.keys(),
    usedate=False,usefolder=False)#,mypath='simresults/')
    stlab.savedict(myfile,data2save)
    myfile.close()


def saveivplot(current,voltage,damping,normalized=False,single=False):
    '''
    saves a png of the IVC, with normalized voltage (optional)
    '''
    plt.clf()
    if single:
        if normalized:
            plt.plot(current,voltage/damping[1])
            plt.ylabel(r'$V$ (${}$)'.format(damping[0]))
        else:
            plt.plot(current,voltage)
            plt.ylabel('Voltage ()')
    else:
        if normalized:
            plt.plot(current[:len(current)//2],voltage[:len(current)//2]/damping[1])
            plt.plot(current[len(current)//2:],voltage[len(current)//2:]/damping[1])
            plt.ylabel(r'$V$ (${}$)'.format(damping[0]))
        else:
            plt.plot(current[:len(current)//2],voltage[:len(current)//2])
            plt.plot(current[len(current)//2:],voltage[len(current)//2:])
            plt.ylabel('Voltage ()')
    plt.xlabel(r'Current ($I_c$)')
    path = '../plots/iv/'
    ensure_dir(path)
    plt.savefig(path+'_{}={:08.4f}.png'.format(damping[0],damping[1]))
    plt.close()
    

def saveiv(current,voltage,damping,normalized):
    '''
    saves a .dat file of IVC, with normalized voltage (optional)
    '''
    if normalized:
        voltage = voltage/damping[1]
    data2save = stlab.stlabdict({'Current (Ic)': current, 'Voltage (V)': voltage})
    data2save.addparcolumn('{} ():'.format(damping[0]),damping[1])
    idstring = '{}={:08.4f}'.format(damping[0],damping[1])
    myfile = stlab.newfile('../simresults/ivcs/iv',idstring,data2save.keys(),
        usedate=False,usefolder=False)
    stlab.savedict(myfile,data2save)
    myfile.close()    
    

def savepickle(data,filepath):
    '''
    saves data to pickle
    '''
    pickle.dump(data, open(filepath,'wb'))
    

def loadpickle(filepath):
    '''
    loads data from pickle
    '''
    return pickle.load(open(filepath,'rb'))

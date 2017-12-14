import numpy as np

from scipy.signal import argrelextrema
import scipy.integrate as integrate
import scipy.special as special
from scipy.integrate import odeint
from scipy.constants import constants as const
from scipy.fftpack import fft, fftfreq

import matplotlib.pyplot as plt

import stlab
from collections import OrderedDict

from rcsj.utils.funcs import *

##################
##################

hbar, ec = const.hbar, const.e



def Qp(params):
    '''
    returns physical quality factor
    params = {'R':,'Ic':,'C':}
    '''
    R, Ic, C = params['R'], params['Ic'], params['C']
    return R*np.sqrt(2*ec*Ic*C/hbar)


def betac(params):
    '''
    returns Stewart-Mccumber parameter
    '''
    return Qp(params)**2
    
    
def omegap(params):
    '''
    returns plasma frequency
    '''
    C, Ic = params['C'], params['Ic']
    return np.sqrt(2*ec*Ic/(hbar*C))


def omegac(params):
    '''
    returns characteristic frequency
    '''
    Rn, Ic = params['Rn'], params['Ic']
    return 2*ec*Ic*Rn/hbar
    
    
def rcsj_curr(y, t, i, damping):
    '''
    current biased rcsj model
    damping has to be a tuple of (key,val)
    key = 'beta': returns Gross version
    key = 'Q': returns Tinkham version
    '''
    # y0 = phi, y1 = dphi/dt
    y0, y1 = y
    if damping[0]=='beta':
        beta = damping[1]
        dydt = (y1, (-y1 - np.sin(y0) + i)/beta)
    elif damping[0]=='Q':
        Q = damping[1]
        dydt = (y1, -y1/Q -np.sin(y0) +i)
    else:
        raise KeyError('wrong key for ODE provided! Must be either beta or Q.')
    return dydt

    
"""
CAREFUL HERE!!!
def rcsj_volt(y, t, i, Q, R1, R2):
    '''
    voltage biased rcsj model
    '''
    y0, y1 = y
    dydt = [y1, -y1/Q/(1+R2/R1) - np.sin(y0) + i/(1+R2/R1)] # check for errors
    return dydt
"""


def rcsj(current, damping, prefix=[], fft=False,svpng=False,svvolt=False,saveplot=False,savefile=False,normalized=False,printmessg=True):
    '''
    iv sweep for rcsj model
    - damping: tuple of either 'Q' or 'beta' and respective value
    returns IV curve with options:
    - svpng: save each iteration to png
    - svvolt: save peak detection of voltage to png
    - saveplot: save ivc to .png
    - savefile: save ivc to .dat
    - normalized: returns voltage/Q
    - printmessg: print statusmessage after iteration
    '''

    current = current.tolist()      # makes it faster ?
    voltage = []
    freq = []
    volt_fft = []
    
    t, tsamp = timeparams(damping)
    y0 = (0,0) # always start at zero phase and zero current
    idxstart = int(-tsamp*len(t)) # only sample the last tsamp=1% of evaluated time
    for k,i in enumerate(current):
        
        y = odeint(rcsj_curr, y0, t, args=(i,damping))
        #y0 = (0,max(y[:,1])) 
        y0 = y[-1,:]             # new initial condition based on last iteration
        
        idx = argrelextrema(y[idxstart:,1], np.greater)
        
        if len(idx[0])<2:
            mean = 0
            voltage.append(mean)
        else:
            x1, x2 = idx[0][-2], idx[0][-1]
            mean = np.mean([y[x1+idxstart:x2+idxstart,1]])
            voltage.append(mean)
            
            if svpng:
                path='../plots/voltage/{}={:E}/'.format(damping[0],damping[1])
                ensure_dir(path)
                plt.plot(t[idxstart:],y[idxstart:,1])
                plt.plot([t[x1+idxstart],t[x2+idxstart]],[y[x1+idxstart,1],y[x2+idxstart,1]],'o')
                plt.ylim(0,3*damping[1])
                plt.savefig(path+'i={:2.3f}.png'.format(i))
                plt.close()
        
        if prefix:
            #timedata = {'Time (wp*t)' : t, 'Phase (rad)' : y[:,0], 'AC Voltage (V)' : y[:,1]}
            #ivdata = {'Current (Ic)': i, 'DC Voltage (V)': mean, 'beta ()': Q}
            #idstring = 'beta={:.2f}'.format(ivdata['beta ()'])
            #savedata((k,len(current)),prefix,idstring,timedata,ivdata)
            
            data2save = {'Time (wp*t)' : t, 'Phase (rad)' : y[:,0], 'AC Voltage (V)' : y[:,1]}
            data2save = stlab.stlabdict(data2save)
            data2save.addparcolumn('Current (Ic)',i,last=False)
            data2save.addparcolumn('DC Voltage (V)',mean)
            data2save.addparcolumn('{} ()'.format(damping[0]),damping[1])
            if k == 0:
                idstring = '{}={:2.2f}'.format(damping[0],damping[1])
                ensure_dir(prefix)
                myfile = stlab.newfile(prefix,idstring,data2save.keys(),
                usedate=False,usefolder=False)#,mypath='simresults/')
            stlab.savedict(myfile,data2save)
            if k == len(current):
                myfile.close()
                
               
        if svvolt:
            path='../plots/sols/{}={:E}/'.format(damping[0],damping[1])
            ensure_dir(path)
            fig, ax = plt.subplots(2,sharex=True)
            ax[0].plot(t,y[:,0])
            ax[1].plot(t,y[:,1])
            ax[0].set_ylabel(r'$\phi$')
            ax[1].set_ylabel(r'd$\phi$/dt')
            ax[1].set_xlabel(r'$\tau=t/\tau_c$')
            fig.subplots_adjust(hspace=0)
            plt.savefig(path+'i={:2.3f}.png'.format(i))
            plt.close()
        
        
        if fft:
            F, signal_fft = analyze_fft(t,y[:,1])
            freq.append(F)
            volt_fft.append(abs(signal_fft))
        
            
        if printmessg:
            print('Done: {}={:E}, i={:2.3f}'.format(damping[0],damping[1],i)) 

    current, voltage = np.asarray(current), np.asarray(voltage)
    
    if savefile:
        saveiv(current,voltage,damping,normalized)
        
    if saveplot:
        saveivplot(current,voltage,damping,normalized)

    if normalized:
        voltage = voltage/damping[1]
    
    if not fft:    
        return {'Current': current, 'DC Voltage': voltage}
    else:
        return {'Current': current, 'DC Voltage': voltage, 'Frequency': freq[0], 'FFT': np.asarray(volt_fft)}

##################
##################


if __name__ == '__main__':
    currents = np.arange(0.,2.005,0.005)
    all_currents = np.concatenate([currents[:-1],currents[::-1]])

    dampvals = [20,10,4,3,2,1,0.1,0.05]
    #dampvals = [1,0.5,0.1]
    iv = []
    prefix = '../simresults/rcsj_time/' # several GB per file
    iv = [rcsj_iv(all_currents,damping=('Q',dd), saveplot=True,savefile=True,prefix=prefix) for dd in dampvals]

    [plt.plot(ivv['Current'],ivv['Voltage']/dd,'.-',label=str(dd)) for ivv,dd in zip(iv,dampvals)]

    plt.xlabel(r'$I/I_c$')
    plt.ylabel(r'$V/Q$')
    plt.legend()
    plt.savefig('../plots/ivcs_updown.png',bbox_to_inches='tight')
    plt.show()
    plt.close()






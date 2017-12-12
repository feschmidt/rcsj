import numpy as np

from scipy.signal import argrelextrema
import scipy.integrate as integrate
import scipy.special as special
from scipy.integrate import odeint
from scipy.constants import constants as const
from scipy.fftpack import fft, fftfreq

import matplotlib.pyplot as plt

import stlab

from rcsj.utils.funcs import *

# BROKEN from rcsj.utils.funcs import savedata

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
    
def rcsj_curr(y, t, i, Q):
    '''
    current biased rcsj model
    '''
    # y0 = phi, y1 = dphi/dt
    y0, y1 = y
    dydt = (y1, (-y1 - np.sin(y0) + i)/Q)
    return dydt

def rcsj_volt(y, t, i, Q, R1, R2):
    '''
    voltage biased rcsj model
    '''
    y0, y1 = y
    dydt = [y1, -y1/Q/(1+R2/R1) - np.sin(y0) + i/(1+R2/R1)] # check for errors
    return dydt

def rcsj_iv(current, Q=4, svpng=False, printmessg=True, prefix=[],
    savefile=False, saveplot=False, normalized=False, full_output=False):
    '''
    iv sweep for rcsj model
    returns IV curve with options:
    - svpng: save each iteration to png
    - saveiv: save ivc to .dat
    - normalized: returns voltage/Q
    '''
    
    current = current.tolist()      # makes it faster ?
    voltage = []
    
    t, tsamp = timeparams(Q)
    y0 = (0,0) # always start at zero phase and zero current
    idxstart = int(-tsamp*len(t)) # only sample the last tsamp=1% of evaluated time
    for k,i in enumerate(current):
        
        y = odeint(rcsj_curr, y0, t, args=(i,Q), printmessg=printmessg)
        y0 = (0,max(y[:,1])) 
        #y0 = y[-1,:]             # new initial condition based on last iteration
        #print(y0)
        idx = argrelextrema(y[idxstart:,1], np.greater)
        
        if len(idx[0])<2:
            mean = 0
            voltage.append(mean)
        else:
            x1, x2 = idx[0][-2], idx[0][-1]
            mean = np.mean([y[x1+idxstart:x2+idxstart,1]])
            voltage.append(mean)
            
            if svpng:
                path='../plots/voltage/Q={:E}/'.format(Q)
                ensure_dir(path)
                plt.plot(t[idxstart:],y[idxstart:,1])
                plt.plot([t[x1+idxstart],t[x2+idxstart]],[y[x1+idxstart,1],y[x2+idxstart,1]],'o')
                plt.ylim(0,3*Q)
                plt.savefig(path+'i={:2.3f}.png'.format(i))
                plt.close()
        
        if prefix:
            #timedata = {'Time (wp*t)' : t, 'Phase (rad)' : y[:,0], 'AC Voltage (V)' : y[:,1]}
            #ivdata = {'Current (Ic)': i, 'DC Voltage (V)': mean, 'Q ()': Q}
            #idstring = 'Q={:.2f}'.format(ivdata['Q ()'])
            #savedata((k,len(current)),prefix,idstring,timedata,ivdata)
            
            data2save = {'Time (wp*t)' : t, 'Phase (rad)' : y[:,0], 'AC Voltage (V)' : y[:,1]}
            data2save = stlab.stlabdict(data2save)
            data2save.addparcolumn('Current (Ic)',i)
            data2save.addparcolumn('DC Voltage (V)',mean)
            data2save.addparcolumn('Q ()',Q)
            if k == 0:
                idstring = 'Q={:2.2f}'.format(Q)
                myfile = stlab.newfile(prefix,idstring,data2save.keys(),
                usedate=False,usefolder=False)#,mypath='simresults/')
            stlab.savedict(myfile,data2save)
            if k == len(current):
                myfile.close()
                
               
        if svpng:
            path='../plots/sols/Q={:E}/'.format(Q)
            ensure_dir(path)
            fig, ax = plt.subplots(2,sharex=True)
            ax[0].plot(t,y[:,0])
            ax[1].plot(t,y[:,1])
            fig.subplots_adjust(hspace=0)
            plt.savefig(path+'i={:2.3f}.png'.format(i))
            plt.close()
            
        if printmessg:
            print('Done: Q={:E}, i={:2.3f}'.format(Q,i)) 

    current, voltage = np.asarray(current), np.asarray(voltage)
    
    if savefile:
        saveiv(current,voltage,Q,normalized)
        
    if saveplot:
        saveivplot(current,voltage,Q,normalized)

    if normalized:
        voltage = voltage/Q
        
    return (current, voltage)

##################
##################


if __name__ == '__main__':
    currents = np.arange(0.,2.01,0.01)
    all_currents = np.concatenate([currents[:-1],currents[::-1]])

    #qs = [20,10,4,3,2,1,0.1,0.05]
    qs = [10,4,1,0.1]
    iv = []
    prefix = '../simresults/rcsj_time' # 1.9GB per file
    iv = [rcsj_iv(all_currents,Q=qq,svpng=False,prefix=prefix) for qq,tt in zip(qs,ts)]

    [plt.plot(ivv[0],ivv[1]/Q,'.-',label=str(Q)) for ivv,Q in zip(iv,qs)]

    plt.xlabel(r'$I/I_c$')
    plt.ylabel(r'$V/Q$')
    plt.legend()
    plt.savefig('../plots/ivcs_updown.png',bbox_to_inches='tight')
    plt.show()
    plt.close()






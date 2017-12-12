import stlab
import matplotlib.pyplot as plt
import numpy as np
import peakutils
import os

def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        
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


def peakidx(y,x=(0,-1),thres=0.3):
    '''
    returns peak indices for FFT analysis
    '''
    localmax = argrelextrema(y[x[0]:x[1]], np.greater)
    mindist = 0.9*np.squeeze(localmax)[0] # filter out peaks
    peaks = peakutils.indexes(y,thres=thres,min_dist=mindist)
    return peaks


def timeparams(Q):
    '''
    reasonable parameters for time and sampling, tested for 1e-2<Q<1e2
    returns (time,ts)
    '''

    if Q < 0.1:
        times = np.arange(0,1000,0.01)
        ts = 0.8
    elif Q < 1.:
        times = np.arange(0,1000,0.01)
        ts = 0.8
    elif Q < 10.:
        times = np.arange(0,500,0.01)
        ts = 5e-2
    elif Q < 100.:
        times = np.arange(0,400,0.01)
        ts = 5e-2
    else: # unnecessary?
        times = np.arange(0,400,0.01)
        ts = 5e-2
    if Q<1e-2:
        print('Warning: Q={:E} too low! Calculation might be inaccurate.'.format(Q))
    if 1e2<Q:
        print('Warning: Q={:E} too high! Calculation might take very long.'.format(Q))
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


def saveivplot(current,voltage,Q,normalized=False):
    '''
    saves a png of the IVC, with normalized voltage (optional)
    '''
    plt.clf()
    if normalized:
        plt.plot(current,voltage/Q)
        plt.ylabel('Voltage (Q)')
    else:
        plt.plot(current,voltage)
        plt.ylabel('Voltage ()')
    plt.xlabel('Current (Ic)')
    plt.savefig('../plots/iv_Q={:08.4f}.png'.format(Q))
    plt.close()
    

def saveiv(current,voltage,Q,normalized):
    '''
    saves a .dat file of IVC, with normalized voltage (optional)
    '''
    if normalized:
        voltage = voltage/Q
    data2save = stlab.stlabdict({'Current (Ic)': current, 'Voltage (V)': voltage})
    data2save.addparcolumn('Q ():',Q)
    idstring = 'Q={:08.4f}'.format(Q)
    myfile = stlab.newfile('../simresults/ivcs/iv',idstring,data2save.keys(),
        usedate=False,usefolder=False)
    stlab.savedict(myfile,data2save)
    myfile.close()    
    
'''
*** BROKEN
def savedata(k,prefix,idstring,timedata,ivdata):
    #k = (<running idx>,<len(current)>)
    #timedata = {'Time (wp*t)' : time, 'Phase (rad)' : y[:,0], 'AC Voltage (V)' : y[:,1]}
    #ivdata = {'Current (Ic)': curr, 'DC Voltage (V)': mean, 'Q ()': Q}
    #idstring = 'Q={:.2f}'.format(ivdata['Q ()'])
    
    data2save = stlab.stlabdict(timedata)
    #if kwargs:
    #   for key, val in kwargs.items():
    #       data2save.addparcolumn(key,val)
    for key, val in ivdata.items():
        data2save.addparcolumn(key,val)
    if k[0] == 0:
        myfile = stlab.newfile(prefix,idstring,data2save.keys(),usedate=False,usefolder=False)
        return myfile
    # this doesn't work because myfile gets lost during iterations...
    stlab.savedict(myfile,data2save)
    if k[0] == k[1]:
        myfile.close()
'''

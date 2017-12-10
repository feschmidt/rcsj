import stlab
import matplotlib.pyplot as plt

def testplot(x,y,scale=('','')):
    plt.clf()
    plt.plot(x,y)
    if scale[0]:
        plt.yscale(scale[0])
    if scale[1]:
        plt.xscale(scale[1])
    plt.show()
    plt.close()

def critical_currents(current,voltage,thres=1e-5):
    clist = current[voltage>thres]
    iswitch = clist[0]
    iretrap = clist[-1]
    return (iswitch,iretrap)

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
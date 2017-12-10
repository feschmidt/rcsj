import numpy as np
import matplotlib.pyplot as plt


def saveplot(x,y,path=[],show='False',**kwargs):
    fig,ax=plt.subplots()
    ax.plot(x,y)
    for key, val in kwargs.items():
        getattr(ax,'set_'+key)(val)
    if path:
        plt.savefig(path)
    if show:
        plt.show()
    plt.close()

def save2plot(x,y1,y2,path=[],show='False',**kwargs):
    fig, ax = plt.subplots(2,sharex=True)
    ax[0].plot(x,y1)
    ax[1].plot(x,y2)
    for key, val in kwargs.items():
        getattr(ax[0],'set_'+key)(val)
        getattr(ax[1],'set_'+key)(val)
    if path:
        plt.savefig(path)
    if show:
        plt.show()
    plt.close()

x=np.linspace(-10,10,101)
y=np.sin(x)
y2=np.cos(x)

saveplot(x,y,show='True')
save2plot(x,y,y2,path='test2.png',show='True',ylim=(0,1))


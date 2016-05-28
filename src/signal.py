# -*- coding: utf-8 -*-


import numpy as np

def ricker(nt=750, dt=0.004, f=20, tshift=0, amp=1, sc=0):
    '''
    Ricker signal
    '''
    t = np.arange(0,nt-1)*dt # time vec
    ts = 1./f;
    tau = np.pi*(t-1.5*ts-tshift)/ts
    ricker = amp*(((1.0-2.0*tau*tau)*np.exp(-tau*tau)))

    if sc == 1:
        ricker = np.cumsum(ricker)
        ricker = ricker / max(abs(ricker))*amp
    return ricker

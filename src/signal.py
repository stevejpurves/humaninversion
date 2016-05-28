# -*- coding: utf-8 -*-


import numpy as np
from scipy.signal import hilbert


def Rotation(w,phase):
    '''
    Function Rotation: signal rotation.
    
    Input:
    w: signal (array)
    phase: phase rotation (scalar, unit: radians)
    
    Outpout:
    w_rot: rotated signal (array)
    '''  
    hw = hilbert(w) #Returns analytic signal        
    wrot = w*np.cos(phase) + hw.imag*np.sin(phase) #Applies rotation
        
    return wrot

#def ricker(nt=750, dt=0.004, f=20, tshift=0, amp=1, sc=0, phase=0.0):
def ricker(nt=750, dt=0.004, f=20, tshift=0, amp=1,phase=0.0):

    '''
    Ricker signal
    
    Input:
    phase: angle (scalar, unit: radians)
    '''
    t = np.arange(0,nt-1)*dt # time vec
    ts = 1./f;
    tau = np.pi*(t-1.5*ts-tshift)/ts
    ricker = amp*(((1.0-2.0*tau*tau)*np.exp(-tau*tau)))

    ricker = Rotation(ricker, phase)
    '''
    if sc == 1:
        ricker = np.cumsum(ricker)
        ricker = ricker / max(abs(ricker))*amp
    '''
    return ricker

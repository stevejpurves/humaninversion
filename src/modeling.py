# -*- coding: utf-8 -*-
"""
Created on Sat May 28 07:07:29 2016

@author: Carlos
"""
import numpy as np
from ricker import Ricker
'''
####Functions####
Function Noise: creates gaussian noise. The standard deviaton is a
    percentage of the maximum absolut amplitude.
    
ConvModel: uses convolution to create a synthetic seismic trace.

GetR: calculate reflection coeficient for each interface.
    Assumption: normal incidence.
    
GetI: get impedance from de reflection coeficients.

##############
'''

def Noise(trace, perc=0.01):
    '''
    Function Noise: creates gaussian noise. The standard deviaton is a
    percentage of the maximum absolut amplitude.
    
    Input:
    trace: seismic trace (array)
    perc: percedntage (scalar)
    
    Output:
    noise: noise (array)
    '''
    perc = perc/100.0
    std = perc*max(abs(trace)) #standard
    ns = len(trace) #number of samples
    noise = np.random.normal(0.0, std, ns)
    
    return noise


def ConvModel(r, w, perc=1.0):
    '''
    Function ConvModel: uses convolution to create a synthetic seismic
    trace.
    
    Input:
    r: reflectivity series (array)
    w: wavelet (array)
    
    Outpout:
    tr: synthetic seismic trace (Array)
    '''    
    tr = np.convolve(r, w, 'same')
    tr = tr + Noise(tr, perc=1.0)
    return tr
    
def GetR(I):

    '''
    Function GetR: calculate reflection coeficient for each interface.
    Assumption: normal incidence.
    
    Input:
    I: impedances for each layer (array)
    
    Output:
    r: reflection coeficient (array)
    '''
    
    ns = len(I) #number of samples
    
    r = np.zeros(ns)
    
    #calcule impedance for each interface
    for i in range(ns-1):
        r[i] = (I[i+1]-I[i])/(I[i+1]+I[i])
        
    return r
    
def GetI(r,Ib):
    '''
    Function GetI: get impedance from de reflection coeficients.
    
    Input:
    r: reflection coeficients (array)
    Ib: impedance from the first layer (scalar)
    
    Output:
    I: impedance for each layer (array)
    
    '''
    
    ns = len(r) #number of samples
    
    I = np.zeros(ns) #Impedance
    I[0] =Ib
    for i in range(1,ns):
        I[i] = I[i-1]*(1.0+r[i-1])/(1.0-r[i-1])
        
    return I
    
def RandModel(nr, ns=500):
    
    '''
    Function RandModel: create a Random reflectivity sequence. Position
    is also random.
    
    Input:
    nr: number reflection coeficients (scalar)
    ns: number of samples (scalar)
    
    Output:
    R: reflectivity sequence (array)
    '''
    
    r = np.random.normal(0.0, 0.5,nr)
    R = np.zeros(ns)

    for i in range(nr):
        pos = abs(np.random.normal(0.0, ns, 1))
        while pos>=ns:
           pos = abs(np.random.normal(0.0, ns, 1))

        R[int(pos)] = r[i]
        
    return R
    
def MarineRandModel(nr, ns=500, fstlayer=25):
    '''
    Function RandModel: create a Random reflectivity sequence. Position
    is also random.
    
    Input:
    nr: number reflection coeficients (scalar)
    ns: number of samples (scalar)
    
    Output:
    R: reflectivity sequence (array)
    '''
    nr = nr-1 #Discounting one because seabad is already considered
    r = np.random.normal(0.0, 0.25,nr)
    R = np.zeros(ns)
    R[fstlayer] = 0.3
    for i in range(nr):
        pos = abs(np.random.normal(0.0, ns, 1))
        while pos>=ns or pos<=fstlayer:
           pos = abs(np.random.normal(0.0, ns, 1))

        R[int(pos)] = r[i]
        
    return R
    
def UserModeling(r):
    r = np.asarray(r)
    w = Ricker(ns=128, dt=0.004, fp=10.0,phase=0.0)
    tr = ConvModel(r, w,perc=1.0)
    
    return tr
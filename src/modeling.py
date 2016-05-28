# -*- coding: utf-8 -*-
"""
Created on Sat May 28 07:07:29 2016

@author: Carlos
"""
import numpy as np
'''
####Functions####
ConvModel: uses convolution to create a synthetic seismic trace.

GetR: calculate reflection coeficient for each interface.
    Assumption: normal incidence.
    
GetI: get impedance from de reflection coeficients.

##############
'''
def ConvModel(r, w):
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
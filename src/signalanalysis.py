# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 11:01:38 2016

@author: cassis

Description: functions for signal analysis

######################FUNCTIONS################################################
Rotation: signal rotation.

Smooth: smooth an array.

Timeshift: shift a whole array some samples.

Timeshift: shift a whole array some samples.

fft1D: applies FFT to an array.

###############################################################################
"""

import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt


def Rotation(w,phase):
    '''
    Function Rotation: signal rotation.
    
    Input:
    w: signal (array)
    phase: phase rotation (scalar, unit: radians)
    
    Outpout:
    wrot: rotated signal (array)
    '''  
    hw = hilbert(w) #Returns analytic signal        
    wrot = w*np.cos(phase) + hw.imag*np.sin(phase) #Applies rotation
        
    return wrot
    
 

def Smooth (sig,n):
    
    '''
    Function Smooth: smooth an array.
    
    Input: 
    sig: signal (array)
    n:number of samples of the smooth operator (scalar)
    
    Output:
    smt: smoothed signal (array)
    '''
    
    ns = len(sig) #number of samples
    

   
    win = np.ones(n) #smoothing window
    
    smt = np.convolve(sig, win,'same') 
    
    norm = np.ones(ns)*n
    norm[:n] = np.arange(1, n)
    norm[(ns-n):] = np.arange(n,1,-1)

    smt = smt/norm
    return smt

def Timeshift(sig, nt):
    '''
    Function Timeshift: shift a whole array some samples.
    
    Input:
    sig: signal (array)
    nt: number of samples to shift the array (scalar)
    
    Output:
    sigout: shifted signal (array)
    '''    
    ns = len(sig)
    sigf = np.fft.fft(sig)
    df = 1.0/(ns)
    fmax = df*ns/2.0
    f = np.arange(-fmax, fmax,df)
    f = np.fft.fftshift(f)
    sigout = np.real(np.fft.ifft(sigf*np.exp(-1j*2.0*np.pi*f*nt)))
    
    return sigout
    

def xcorr2(x,y=None):

  '''
  Function xcorr2: calculate the correlation of two signals x and y.
    
  Input:
  x: signal x (array)
  y: signal y (array)
    
  Output:
  out: correlation (array)
  '''
  if y is None:
      y=x
  x = x/max(x)
  y = y/max(y)
  ns = len(x)
  N = 2*ns - 1
  out = np.zeros(N)
  for i in range(N):
  
    if i<ns:
        

     out[i] = np.dot(x[(N-ns-i):ns],y[:(i+1)])/(i+1)

    else:
     out[i] = np.dot(x[:(N-i)],y[(i-ns+1):])/(N-i)

  return out
  
    
def fft1D(d,n=1, dt=1e-3,nsfft=0, tmax=-1):
    
  '''
  Function fft1D: applies FFT to an array.
  
  Input:
  d: seismic trace (array 1D)
  dt: sampling interval (scalar, seconds)
  nsfft: number of samples to be considering in the FFT. This number must be
  greater than the input signal number os samples.
  tmax: last original array sample to be considered by FFT.
  
  Output:
  x: frequencies (array)
  y: normalized amplitude spectrum (array)
  maxX: peak frequency (scalar)

  '''
  d = d[0:tmax]
  
  if nsfft == 0:
     nsfft = len(d)
  
  dft = np.fft.fft(d,n=nsfft,axis=0)
  
  ns = len(dft)
  df = 1.0/(ns*dt)
  nf = ns/2+1
  x = np.arange(0,nf,1.0)*df
  y = abs(dft[0:nf])
  y = Smooth(y,n)
  
  ymax = max(y)
  
  idx = list(y).index(ymax)
  maxX = x[idx]
 
  y = y/ymax
  
  return (x,y,maxX)
    
def Envelope(d):
    
    '''
    Envelope: Calculated using analytic signal.
    
    Input:
    d: seismic trace (array)
    
    Output:
    amp: envelope.
    '''
    asig = hilbert(d) #Analytic signal
   
    amp = abs(asig)
    
    return amp
    
def CosPhase(d):
    
    '''
    CosPhase: Cosine of instantaneous phase. Calculated using analytic signal.
    
    Input:
    d: seismic trace (array)
    
    Output:
    amp: cosine of instantaneous phase.
    '''
    asig = hilbert(d) #Analytic signal
   
    cosphase = np.cos(np.angle(asig))
    
    return cosphase


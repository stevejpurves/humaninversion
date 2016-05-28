# -*- coding: utf-8 -*-
"""
Created on Fri Jan 08 11:01:38 2016

@author: cassis

Descrição: biblioteca contendo função para analise de sinais

######################IMPLEMENTAÇÕES###########################################
*Função Rotação: Rotaciona um sinal

*Função Convolucao: convolução de um sinal w com um sinal R.

*Função RMS: calcula o valor RMS de cada amostra sempre partindo do inicio do array
    
*Função Smooth: suaviza um vetor.

*Função Timeshift: desloca um vetor determinado numero de amostras. O padrão
    é um deslocamento para a direita.
    
*Função xcorr2: calcula a correção de dois sinais x e y. Ou a autocorrelação
  de um sinal x.
  
*Função BandPass: filtro passa-banda trapezoidal.  Observação: f1<f2<f3<f4

###############################################################################
"""

import numpy as np
from scipy.signal import hilbert
import matplotlib.pyplot as plt


def Rotacao(w,fase):
    '''
    Função Rotação: Rotaciona um sinal
    
    #Entrada:
    w: sinal
    fase: fase em radianos
    
    #Saida:
    w_rot: wavelet rotacionada
    '''  
    hw = hilbert(w) #Transformada de Hilbert        
    wrot = w*np.cos(fase) + hw.imag*np.sin(fase) #Aplica a rotação
        
    return wrot
    
 
def Convolucao(R, w):
    '''
    Função Convolucao: convolução de um sinal w com um sinal R.
    Entrada:
    R: série refletividades (array)
    w: wavelet (array)    
    
    Saida:
    tr: resultado da convolução, mantem o tamanho original de R
    '''   
    
    tr=np.convolve(w, R, 'same')
    return tr
   


def RMS(v):
    
    '''
    Função RMS: calcula o valor RMS de cada amostra sempre partindo do inicio 
    do array
    
    Entrada:
    v: array 1D
    
    Saida:
    vrms: valor rms para cada amostra de v (array)
    '''
    n = np.arange(len(v))+1
    vrms = np.sqrt(np.cumsum(v**2.0)/n)
    
    return vrms     
        

def Smooth (sig,n):
    
    '''
    Função Smooth: suaviza um vetor.
    
    Entrada: 
    sig: sinal (array)
    n:numero de amostra do operador de suavização
    
    Saida:
    smt: signal suavizado
    '''
    
    ns = len(sig) #Numero de amostras de sig
    
    tmp = np.zeros(ns+2*n) #Cria vetor extendido
    
	#Atribui sig ao array tmp
    tmp[:(n-1)] = sig[0]
    tmp[(ns-1):] = sig[-1]
    tmp[(n-1):(ns+n-1)] = sig
   
    win = np.ones(n)/n #Operador de suavização
    
    smt = np.convolve(tmp,win,'same') #Aplica a suavização
    
    smt = smt[n:(ns+n)] #Mantem o mesmo numero de amostras do vetor sig de entrada.
    return smt

def Timeshift(sig, nt):
    '''
    Função Timeshift: desloca um vetor determinado numero de amostras. O padrão
    é um deslocamento para a direita.
    
    Entrada:
    sig: sinal (array)
    nt: numero de amostras a serem deslocadas (escalar)
    
    Saida:
    sigout: sinal deslocado nt amostras (array)
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
  Função xcorr2: calcula a correção de dois sinais x e y. Ou a autocorrelação
  de um sinal x.
    
  Entrada:
  x: sinal x (array)
  y: sinal y (array)
    
  Saida:
  out: correlação (array)
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
        
     #print x[(N-ns-i):ns]
     #print y[:(i+1)]
     out[i] = np.dot(x[(N-ns-i):ns],y[:(i+1)])/(i+1)
    #elif i == ns:
    # out[i] = np.dot(x,y)
    else:
     out[i] = np.dot(x[:(N-i)],y[(i-ns+1):])/(N-i)

  return out
  
def BandPass(sig, dt, f1, f2, f3, f4):
    '''
    Função BandPass: filtro passa-banda trapezoidal.
    Observação: f1<f2<f3<f4
    
    Entrada:
    sig: sinal (array)
    dt: intervalo de amostragem (escalar, segundos)
    f1, f2, f3, f4: frequencias em ordem crescrente (escalares, Hz)
    
    Sajda:
    sigbp: sinal filtrado (array)
    '''             
    sig = sig.flatten()
    ns = len(sig)
    nsf = ns
    df = 1.0/(ns*dt) 
    
    #Garante que a amostragem em frequência sera de pelo menos 1 Hz
    if df>1.0:
        nsf = int(round(1.0/dt))
        df = 1.0
    fmax = 1.0/(2.0*dt)
    #print 'df', df    
    n1 = round(f1/df)
    n2 = round((f2-f1)/df)
    n3 = round((f3-f2)/df)
    n4 = round((f4-f3)/df)
    n5 = round((fmax-f4)/df)

    nt = n1 + n2 + n3 + n4 + n5    
    if nt<nsf:
        n5 = n5 + round((nsf/2-nt))
    #Cria o filtro
    filtro = np.concatenate((np.zeros(n1), 
                             np.linspace(0.,1.0,n2), 
                             np.ones(n3), 
                             np.linspace(1.0, 0.,n4),
                             np.zeros(n5)), axis=0)  
    filtroshift = np.concatenate((filtro, filtro[::-1]), axis=0)
    sigf = np.fft.fft(sig, n=nsf) #fft do sinal original
    amp = np.abs(sigf) #valor absoluto da fft
    fase = np.arctan2(np.imag(sigf), np.real(sigf)) #fase do sinal
    
    ampbp = amp*filtroshift #filtragem
    
    sigbp = np.real(np.fft.ifft(ampbp*np.exp(1j*fase), n=nsf))
    sigbp = np.copy(sigbp[:ns])
    f = np.linspace(-fmax, fmax, nsf)
    f = np.fft.fftshift(f)

    return sigbp
    
def fft1D(d,n=1, dt=1e-3,nsfft=0, tmax=-1):
    
  '''
  Função fft1D: aplica a transformada de Fourier a vetor.
  
  Entrada:
  d: traço sísmico (array 1D)
  dt: intervalo de amostragem (escalar, segundos)
  nsfft: numero de amostras a ser considerado na aplicação da transformada.
  Este numero deve ser maior que o numero de amostras do vetor de entrada.
  tmax: ultima amostra do vetor de entrada a ser considerada na transformação.
  
  Saida:
  x: vetor de frequências (array)
  y: espectro de amplitude normalizado (array)
  maxX: frequência de pico (escalar)

  '''
  d = d[0:tmax]
  
  if nsfft == 0:
     nsfft = len(d)
  
  dft = np.fft.fft(d,n=nsfft,axis=0)
  
  ns = len(dft)
  df = 1.0/(ns*dt)
  #print 'df: %f' %df
  nf = ns/2+1
  x = np.arange(0,nf,1.0)*df
  y = abs(dft[0:nf])
  y = Smooth(y,n)
  
  #y = 20.0*np.log10(y)+40 #Decibel

  ymax = max(y)
  
  idx = list(y).index(ymax)
  maxX = x[idx]
 
  y = y/ymax
  
  #y = 20*np.log(y)
  return (x,y,maxX)
    
        
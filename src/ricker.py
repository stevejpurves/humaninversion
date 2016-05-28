#Pulso de Ricker
#Copiado da funcao Fortran do Sergio


import pylab as np

def Ricker(ns, dt,fp, A=1.0):
    
    '''
    Entrada:
    ns - Numero de amostras (escalar)
    dt - interlavo de amostragem (escalar, segundos)
    fp - frequencia de pico (escalar, Hz)
    A  - fator de escala da amplitude (escalar)
    
    Saida:
    pulso: wavelet de ricker (array)
    '''

    delay = ns/2
  
    t = np.arange(0,ns,1)*dt - delay*dt
    pulso=A*(1.-2.*(np.pi*fp*t)**2.)*np.exp(-1.*(np.pi*fp*t)**2.)

    return pulso


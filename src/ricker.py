#Pulso de Ricker
#Copiado da funcao Fortran do Sergio


import pylab as np
from signalanalysis import Rotation

def Ricker(ns, dt, fp, phase=0.0, A=1.0):

    '''
    Function Ricker: create Ricker wavelet

    Input:
    ns - number os samples (scalar)
    dt - sampling interval (scalar, seconds)
    fp - peak frequency (scalar, Hz)
    phase - angle (scalar, unit: degree)
    A  - amplitude scaling factor (scalar)

    Output:
    pulse: ricker wavelet (array)
    '''
    phase = np.rad2deg(phase)
    delay = (ns-1)/2

    t = np.arange(0,ns,1)*dt - delay*dt
    pulse=A*(1.-2.*(np.pi*fp*t)**2.)*np.exp(-1.*(np.pi*fp*t)**2.)
    pulse = Rotation(pulse, phase)
    return pulse


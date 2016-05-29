# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:16:57 2016

@author: Carlos
"""
from ricker import Ricker
import numpy as np
from modeling import ConvModel, RandModel, GetI, MarineRandModel
import matplotlib.pyplot as plt
import json
from signalanalysis import Envelope, CosPhase

'''
def Decon(tr, w):
    
    ns = len(tr)
    TR = np.fft.fft(tr)
    W = np.fft.fft(w, n=ns)
    
    R = TR*2.0/(W+0.05*max(abs(W)))
    r = np.real(np.fft.ifft(R))
    return r
'''    
r = MarineRandModel(3, 400)

w = Ricker(128, 0.004, 25.0, 90.0)
tr = ConvModel(r, w,perc=1.0)

data = {'seismic':list(tr), 'model':list(r)}

#with open('../Data/Model1.txt', 'w') as outfile:
#    json.dump(data, outfile)
#r2 = Decon(tr, w)
plt.plot(r, 'k', linewidth=3, label='Random Reflectivity')
plt.plot(data['seismic'], label='Trace')
plt.plot(Envelope(tr))

plt.figure()
plt.plot(GetI(r, 1500.0))
plt.legend()


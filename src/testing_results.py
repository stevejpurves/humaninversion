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
from signalanalysis import Envelope, CosPhase, xcorr2
from results import Results, ExportResults

#r = MarineRandModel(5, 300)


r = np.zeros(300)
r[30] = 0.3
r[150] = 0.15
r[160] = -0.1

w = Ricker(128, 0.004, 20.0, 0.0)
tr = ConvModel(r, w,perc=1.0)
r[160] = 0.1
tr2 = ConvModel(r, w,perc=1.0)


I = GetI(r, 1500.0)
env = Envelope(tr)
data = { 'reflectivity':list(r), 'impedance:':list(I) ,'seismic':list(tr), 'envelope': list(env)}
res = Results(tr, tr2)
ExportResults(tr, tr2)
#r2 = Decon(tr, w)
print(type(res))
print(res)
plt.figure()
plt.plot(r, 'k', linewidth=3, label='Random Reflectivity')
plt.plot(data['seismic'], label='Trace')
plt.plot(tr2, '*',label='Tr2')
plt.plot(env, label='Envelope')
plt.legend()

#plt.figure()
#plt.plot(I)


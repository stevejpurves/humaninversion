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


r = MarineRandModel(30, 300)

'''
r = np.zeros(300)
r[30] = 0.3
r[150] = 0.15
r[160] = -0.1
'''
w = Ricker(128, 0.004, 20.0, 0.0)
tr = ConvModel(r, w,perc=1.0)
I = GetI(r, 1500.0)
env = Envelope(tr)
data = { 'reflectivity':list(r), 'impedance:':list(I) ,'seismic':list(tr),
'envelope': list(env), 'min':np.min(tr), 'max':np.max(tr) }

with open('../static/data/model4.txt', 'w') as outfile:
    json.dump(data, outfile)
#r2 = Decon(tr, w)
plt.plot(r, 'k', linewidth=3, label='Random Reflectivity')
plt.plot(data['seismic'], label='Trace')
plt.plot(env)

plt.figure()
plt.plot(I)
plt.legend()
plt.show()


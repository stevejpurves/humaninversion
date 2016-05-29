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

r = MarineRandModel(4, 300)

w = Ricker(128, 0.004, 25.0, 0.0)
tr = ConvModel(r, w, perc=1.0)

trmin = np.min(tr)
trmax = np.max(tr)

print trmin
print trmax

I = GetI(r, 1500.0)
env = Envelope(tr)

# data = {'seismic':list(tr), 'model':list(r), 'min':trmin, 'max':trmax}
# data = {'seismic':list(tr), 'model':list(r)}

# w = Ricker(128, 0.004, 10.0, 0.0)
# tr = ConvModel(r, w,perc=1.0)

data = { 'reflectivity':list(r), 'impedance:':list(I) ,'seismic':list(tr),
'envelope': list(env), 'min':trmin, 'max':trmax }


with open('../static/data/model5.txt', 'w') as outfile:
   json.dump(data, outfile)

# r2 = Decon(tr, w)
# plt.plot(r, 'k', linewidth=3, label='Random Reflectivity')
# plt.plot(data['seismic'], label='Trace')
# plt.plot(Envelope(tr))

# plt.figure()
# plt.plot(GetI(r, 1500.0))
# plt.legend()
# plt.show()



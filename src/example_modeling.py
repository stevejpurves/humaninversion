# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:16:57 2016

@author: Carlos
"""
from ricker import Ricker
import numpy as np
from modeling import ConvModel
import matplotlib.pyplot as plt
import json
r = np.zeros(500)
r[100] = 0.3
r[200] = -0.5
r[300] = 0.65

w = Ricker(128, 0.004, 25.0)
tr = ConvModel(r, w)

data = {'seismic':list(tr), 'model':list(r)}


with open('../Data/Model1.txt', 'w') as outfile:
    json.dump(data, outfile)
plt.plot(data['seismic'])


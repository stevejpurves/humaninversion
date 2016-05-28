# -*- coding: utf-8 -*-
"""
Created on Sat May 28 10:16:57 2016

@author: Carlos
"""
from ricker import Ricker
import numpy as np
from modeling import ConvModel
import matplotlib.pyplot as plt
r = np.zeros(500)
r[100] = 1.0
r[200] = 0.5
r[300] = 1.0

w = Ricker(128, 0.004, 25.0)
tr = ConvModel(r, w)

plt.plot(tr)


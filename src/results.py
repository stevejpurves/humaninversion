# -*- coding: utf-8 -*-
"""
Created on Sun May 29 04:39:34 2016

@author: Carlos
"""

import numpy as np
from signalanalysis import xcorr2
import matplotlib.pyplot as plt
import json

def Results(tmodel, umodel):
    '''
    Function Results: compares true model (tmodel) to the user model (umodel).
    
    Input:
    tmodel: true model (array)
    umodel: user model (array)
    
    Output:
    results: Everything is a percentage (dictionary) 
    keys: 
    total: total similarity  
    coor: normalized correlation
    energy: normarlied energy
    Ediff: energy difference
    
    '''
    tmodel  = np.asarray(tmodel)
    umodel = np.asarray(umodel)
    Et = sum(tmodel**2.0) #True model energy
    Eu = sum(umodel**2.0) #User model energy
    
    #Energy normalization
    if Et>Eu:
        energy = Eu/Et
    else:
        energy = Et/Eu
        
    ediff = (Et-Eu)/Et #Energy difference
    
    txc = max(xcorr2(tmodel, tmodel)) #True model auto-correlation
    xc = max(xcorr2(tmodel, umodel))  #Cross-correlation: true and user model
    corr = xc/txc #normalized cross-correlation
    
    total = np.round(corr*energy, decimals=2) #Total similarity


    #Dictionary with all the similarities.    
    results = {'total':100.0*total, 'coor': 100.0*corr, 
    'Energy':100.0*energy, 'Ediff':100.0*ediff}
    
    return results
    
def ExportResults(tmodel, umodel, arq='results.txt', fileDir="..\static\Data\\"):
    
    '''
    Function ExportResults: compute and exports the results to json file.
    
    Input:
    tmodel: true model (array)
    umodel: usermodel (array)
    
    Output:
    None
    
    '''
    
    results = Results(tmodel, umodel)
    
    arqPath = fileDir + arq
    
    with open(arqPath, 'w') as outfile:
        json.dump(results, outfile)
import numpy as np
import pandas as pd

import sklearn.linear_model
import sklearn.preprocessing
import sklearn.model_selection

import scipy.stats as sstats
import statsmodels.stats.multitest as multitest

import scipy.io as sio
import h5py

import os


class GlucoseDecoder:
    def __init__(self, model, linear_correction=True,normalize=True):
        self.model = model
        self.TF_scaler = sklearn.preprocessing.StandardScaler()
        
        if linear_correction:
            self.linear_correction = sklearn.linear_model.LinearRegression()
        else:
            self.linear_correction = None
        
        self.fit_complete = False
        self.normalize = normalize

    def fit_model(self,linkedTF,linkedBG):
        if self.normalize:
            # Renormalize Time-Frequency Data to z-scores
            linkedTF_normalized = self.TF_scaler.fit_transform(linkedTF)
        else:
            linkedTF_normalized = linkedTF
        
        # Perform model fit
        self.model.fit(linkedTF_normalized,linkedBG)
        predictions = self.model.predict(linkedTF_normalized).T
        
        # Fit in second linear model if requested
        if self.linear_correction is not None:
            self.linear_correction.fit(predictions.reshape(-1, 1),linkedBG.reshape(-1, 1))
            predictions_corrected = self.linear_correction.predict(predictions.reshape(-1, 1))
            #predictions = predictions_corrected
        else:
            predictions_corrected = predictions
        
        if np.std(linkedBG) == 0 or np.std(predictions_corrected) == 0:
            rvalue = 0
        else:
            rvalue = np.corrcoef(linkedBG.T,predictions_corrected.T)[0,1]
        
        self.fit_complete = True
        return (predictions,predictions_corrected,rvalue)
    
    def predict(self,linkedTF,linkedBG=None):
        if not self.fit_complete:
            raise RuntimeError("Model not fit yet!")
        
        linkedTF_normalized = self.TF_scaler.fit_transform(linkedTF)
        predictions = self.model.predict(linkedTF_normalized).T
        
        
        # Use second linear model if requested
        if self.linear_correction is not None:
            predictions = self.linear_correction.predict(predictions.reshape(-1, 1))
            
        if linkedBG is not None:
            if np.std(linkedBG) == 0 or np.std(predictions) == 0:
                rvalue = 0
            else:
                rvalue = np.corrcoef(linkedBG.T,predictions.T)[0,1]
            return (predictions,rvalue)
        
        return predictions
    
    
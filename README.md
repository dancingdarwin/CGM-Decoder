# Spectro-spatial features in distributed human intracranial activity proactively encode peripheral metabolic activity
CGM Decoder Demo for submission to Nature Communciations.

Authors: Huang, Y.\*, Wang, J.B.\*, Parker, J.J., Shivacharan, R., Lal, R.A., Halpern. C.H.

## Dependencies
* h5py >= 2.10.0
* numpy >= 1.19.2
* scikit_learn >= 1.1.2
* scipy >= 1.5.4

## Installation
Runs out of the box assuming dependencies have been installed. Installation time is negligible.

## Running the Code
`CGM_Decoder.ipynb` provides a minimal example of the decoder trained and tested on data for a single patient without any time delay.

The core of the decoder runs out of the `GlucoseDecoder` class in `Decoder.py`. It has several key functions:

### Constructor
```
Decoder(model, linear_correction=True,normalize=True)
```
Inputs:
* `model` is the choice of model, in our case a LASSO as implemented in SKLearn
* `linear_correction` applies a second linear model after the LASSO fit
* `normalize` will normalize all inputs to unit variance prior to model application.


### Fitting a model
```
(predictions,predictions_corrected,rvalue) = fit_model(linkedTF,linkedBG)
```
Inputs:
* `linkedTF` is a $ N\times M$ array where $N$ is the number of time points, and $M$ is the number of features (e.g. combinations of electrodes and frequency band)
* `linkedBG` is a $N\times1$ array listing the blood glucose corresponding to each time point.

Outputs:
* `predictions` is an $N\times1$ array listing the predicted blood glucose prior to linear correction discussed above
* `predictions_corrected` is an $N\times1$ array listing the predicted blood glucose after linear correction discussed above. Assuming default settings this should be the prediction used
* `rvalue` is the Pearson Correlation between corrected predicted and actual blood glucose values

### Predicting with the model
```
predictions = predict(self,linkedTF,linkedBG=None)
```
Inputs:
* `linkedTF` is a $ N\times M$ array where $N$ is the number of time points, and $M$ is the number of features (e.g. combinations of electrodes and frequency band)
* `linkedBG` is an *optional* $N\times1$ array listing the blood glucose corresponding to each time point

Outputs:
* `predictions` is an $N\times1$ array listing the predicted blood glucose after linear correction discussed above
* `rvalue` is the Pearson Correlation between corrected predicted and actual blood glucose values if `linkedBG` is provided
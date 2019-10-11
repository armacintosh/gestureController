# Generated with SMOP  0.41
from libsmop import *
# calcRMS.m

    
@function
def calcRMS(EMGb=None,*args,**kwargs):
    varargin = calcRMS.varargin
    nargin = calcRMS.nargin

    # Returns the RMS in each bin
    
    # for when there is ia 3 dimensionial array, 3rd D is nFrames
    winLen,nCH,nFrames=size(EMGb,nargout=3)
# calcRMS.m:5
    
    answ=rms(EMGb(arange(),arange(),arange()),1)
# calcRMS.m:7
    
    # this is an array  nCH colomuns long and N bin rows
    rms_OUT=reshape(answ,concat([nCH,nFrames])).T
# calcRMS.m:10
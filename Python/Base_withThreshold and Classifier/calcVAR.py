# Generated with SMOP  0.41
from libsmop import *
# calcVAR.m

    
@function
def calcVAR(EMGb=None,*args,**kwargs):
    varargin = calcVAR.varargin
    nargin = calcVAR.nargin

    # Returns the Var in each bin
    
    # for when there is ia 3 dimensionial array, 3rd D is nFrames
    winLen,nCH,nFrames=size(EMGb,nargout=3)
# calcVAR.m:5
    
    # answ = var(binned_signal,0,2);
# ABS already done
    answ=var(EMGb(arange(),arange(),arange()),1)
# calcVAR.m:9
    
    # this is an array  nCH colomuns long and N bin rows
    answ_OUT=reshape(answ,concat([nCH,nFrames])).T
# calcVAR.m:12
# Generated with SMOP  0.41
from libsmop import *
# calcCCI.m

    
@function
def calcCCI(EMGb=None,const=None,*args,**kwargs):
    varargin = calcCCI.varargin
    nargin = calcCCI.nargin

    try:
        senE=const.Cal_extensor_sensors
# calcCCI.m:4
        senF=const.Cal_flexor_sensors
# calcCCI.m:5
    finally:
        pass
    
    
    # for when there is ia 3 dimensionial array, 3rd D is nFrames
    winLen,nCH,nFrames=size(EMGb,nargout=3)
# calcCCI.m:12
    
    # RMS
    preCCI=rms(EMGb(arange(),concat([senE,senF]),arange()),1)
# calcCCI.m:15
    
    rmsEx=mean(preCCI(arange(),arange(1,2),arange()),2)
# calcCCI.m:17
    rmsFx=mean(preCCI(arange(),arange(3,4),arange()),2)
# calcCCI.m:18
    # Should be 1 col * nFrames rows
    answ=rmsEx / rmsFx
# calcCCI.m:21
    # this is an array  N bin rows and 1 colomuns
    CCI_OUT=reshape(answ,concat([1,nFrames])).T
# calcCCI.m:25
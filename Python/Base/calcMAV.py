# Generated with SMOP  0.41
from libsmop import *
# calcMAV.m

    
@function
def calcMAV(EMGb=None,*args,**kwargs):
    varargin = calcMAV.varargin
    nargin = calcMAV.nargin

    # for when there is ia 3 dimensionial array, 3rd D is nFrames
    winLen,nCH,nFrames=size(EMGb,nargout=3)
# calcMAV.m:4
    
    # ABS already done
    answ=mean(EMGb(arange(),arange(),arange()),1)
# calcMAV.m:7
    
    # this is an array  nCH colomuns long and N bin rows
    answ_OUT=reshape(answ,concat([nCH,nFrames])).T
# calcMAV.m:10
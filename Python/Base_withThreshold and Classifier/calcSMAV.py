# Generated with SMOP  0.41
from libsmop import *
# calcSMAV.m

    
@function
def calcSMAV(EMGb=None,*args,**kwargs):
    varargin = calcSMAV.varargin
    nargin = calcSMAV.nargin

    # Channel MAV scaled to average of whole arm at that instant.
    
    if isa(EMGb,'double'):
        # for when there is ia 3 dimensionial array, 3rd D is nFrames
        __,nCH,nFrames=size(EMGb,nargout=3)
# calcSMAV.m:9
        preMMAV=mean(EMGb,1)
# calcSMAV.m:11
        MMAV=mean(preMMAV,2)
# calcSMAV.m:12
        smav=preMMAV / MMAV
# calcSMAV.m:14
        # reshape
    # this is an array  nCH colomuns long and N bin rows
        smav_OUT=reshape(smav,concat([nCH,nFrames])).T
# calcSMAV.m:18
    
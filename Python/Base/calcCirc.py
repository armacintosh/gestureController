# Generated with SMOP  0.41
from libsmop import *
# calcCirc.m

    
@function
def calcCirc(EMGb=None,const=None,calcOnFtName=None,*args,**kwargs):
    varargin = calcCirc.varargin
    nargin = calcCirc.nargin

    ##
    
    __,nCH,nFrames=size(EMGb,nargout=3)
# calcCirc.m:5
    
    preMMAV=mean(EMGb,1)
# calcCirc.m:6
    
    mav=reshape(preMMAV,concat([nFrames,nCH]))
# calcCirc.m:7
    ## Using Circstat2012a toolbox
    
    if 'circMean' == calcOnFtName:
        circStat[nFrames,1]=circ_mean(const.ori,mav(nFrames,arange()),2)
# calcCirc.m:16
    else:
        if 'circVar' == calcOnFtName:
            circStat[nFrames,1]=circ_var(const.ori,mav(nFrames,arange()),const.dori,2)
# calcCirc.m:18
        else:
            if 'circStd' == calcOnFtName:
                circStat[nFrames,1]=circ_std(const.ori,mav(nFrames,arange()),const.dori,2)
# calcCirc.m:20
            else:
                if 'circSkw' == calcOnFtName:
                    circStat[nFrames,1]=circ_skewness(const.ori,mav(nFrames,arange()),2)
# calcCirc.m:22
                else:
                    if 'circKrt' == calcOnFtName:
                        circStat[nFrames,1]=circ_kurtosis(const.ori,mav(nFrames,arange()),2)
# calcCirc.m:24
                    else:
                        if 'circR' == calcOnFtName:
                            circStat[nFrames,1]=circ_r(const.ori,mav(nFrames,arange()),const.dori,2)
# calcCirc.m:26
    
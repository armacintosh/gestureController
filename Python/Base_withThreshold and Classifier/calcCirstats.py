# Generated with SMOP  0.41
from libsmop import *
# calcCirstats.m

    
@function
def calcCirstats(EMGb=None,*args,**kwargs):
    varargin = calcCirstats.varargin
    nargin = calcCirstats.nargin

    ##
    
    __,nCH,nFrames=size(EMGb,nargout=3)
# calcCirstats.m:5
    
    preMMAV=mean(EMGb,1)
# calcCirstats.m:6
    
    mav=reshape(preMMAV,concat([nFrames,nCH]))
# calcCirstats.m:7
    OriIncrement=pi / (size(mav,2) / 2)
# calcCirstats.m:9
    
    ori=arange(0,dot(2,pi) - OriIncrement,OriIncrement)
# calcCirstats.m:10
    dori=diff(ori(arange(1,2)))
# calcCirstats.m:11
    
    R,C=size(mav,nargout=2)
# calcCirstats.m:12
    ##
    
    # would like to make these into array functions.
    circMean,circVar,circStd,circSkw,circKrt,circR=deal(zeros(R,1),nargout=6)
# calcCirstats.m:17
    for bin in arange(1,R).reshape(-1):
        # store circ stat values for each bin
        circMean[bin,1]=circ_mean(ori,mav(bin,arange()),2)
# calcCirstats.m:20
        circVar[bin,1]=circ_var(ori,mav(bin,arange()),dori,2)
# calcCirstats.m:21
        circStd[bin,1]=circ_std(ori,mav(bin,arange()),dori,2)
# calcCirstats.m:22
        circSkw[bin,1]=circ_skewness(ori,mav(bin,arange()),2)
# calcCirstats.m:23
        circKrt[bin,1]=circ_kurtosis(ori,mav(bin,arange()),2)
# calcCirstats.m:24
        circR[bin,1]=circ_r(ori,mav(bin,arange()),dori,2)
# calcCirstats.m:25
    
    circTbl=table(circMean,circVar,circStd,circSkw,circKrt,circR)
# calcCirstats.m:29
    circTbl.Properties.VariableNames = copy(cellarray(['C_circMean','C_circVar','C_circStd','C_circSkw','C_circKrt','C_circR']))
# calcCirstats.m:30
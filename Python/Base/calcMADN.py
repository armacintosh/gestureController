# Generated with SMOP  0.41
from libsmop import *
# calcMADN.m

    
@function
def calcMADN(EMGb=None,*args,**kwargs):
    varargin = calcMADN.varargin
    nargin = calcMADN.nargin

    # described from: https://bidal.sfsu.edu/~kazokada/research/okada_embc17_myoFeature.pdf v
    
    if isa(EMGb,'double'):
        ##
    # for when there is ia 3 dimensionial array, 3rd D is nFrames
        winLen,nCH,nFrames=size(EMGb,nargout=3)
# calcMADN.m:7
        # each window of data first has its mean value subtracted from each raw data point
        preMMAV=mean(EMGb,1)
# calcMADN.m:10
        frameMean=mean(preMMAV,2)
# calcMADN.m:11
        C=EMGb - frameMean
# calcMADN.m:12
        frameVals=reshape(EMGb,concat([dot(winLen,nCH),nFrames]))
# calcMADN.m:15
        frameSTD=std(frameVals)
# calcMADN.m:16
        frameSTD=reshape(frameSTD,concat([1,1,nFrames]))
# calcMADN.m:17
        D=C / frameSTD
# calcMADN.m:20
        # Numerator:
        # element wise abs diff between nCH and nCH+1
        Dif18=abs(D(arange(),1,arange()) - D(arange(),nCH,arange()))
# calcMADN.m:27
        y=abs(diff(D,[],2))
# calcMADN.m:28
        y=concat([y,Dif18])
# calcMADN.m:29
        ySum=sum(y)
# calcMADN.m:32
        madn=ySum / winLen
# calcMADN.m:35
        madn_OUT=reshape(madn,concat([nCH,nFrames])).T
# calcMADN.m:38
    
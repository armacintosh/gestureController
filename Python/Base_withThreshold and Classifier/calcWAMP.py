# Generated with SMOP  0.41
from libsmop import *
# calcWAMP.m

    
@function
def calcWAMP(EMGb=None,*args,**kwargs):
    varargin = calcWAMP.varargin
    nargin = calcWAMP.nargin

    # Calculates the Willison amplitude (WAMP) of a bin
    
    # WAMP equals the number of times the absolute difference between
# two consecutive EMG samples exceeds a predetermined threshold
    R,C,F=size(EMGb,nargout=3)
# calcWAMP.m:6
    absdiff=abs(diff(EMGb,[],1))
# calcWAMP.m:9
    answ=zeros(1,C,F)
# calcWAMP.m:11
    for f in arange(1,F).reshape(-1):
        for i in arange(1,C).reshape(-1):
            thresh=abs(mean(prctile(absdiff(arange(),i,arange()),20)))
# calcWAMP.m:14
            count=0
# calcWAMP.m:15
            for j in arange(1,R - 1).reshape(-1):
                if absdiff(j,i,f) >= thresh:
                    count=count + 1
# calcWAMP.m:18
            answ[1,i,f]=count
# calcWAMP.m:21
    
    answ_OUT=reshape(answ,concat([C,F])).T
# calcWAMP.m:25
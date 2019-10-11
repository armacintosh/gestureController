# Generated with SMOP  0.41
from libsmop import *
# calcZC.m

    
@function
def calcZC(EMGb=None,*args,**kwargs):
    varargin = calcZC.varargin
    nargin = calcZC.nargin

    # Returns the number of times the signal amplitude in each bin crosses the Thresh
    
    R,C,F=size(EMGb,nargout=3)
# calcZC.m:4
    answ=zeros(1,C,F)
# calcZC.m:6
    for f in arange(1,F).reshape(-1):
        for i in arange(1,C).reshape(-1):
            thresh=abs(mean(prctile(EMGb(arange(),i,arange()),50)))
# calcZC.m:9
            #         thresh = 0;
            count=0
# calcZC.m:11
            for j in arange(1,R - 2).reshape(-1):
                if ((((EMGb(j,i,f) > 0) and (EMGb(j + 1,i,f) < 0)) or ((EMGb(j,i,f) < 0) and (EMGb(j + 1,i,f) > 0))) and ((abs(EMGb(j,i,f)) >= thresh) or (abs(EMGb(j + 1,i,f)) >= thresh))):
                    count=count + 1
# calcZC.m:17
            answ[1,i,f]=count
# calcZC.m:20
    
    answ_OUT=reshape(answ,concat([C,F])).T
# calcZC.m:24
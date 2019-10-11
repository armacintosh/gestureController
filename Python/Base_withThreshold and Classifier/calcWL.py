# Generated with SMOP  0.41
from libsmop import *
# calcWL.m

    
@function
def calcWL(EMGb=None,*args,**kwargs):
    varargin = calcWL.varargin
    nargin = calcWL.nargin

    # Returns the waveform length for the signal in each bin
##
    R,C,F=size(EMGb,nargout=3)
# calcWL.m:4
    answ=zeros(1,C,F)
# calcWL.m:5
    for f in arange(1,F).reshape(-1):
        for i in arange(1,C).reshape(-1):
            len_=0
# calcWL.m:8
            for j in arange(1,R - 1).reshape(-1):
                len_=len_ + abs(EMGb(j + 1,i,f) - EMGb(j,i,f))
# calcWL.m:10
            answ[1,i,f]=len_
# calcWL.m:12
    
    answ_OUT=reshape(answ,concat([C,F])).T
# calcWL.m:17
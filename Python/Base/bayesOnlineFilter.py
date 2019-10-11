# Generated with SMOP  0.41
from libsmop import *
# bayesOnlineFilter.m

    
@function
def bayesOnlineFilter(param=None,Data_=None,*args,**kwargs):
    varargin = bayesOnlineFilter.varargin
    nargin = bayesOnlineFilter.nargin

    # perform the filtering
    bayesSTD=zeros(size(Data_))
# bayesOnlineFilter.m:4
    for j in arange(1,size(Data_,2)).reshape(-1):
        for i in arange(1,size(Data_,1)).reshape(-1):
            bayesSTD(i,j),param.pri=BayesFilter(Data_(i,j),param.pri,param.sig,param,nargout=2)
# bayesOnlineFilter.m:7
    
    emgF=dot(bayesSTD,param.sigmaMVC)
# bayesOnlineFilter.m:10
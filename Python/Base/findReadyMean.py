# Generated with SMOP  0.41
from libsmop import *
# findReadyMean.m

    
@function
def findReadyMean(const=None,calData=None,*args,**kwargs):
    varargin = findReadyMean.varargin
    nargin = findReadyMean.nargin

    # index of start
    strtInd=const.CalGoTime
# findReadyMean.m:4
    
    # Gets data recorded during 'ready set go'
    ExRaw=calData.cal(arange(1,strtInd),arange(2,end()))
# findReadyMean.m:7
    # find the mean of the phase before starting to extend, the mean of bottom 90# of activity
    ExSum=sum(ExRaw,2)
# findReadyMean.m:10
    
    __,i=sort(ExSum,nargout=2)
# findReadyMean.m:11
    
    iuse=i(arange(1,floor(length(ExRaw) / 2)))
# findReadyMean.m:12
    # 1 row of mean values during ready position const.myoCHsUsed(2:end) cols long
    const.ReadyMean = copy(mean(ExRaw(iuse,arange())))
# findReadyMean.m:15
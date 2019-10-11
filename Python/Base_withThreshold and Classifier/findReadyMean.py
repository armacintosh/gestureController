# Generated with SMOP  0.41
from libsmop import *
# findReadyMean.m

    
@function
def findReadyMean(const=None,calData=None,*args,**kwargs):
    varargin = findReadyMean.varargin
    nargin = findReadyMean.nargin

    # index of const.startTime1_active -- is when it changed from rest to active
    strtInd=calData.switch1
# findReadyMean.m:4
    # Gets data recorded during 'ready set go'
    ExRaw=calData.cal(arange(1,strtInd),arange(2,end()))
# findReadyMean.m:7
    # find the mean of the phase before starting to extend, the mean of bottom 90# of activity
    Ready=ExRaw(ExRaw(arange(1,strtInd)) == prctile(ExRaw(arange(1,strtInd)),50),arange())
# findReadyMean.m:10
    # 1 row of mean values during ready position const.myoCHsUsed(2:end) cols long
    const.ReadyMean = copy(mean(Ready))
# findReadyMean.m:13
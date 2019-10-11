# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_findReadyMean.m

    
@function
def classifyCalibrations_findReadyMean(restData=None,*args,**kwargs):
    varargin = classifyCalibrations_findReadyMean.varargin
    nargin = classifyCalibrations_findReadyMean.nargin

    ##
    restData=restData(arange(),arange(2,end()))
# classifyCalibrations_findReadyMean.m:4
    
    restData=abs(restData[arange(),arange()]) / 128
# classifyCalibrations_findReadyMean.m:5
    
    # find the mean of the phase before starting to extend, the mean of bottom 90# of activity
# only keep the middle 50# of the data
    Ready=copy(restData)
# classifyCalibrations_findReadyMean.m:9
    ReadyMean=zeros(1,size(Ready,2))
# classifyCalibrations_findReadyMean.m:10
    p=prctile(restData,concat([5,95]))
# classifyCalibrations_findReadyMean.m:11
    for col in arange(1,size(Ready,2)).reshape(-1):
        mid=Ready(Ready(arange(),col) >= p(1,col))
# classifyCalibrations_findReadyMean.m:13
        mid=mid(mid <= p(2,col))
# classifyCalibrations_findReadyMean.m:14
        ReadyMean[1,col]=mean(mid)
# classifyCalibrations_findReadyMean.m:15
    
    ##
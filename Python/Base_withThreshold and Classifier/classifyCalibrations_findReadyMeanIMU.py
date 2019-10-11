# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_findReadyMeanIMU.m

    
@function
def classifyCalibrations_findReadyMeanIMU(restData=None,*args,**kwargs):
    varargin = classifyCalibrations_findReadyMeanIMU.varargin
    nargin = classifyCalibrations_findReadyMeanIMU.nargin

    ##
    restData=restData[arange(),arange(2,end())]
# classifyCalibrations_findReadyMeanIMU.m:4
    
    # restData = abs(restData {:,:}) ./ 128; # change units of EMG
    
    # find the mean of the phase before starting to extend, the mean of bottom 90# of activity
# only keep the middle 50# of the data
    ReadyMean=mean(restData)
# classifyCalibrations_findReadyMeanIMU.m:9
    ##
# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_binDataIMU.m

    
@function
def classifyCalibrations_binDataIMU(IMU=None,EMGb=None,const=None,*args,**kwargs):
    varargin = classifyCalibrations_binDataIMU.varargin
    nargin = classifyCalibrations_binDataIMU.nargin

    # matches the number of bins from the EMG Bin.
    Dd=IMU[arange(),arange(2,end())]
# classifyCalibrations_binDataIMU.m:4
    
    # WINBIN rows * NCH cols * N Frames of time
    remainder=rem(size(Dd,1),round(const.WINBIN / 4))
# classifyCalibrations_binDataIMU.m:7
    
    x=Dd(arange(1,end() - remainder),arange())
# classifyCalibrations_binDataIMU.m:8
    x=x.T
# classifyCalibrations_binDataIMU.m:9
    x=ravel(x)
# classifyCalibrations_binDataIMU.m:10
    Db=permute(reshape(x,size(Dd,2),round(const.WINBIN / 4),[]),concat([2,1,3]))
# classifyCalibrations_binDataIMU.m:12
    
    # Take the smaller of the 2 binned samples
    nBinsEMG=size(EMGb,3)
# classifyCalibrations_binDataIMU.m:16
    nBinsIMU=size(Db,3)
# classifyCalibrations_binDataIMU.m:17
    cutTo=min(concat([nBinsEMG,nBinsIMU]))
# classifyCalibrations_binDataIMU.m:18
    EMGb=EMGb(arange(),arange(),arange(1,cutTo))
# classifyCalibrations_binDataIMU.m:20
    IMUb=Db(arange(),arange(),arange(1,cutTo))
# classifyCalibrations_binDataIMU.m:21
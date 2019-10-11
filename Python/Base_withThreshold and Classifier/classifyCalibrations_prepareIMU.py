# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_prepareIMU.m

    
@function
def classifyCalibrations_prepareIMU(Data_=None,const=None,ind=None,*args,**kwargs):
    varargin = classifyCalibrations_prepareIMU.varargin
    nargin = classifyCalibrations_prepareIMU.nargin

    ##
    
    ## Get resting data (ReadyMean)
    
    RestUse=concat([arange(ind.IMU.startTime1_rest,ind.IMU.startTime1_active),arange(ind.IMU.startTime2_rest,ind.IMU.startTime2_active),arange(ind.IMU.startTime3_rest,ind.IMU.startTime3_active)])
# classifyCalibrations_prepareIMU.m:7
    IMUReady=Data_.IMU(RestUse,arange())
# classifyCalibrations_prepareIMU.m:11
    
    ReadyMeanIMU=classifyCalibrations_findReadyMean(IMUReady)
# classifyCalibrations_prepareIMU.m:12
    
    ## FIND CORRECT IMU DATA
    
    # Fingers Open
    E2=Data_.IMU(arange(ind.IMU.startTime1_active,ind.IMU.startTime1_end),arange())
# classifyCalibrations_prepareIMU.m:17
    TL=dot(ones(size(E2,1),1),2)
# classifyCalibrations_prepareIMU.m:18
    E2=concat([E2,array2table(TL)])
# classifyCalibrations_prepareIMU.m:19
    # Fingers closed
    E1=Data_.IMU(arange(ind.IMU.startTime2_active,ind.IMU.startTime2_end),arange())
# classifyCalibrations_prepareIMU.m:22
    
    TL=ones(size(E1,1),1)
# classifyCalibrations_prepareIMU.m:23
    E1=concat([E1,array2table(TL)])
# classifyCalibrations_prepareIMU.m:24
    # Pinch
    E3=Data_.IMU(arange(ind.IMU.startTime3_active,ind.IMU.startTime3_end),arange())
# classifyCalibrations_prepareIMU.m:27
    
    TL=dot(ones(size(E3,1),1),3)
# classifyCalibrations_prepareIMU.m:28
    E3=concat([E3,array2table(TL)])
# classifyCalibrations_prepareIMU.m:29
    IMU=concat([[E2],[E1],[E3]])
# classifyCalibrations_prepareIMU.m:31
    
    IMU.Properties.VariableNames = copy(cellarray(['time','Accel_x','Accel_y','Accel_z','Gyro_x','Gyro_y','Gyro_z','Orient_x','Orient_y','Orient_z','Orient_w','TL']))
# classifyCalibrations_prepareIMU.m:32
    IMU[arange(),arange(2,end() - 1)]=IMU[arange(),arange(2,end() - 1)] - ReadyMeanIMU
# classifyCalibrations_prepareIMU.m:33
    
    D_IMUF=copy(IMU)
# classifyCalibrations_prepareIMU.m:35
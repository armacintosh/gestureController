# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_calcFtTbl.m

    
@function
def classifyCalibrations_calcFtTbl(Data_=None,*args,**kwargs):
    varargin = classifyCalibrations_calcFtTbl.varargin
    nargin = classifyCalibrations_calcFtTbl.nargin

    ## Setup
    
    const=Data_.const
# classifyCalibrations_calcFtTbl.m:5
    ## Setup data set to use for calibraiton
    
    # const.startTime1_rest; # Pressed enter for Gesture: Fingers Active  
# const.startTime1_active; # switched from rest to active for Gesture: Fingers active
# const.startTime1_end; # the last time element for the gesture Fingers Active
    
    # The last time elements for getsture: 
# extension with fingers open
    E1=find(Data_.Trial.pressed == 10,1,'last')
# classifyCalibrations_calcFtTbl.m:15
    const.startTime1_end = copy(Data_.Trial.time(E1))
# classifyCalibrations_calcFtTbl.m:16
    # extended fingers relaxed
    E2=find(Data_.Trial.pressed == 20,1,'last')
# classifyCalibrations_calcFtTbl.m:18
    const.startTime2_end = copy(Data_.Trial.time(E2))
# classifyCalibrations_calcFtTbl.m:19
    # pinch
    E3=find(Data_.Trial.pressed == 30,1,'last')
# classifyCalibrations_calcFtTbl.m:21
    const.startTime3_end = copy(Data_.Trial.time(E3))
# classifyCalibrations_calcFtTbl.m:22
    ## find time index of EMG and IMU to use
    
    # Raw data indicies for Fingers Open Gesture calibration
    ind.EMG.startTime1_rest = copy(find(Data_.EMG.Time >= const.startTime1_rest,1,'first'))
# classifyCalibrations_calcFtTbl.m:28
    ind.EMG.startTime1_active = copy(find(Data_.EMG.Time >= const.startTime1_active,1,'first'))
# classifyCalibrations_calcFtTbl.m:29
    ind.EMG.startTime1_end = copy(find(Data_.EMG.Time >= const.startTime1_end,1,'first'))
# classifyCalibrations_calcFtTbl.m:30
    ind.IMU.startTime1_rest = copy(find(Data_.IMU.Time >= const.startTime1_rest,1,'first'))
# classifyCalibrations_calcFtTbl.m:31
    ind.IMU.startTime1_active = copy(find(Data_.IMU.Time >= const.startTime1_active,1,'first'))
# classifyCalibrations_calcFtTbl.m:32
    ind.IMU.startTime1_end = copy(find(Data_.IMU.Time >= const.startTime1_end,1,'first'))
# classifyCalibrations_calcFtTbl.m:33
    # Raw data indicies for Fingers CLOSED Gesture calibration
    ind.EMG.startTime2_rest = copy(find(Data_.EMG.Time >= const.startTime2_rest,1,'first'))
# classifyCalibrations_calcFtTbl.m:36
    ind.EMG.startTime2_active = copy(find(Data_.EMG.Time >= const.startTime2_active,1,'first'))
# classifyCalibrations_calcFtTbl.m:37
    ind.EMG.startTime2_end = copy(find(Data_.EMG.Time >= const.startTime2_end,1,'first'))
# classifyCalibrations_calcFtTbl.m:38
    ind.IMU.startTime2_rest = copy(find(Data_.IMU.Time >= const.startTime2_rest,1,'first'))
# classifyCalibrations_calcFtTbl.m:39
    ind.IMU.startTime2_active = copy(find(Data_.IMU.Time >= const.startTime2_active,1,'first'))
# classifyCalibrations_calcFtTbl.m:40
    ind.IMU.startTime2_end = copy(find(Data_.IMU.Time >= const.startTime2_end,1,'first'))
# classifyCalibrations_calcFtTbl.m:41
    # Raw data indicies for Fingers Pinched Gesture calibration
    ind.EMG.startTime3_rest = copy(find(Data_.EMG.Time >= const.startTime3_rest,1,'first'))
# classifyCalibrations_calcFtTbl.m:44
    ind.EMG.startTime3_active = copy(find(Data_.EMG.Time >= const.startTime3_active,1,'first'))
# classifyCalibrations_calcFtTbl.m:45
    ind.EMG.startTime3_end = copy(find(Data_.EMG.Time >= const.startTime3_end,1,'first'))
# classifyCalibrations_calcFtTbl.m:46
    ind.IMU.startTime3_rest = copy(find(Data_.IMU.Time >= const.startTime3_rest,1,'first'))
# classifyCalibrations_calcFtTbl.m:47
    ind.IMU.startTime3_active = copy(find(Data_.IMU.Time >= const.startTime3_active,1,'first'))
# classifyCalibrations_calcFtTbl.m:48
    ind.IMU.startTime3_end = copy(find(Data_.IMU.Time >= const.startTime3_end,1,'first'))
# classifyCalibrations_calcFtTbl.m:49
    ## Organize calibration data into tables
    
    # returns filtered and raw data
# Prepare Raw EMG data
    const,D_EMG,D_EMGF=classifyCalibrations_prepareEMG(Data_,const,ind,nargout=3)
# classifyCalibrations_calcFtTbl.m:56
    
    # Prepare Raw IMU data
    const,D_IMU,D_IMUF=classifyCalibrations_prepareIMU(Data_,const,ind,nargout=3)
# classifyCalibrations_calcFtTbl.m:58
    
    ##
    
    # get main extensor sensor
    EM=D_EMGF.TL < 3
# classifyCalibrations_calcFtTbl.m:63
    
    EMGUse=table2array(D_EMGF(EM,arange(2,end() - 1)))
# classifyCalibrations_calcFtTbl.m:64
    x=mean(EMGUse)
# classifyCalibrations_calcFtTbl.m:65
    # get the index with highest activity
    __,I0=sort(x,'descend',nargout=2)
# classifyCalibrations_calcFtTbl.m:68
    y=const.EMGch(I0(1))
# classifyCalibrations_calcFtTbl.m:69
    
    ## Store
    
    calibrationData.EMG = copy(D_EMG)
# classifyCalibrations_calcFtTbl.m:74
    calibrationData.EMGf = copy(D_EMGF)
# classifyCalibrations_calcFtTbl.m:75
    calibrationData.IMU = copy(D_IMU)
# classifyCalibrations_calcFtTbl.m:76
    calibrationData.IMUf = copy(D_IMUF)
# classifyCalibrations_calcFtTbl.m:77
    ## BIN DATA
    
    # check WINBIN/4 must be int to have whole bins for IMU data
# this happens already in setupConst. Normally should not be an issue
    if mod(const.WINBIN / 4,1) == 0:
        # integer is good
        const.binsize = copy(const.WINBIN / const.sf)
# classifyCalibrations_calcFtTbl.m:85
    else:
        # change WINBIN so that WINBIN/4 is an integer
        const.WINBIN = copy(dot(4,round(const.WINBIN / 4)))
# classifyCalibrations_calcFtTbl.m:88
        const.binsize = copy(const.WINBIN / const.sf)
# classifyCalibrations_calcFtTbl.m:89
    
    D_EMGb,TLb=classifyCalibrations_binDataEMG(D_EMG,const,nargout=2)
# classifyCalibrations_calcFtTbl.m:92
    
    D_EMGFb,__=classifyCalibrations_binDataEMG(D_EMGF,const,nargout=2)
# classifyCalibrations_calcFtTbl.m:93
    
    D_IMUb,D_EMGb=classifyCalibrations_binDataIMU(D_IMU,D_EMGb,const,nargout=2)
# classifyCalibrations_calcFtTbl.m:95
    
    D_IMUFb,D_EMGFb=classifyCalibrations_binDataIMU(D_IMUF,D_EMGFb,const,nargout=2)
# classifyCalibrations_calcFtTbl.m:96
    
    ## calculate FtTbl
    
    # MAKE SURE THIS WORKS NOW
    FtTbl=makeFtTbl_Offline(D_EMGb,D_IMUb,D_EMGFb,D_IMUFb,const)
# classifyCalibrations_calcFtTbl.m:101
    ## add Truelabel
    
    TL=TLb(1,1,arange())
# classifyCalibrations_calcFtTbl.m:105
    TrueLabel=reshape(TL,size(TL,3),1)
# classifyCalibrations_calcFtTbl.m:106
    
    FtTbl=concat([array2table(TrueLabel),FtTbl])
# classifyCalibrations_calcFtTbl.m:107
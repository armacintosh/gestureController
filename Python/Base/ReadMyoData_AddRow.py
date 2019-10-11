# Generated with SMOP  0.41
from libsmop import *
# ReadMyoData_AddRow.m

    
@function
def ReadMyoData_AddRow(myo=None,const=None,state=None,*args,**kwargs):
    varargin = ReadMyoData_AddRow.varargin
    nargin = ReadMyoData_AddRow.nargin

    
    timestart=datetime()
# ReadMyoData_AddRow.m:4
    
    bSuccess=0
# ReadMyoData_AddRow.m:7
    try:
        # wait until enough data is there...
        while (myo.tEMG.BytesAvailable < 16):

            if const.errorChecking == 1:
                if seconds(datetime() - timestart) > const.secondsMissing:
                    const.playAstro = copy(0)
# ReadMyoData_AddRow.m:15
                    fprintf('time %.2f \n',seconds(datetime() - timestart))
                    try:
                        if isempty(findobj('type','figure','name','Restart Notice')):
                            const,myo,state,timestart=errorProcess(const,state,nargout=4)
# ReadMyoData_AddRow.m:21
                        if state.hadForceQuit == 1 or state.stopTrial == 1:
                            break
                    finally:
                        pass

        # reading myo data from myoserver (one row)
        dataRead=read(myo.tEMG,16,'int8')
# ReadMyoData_AddRow.m:46
        bSuccess=1
# ReadMyoData_AddRow.m:47
        myo.lastTimeEMG = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:48
    finally:
        pass
    
    
    # if it reads data, then put it into a emgData
    if (bSuccess == 1):
        timeInput=dataRead(arange(1,8))
# ReadMyoData_AddRow.m:56
        myo.emgData[myo.emgDataIndex,1]=typecast(int8(timeInput),'uint64')
# ReadMyoData_AddRow.m:57
        myo.emgData[myo.emgDataIndex,2]=myo.lastTimeEMG
# ReadMyoData_AddRow.m:58
        myo.emgData[myo.emgDataIndex,arange(3,10)]=dataRead(arange(9,16))
# ReadMyoData_AddRow.m:59
        myo.emgDataIndex = copy(myo.emgDataIndex + 1)
# ReadMyoData_AddRow.m:60
    
    
    #    read accelerometer
    bSuccess=0
# ReadMyoData_AddRow.m:64
    try:
        if (myo.tAccel.BytesAvailable >= 20):
            dataRead=read(myo.tAccel,20,'uint8')
# ReadMyoData_AddRow.m:67
            bSuccess=1
# ReadMyoData_AddRow.m:68
            myo.lastTime = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:69
    finally:
        pass
    
    if (bSuccess == 1):
        timeInput=dataRead(arange(1,8))
# ReadMyoData_AddRow.m:78
        myo.accelData[myo.accelDataIndex,1]=typecast(uint8(timeInput),'uint64')
# ReadMyoData_AddRow.m:79
        myo.accelData[myo.accelDataIndex,2]=myo.lastTime
# ReadMyoData_AddRow.m:80
        myo.accelData[myo.accelDataIndex,3]=typecast(uint8(dataRead(arange(9,12))),'single')
# ReadMyoData_AddRow.m:81
        myo.accelData[myo.accelDataIndex,4]=typecast(uint8(dataRead(arange(13,16))),'single')
# ReadMyoData_AddRow.m:82
        myo.accelData[myo.accelDataIndex,5]=typecast(uint8(dataRead(arange(17,20))),'single')
# ReadMyoData_AddRow.m:83
        myo.accelDataIndex = copy(myo.accelDataIndex + 1)
# ReadMyoData_AddRow.m:84
    
    
    
    #    read gyro
    bSuccess=0
# ReadMyoData_AddRow.m:90
    try:
        if (myo.tGyro.BytesAvailable >= 20):
            dataRead=read(myo.tGyro,20,'uint8')
# ReadMyoData_AddRow.m:93
            bSuccess=1
# ReadMyoData_AddRow.m:94
            myo.lastTime = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:95
    finally:
        pass
    
    if (bSuccess == 1):
        timeInput=dataRead(arange(1,8))
# ReadMyoData_AddRow.m:104
        myo.gyroData[myo.gyroDataIndex,1]=typecast(uint8(timeInput),'uint64')
# ReadMyoData_AddRow.m:105
        myo.gyroData[myo.gyroDataIndex,2]=myo.lastTime
# ReadMyoData_AddRow.m:106
        myo.gyroData[myo.gyroDataIndex,3]=typecast(uint8(dataRead(arange(9,12))),'single')
# ReadMyoData_AddRow.m:107
        myo.gyroData[myo.gyroDataIndex,4]=typecast(uint8(dataRead(arange(13,16))),'single')
# ReadMyoData_AddRow.m:108
        myo.gyroData[myo.gyroDataIndex,5]=typecast(uint8(dataRead(arange(17,20))),'single')
# ReadMyoData_AddRow.m:109
        myo.gyroDataIndex = copy(myo.gyroDataIndex + 1)
# ReadMyoData_AddRow.m:110
    
    #    read orientation
    bSuccess=0
# ReadMyoData_AddRow.m:114
    try:
        if (myo.tOrient.BytesAvailable >= 24):
            dataRead=read(myo.tOrient,24,'uint8')
# ReadMyoData_AddRow.m:117
            bSuccess=1
# ReadMyoData_AddRow.m:118
            myo.lastTime = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:119
    finally:
        pass
    
    if (bSuccess == 1):
        timeInput=dataRead(arange(1,8))
# ReadMyoData_AddRow.m:128
        myo.orientData[myo.orientDataIndex,1]=typecast(uint8(timeInput),'uint64')
# ReadMyoData_AddRow.m:129
        myo.orientData[myo.orientDataIndex,2]=myo.lastTime
# ReadMyoData_AddRow.m:130
        myo.orientData[myo.orientDataIndex,3]=typecast(uint8(dataRead(arange(9,12))),'single')
# ReadMyoData_AddRow.m:131
        myo.orientData[myo.orientDataIndex,4]=typecast(uint8(dataRead(arange(13,16))),'single')
# ReadMyoData_AddRow.m:132
        myo.orientData[myo.orientDataIndex,5]=typecast(uint8(dataRead(arange(17,20))),'single')
# ReadMyoData_AddRow.m:133
        myo.orientData[myo.orientDataIndex,6]=typecast(uint8(dataRead(arange(21,24))),'single')
# ReadMyoData_AddRow.m:134
        myo.orientDataIndex = copy(myo.orientDataIndex + 1)
# ReadMyoData_AddRow.m:135
    
    
    ##
  # read event
    bSuccess=0
# ReadMyoData_AddRow.m:141
    try:
        if (myo.tEvent.BytesAvailable > 0):
            dataRead=read(myo.tEvent,1,'int8')
# ReadMyoData_AddRow.m:144
            bSuccess=1
# ReadMyoData_AddRow.m:145
            myo.lastTime = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:146
    finally:
        pass
    
    
    if (bSuccess == 1):
        myo.eventData[myo.eventDataIndex,1]=myo.lastTime
# ReadMyoData_AddRow.m:153
        myo.eventData[myo.eventDataIndex,2]=dataRead
# ReadMyoData_AddRow.m:154
        myo.eventDataIndex = copy(myo.eventDataIndex + 1)
# ReadMyoData_AddRow.m:155
    
    
    # EVENT CODES 
    # 1: Connected to the myo device
    # 2: No data received from the myo device since {0}, attempting reconnection...
    # 3: Connected to the MyoConnect application
    # 4: Couldn't connect to the MyoConnect application, last timestamp {0}
    # 5: first time EMG data is received
    
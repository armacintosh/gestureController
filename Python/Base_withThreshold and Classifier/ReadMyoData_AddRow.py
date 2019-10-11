# Generated with SMOP  0.41
from libsmop import *
# ReadMyoData_AddRow.m

    
@function
def ReadMyoData_AddRow(myo=None,const=None,state=None,*args,**kwargs):
    varargin = ReadMyoData_AddRow.varargin
    nargin = ReadMyoData_AddRow.nargin

    
    timestart=datetime()
# ReadMyoData_AddRow.m:3
    
    bSuccess=0
# ReadMyoData_AddRow.m:6
    try:
        # wait until enough data is there...
        while (myo.tEMG.BytesAvailable < 16):

            # check how long it has been since last fill
#             fprintf('time since last : #.2f \n', seconds(datetime()-timestart));
#             fprintf('inError Status: #i \n',const.inError);
#             fprintf('myo.tEMG.BytesAvailable = #i \n\n', myo.tEMG.BytesAvailable);
            if const.errorChecking == 1:
                if seconds(datetime() - timestart) > 3:
                    #                     state.inError = 1;
                    const.playAstro = copy(0)
# ReadMyoData_AddRow.m:21
                    fprintf('time %.2f \n',seconds(datetime() - timestart))
                    #                     fprintf('const.inError ==  #i \n', const.inError);
                    # call the Error to restart myoConnect and myoServer
                    try:
                        if isempty(findobj('type','figure','name','Restart Notice')):
                            const,myo,state,timestart=errorProcess(const,state,nargout=4)
# ReadMyoData_AddRow.m:27
                        if state.hadForceQuit == 1:
                            break
                    finally:
                        pass
                    #                     [myo] = serverErrorReset(const);

        # reading myo data from myoserver (one row)
        dataRead=read(myo.tEMG,16,'int8')
# ReadMyoData_AddRow.m:52
        bSuccess=1
# ReadMyoData_AddRow.m:53
        myo.lastTimeEMG = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:54
    finally:
        pass
    
    
    # if it reads data, then put it into a emgData
    if (bSuccess == 1):
        timeInput=dataRead(arange(1,8))
# ReadMyoData_AddRow.m:65
        myo.emgData[myo.emgDataIndex,1]=typecast(int8(timeInput),'uint64')
# ReadMyoData_AddRow.m:66
        myo.emgData[myo.emgDataIndex,2]=myo.lastTimeEMG
# ReadMyoData_AddRow.m:67
        myo.emgData[myo.emgDataIndex,arange(3,10)]=dataRead(arange(9,16))
# ReadMyoData_AddRow.m:68
        myo.emgDataIndex = copy(myo.emgDataIndex + 1)
# ReadMyoData_AddRow.m:69
    
    
    #    read accelerometer
    bSuccess=0
# ReadMyoData_AddRow.m:73
    try:
        if (myo.tAccel.BytesAvailable >= 20):
            dataRead=read(myo.tAccel,20,'uint8')
# ReadMyoData_AddRow.m:76
            bSuccess=1
# ReadMyoData_AddRow.m:77
            myo.lastTime = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:78
    finally:
        pass
    
    if (bSuccess == 1):
        timeInput=dataRead(arange(1,8))
# ReadMyoData_AddRow.m:87
        myo.accelData[myo.accelDataIndex,1]=typecast(uint8(timeInput),'uint64')
# ReadMyoData_AddRow.m:88
        myo.accelData[myo.accelDataIndex,2]=myo.lastTime
# ReadMyoData_AddRow.m:89
        myo.accelData[myo.accelDataIndex,3]=typecast(uint8(dataRead(arange(9,12))),'single')
# ReadMyoData_AddRow.m:90
        myo.accelData[myo.accelDataIndex,4]=typecast(uint8(dataRead(arange(13,16))),'single')
# ReadMyoData_AddRow.m:91
        myo.accelData[myo.accelDataIndex,5]=typecast(uint8(dataRead(arange(17,20))),'single')
# ReadMyoData_AddRow.m:92
        myo.accelDataIndex = copy(myo.accelDataIndex + 1)
# ReadMyoData_AddRow.m:93
    
    
    
    #    read gyro
    bSuccess=0
# ReadMyoData_AddRow.m:99
    try:
        if (myo.tGyro.BytesAvailable >= 20):
            dataRead=read(myo.tGyro,20,'uint8')
# ReadMyoData_AddRow.m:102
            bSuccess=1
# ReadMyoData_AddRow.m:103
            myo.lastTime = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:104
    finally:
        pass
    
    if (bSuccess == 1):
        timeInput=dataRead(arange(1,8))
# ReadMyoData_AddRow.m:113
        myo.gyroData[myo.gyroDataIndex,1]=typecast(uint8(timeInput),'uint64')
# ReadMyoData_AddRow.m:114
        myo.gyroData[myo.gyroDataIndex,2]=myo.lastTime
# ReadMyoData_AddRow.m:115
        myo.gyroData[myo.gyroDataIndex,3]=typecast(uint8(dataRead(arange(9,12))),'single')
# ReadMyoData_AddRow.m:116
        myo.gyroData[myo.gyroDataIndex,4]=typecast(uint8(dataRead(arange(13,16))),'single')
# ReadMyoData_AddRow.m:117
        myo.gyroData[myo.gyroDataIndex,5]=typecast(uint8(dataRead(arange(17,20))),'single')
# ReadMyoData_AddRow.m:118
        myo.gyroDataIndex = copy(myo.gyroDataIndex + 1)
# ReadMyoData_AddRow.m:119
    
    #    read orientation
    bSuccess=0
# ReadMyoData_AddRow.m:123
    try:
        if (myo.tOrient.BytesAvailable >= 24):
            dataRead=read(myo.tOrient,24,'uint8')
# ReadMyoData_AddRow.m:126
            bSuccess=1
# ReadMyoData_AddRow.m:127
            myo.lastTime = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:128
    finally:
        pass
    
    if (bSuccess == 1):
        timeInput=dataRead(arange(1,8))
# ReadMyoData_AddRow.m:137
        myo.orientData[myo.orientDataIndex,1]=typecast(uint8(timeInput),'uint64')
# ReadMyoData_AddRow.m:138
        myo.orientData[myo.orientDataIndex,2]=myo.lastTime
# ReadMyoData_AddRow.m:139
        myo.orientData[myo.orientDataIndex,3]=typecast(uint8(dataRead(arange(9,12))),'single')
# ReadMyoData_AddRow.m:140
        myo.orientData[myo.orientDataIndex,4]=typecast(uint8(dataRead(arange(13,16))),'single')
# ReadMyoData_AddRow.m:141
        myo.orientData[myo.orientDataIndex,5]=typecast(uint8(dataRead(arange(17,20))),'single')
# ReadMyoData_AddRow.m:142
        myo.orientData[myo.orientDataIndex,6]=typecast(uint8(dataRead(arange(21,24))),'single')
# ReadMyoData_AddRow.m:143
        myo.orientDataIndex = copy(myo.orientDataIndex + 1)
# ReadMyoData_AddRow.m:144
    
    
    ##
  # read event
    bSuccess=0
# ReadMyoData_AddRow.m:150
    try:
        if (myo.tEvent.BytesAvailable > 0):
            dataRead=read(myo.tEvent,1,'int8')
# ReadMyoData_AddRow.m:153
            bSuccess=1
# ReadMyoData_AddRow.m:154
            myo.lastTime = copy(datenum(datetime()))
# ReadMyoData_AddRow.m:155
    finally:
        pass
    
    
    if (bSuccess == 1):
        myo.eventData[myo.eventDataIndex,1]=myo.lastTime
# ReadMyoData_AddRow.m:162
        myo.eventData[myo.eventDataIndex,2]=dataRead
# ReadMyoData_AddRow.m:163
        myo.eventDataIndex = copy(myo.eventDataIndex + 1)
# ReadMyoData_AddRow.m:164
    
    
    # EVENT CODES 
    # 1: Connected to the myo device
    # 2: No data received from the myo device since {0}, attempting reconnection...
    # 3: Connected to the MyoConnect application
    # 4: Couldn't connect to the MyoConnect application, last timestamp {0}
    # 5: first time EMG data is received
    
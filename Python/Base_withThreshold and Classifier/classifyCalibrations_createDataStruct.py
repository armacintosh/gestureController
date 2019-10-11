# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_createDataStruct.m

    
@function
def classifyCalibrations_createDataStruct(resultsPath=None,trialDataFiles=None,tr=None,*args,**kwargs):
    varargin = classifyCalibrations_createDataStruct.varargin
    nargin = classifyCalibrations_createDataStruct.nargin

    # get the file name
# trFileName = ParticipantVid.trialDataFileName{tr}; # for videoDate
    trFileName=trialDataFiles[tr]
# classifyCalibrations_createDataStruct.m:5
    
    # get the names of all corresponding files based on time string
# get file names --> to change to automatically by time.
    fileTrial=strcat(resultsPath,'trialData\',trFileName)
# classifyCalibrations_createDataStruct.m:9
    timeString=fileTrial(arange(end() - 16,end() - 4))
# classifyCalibrations_createDataStruct.m:10
    # get associated file names
    fileConst=strcat(resultsPath,'trialData\','trialConst_',timeString,'.mat')
# classifyCalibrations_createDataStruct.m:13
    fileEMG=strcat(resultsPath,'myoServer\EMG_',timeString,'.csv')
# classifyCalibrations_createDataStruct.m:14
    fileAccel=strcat(resultsPath,'myoServer\Accelerometer_',timeString,'.csv')
# classifyCalibrations_createDataStruct.m:15
    fileGyro=strcat(resultsPath,'myoServer\Gyroscope_',timeString,'.csv')
# classifyCalibrations_createDataStruct.m:16
    fileOrient=strcat(resultsPath,'myoServer\Orientation_',timeString,'.csv')
# classifyCalibrations_createDataStruct.m:17
    fileServer=strcat(resultsPath,'myoServer\Server_',timeString,'.csv')
# classifyCalibrations_createDataStruct.m:18
    d=dir(strcat(resultsPath,'gameData\Events_*_',timeString,'.csv'))
# classifyCalibrations_createDataStruct.m:20
    disp('Loading data, may take a minute...')
    ## Load data
    
    # make all import stuff into a function
    
    # import trialData
    fileID=fopen(fileTrial)
# classifyCalibrations_createDataStruct.m:28
    formatSpec='%s'
# classifyCalibrations_createDataStruct.m:29
    # get header
    tDHeader=textscan(fileID,'%[^\n]',1)
# classifyCalibrations_createDataStruct.m:32
    tDHeader=split(tDHeader[1,1],',').T
# classifyCalibrations_createDataStruct.m:33
    
    # get data
    tD=textscan(fileID,formatSpec,'HeaderLines',1)
# classifyCalibrations_createDataStruct.m:36
    tD=split(tD[1,1],',')
# classifyCalibrations_createDataStruct.m:37
    
    # format Time from str to datetime
    tDTime=datetime(tD(arange(),1),'InputFormat','HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:40
    tDTime.Format = copy('HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:41
    # format Other cols. from str. to num
    tDData=str2double(tD(arange(),arange(2,end())))
# classifyCalibrations_createDataStruct.m:44
    # put back together into table (or other usefule format)
    t1=array2table(tDTime)
# classifyCalibrations_createDataStruct.m:47
    t2=array2table(tDData)
# classifyCalibrations_createDataStruct.m:48
    trialData=concat([t1,t2])
# classifyCalibrations_createDataStruct.m:49
    trialData.Properties.VariableNames = copy(tDHeader)
# classifyCalibrations_createDataStruct.m:50
    # close file, and stuff I do not eed
    fclose(fileID)
    # clear_all_but ('resultsPath','trialData');
    
    # load const data
    load(fileConst)
    ## Load game data...
    
    gameData=[]
# classifyCalibrations_createDataStruct.m:61
    # put all events together:
    for lv in arange(1,length(d)).reshape(-1):
        fileEvenet=strcat(resultsPath,'gameData\',d(lv).name)
# classifyCalibrations_createDataStruct.m:65
        # need to just find the matching date/time end string
        fileID=fopen(fileEvenet)
# classifyCalibrations_createDataStruct.m:68
        formatSpec='%s'
# classifyCalibrations_createDataStruct.m:69
        tDHeader=textscan(fileID,'%[^\n]',1)
# classifyCalibrations_createDataStruct.m:72
        tDHeader=split(tDHeader[1,1],',').T
# classifyCalibrations_createDataStruct.m:73
        # get data
        tD=textscan(fileID,formatSpec,'HeaderLines',1,'Delimiter',',')
# classifyCalibrations_createDataStruct.m:76
        tDTime=tD[1,1](arange(1,end() - 1,2),arange())
# classifyCalibrations_createDataStruct.m:77
        tDTime=datetime(tDTime(arange(),1),'InputFormat','HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:78
        tDTime.Format = copy('HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:79
        tDEvent=tD[1,1](arange(2,end(),2),arange())
# classifyCalibrations_createDataStruct.m:82
        t1=array2table(tDTime)
# classifyCalibrations_createDataStruct.m:85
        t2=array2table(tDEvent)
# classifyCalibrations_createDataStruct.m:86
        gameDataf=concat([t1,t2])
# classifyCalibrations_createDataStruct.m:87
        fclose(fileID)
        gameData=concat([[gameData],[gameDataf]])
# classifyCalibrations_createDataStruct.m:93
    
    gameData.Properties.VariableNames = copy(tDHeader)
# classifyCalibrations_createDataStruct.m:96
    ## Load MyoServer Raw data
    
    ## EMG
    
    fileID=fopen(fileEMG)
# classifyCalibrations_createDataStruct.m:102
    formatSpec='%s'
# classifyCalibrations_createDataStruct.m:103
    # get header
    tDHeader=textscan(fileID,'%[^\n]',1)
# classifyCalibrations_createDataStruct.m:106
    tDHeader=split(tDHeader[1,1],',').T
# classifyCalibrations_createDataStruct.m:107
    
    # get data
    tD=textscan(fileID,formatSpec,'HeaderLines',1)
# classifyCalibrations_createDataStruct.m:110
    tD=split(tD[1,1],',')
# classifyCalibrations_createDataStruct.m:111
    
    # format Time from str to datetime
    tDTime=datetime(tD(arange(),1),'InputFormat','HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:114
    tDTime.Format = copy('HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:115
    # format Other cols. from str. to num
    tDData=str2double(tD(arange(),arange(3,end())))
# classifyCalibrations_createDataStruct.m:118
    
    # put back together into table (or other usefule format)
    t1=array2table(tDTime)
# classifyCalibrations_createDataStruct.m:121
    t2=array2table(tDData)
# classifyCalibrations_createDataStruct.m:122
    EMG=concat([t1,t2])
# classifyCalibrations_createDataStruct.m:123
    EMG.Properties.VariableNames = copy(concat([tDHeader(1),tDHeader(arange(3,end()))]))
# classifyCalibrations_createDataStruct.m:124
    # close file, and stuff I do not eed
    fclose(fileID)
    ## IMU
    
    fileID=fopen(fileAccel)
# classifyCalibrations_createDataStruct.m:131
    formatSpec='%s'
# classifyCalibrations_createDataStruct.m:132
    # get header
    tDHeader=textscan(fileID,'%[^\n]',1)
# classifyCalibrations_createDataStruct.m:135
    tDHeader=split(tDHeader[1,1],',').T
# classifyCalibrations_createDataStruct.m:136
    
    # get data
    tD=textscan(fileID,formatSpec,'HeaderLines',1)
# classifyCalibrations_createDataStruct.m:139
    tD=split(tD[1,1],',')
# classifyCalibrations_createDataStruct.m:140
    
    # format Time from str to datetime
    tDTime=datetime(tD(arange(),1),'InputFormat','HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:143
    tDTime.Format = copy('HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:144
    # format Other cols. from str. to num
    tDData=str2double(tD(arange(),arange(3,end())))
# classifyCalibrations_createDataStruct.m:147
    
    # put together into table (or other usefule format)
    t1=array2table(tDTime)
# classifyCalibrations_createDataStruct.m:150
    t2=array2table(tDData)
# classifyCalibrations_createDataStruct.m:151
    Accel=concat([t1,t2])
# classifyCalibrations_createDataStruct.m:152
    # add Accel to header of xyz
    AccelHeader=strcat('Accel_',tDHeader(arange(3,end())))
# classifyCalibrations_createDataStruct.m:155
    Accel.Properties.VariableNames = copy(concat([tDHeader(1),AccelHeader]))
# classifyCalibrations_createDataStruct.m:156
    # close file, and stuff I do not eed
    fclose(fileID)
    ##
    
    # GYRO
    fileID=fopen(fileGyro)
# classifyCalibrations_createDataStruct.m:164
    formatSpec='%s'
# classifyCalibrations_createDataStruct.m:165
    # get header
    tDHeader=textscan(fileID,'%[^\n]',1)
# classifyCalibrations_createDataStruct.m:168
    tDHeader=split(tDHeader[1,1],',').T
# classifyCalibrations_createDataStruct.m:169
    
    # get data
    tD=textscan(fileID,formatSpec,'HeaderLines',1)
# classifyCalibrations_createDataStruct.m:172
    tD=split(tD[1,1],',')
# classifyCalibrations_createDataStruct.m:173
    
    # format Time from str to datetime
    tDTime=datetime(tD(arange(),1),'InputFormat','HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:176
    tDTime.Format = copy('HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:177
    # format Other cols. from str. to num
    tDData=str2double(tD(arange(),arange(3,end())))
# classifyCalibrations_createDataStruct.m:180
    
    # put together into table (or other usefule format)
    t1=array2table(tDTime)
# classifyCalibrations_createDataStruct.m:183
    t2=array2table(tDData)
# classifyCalibrations_createDataStruct.m:184
    Gyro=concat([t1,t2])
# classifyCalibrations_createDataStruct.m:185
    # add Accel to header of xyz
    GyroHeader=strcat('Gyro_',tDHeader(arange(3,end())))
# classifyCalibrations_createDataStruct.m:188
    Gyro.Properties.VariableNames = copy(concat([tDHeader(1),GyroHeader]))
# classifyCalibrations_createDataStruct.m:189
    # close file, and stuff I do not eed
    fclose(fileID)
    ## Orientation
    
    fileID=fopen(fileOrient)
# classifyCalibrations_createDataStruct.m:197
    formatSpec='%s'
# classifyCalibrations_createDataStruct.m:198
    # get header
    tDHeader=textscan(fileID,'%[^\n]',1)
# classifyCalibrations_createDataStruct.m:201
    tDHeader=split(tDHeader[1,1],',').T
# classifyCalibrations_createDataStruct.m:202
    
    # get data
    tD=textscan(fileID,formatSpec,'HeaderLines',1)
# classifyCalibrations_createDataStruct.m:205
    tD=split(tD[1,1],',')
# classifyCalibrations_createDataStruct.m:206
    
    # format Time from str to datetime
    tDTime=datetime(tD(arange(),1),'InputFormat','HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:209
    tDTime.Format = copy('HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:210
    # format Other cols. from str. to num
    tDData=str2double(tD(arange(),arange(3,end())))
# classifyCalibrations_createDataStruct.m:213
    
    # put together into table (or other usefule format)
    t1=array2table(tDTime)
# classifyCalibrations_createDataStruct.m:216
    t2=array2table(tDData)
# classifyCalibrations_createDataStruct.m:217
    Orient=concat([t1,t2])
# classifyCalibrations_createDataStruct.m:218
    # add Accel to header of xyz
    OrientHeader=strcat('Orient_',tDHeader(arange(3,end())))
# classifyCalibrations_createDataStruct.m:221
    Orient.Properties.VariableNames = copy(concat([tDHeader(1),OrientHeader]))
# classifyCalibrations_createDataStruct.m:222
    # close file, and stuff I do not eed
    fclose(fileID)
    ## Server Events data
    
    fileID=fopen(fileServer)
# classifyCalibrations_createDataStruct.m:229
    formatSpec='%s'
# classifyCalibrations_createDataStruct.m:230
    # get header
    tDHeader=textscan(fileID,'%[^\n]',1)
# classifyCalibrations_createDataStruct.m:233
    tDHeader=split(tDHeader[1,1],',').T
# classifyCalibrations_createDataStruct.m:234
    
    # get data
    tD=textscan(fileID,formatSpec,'Delimiter',',','HeaderLines',1)
# classifyCalibrations_createDataStruct.m:237
    # time
    tDTime=tD[1,1](arange(1,end() - 1,2),arange())
# classifyCalibrations_createDataStruct.m:240
    tDTime=datetime(tDTime(arange(),1),'InputFormat','HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:241
    tDTime.Format = copy('HH:mm:ss.SSS')
# classifyCalibrations_createDataStruct.m:242
    # event
    tDData=tD[1,1](arange(2,end(),2),arange())
# classifyCalibrations_createDataStruct.m:245
    # put together into table (or other usefule format)
    t1=array2table(tDTime)
# classifyCalibrations_createDataStruct.m:248
    t2=array2table(tDData)
# classifyCalibrations_createDataStruct.m:249
    Server=concat([t1,t2])
# classifyCalibrations_createDataStruct.m:250
    # add Accel to header of xyz
    ServerHeader=strcat('Server_',tDHeader(arange(2,end())))
# classifyCalibrations_createDataStruct.m:253
    Server.Properties.VariableNames = copy(concat([tDHeader(1),ServerHeader]))
# classifyCalibrations_createDataStruct.m:254
    # close file, and stuff I do not end
    fclose(fileID)
    ## Put all data together
    
    # put IMU into same table
    IMU=concat([Accel,Gyro(arange(),arange(2,end())),Orient(arange(),arange(2,end()))])
# classifyCalibrations_createDataStruct.m:262
    # put myoServer data together
    myoServer=struct()
# classifyCalibrations_createDataStruct.m:265
    myoServer.EMG = copy(EMG)
# classifyCalibrations_createDataStruct.m:266
    myoServer.IMU = copy(IMU)
# classifyCalibrations_createDataStruct.m:267
    myoServer.Events = copy(Server)
# classifyCalibrations_createDataStruct.m:268
    # add Dashy events to trialData at the correct time
    trialData.dashyEvent = copy(cell(size(trialData,1),1))
# classifyCalibrations_createDataStruct.m:271
    ravel[trialData.dashyEvent]=cellarray([''])
# classifyCalibrations_createDataStruct.m:272
    for evt in arange(1,size(gameData.Time)).reshape(-1):
        __,EventInd(evt)=min(abs(trialData.time - gameData.Time(evt)),nargout=2)
# classifyCalibrations_createDataStruct.m:274
        trialData.dashyEvent[EventInd(evt)]=gameData.Event(evt)
# classifyCalibrations_createDataStruct.m:275
    
    ## Put Data together and Save
    
    Data_.EMG = copy(myoServer.EMG)
# classifyCalibrations_createDataStruct.m:281
    Data_.IMU = copy(myoServer.IMU)
# classifyCalibrations_createDataStruct.m:282
    # Data.VID = ParticipantVid.VideoData{tr};
    Data_.const = copy(const)
# classifyCalibrations_createDataStruct.m:284
    Data_.Trial = copy(trialData)
# classifyCalibrations_createDataStruct.m:285
    Data_.gameData = copy(gameData)
# classifyCalibrations_createDataStruct.m:286
    Data_.myoServerEvents = copy(myoServer.Events)
# classifyCalibrations_createDataStruct.m:287
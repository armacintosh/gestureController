# Generated with SMOP  0.41
from libsmop import *
# saveTrial.m

    
@function
def saveTrial(const=None,*args,**kwargs):
    varargin = saveTrial.varargin
    nargin = saveTrial.nargin

    ##
# move to beginning and put outfolder into const.
# setup file directory
    formatOutFolder='yyyy mm dd'
# saveTrial.m:6
    dateFolder=datestr(now,formatOutFolder)
# saveTrial.m:7
    outputfolderLM=strcat('Results\',dateFolder,'\logMatlab\')
# saveTrial.m:8
    outputfolderMS=strcat('Results\',dateFolder,'\myoServer\')
# saveTrial.m:9
    outputfolderGD=strcat('Results\',dateFolder,'\gameData\')
# saveTrial.m:10
    mkdir(outputfolderLM)
    mkdir(outputfolderMS)
    mkdir(outputfolderGD)
    save(const.trialConst,'const')
    trialTime=const.trialDatafile(arange(end() - 16,end() - 4))
# saveTrial.m:16
    ## Myo Server
    
    # save raw from MyoServer
    ServerLogFolder='Programs\MyoServer\Logs\'
# saveTrial.m:21
    
    # rename to match trial
    serverFiles=dir(fullfile(ServerLogFolder,'*-*'))
# saveTrial.m:24
    serverFiles=struct2table(serverFiles)
# saveTrial.m:25
    serverFiles=sortrows(serverFiles,'date','descend')
# saveTrial.m:26
    
    if numel(serverFiles) > 0:
        # only keep the most recent
        serverFiles=serverFiles(arange(1,5),arange())
# saveTrial.m:32
        ServerNameOld=strcat(ServerLogFolder,char(serverFiles.name(arange(),arange())))
# saveTrial.m:33
        serverTime=serverFiles.name[1,1](arange(1,15))
# saveTrial.m:36
        serverFiles.name = copy(strrep(serverFiles.name,serverTime,''))
# saveTrial.m:37
        suffix=strcat('_',trialTime,'.csv')
# saveTrial.m:38
        serverFiles.name = copy(strrep(serverFiles.name,'.csv',suffix))
# saveTrial.m:39
        ServerNameNew=strcat(outputfolderMS,char(serverFiles.name(arange(),arange())))
# saveTrial.m:40
        # will not work if half saved files...
        for filenum in arange(1,size(ServerNameNew,1)).reshape(-1):
            movefile(ServerNameOld(filenum,arange()),ServerNameNew(filenum,arange()))
        # delete old data, should already be gone.
        delete(strcat(ServerLogFolder,'*.csv'))
    else:
        # note in a text file that there were no files to store
        noteText=strcat(outputfolderMS,'No MyoServer data to write','_',trialTime,'.txt')
# saveTrial.m:52
        fid=fopen(noteText,'w+')
# saveTrial.m:53
        fprintf(fid,'%s\n','No MyoServer data to write')
        fclose(fid)
    
    ## Myo Jumper
    
    # save raw from MyoServer
    JumperLogFolder='Programs\MyoJumper\MyoJumper_Data\Logs\'
# saveTrial.m:63
    
    # rename to match trial
    JumperFiles=dir(fullfile(JumperLogFolder,'*-*'))
# saveTrial.m:66
    JumperFiles=struct2table(JumperFiles)
# saveTrial.m:67
    JumperFiles=sortrows(JumperFiles,'date','descend')
# saveTrial.m:68
    
    if numel(JumperFiles) > 0:
        # only keep the most recent
        JumperFiles=JumperFiles(1,arange())
# saveTrial.m:74
        ServerNameOld=strcat(JumperLogFolder,char(JumperFiles.name(arange(),arange())))
# saveTrial.m:75
        ServerNameNew=strcat(outputfolderGD,'JumperEvents_',trialTime,'.csv')
# saveTrial.m:76
        for filenum in arange(1,size(ServerNameNew,1)).reshape(-1):
            movefile(ServerNameOld(filenum,arange()),ServerNameNew(filenum,arange()))
        # delete old data, should already be gone.
        delete(strcat(JumperLogFolder,'*.csv'))
    else:
        # note in a text file that there were no files to store
        noteText=strcat(outputfolderMS,'No MyoJumper data to write','_',trialTime,'.txt')
# saveTrial.m:87
        fid=fopen(noteText,'w+')
# saveTrial.m:88
        fprintf(fid,'%s\n','No MyoJumper data to write')
        fclose(fid)
    
    
    ## save raw Dashy
    DashyFolder='Programs\Games\Results\'
# saveTrial.m:96
    # rename results to match time stamps...
    gameFiles=dir(fullfile(DashyFolder,'*-*'))
# saveTrial.m:99
    gameFiles=struct2table(gameFiles)
# saveTrial.m:100
    gameFiles=sortrows(gameFiles,'date','descend')
# saveTrial.m:101
    
    if numel(gameFiles) > 0:
        # this will get all the game files, even if dashy was opened without matlab saving it..
        gameFileNameOld=strcat(DashyFolder,char(gameFiles.name(arange(),arange())))
# saveTrial.m:107
        gameFiles.name = copy(strrep(gameFiles.name,'.csv',''))
# saveTrial.m:110
        if iscell(gameFiles.name):
            gameDate=gameFiles.name[1](arange(1,9))
# saveTrial.m:114
            gameFiles.name = copy(strrep(gameFiles.name,gameDate,''))
# saveTrial.m:115
            gameFiles.name = copy(strrep(gameFiles.name,'-','_'))
# saveTrial.m:116
            B=cellfun(lambda x=None: x(arange(1,6)),gameFiles.name,'un',0)
# saveTrial.m:118
            gameFiles.name = copy(cellfun(lambda x=None: strrep(x,x(arange(1,7)),''),gameFiles.name,'un',0))
# saveTrial.m:120
            suffix=strcat('_',trialTime,'.csv')
# saveTrial.m:122
            gameFiles.name = copy(strcat(gameFiles.name,'_',B,suffix))
# saveTrial.m:123
        else:
            gameDate=gameFiles.name(arange(1,9))
# saveTrial.m:125
            gameFiles.name = copy(strrep(gameFiles.name,gameDate,''))
# saveTrial.m:126
            gameFiles.name = copy(strrep(gameFiles.name,'-','_'))
# saveTrial.m:127
            B=gameFiles.name(arange(1,6))
# saveTrial.m:129
            gameFiles.name = copy(strrep(gameFiles.name,gameFiles.name(arange(1,7)),''))
# saveTrial.m:131
            suffix=strcat('_',trialTime,'.csv')
# saveTrial.m:133
            gameFiles.name = copy(strcat(gameFiles.name,'_',B,suffix))
# saveTrial.m:134
        gameFileNameNew=strcat(outputfolderGD,char(gameFiles.name(arange(),arange())))
# saveTrial.m:137
        for filenum in arange(1,size(gameFileNameNew,1)).reshape(-1):
            movefile(gameFileNameOld(filenum,arange()),gameFileNameNew(filenum,arange()))
    else:
        # note in a text file that there were no files to store
        noteText=strcat(outputfolderGD,'No Dashy data to write','_',trialTime,'.txt')
# saveTrial.m:146
        fid=fopen(noteText,'w+')
# saveTrial.m:147
        fprintf(fid,'%s\n','No Dashy data to write')
        fclose(fid)
    
    ##
    
    # add time to logFileMatlab
    logFileMatlabNew=strcat(outputfolderLM,const.logFileMatlab(arange(1,end() - 4)),'_',trialTime,'.txt')
# saveTrial.m:156
    movefile(const.logFileMatlab,logFileMatlabNew)
    # Log file notes if required.
    logTrialNotes(const,dateFolder,trialTime)
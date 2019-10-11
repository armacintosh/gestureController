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
    
    # copyfile(ServerLogFolder,outputfolderMS);
    
    # rename to match trial
    serverFiles=dir(fullfile(ServerLogFolder,'*-*'))
# saveTrial.m:25
    serverFiles=struct2table(serverFiles)
# saveTrial.m:26
    serverFiles=sortrows(serverFiles,'date','descend')
# saveTrial.m:27
    
    if numel(serverFiles) > 0:
        # only keep the most recent
        serverFiles=serverFiles(arange(1,5),arange())
# saveTrial.m:33
        ServerNameOld=strcat(ServerLogFolder,char(serverFiles.name(arange(),arange())))
# saveTrial.m:34
        serverTime=serverFiles.name[1,1](arange(1,15))
# saveTrial.m:37
        serverFiles.name = copy(strrep(serverFiles.name,serverTime,''))
# saveTrial.m:38
        suffix=strcat('_',trialTime,'.csv')
# saveTrial.m:39
        serverFiles.name = copy(strrep(serverFiles.name,'.csv',suffix))
# saveTrial.m:40
        ServerNameNew=strcat(outputfolderMS,char(serverFiles.name(arange(),arange())))
# saveTrial.m:41
        # will not work if half saved files...
        for filenum in arange(1,size(ServerNameNew,1)).reshape(-1):
            movefile(ServerNameOld(filenum,arange()),ServerNameNew(filenum,arange()))
        # delete old data, should already be gone.
        delete(strcat(ServerLogFolder,'*.csv'))
    else:
        # note in a text file that there were no files to store
        noteText=strcat(outputfolderMS,'No MyoServer data to write','_',trialTime,'.txt')
# saveTrial.m:53
        fid=fopen(noteText,'w+')
# saveTrial.m:54
        fprintf(fid,'%s\n','No MyoServer data to write')
        fclose(fid)
    
    ##
    
    ##
## Myo Jumper
    
    # save raw from MyoServer
    JumperLogFolder='Programs\MyoJumper\MyoJumper_Data\Logs\'
# saveTrial.m:66
    
    # copyfile(JumperLogFolder,outputfolderMS);
    
    # rename to match trial
    JumperFiles=dir(fullfile(JumperLogFolder,'*-*'))
# saveTrial.m:70
    JumperFiles=struct2table(JumperFiles)
# saveTrial.m:71
    JumperFiles=sortrows(JumperFiles,'date','descend')
# saveTrial.m:72
    
    if numel(JumperFiles) > 0:
        # only keep the most recent
        JumperFiles=JumperFiles(arange(),arange())
# saveTrial.m:78
        ServerNameOld=strcat(JumperLogFolder,char(JumperFiles.name(arange(),arange())))
# saveTrial.m:79
        #         # rename
#         serverTime = JumperFiles.name{1,1}(1:16);
#         JumperFiles.name = strrep(JumperFiles.name,serverTime,''); 
#         suffix = strcat('_',trialTime,'.csv');
#         JumperFiles.name = strrep(JumperFiles.name,'.csv',suffix);
        ServerNameNew=strcat(outputfolderGD,'JumperEvents_',trialTime,'.csv')
# saveTrial.m:86
        for filenum in arange(1,size(ServerNameNew,1)).reshape(-1):
            movefile(ServerNameOld(filenum,arange()),ServerNameNew(filenum,arange()))
        # delete old data, should already be gone.
        delete(strcat(JumperLogFolder,'*.csv'))
    else:
        # note in a text file that there were no files to store
        noteText=strcat(outputfolderMS,'No MyoJumper data to write','_',trialTime,'.txt')
# saveTrial.m:97
        fid=fopen(noteText,'w+')
# saveTrial.m:98
        fprintf(fid,'%s\n','No MyoJumper data to write')
        fclose(fid)
    
    
    ##
## save raw Dashy
    DashyFolder='Programs\Games\Results\'
# saveTrial.m:106
    # rename results to match time stamps...
    gameFiles=dir(fullfile(DashyFolder,'*-*'))
# saveTrial.m:109
    gameFiles=struct2table(gameFiles)
# saveTrial.m:110
    gameFiles=sortrows(gameFiles,'date','descend')
# saveTrial.m:111
    
    if numel(gameFiles) > 0:
        # this will get all the game files, even if dashy was opened without matlab saving it..
        gameFileNameOld=strcat(DashyFolder,char(gameFiles.name(arange(),arange())))
# saveTrial.m:117
        # remove the first item, Data, 
            # move second item (time) to after the words, 
            # place trailTime at end, add extension
            # cut based on '-'
        # remove extension
        gameFiles.name = copy(strrep(gameFiles.name,'.csv',''))
# saveTrial.m:126
        if iscell(gameFiles.name):
            gameDate=gameFiles.name[1](arange(1,9))
# saveTrial.m:130
            gameFiles.name = copy(strrep(gameFiles.name,gameDate,''))
# saveTrial.m:131
            gameFiles.name = copy(strrep(gameFiles.name,'-','_'))
# saveTrial.m:132
            B=cellfun(lambda x=None: x(arange(1,6)),gameFiles.name,'un',0)
# saveTrial.m:134
            gameFiles.name = copy(cellfun(lambda x=None: strrep(x,x(arange(1,7)),''),gameFiles.name,'un',0))
# saveTrial.m:136
            suffix=strcat('_',trialTime,'.csv')
# saveTrial.m:138
            gameFiles.name = copy(strcat(gameFiles.name,'_',B,suffix))
# saveTrial.m:139
        else:
            gameDate=gameFiles.name(arange(1,9))
# saveTrial.m:141
            gameFiles.name = copy(strrep(gameFiles.name,gameDate,''))
# saveTrial.m:142
            gameFiles.name = copy(strrep(gameFiles.name,'-','_'))
# saveTrial.m:143
            B=gameFiles.name(arange(1,6))
# saveTrial.m:145
            gameFiles.name = copy(strrep(gameFiles.name,gameFiles.name(arange(1,7)),''))
# saveTrial.m:147
            suffix=strcat('_',trialTime,'.csv')
# saveTrial.m:149
            gameFiles.name = copy(strcat(gameFiles.name,'_',B,suffix))
# saveTrial.m:150
        gameFileNameNew=strcat(outputfolderGD,char(gameFiles.name(arange(),arange())))
# saveTrial.m:153
        for filenum in arange(1,size(gameFileNameNew,1)).reshape(-1):
            movefile(gameFileNameOld(filenum,arange()),gameFileNameNew(filenum,arange()))
    else:
        # note in a text file that there were no files to store
        noteText=strcat(outputfolderGD,'No Dashy data to write','_',trialTime,'.txt')
# saveTrial.m:162
        fid=fopen(noteText,'w+')
# saveTrial.m:163
        fprintf(fid,'%s\n','No Dashy data to write')
        fclose(fid)
    
    ##
    
    # add time to logFileMatlab
    logFileMatlabNew=strcat(outputfolderLM,const.logFileMatlab(arange(1,end() - 4)),'_',trialTime,'.txt')
# saveTrial.m:172
    movefile(const.logFileMatlab,logFileMatlabNew)
    # Log file notes if required.
    logTrialNotes(const,dateFolder,trialTime)
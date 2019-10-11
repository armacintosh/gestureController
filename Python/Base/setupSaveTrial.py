# Generated with SMOP  0.41
from libsmop import *
# setupSaveTrial.m

    
@function
def setupSaveTrial(const=None,out=None,*args,**kwargs):
    varargin = setupSaveTrial.varargin
    nargin = setupSaveTrial.nargin

    ##
# setup file directory
    formatOutFolder='yyyy mm dd'
# setupSaveTrial.m:4
    dateFolder=datestr(now,formatOutFolder)
# setupSaveTrial.m:5
    outputfolderTD=strcat('Results\',dateFolder,'\trialData\')
# setupSaveTrial.m:6
    # outputfolderMS = strcat('Results\',dateFolder,'\myoServer\');
    mkdir(outputfolderTD)
    # mkdir(outputfolderMS);
    
    # output file names
    formatOut='yyyymmdd_HHMM'
# setupSaveTrial.m:12
    date=datestr(now,formatOut)
# setupSaveTrial.m:13
    # trialDatafile = strcat(outputfolderTD,'trialData_',date,'.mat');
    const.trialDatafile = copy(strcat(outputfolderTD,'trialData_',date,'.txt'))
# setupSaveTrial.m:15
    const.outFieldNames = copy(fieldnames(out))
# setupSaveTrial.m:17
    const.dateFormat = copy('HH:MM:SS.FFF')
# setupSaveTrial.m:18
    # save the const file used in this run
    const.trialConst = copy(strcat(outputfolderTD,'trialConst_',date,'.mat'))
# setupSaveTrial.m:21
    # save(trialConst,'const');
    
    ## save the first row headers of trial data
    
    const.fileID_STORE = copy(fopen(const.trialDatafile,'a'))
# setupSaveTrial.m:27
    storeStartInd=find(strcmp(const.outFieldNames,'time'))
# setupSaveTrial.m:29
    
    for fieldIndex in arange(storeStartInd,length(const.outFieldNames)).reshape(-1):
        field=char(const.outFieldNames(fieldIndex))
# setupSaveTrial.m:32
        if fieldIndex == length(const.outFieldNames):
            fprintf(const.fileID_STORE,'%s',field)
        else:
            fprintf(const.fileID_STORE,'%s,',field)
    
    fprintf(const.fileID_STORE,' \n')
    ## 
# save the first instance of the const file
    save(const.trialConst,'const')
    ##
    
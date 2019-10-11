# Generated with SMOP  0.41
from libsmop import *
# loadTrialData.m

    
@function
def loadTrialData(fileTrial=None,*args,**kwargs):
    varargin = loadTrialData.varargin
    nargin = loadTrialData.nargin

    # make all import stuff into a function
    
    # import trialData
    fileID=fopen(fileTrial)
# loadTrialData.m:6
    formatSpec='%s'
# loadTrialData.m:7
    # get header
    tDHeader=textscan(fileID,'%[^\n]',1)
# loadTrialData.m:10
    tDHeader=split(tDHeader[1,1],',').T
# loadTrialData.m:11
    
    # get data
    tD=textscan(fileID,formatSpec,'HeaderLines',1)
# loadTrialData.m:14
    tD=split(tD[1,1],',')
# loadTrialData.m:15
    
    # format Time from str to datetime
    tDTime=datetime(tD(arange(),1),'InputFormat','HH:mm:ss.SSS')
# loadTrialData.m:18
    tDTime.Format = copy('HH:mm:ss.SSS')
# loadTrialData.m:19
    # format Other cols. from str. to num
    tDData=str2double(tD(arange(),arange(2,end())))
# loadTrialData.m:22
    # put back together into table (or other usefule format)
    t1=array2table(tDTime)
# loadTrialData.m:25
    t2=array2table(tDData)
# loadTrialData.m:26
    trialData=concat([t1,t2])
# loadTrialData.m:27
    trialData.Properties.VariableNames = copy(tDHeader)
# loadTrialData.m:28
    # close file, and stuff I do not eed
    fclose(fileID)
    # clear_all_but ('resultsPath','trialData');
# Generated with SMOP  0.41
from libsmop import *
# logTrialNotes.m

    
@function
def logTrialNotes(const=None,dateFolder=None,trialTime=None,*args,**kwargs):
    varargin = logTrialNotes.varargin
    nargin = logTrialNotes.nargin

    # Open trial log and input new trial information save excel log
    
    formatOutFolder='yyyymmdd'
# logTrialNotes.m:4
    Today=datestr(now,formatOutFolder)
# logTrialNotes.m:5
    logfile=strcat('Results\',dateFolder,'\TrialLog_',Today,'.txt')
# logTrialNotes.m:7
    header=cellarray(['time','trial','note'])
# logTrialNotes.m:8
    
    if exist(logfile,'file') == 0:
        # make the file
        disp('Creating Log File')
        fid=fopen(logfile,'wt')
# logTrialNotes.m:16
        rows,__=size(header,nargout=2)
# logTrialNotes.m:17
        for i in arange(1,rows).reshape(-1):
            fprintf(fid,'%s,',header[i,arange(1,end() - 1)])
            fprintf(fid,'%s\n',header[i,end()])
        fclose(fid)
    
    
    # build the row to add
    postcollectiontime=datetime('now','Format','yyyy mm dd hh:mm:ss:ms')
# logTrialNotes.m:26
    if const.makeTrialNotes == 1:
        Note=inputdlg(cellarray(['Enter Stage number (Calibration = 1, Think aloud = 2, Alg/Explore = 3 )','Write any notes for this trial - dont use commas']),'Config Trial',concat([[1,100],[1,100]]))
# logTrialNotes.m:29
    else:
        Note=cellarray([[''],['']])
# logTrialNotes.m:34
    
    
    appendLog=cellarray([char(trialTime),char(Note(1)),char(Note(2))])
# logTrialNotes.m:37
    
    fid=fopen(logfile,'at')
# logTrialNotes.m:40
    rows2,__=size(appendLog,nargout=2)
# logTrialNotes.m:41
    for i in arange(1,rows2).reshape(-1):
        fprintf(fid,'%s,',appendLog[i,arange(1,end() - 1)])
        fprintf(fid,'%s\n',appendLog[i,end()])
    
    fclose(fid)
# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_RndFrstSVMgrd_Now.m

    
@function
def classifyCalibrations_RndFrstSVMgrd_Now(*args,**kwargs):
    varargin = classifyCalibrations_RndFrstSVMgrd_Now.varargin
    nargin = classifyCalibrations_RndFrstSVMgrd_Now.nargin

    # to adjust as desired
    topPercent=80
# classifyCalibrations_RndFrstSVMgrd_Now.m:4
    ## import ParticipantVid table
    trialoutput_file,trialoutput_path,__=uigetfile('Results\*.txt','multiselect','on','select the trialData_DATE file you want to use to classify',nargout=3)
# classifyCalibrations_RndFrstSVMgrd_Now.m:7
    resultsfolder=strrep(trialoutput_path,'trialData\','')
# classifyCalibrations_RndFrstSVMgrd_Now.m:8
    ## CHAR for single trial
    if class_(trialoutput_file) == 'cell':
        trialoutput_file=sort(trialoutput_file)
# classifyCalibrations_RndFrstSVMgrd_Now.m:12
    else:
        # turn single string into cell 1x1
        trialoutput_file=cellarray([trialoutput_file])
# classifyCalibrations_RndFrstSVMgrd_Now.m:15
    
    ## Select participant
    
    #Options
    option=concat([cellarray(['F01']),cellarray(['F02']),cellarray(['F03']),cellarray(['F04']),cellarray(['F05']),cellarray(['F06']),cellarray(['F07']),cellarray(['F08']),cellarray(['F09']),cellarray(['F10']),cellarray(['AM']),cellarray(['P12']),cellarray(['P43']),cellarray(['P52']),cellarray(['P63']),cellarray(['P81']),cellarray(['P84']),cellarray(['P96']),cellarray(['P97']),cellarray(['P98']),cellarray(['A']),cellarray(['B']),cellarray(['C']),cellarray(['D']),cellarray(['E']),cellarray(['F']),cellarray(['G'])])
# classifyCalibrations_RndFrstSVMgrd_Now.m:21
    # get user to select gesture code 1 or 2
    s,__=listdlg('PromptString','Select Participant','SelectionMode','single','ListSize',concat([200,100]),'ListString',option,nargout=2)
# classifyCalibrations_RndFrstSVMgrd_Now.m:52
    participant=option[s]
# classifyCalibrations_RndFrstSVMgrd_Now.m:57
    ## for each trial
    
    for t in arange(1,length(trialoutput_file)).reshape(-1):
        # put File components together
        Data_,__=classifyCalibrations_createDataStruct(resultsfolder,trialoutput_file,t,nargout=2)
# classifyCalibrations_RndFrstSVMgrd_Now.m:65
        CalFtTbl,const,__,y=classifyCalibrations_calcFtTbl(Data_,nargout=4)
# classifyCalibrations_RndFrstSVMgrd_Now.m:68
    
    ## do one Random Forest and SVM grid for all calData trials put together
    
    # remove selected gestures
    FtTbl=CalFtTbl(CalFtTbl.TrueLabel < 3,arange())
# classifyCalibrations_RndFrstSVMgrd_Now.m:76
    
    # normalize FtTbl to mu and SD, after i have all true labels
    FtTblN,const.mu,const.stddev=calcFtTblNorm(FtTbl(arange(),arange(2,end())),nargout=3)
# classifyCalibrations_RndFrstSVMgrd_Now.m:79
    # truelabel first in FtTbleNorm
    TrueLabel=array2table(FtTbl.TrueLabel)
# classifyCalibrations_RndFrstSVMgrd_Now.m:83
    TrueLabel.Properties.VariableNames = copy(cellarray(['TrueLabel']))
# classifyCalibrations_RndFrstSVMgrd_Now.m:84
    FtTblNorm=concat([TrueLabel,FtTblN])
# classifyCalibrations_RndFrstSVMgrd_Now.m:85
    ##  Random Forest
    
    # returns the FtTble with only most important features
    fprintf('learning gestures \n')
    outPut=StaticAnalysis_RandomForest_setup(FtTblNorm,topPercent)
# classifyCalibrations_RndFrstSVMgrd_Now.m:92
    FtTblTop=outPut.FtTblTop
# classifyCalibrations_RndFrstSVMgrd_Now.m:93
    
    # get the top mu and sd to use in
    const.muTop = copy(const.mu(1,outPut.indkpTop - 1))
# classifyCalibrations_RndFrstSVMgrd_Now.m:96
    const.sdTop = copy(const.stddev(1,outPut.indkpTop - 1))
# classifyCalibrations_RndFrstSVMgrd_Now.m:97
    ## SVM Grid using top features.
    
    # SVM using only the top features, found during random forest
    ClassOutputTop=StatisticalAnalysis_SVMGrid_setup(FtTblTop)
# classifyCalibrations_RndFrstSVMgrd_Now.m:102
    fprintf('done learning gestures \n')
    ## setup save struct
    
    # get the model to use in the game.
    gameClass.Mdl = copy(ClassOutputTop[1,1].TestingModel)
# classifyCalibrations_RndFrstSVMgrd_Now.m:108
    # need mu and SD to normalize in game
    gameClass.mu = copy(const.muTop)
# classifyCalibrations_RndFrstSVMgrd_Now.m:111
    gameClass.std = copy(const.sdTop)
# classifyCalibrations_RndFrstSVMgrd_Now.m:112
    ## get distance from extensor sensor of channels used in classification
    # ID channels used in classificaiton
    
    # gets last char from each feature name
    FtTopNames=gameClass.Mdl.ExpandedPredictorNames
# classifyCalibrations_RndFrstSVMgrd_Now.m:119
    ch=cellfun(lambda S=None: S(1,end()),FtTopNames,'Uniform',0)
# classifyCalibrations_RndFrstSVMgrd_Now.m:120
    
    for Ft in arange(1,length(ch)).reshape(-1):
        # dont actually need this anymore
        if length(const.EMGch) == 4:
            isCH=strfind('3456',ch[Ft])
# classifyCalibrations_RndFrstSVMgrd_Now.m:127
        else:
            if length(const.EMGch) == 6:
                isCH=strfind('234567',ch[Ft])
# classifyCalibrations_RndFrstSVMgrd_Now.m:129
            else:
                isCH=strfind('12345678',ch[Ft])
# classifyCalibrations_RndFrstSVMgrd_Now.m:131
        # incase circ is the feature
        if isCH:
            # set distance from extensor sensor for that Feature
            chABS=str2double(ch[Ft])
# classifyCalibrations_RndFrstSVMgrd_Now.m:137
            chdist[1,Ft]=chABS - y
# classifyCalibrations_RndFrstSVMgrd_Now.m:138
        else:
            chdist[1,Ft]=nan
# classifyCalibrations_RndFrstSVMgrd_Now.m:141
    
    
    gameClass.FtChDist = copy(chdist)
# classifyCalibrations_RndFrstSVMgrd_Now.m:146
    gameClass.allFts = copy(FtTblNorm.Properties.VariableNames)
# classifyCalibrations_RndFrstSVMgrd_Now.m:147
    ## Save the workspace for review/ safe keeping
    
    # update name and date saving
    formatOutFolder='yyyymmdd'
# classifyCalibrations_RndFrstSVMgrd_Now.m:153
    dateFolder=datestr(now,formatOutFolder)
# classifyCalibrations_RndFrstSVMgrd_Now.m:154
    gameClassfile=strcat(trialoutput_path,participant,'_1v2_gameClass_',dateFolder)
# classifyCalibrations_RndFrstSVMgrd_Now.m:155
    Classfile=strcat(trialoutput_path,participant,'_1v2_RndFrstSVMgrd_',dateFolder)
# classifyCalibrations_RndFrstSVMgrd_Now.m:156
    save(strcat(trialoutput_path,'CurrentUserClassifier.mat'),'gameClass')
    save(strcat(trialoutput_path,'CurrentUserClassifier_',participant,'_',dateFolder,'.mat'),'gameClass')
    save(gameClassfile,'gameClass')
    
    save(Classfile,'ClassOutputTop')
    
    ##
    
    start=gameClass.Mdl.PredictorNames
# classifyCalibrations_RndFrstSVMgrd_Now.m:165
    start=cellfun(lambda c=None: concat([c,', ']),start,'uni',false)
# classifyCalibrations_RndFrstSVMgrd_Now.m:166
    finish=arrayfun(lambda i=None: concat([start[i,arange()]]),arange(1,size(start,1)),'UniformOutput',false).T
# classifyCalibrations_RndFrstSVMgrd_Now.m:167
    Output1=strcat('Top Features are:',finish)
# classifyCalibrations_RndFrstSVMgrd_Now.m:168
    confmat=num2str(ClassOutputTop[1,1].ConfusionMat[arange(),arange()])
# classifyCalibrations_RndFrstSVMgrd_Now.m:170
    Output2a=strcat('Confusion Matrix (code 1): ',num2str(confmat(1,arange())))
# classifyCalibrations_RndFrstSVMgrd_Now.m:171
    Output2b=strcat('Confusion Matrix (code 2): ',confmat(2,arange()))
# classifyCalibrations_RndFrstSVMgrd_Now.m:172
    Output=msgbox(cellarray([[Output1[1]],[Output2a],[Output2b]]))
# classifyCalibrations_RndFrstSVMgrd_Now.m:174
    ##
# Open the folder where data is saved
    winopen(trialoutput_path)
    msgbox('Copy constFile.txt and CurrentUserClassifier.mat to users MyoDashy folder')
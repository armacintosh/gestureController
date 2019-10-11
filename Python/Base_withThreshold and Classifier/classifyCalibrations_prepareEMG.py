# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_prepareEMG.m

    
@function
def classifyCalibrations_prepareEMG(Data_=None,const=None,ind=None,*args,**kwargs):
    varargin = classifyCalibrations_prepareEMG.varargin
    nargin = classifyCalibrations_prepareEMG.nargin

    ## Renew const file
    
    const=classifyCalibrations_setupEMG_Const(const)
# classifyCalibrations_prepareEMG.m:5
    
    ## Get resting data (ReadyMean)
    
    ChUsed=concat([1,const.EMGch + 1])
# classifyCalibrations_prepareEMG.m:9
    RestUse=concat([arange(ind.EMG.startTime1_rest,ind.EMG.startTime1_active),arange(ind.EMG.startTime2_rest,ind.EMG.startTime2_active),arange(ind.EMG.startTime3_rest,ind.EMG.startTime3_active)])
# classifyCalibrations_prepareEMG.m:10
    EMGReady=Data_.EMG(RestUse,ChUsed)
# classifyCalibrations_prepareEMG.m:14
    
    ReadyMeanEMG=classifyCalibrations_findReadyMean(EMGReady)
# classifyCalibrations_prepareEMG.m:15
    
    ## FIND CORRECT EMG DATA
    
    # Fingers Open
    E2=Data_.EMG(arange(ind.EMG.startTime1_active,ind.EMG.startTime1_end),ChUsed)
# classifyCalibrations_prepareEMG.m:21
    TL=dot(ones(size(E2,1),1),2)
# classifyCalibrations_prepareEMG.m:22
    E2=concat([E2,array2table(TL)])
# classifyCalibrations_prepareEMG.m:23
    # Fingers closed
    E1=Data_.EMG(arange(ind.EMG.startTime2_active,ind.EMG.startTime2_end),ChUsed)
# classifyCalibrations_prepareEMG.m:26
    
    TL=ones(size(E1,1),1)
# classifyCalibrations_prepareEMG.m:27
    E1=concat([E1,array2table(TL)])
# classifyCalibrations_prepareEMG.m:28
    # Pinch
    E3=Data_.EMG(arange(ind.EMG.startTime3_active,ind.EMG.startTime3_end),ChUsed)
# classifyCalibrations_prepareEMG.m:31
    
    TL=dot(ones(size(E3,1),1),3)
# classifyCalibrations_prepareEMG.m:32
    E3=concat([E3,array2table(TL)])
# classifyCalibrations_prepareEMG.m:33
    EMG=concat([[E2],[E1],[E3]])
# classifyCalibrations_prepareEMG.m:35
    
    if 1 == const.EMGS1:
        EMG.Properties.VariableNames = copy(cellarray(['time','S1','S2','S3','S4','S5','S6','S7','S8','TL']))
# classifyCalibrations_prepareEMG.m:39
    else:
        if 2 == const.EMGS1:
            EMG.Properties.VariableNames = copy(cellarray(['time','S2','S3','S4','S5','S6','S7','TL']))
# classifyCalibrations_prepareEMG.m:41
        else:
            if 3 == const.EMGS1:
                EMG.Properties.VariableNames = copy(cellarray(['time','S3','S4','S5','S6','TL']))
# classifyCalibrations_prepareEMG.m:43
    
    EMG[arange(),arange(2,end() - 1)]=abs(EMG[arange(),arange(2,end() - 1)]) / 128
# classifyCalibrations_prepareEMG.m:46
    
    EMG[arange(),arange(2,end() - 1)]=EMG[arange(),arange(2,end() - 1)] - ReadyMeanEMG
# classifyCalibrations_prepareEMG.m:47
    
    ## Bayes Filter
    
    # create Bayes filtered version of D_EMG
# most features use filtered data (these do not filter: SSC, ZC, WAMP)
    if const.BayesFilter == 1:
        D_EMGF=copy(EMG)
# classifyCalibrations_prepareEMG.m:55
        param,D_EMGF[arange(),arange(2,end() - 1)]=bayesOnlineFilter(const.param,D_EMGF[arange(),arange(2,end() - 1)],nargout=2)
# classifyCalibrations_prepareEMG.m:56
        const.param = copy(param)
# classifyCalibrations_prepareEMG.m:57
        if sum(ismissing(D_EMGF[arange(),arange(2,end() - 1)])) > 0:
            fprintf('NAN in filtered data \n\n')
        else:
            fprintf('all EMG filtered \n\n')
    
# Generated with SMOP  0.41
from libsmop import *
# setupClassifier.m

    
@function
def setupClassifier(const=None,*args,**kwargs):
    varargin = setupClassifier.varargin
    nargin = setupClassifier.nargin

    ## Select the features to calculate (only the tops)
    
    predictors=const.classify.Mdl.PredictorNames
# setupClassifier.m:5
    C=cellfun(lambda S=None: strsplit(S,'_'),predictors,'Uniform',0)
# setupClassifier.m:6
    fprintf('Full Model Features: %s \n',C[1][2])
    for topFt in arange(1,length(C)).reshape(-1):
        ftUse[topFt]=C[1,topFt](2)
# setupClassifier.m:10
    
    const.classify.ftUse = copy(ftUse)
# setupClassifier.m:13
    ## re-align the channels
    
    # is the index of the e channel... on 3/6 this means e == 4 is ch 6
    eInd=const.extensor_sensors(1) - 1
# setupClassifier.m:19
    
    e=const.EMGch(eInd)
# setupClassifier.m:20
    dist=const.classify.FtChDist
# setupClassifier.m:21
    ftChRaw=e + dist
# setupClassifier.m:22
    #  Get new channel for each feature
    for ftNum in arange(1,length(ftChRaw)).reshape(-1):
        # check if the distance exceeds the channels used
        if ftChRaw(ftNum) > const.EMGch(end()):
            ftCh[ftNum]=ftChRaw(ftNum) - length(const.EMGch)
# setupClassifier.m:28
        else:
            if ftChRaw(ftNum) < const.EMGch(1):
                ftCh[ftNum]=ftChRaw(ftNum) + length(const.EMGch)
# setupClassifier.m:30
            else:
                ftCh[ftNum]=ftChRaw(ftNum)
# setupClassifier.m:32
        ftCh(ftNum)
    
    
    # if a mulit-ch feature, then ftCh == NaN
    const.classify.ftChUse = copy(ftCh)
# setupClassifier.m:38
    
    
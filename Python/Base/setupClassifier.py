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
    
    # # for testing
#     y = 2; # will have to do this after I have selected channels.
# #     chABS = randi([1 8], [1 7])
#     dist = chABS - y
    # is the index of the e channel... on 3/6 this means e == 4 is ch 6
    eInd=const.extensor_sensors(1) - 1
# setupClassifier.m:23
    
    e=const.EMGch(eInd)
# setupClassifier.m:24
    dist=const.classify.FtChDist
# setupClassifier.m:26
    #     e = 8; # new y new Extensor Channel
    # dist can be from -7 to 7, (eCH - ch1:8)
    
    ftChRaw=e + dist
# setupClassifier.m:30
    #     if length (const.EMGch) < 8
#         #  Get new channel for each feature
#         for ftNum = 1:length(ftChRaw)
#             # check if the distance exceeds the channels used
#             if ftChRaw(ftNum) > const.EMGch(end) 
#                 ftCh(ftNum) = ftChRaw(ftNum)  - const.EMGch(end);
#             elseif ftChRaw(ftNum) < const.EMGch(1)
#                 ftCh(ftNum) = ftChRaw(ftNum)  + const.EMGch(end);
#             else 
#                 ftCh(ftNum) = ftChRaw(ftNum);
#             end 
#            ftCh(ftNum)
#         end
#     end
    
    #  Get new channel for each feature
    for ftNum in arange(1,length(ftChRaw)).reshape(-1):
        # check if the distance exceeds the channels used
        if ftChRaw(ftNum) > const.EMGch(end()):
            ftCh[ftNum]=ftChRaw(ftNum) - length(const.EMGch)
# setupClassifier.m:51
        else:
            if ftChRaw(ftNum) < const.EMGch(1):
                ftCh[ftNum]=ftChRaw(ftNum) + length(const.EMGch)
# setupClassifier.m:53
            else:
                ftCh[ftNum]=ftChRaw(ftNum)
# setupClassifier.m:55
        ftCh(ftNum)
    
    
    #     ftCh
    # if a mulit-ch feature, then ftCh == NaN
    const.classify.ftChUse = copy(ftCh)
# setupClassifier.m:62
    
    
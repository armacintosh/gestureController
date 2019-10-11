# Generated with SMOP  0.41
from libsmop import *
# makeFtTbl_Online.m

    
@function
def makeFtTbl_Online(const=None,out=None,*args,**kwargs):
    varargin = makeFtTbl_Online.varargin
    nargin = makeFtTbl_Online.nargin

    # Input: emg data split into 20 rows, 10 cols, N = 1 bin in real time)
# Picks which features to calculate based on setupClasifier.m output
# Output: nRow (1 for real time) * FtTop Cols.
    
    # assumes out.EMG has been: 
#     Done abs, / 128
#     rest subtracted
    
    ## Bayes Filter
    
    # some features use filtered data (these do not filter: SSC, ZC, WAMP)
    if const.BayesFilter == 1:
        param,out.dataEMG(arange(),arange(2,end()))=bayesOnlineFilter(const.param,out.dataEMG(arange(),arange(2,end())),nargout=2)
# makeFtTbl_Online.m:15
        const.param = copy(param)
# makeFtTbl_Online.m:16
        if sum(ismissing(out.dataEMG(arange(),arange(2,end())))) > 0:
            fprintf('NAN in filtered EMG data \n\n')
        else:
            fprintf('using filtered EMG \n\n')
    
    ## for each top Feature, make the corresponding calculation
    
    topFtVal=zeros(1,length(const.classify.Mdl.PredictorNames))
# makeFtTbl_Online.m:28
    for topFt in arange(1,length(const.classify.Mdl.PredictorNames)).reshape(-1):
        # get the feature
        calcOnFtName=char(const.classify.ftUse(topFt))
# makeFtTbl_Online.m:32
        if contains(calcOnFtName,'circ'):
            calcOnFt='circ'
# makeFtTbl_Online.m:36
        else:
            calcOnFt=copy(calcOnFtName)
# makeFtTbl_Online.m:38
        # get the channel, actually want:
        if length(const.EMGch) == 8:
            calcOnCH=1 + const.EMGch(const.EMGch == const.classify.ftChUse(topFt))
# makeFtTbl_Online.m:43
        else:
            __,ii=find(const.EMGch == const.classify.ftChUse(topFt),nargout=2)
# makeFtTbl_Online.m:45
            calcOnCH=1 + ii
# makeFtTbl_Online.m:46
        # do calculation on the corresponding feature and channel, always one frame
        if 'CCI' == calcOnFt:
            topFtVal[1,topFt]=calcCCI(out.dataEMG(arange(),arange(2,end())),const)
# makeFtTbl_Online.m:54
        else:
            if 'SCCI' == calcOnFt:
                if logical_not(exist('smav','var')):
                    smav=calcSMAV(out.dataEMG(arange(),arange(2,end())))
# makeFtTbl_Online.m:58
                topFtVal[1,topFt]=calcSCCI(smav,const)
# makeFtTbl_Online.m:60
            else:
                if 'circ' == calcOnFt:
                    # need to modify calcCirc
                    topFtVal[1,topFt]=calcCirc(out.dataEMG(arange(),arange(2,end())),const,calcOnFtName)
# makeFtTbl_Online.m:64
                else:
                    if 'MADN' == calcOnFt:
                        if logical_not(exist('madn','var')):
                            madn=calcMADN(out.dataEMG(arange(),arange(2,end())))
# makeFtTbl_Online.m:68
                        topFtVal[1,topFt]=madn(arange(),calcOnCH - 1)
# makeFtTbl_Online.m:70
                    else:
                        if 'SMAV' == calcOnFt:
                            if logical_not(exist('smav','var')):
                                smav=calcSMAV(out.dataEMG(arange(),arange(2,end())))
# makeFtTbl_Online.m:74
                            topFtVal[1,topFt]=smav(arange(),calcOnCH - 1)
# makeFtTbl_Online.m:76
                        else:
                            if 'RMS' == calcOnFt:
                                topFtVal[1,topFt]=calcRMS(out.dataEMG(arange(),calcOnCH))
# makeFtTbl_Online.m:81
                            else:
                                if 'MAV' == calcOnFt:
                                    topFtVal[1,topFt]=calcMAV(out.dataEMG(arange(),calcOnCH))
# makeFtTbl_Online.m:83
                                else:
                                    if 'WL' == calcOnFt:
                                        topFtVal[1,topFt]=calcWL(out.dataEMG(arange(),calcOnCH))
# makeFtTbl_Online.m:85
                                        # uses Raw signal never filtered
                                    else:
                                        if 'VAR' == calcOnFt:
                                            if const.BayesFilter == 1:
                                                topFtVal[1,topFt]=calcVAR(out.dataEMGraw(arange(),calcOnCH))
# makeFtTbl_Online.m:90
                                            else:
                                                topFtVal[1,topFt]=calcVAR(out.dataEMG(arange(),calcOnCH))
# makeFtTbl_Online.m:92
                                        else:
                                            if 'SSC' == calcOnFt:
                                                if const.BayesFilter == 1:
                                                    topFtVal[1,topFt]=calcSSC(out.dataEMGraw(arange(),calcOnCH))
# makeFtTbl_Online.m:96
                                                else:
                                                    topFtVal[1,topFt]=calcSSC(out.dataEMG(arange(),calcOnCH))
# makeFtTbl_Online.m:98
                                            else:
                                                if 'ZC' == calcOnFt:
                                                    if const.BayesFilter == 1:
                                                        topFtVal[1,topFt]=calcZC(out.dataEMGraw(arange(),calcOnCH))
# makeFtTbl_Online.m:102
                                                    else:
                                                        topFtVal[1,topFt]=calcZC(out.dataEMG(arange(),calcOnCH))
# makeFtTbl_Online.m:104
                                                else:
                                                    if 'WAMP' == calcOnFt:
                                                        if const.BayesFilter == 1:
                                                            topFtVal[1,topFt]=calcWAMP(out.dataEMGraw(arange(),calcOnCH))
# makeFtTbl_Online.m:108
                                                        else:
                                                            topFtVal[1,topFt]=calcWAMP(out.dataEMG(arange(),calcOnCH))
# makeFtTbl_Online.m:110
                                                        # IMU features
        # mag Can use filtered data
                                                    else:
                                                        if 'A_AccMag' == calcOnFt:
                                                            topFtVal[1,topFt]=calcIMUMag_OL(out.dataAccel(arange(),arange(3,5)))
# makeFtTbl_Online.m:116
                                                        else:
                                                            if 'A_GyrMag' == calcOnFt:
                                                                topFtVal[1,topFt]=calcIMUMag_OL(out.dataGyro(arange(),arange(3,5)))
# makeFtTbl_Online.m:118
                                                                # variance uses raw data
                                                            else:
                                                                if 'A_AccVar' == calcOnFt:
                                                                    topFtVal[1,topFt]=calcIMUVar_OL(out.dataAccel(arange(),arange(3,5)))
# makeFtTbl_Online.m:122
                                                                else:
                                                                    if 'A_GyrVar' == calcOnFt:
                                                                        topFtVal[1,topFt]=calcIMUVar_OL(out.dataGyro(arange(),arange(3,5)))
# makeFtTbl_Online.m:124
    
    
    ## Normalize
    
    # element wise
    FtTbl=(topFtVal - const.classify.mu) / const.classify.std
# makeFtTbl_Online.m:134
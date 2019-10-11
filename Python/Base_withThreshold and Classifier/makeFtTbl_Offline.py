# Generated with SMOP  0.41
from libsmop import *
# makeFtTbl_Offline.m

    
@function
def makeFtTbl_Offline(EMGb=None,IMUb=None,EMGbF=None,IMUbF=None,const=None,*args,**kwargs):
    varargin = makeFtTbl_Offline.varargin
    nargin = makeFtTbl_Offline.nargin

    # EMGb is no abs yet.
    rEMGb=copy(EMGb)
# makeFtTbl_Offline.m:4
    EMGb=abs(EMGb)
# makeFtTbl_Offline.m:5
    ##
    
    FtTbl=[]
# makeFtTbl_Offline.m:9
    
    if const.BayesFilter == 1:
        # features calculated using multiple channels
        smav=calcSMAV(EMGbF)
# makeFtTbl_Offline.m:13
        madn=calcMADN(EMGbF)
# makeFtTbl_Offline.m:14
        CCI=calcCCI(EMGbF,const)
# makeFtTbl_Offline.m:15
        SCCI=calcSCCI(smav,const)
# makeFtTbl_Offline.m:16
        circTbl=calcCirstats(EMGbF)
# makeFtTbl_Offline.m:17
        # features calculated within a single chanel
        B_RMS_=calcRMS(EMGbF)
# makeFtTbl_Offline.m:20
        B_MAV_=calcMAV(EMGbF)
# makeFtTbl_Offline.m:21
        B_WL_=calcWL(EMGbF)
# makeFtTbl_Offline.m:22
    else:
        # features calculated using multiple channels
        smav=calcSMAV(EMGb)
# makeFtTbl_Offline.m:26
        madn=calcMADN(EMGb)
# makeFtTbl_Offline.m:27
        CCI=calcCCI(EMGb,const)
# makeFtTbl_Offline.m:28
        SCCI=calcSCCI(smav,const)
# makeFtTbl_Offline.m:29
        circTbl=calcCirstats(EMGb)
# makeFtTbl_Offline.m:30
        # features calculated within a single chanel
        B_RMS_=calcRMS(EMGb)
# makeFtTbl_Offline.m:33
        B_MAV_=calcMAV(EMGb)
# makeFtTbl_Offline.m:34
        B_WL_=calcWL(EMGb)
# makeFtTbl_Offline.m:35
    
    # 'freq' based not filtered
    B_VAR_=calcVAR(EMGb)
# makeFtTbl_Offline.m:40
    
    B_SSC_=calcSSC(rEMGb)
# makeFtTbl_Offline.m:41
    B_ZC_=calcZC(rEMGb)
# makeFtTbl_Offline.m:42
    B_WAMP_=calcWAMP(EMGb)
# makeFtTbl_Offline.m:43
    ##
# put into a feature table
    FtTbl=table(CCI)
# makeFtTbl_Offline.m:47
    FtTbl.Properties.VariableNames = copy(cellarray(['D_CCI']))
# makeFtTbl_Offline.m:48
    FtTbl.D_SCCI = copy(SCCI)
# makeFtTbl_Offline.m:49
    FtTbl=concat([FtTbl,circTbl])
# makeFtTbl_Offline.m:50
    for ch in arange(1,size(EMGb,2)).reshape(-1):
        #     chStr = num2str(ch);
        chStr=num2str(const.EMGch(ch))
# makeFtTbl_Offline.m:56
        FtTbl=concat([FtTbl,table(B_RMS_(arange(),ch),'VariableNames',cellarray([strcat('B_RMS_',chStr)]))])
# makeFtTbl_Offline.m:59
        FtTbl=concat([FtTbl,table(B_MAV_(arange(),ch),'VariableNames',cellarray([strcat('B_MAV_',chStr)]))])
# makeFtTbl_Offline.m:60
        FtTbl=concat([FtTbl,table(B_WL_(arange(),ch),'VariableNames',cellarray([strcat('B_WL_',chStr)]))])
# makeFtTbl_Offline.m:61
        FtTbl=concat([FtTbl,table(B_VAR_(arange(),ch),'VariableNames',cellarray([strcat('B_VAR_',chStr)]))])
# makeFtTbl_Offline.m:62
        FtTbl=concat([FtTbl,table(B_SSC_(arange(),ch),'VariableNames',cellarray([strcat('B_SSC_',chStr)]))])
# makeFtTbl_Offline.m:65
        FtTbl=concat([FtTbl,table(B_ZC_(arange(),ch),'VariableNames',cellarray([strcat('B_ZC_',chStr)]))])
# makeFtTbl_Offline.m:66
        FtTbl=concat([FtTbl,table(B_WAMP_(arange(),ch),'VariableNames',cellarray([strcat('B_WAMP_',chStr)]))])
# makeFtTbl_Offline.m:67
        FtTbl=concat([FtTbl,table(smav(arange(),ch),'VariableNames',cellarray([strcat('B_SMAV_',chStr)]))])
# makeFtTbl_Offline.m:70
        FtTbl=concat([FtTbl,table(madn(arange(),ch),'VariableNames',cellarray([strcat('B_MADN_',chStr)]))])
# makeFtTbl_Offline.m:71
    
    ## IMU FEATURES
    
    Acc=IMUb(arange(),arange(1,3),arange())
# makeFtTbl_Offline.m:77
    Gyr=IMUb(arange(),arange(4,6),arange())
# makeFtTbl_Offline.m:78
    FtTbl=concat([FtTbl,table(calcIMUVar_OL(Acc),'VariableNames',cellarray(['A_AccVar']))])
# makeFtTbl_Offline.m:79
    FtTbl=concat([FtTbl,table(calcIMUVar_OL(Gyr),'VariableNames',cellarray(['A_GyrVar']))])
# makeFtTbl_Offline.m:80
    
    if const.BayesFilter == 1:
        Acc=IMUbF(arange(),arange(1,3),arange())
# makeFtTbl_Offline.m:85
        Gyr=IMUbF(arange(),arange(4,6),arange())
# makeFtTbl_Offline.m:86
        FtTbl=concat([FtTbl,table(calcIMUMag_OL(Acc),'VariableNames',cellarray(['A_AccMag']))])
# makeFtTbl_Offline.m:87
        FtTbl=concat([FtTbl,table(calcIMUMag_OL(Gyr),'VariableNames',cellarray(['A_GyrMag']))])
# makeFtTbl_Offline.m:88
    else:
        FtTbl=concat([FtTbl,table(calcIMUMag_OL(Acc),'VariableNames',cellarray(['A_AccMag']))])
# makeFtTbl_Offline.m:92
        FtTbl=concat([FtTbl,table(calcIMUMag_OL(Gyr),'VariableNames',cellarray(['A_GyrMag']))])
# makeFtTbl_Offline.m:93
    
    
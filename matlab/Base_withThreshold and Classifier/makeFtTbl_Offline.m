function [FtTbl] = makeFtTbl_Offline(EMGb,IMUb,EMGbF,IMUbF,const)

% EMGb is no abs yet.
rEMGb = EMGb;
EMGb = abs(EMGb);

%%

FtTbl = [];  % prealloccate

if const.BayesFilter == 1
    % features calculated using multiple channels
    smav = calcSMAV(EMGbF); % nFrames*nCH
    madn = calcMADN(EMGbF); % nFrames*nCH
    CCI = calcCCI(EMGbF,const); % nFrames*1
    SCCI = calcSCCI(smav, const); % nFrames*1
    circTbl = calcCirstats(EMGbF); % nFrames*nCircVars, Table

    % features calculated within a single chanel
    B_RMS_ = calcRMS(EMGbF); % nFrames*nCH
    B_MAV_ = calcMAV(EMGbF); % nFrames*nCH
    B_WL_ = calcWL(EMGbF); % nFrames*nCH
    
else 
    % features calculated using multiple channels
    smav = calcSMAV(EMGb); % nFrames*nCH
    madn = calcMADN(EMGb); % nFrames*nCH
    CCI = calcCCI(EMGb,const); % nFrames*1
    SCCI = calcSCCI(smav, const); % nFrames*1
    circTbl = calcCirstats(EMGb); % nFrames*nCircVars, Table

    % features calculated within a single chanel
    B_RMS_ = calcRMS(EMGb); % nFrames*nCH
    B_MAV_ = calcMAV(EMGb); % nFrames*nCH
    B_WL_ = calcWL(EMGb); % nFrames*nCH
end 


% 'freq' based not filtered 
B_VAR_ = calcVAR(EMGb); % nFrames*nCH
B_SSC_ = calcSSC(rEMGb);
B_ZC_ = calcZC(rEMGb);
B_WAMP_ = calcWAMP(EMGb);
    
%%
% put into a feature table
FtTbl  = table(CCI);
FtTbl.Properties.VariableNames = {'D_CCI'};
FtTbl.D_SCCI = SCCI;
FtTbl = [FtTbl circTbl];


for ch = 1:size(EMGb,2)

%     chStr = num2str(ch);
    chStr = num2str(const.EMGch(ch));

    % Amp based
    FtTbl = [FtTbl table(B_RMS_(:,ch),'VariableNames',{strcat('B_RMS_',chStr)})];
    FtTbl = [FtTbl table(B_MAV_(:,ch),'VariableNames',{strcat('B_MAV_',chStr)})];
    FtTbl = [FtTbl table(B_WL_(:,ch),'VariableNames',{strcat('B_WL_',chStr)})];
    FtTbl = [FtTbl table(B_VAR_(:,ch),'VariableNames',{strcat('B_VAR_',chStr)})];

    % using unfiltered data
    FtTbl = [FtTbl table(B_SSC_(:,ch),'VariableNames',{strcat('B_SSC_',chStr)})];
    FtTbl = [FtTbl table(B_ZC_(:,ch),'VariableNames',{strcat('B_ZC_',chStr)})];
    FtTbl = [FtTbl table(B_WAMP_(:,ch),'VariableNames',{strcat('B_WAMP_',chStr)})];

    % Add others to FtTbl
    FtTbl = [FtTbl table(smav(:,ch),'VariableNames',{strcat('B_SMAV_',chStr)})];
    FtTbl = [FtTbl table(madn(:,ch),'VariableNames',{strcat('B_MADN_',chStr)})];

end

%% IMU FEATURES

Acc = IMUb(:,1:3,:);
Gyr = IMUb(:,4:6,:);
FtTbl = [FtTbl table(calcIMUVar_OL(Acc),'VariableNames',{'A_AccVar'})];
FtTbl = [FtTbl table(calcIMUVar_OL(Gyr),'VariableNames',{'A_GyrVar'})]; % 3 axis magnitude


if const.BayesFilter == 1
    
    Acc = IMUbF(:,1:3,:);
    Gyr = IMUbF(:,4:6,:);
    FtTbl = [FtTbl table(calcIMUMag_OL(Acc),'VariableNames',{'A_AccMag'})];
    FtTbl = [FtTbl table(calcIMUMag_OL(Gyr),'VariableNames',{'A_GyrMag'})]; % 3 axis magnitude
    
else

    FtTbl = [FtTbl table(calcIMUMag_OL(Acc),'VariableNames',{'A_AccMag'})];
    FtTbl = [FtTbl table(calcIMUMag_OL(Gyr),'VariableNames',{'A_GyrMag'})]; % 3 axis magnitude

end
    
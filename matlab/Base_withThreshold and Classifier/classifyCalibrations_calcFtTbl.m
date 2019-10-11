function [FtTbl, const, calibrationData, y] = classifyCalibrations_calcFtTbl (Data)

%% Setup

const = Data.const;

%% Setup data set to use for calibraiton 

% const.startTime1_rest; % Pressed enter for Gesture: Fingers Active  
% const.startTime1_active; % switched from rest to active for Gesture: Fingers active
% const.startTime1_end; % the last time element for the gesture Fingers Active

% The last time elements for getsture: 
% extension with fingers open
E1 = find (Data.Trial.pressed == 10,1,'last');
const.startTime1_end = Data.Trial.time(E1);
% extended fingers relaxed
E2 = find (Data.Trial.pressed == 20,1,'last');
const.startTime2_end = Data.Trial.time(E2);
% pinch
E3 = find (Data.Trial.pressed == 30,1,'last');
const.startTime3_end = Data.Trial.time(E3);


%% find time index of EMG and IMU to use

% Raw data indicies for Fingers Open Gesture calibration
ind.EMG.startTime1_rest = find(Data.EMG.Time >= const.startTime1_rest,1,'first');
ind.EMG.startTime1_active = find(Data.EMG.Time >= const.startTime1_active,1,'first');
ind.EMG.startTime1_end = find(Data.EMG.Time >= const.startTime1_end,1,'first');
ind.IMU.startTime1_rest = find(Data.IMU.Time >= const.startTime1_rest,1,'first');
ind.IMU.startTime1_active = find(Data.IMU.Time >= const.startTime1_active,1,'first');
ind.IMU.startTime1_end = find(Data.IMU.Time >= const.startTime1_end,1,'first');

% Raw data indicies for Fingers CLOSED Gesture calibration
ind.EMG.startTime2_rest = find(Data.EMG.Time >= const.startTime2_rest,1,'first');
ind.EMG.startTime2_active = find(Data.EMG.Time >= const.startTime2_active,1,'first');
ind.EMG.startTime2_end = find(Data.EMG.Time >= const.startTime2_end,1,'first');
ind.IMU.startTime2_rest = find(Data.IMU.Time >= const.startTime2_rest,1,'first');
ind.IMU.startTime2_active = find(Data.IMU.Time >= const.startTime2_active,1,'first');
ind.IMU.startTime2_end = find(Data.IMU.Time >= const.startTime2_end,1,'first');

% Raw data indicies for Fingers Pinched Gesture calibration
ind.EMG.startTime3_rest = find(Data.EMG.Time >= const.startTime3_rest,1,'first');
ind.EMG.startTime3_active = find(Data.EMG.Time >= const.startTime3_active,1,'first');
ind.EMG.startTime3_end = find(Data.EMG.Time >= const.startTime3_end,1,'first');
ind.IMU.startTime3_rest = find(Data.IMU.Time >= const.startTime3_rest,1,'first');
ind.IMU.startTime3_active = find(Data.IMU.Time >= const.startTime3_active,1,'first');
ind.IMU.startTime3_end = find(Data.IMU.Time >= const.startTime3_end,1,'first');


%% Organize calibration data into tables

% returns filtered and raw data
% Prepare Raw EMG data
[const,D_EMG, D_EMGF] = classifyCalibrations_prepareEMG(Data, const, ind); % uses const.readyMean
% Prepare Raw IMU data
[const,D_IMU, D_IMUF] = classifyCalibrations_prepareIMU(Data, const, ind); % makes IMU ReadyMean

%%

% get main extensor sensor
EM =  D_EMGF.TL<3; % valid rows (not pinch)
EMGUse = table2array(D_EMGF(EM,2:end-1));
x = mean(EMGUse);
   
% get the index with highest activity
[~,I0] = sort(x,'descend');  
y = const.EMGch(I0(1)); % I is the CH.


%% Store 

calibrationData.EMG = D_EMG;
calibrationData.EMGf = D_EMGF;
calibrationData.IMU = D_IMU;
calibrationData.IMUf = D_IMUF;

%% BIN DATA

% check WINBIN/4 must be int to have whole bins for IMU data
% this happens already in setupConst. Normally should not be an issue
if mod( const.WINBIN/4 ,1) == 0
  % integer is good
  const.binsize = const.WINBIN / const.sf; % number of seconds / bin - This must be even        
else
  % change WINBIN so that WINBIN/4 is an integer
  const.WINBIN  = 4*round(const.WINBIN/4); 
  const.binsize = const.WINBIN / const.sf;
end

[D_EMGb,TLb] = classifyCalibrations_binDataEMG(D_EMG,const); % make into bins - EMG
[D_EMGFb,~] = classifyCalibrations_binDataEMG(D_EMGF,const); % make into bins - EMG

[D_IMUb,D_EMGb] = classifyCalibrations_binDataIMU(D_IMU,D_EMGb,const); % make into bins - IMU, and cuts to match
[D_IMUFb,D_EMGFb] = classifyCalibrations_binDataIMU(D_IMUF,D_EMGFb,const); % make into bins - IMU

%% calculate FtTbl

% MAKE SURE THIS WORKS NOW
[FtTbl] = makeFtTbl_Offline(D_EMGb,D_IMUb,D_EMGFb,D_IMUFb,const);

%% add Truelabel

TL = TLb(1,1,:);
TrueLabel = reshape(TL, size(TL,3),1); % turns a 1x1xN into an Nx1
FtTbl = [array2table(TrueLabel) FtTbl];


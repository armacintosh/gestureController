function [const] = classifyCalibrations_setupEMG_Const(const)


%% CONST

const.WAMPthresh = 0.02; 
const.ZCthresh = 0.02;
const.SSCthresh = 0.02;
% const.WINBIN = 20;
% const.EMGch = 2:9; % D has time in col. 1 and true label in col 10
% const.Cal_extensor_sensors = [1 2]; % since we have always moved it to the top.
% const.Cal_flexor_sensors = [5 6];

% filter characteristics
% const.sfEMG = 200;
% const.low_freq = 2.5;
const.sfIMU = 50;


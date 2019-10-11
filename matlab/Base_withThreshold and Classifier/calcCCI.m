function [ CCI_OUT  ] = calcCCI( EMGb, const )

try
    senE = const.Cal_extensor_sensors;
    senF = const.Cal_flexor_sensors;
catch
    senE = const.extensor_sensors-1;
    senF = const.flexor_sensors-1;
end
    
% for when there is ia 3 dimensionial array, 3rd D is nFrames
[winLen , nCH, nFrames] = size(EMGb); % winLen is the unused dimension

% RMS
preCCI = rms(EMGb(:,[senE senF],:),1); % each CH mean in the frame (ABS already done).

rmsEx = mean(preCCI(:,1:2,:),2);
rmsFx = mean(preCCI(:,3:4,:),2);

% Should be 1 col * nFrames rows
answ = rmsEx ./ rmsFx ; 


% this is an array  N bin rows and 1 colomuns
CCI_OUT = reshape(answ,[1,nFrames])';


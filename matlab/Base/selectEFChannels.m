function [const, out] = selectEFChannels (const, out, calData)

%%
% index of when cal game went from ready to active
strtind = const.CalGoTime ;

% remove rest phase mean ch activity while playing ASTRO
EMG = calData.cal(strtind:end, 2:end ) - const.ReadyMean; 

%% select the top 50 percent of the trail data..

cumEMG = sum(EMG,2); % power of that instant
[B,index] = sortrows(cumEMG); % index the rows and sort by total amplitude
indkp = index(B > median(B)); % the rows of index to keep (median)
EMGuse = EMG(index(indkp),:); % EMG to use for guessing the extensor channels...

%% Select which ch are extensors.

% create const.extensor_sensors
    % third argument to avoid filtering (used in C_calibrateUserProfile.m)
    % 2:end are the EMG CHANNELS (regardless of the number used)
const = findMyoUp(EMGuse, const, 1);  % outputs real channel columns

% select flexors based on either a) calib. flexor distnace, or b) assume the opposite side    
const = selectMyoDown (const); % outputs real channel columns
fprintf('Extensors Sensor == Myo Sensors:  %i-%i \n\n',const.extensor_sensors(1),const.extensor_sensors(2));
fprintf('Flexor Sensor == Myo Sensors:   %i-%i \n\n',const.flexor_sensors(1),const.flexor_sensors(2));

% const.extensor_sensors outputs in terms of actual Myo channles [e.g. 3:6, 1:8, 2:7]
% convert to col. index of const.myoCHsUsed, which has col 1 == time
ESI1 = find(const.EMGch == const.extensor_sensors(1));
ESI2 = find(const.EMGch == const.extensor_sensors(2));
const.extensor_sensors(1) = ESI1 +1; % + 1 for time col.
const.extensor_sensors(2) = ESI2 +1; % + 1 for time col.
% const.extensor_sensors are now the col. index of const.myoCHsUsed to use 

% convert to col. index of const.myoCHsUsed, which has col 1 == time
FSI1 = find(const.EMGch == const.flexor_sensors(1));
FSI2 = find(const.EMGch == const.flexor_sensors(2));
const.flexor_sensors(1) = FSI1+1; % + 1 for time col.
const.flexor_sensors(2) = FSI2+1; % + 1 for time col.
% const.flexor_sensors are now the col. index of const.myoCHsUsed, not the channel number


% maybe to remove if not using old calib.
try
    close('calibrate');
catch
end



function [ smav_OUT ] = calcSMAV( EMGb )
% Channel MAV scaled to average of whole arm at that instant.


% for when there is ia 3 dimensionial array, 3rd D is nFrames
[~ , nCH, nFrames] = size(EMGb); % winLen is the unused dimension

preMMAV = mean(EMGb,1); % each CH mean in the frame (ABS already done).
MMAV = mean(preMMAV,2); % average of whole arm at that instant.

smav = preMMAV./MMAV; % each CH Smav in the frame, 

% reshape
% this is an array  nCH colomuns long and N bin rows
smav_OUT = reshape(smav,[nCH,nFrames])';





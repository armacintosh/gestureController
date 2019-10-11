function [ rms_OUT ] = calcRMS( EMGb )
% Returns the RMS in each bin

% for when there is ia 3 dimensionial array, 3rd D is nFrames
[winLen , nCH, nFrames] = size(EMGb); % winLen is the unused dimension

answ = rms(EMGb(:,:,:),1); % each CH mean in the frame (ABS already done).

% this is an array  nCH colomuns long and N bin rows
rms_OUT = reshape(answ,[nCH,nFrames])';


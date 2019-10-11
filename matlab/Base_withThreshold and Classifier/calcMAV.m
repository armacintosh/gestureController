function [ answ_OUT ] = calcMAV ( EMGb )

% for when there is ia 3 dimensionial array, 3rd D is nFrames
[winLen , nCH, nFrames] = size(EMGb); % winLen is the unused dimension

% ABS already done
answ = mean(EMGb(:,:,:),1); % each CH mean in the frame (ABS already done).
% this is an array  nCH colomuns long and N bin rows
answ_OUT = reshape(answ,[nCH,nFrames])';


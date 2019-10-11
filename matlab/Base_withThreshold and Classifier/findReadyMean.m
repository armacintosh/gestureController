function [const] = findReadyMean (const,calData)

% index of const.startTime1_active -- is when it changed from rest to active
strtInd = calData.switch1;

% Gets data recorded during 'ready set go'
ExRaw = calData.cal(1:strtInd,2:end); 

% find the mean of the phase before starting to extend, the mean of bottom 90% of activity
Ready = ExRaw( ExRaw(1:strtInd) == prctile(ExRaw(1:strtInd),50) ,:);

% 1 row of mean values during ready position const.myoCHsUsed(2:end) cols long
const.ReadyMean = mean(Ready);
function [const] = findReadyMean (const,calData)

% index of start
strtInd = const.CalGoTime; % index of enrow

% Gets data recorded during 'ready set go'
ExRaw = calData.cal(1:strtInd,2:end); 

% find the mean of the phase before starting to extend, the mean of bottom 90% of activity
ExSum = sum(ExRaw,2); % row sum
[~,i] = sort(ExSum);% index of bottom 50% of ExSum
iuse = i(1:floor(length(ExRaw)/2));

% 1 row of mean values during ready position const.myoCHsUsed(2:end) cols long
const.ReadyMean = mean(ExRaw(iuse,:));

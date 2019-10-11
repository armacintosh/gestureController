function [ReadyMean] = classifyCalibrations_findReadyMeanIMU (restData)

%%
restData = restData {:,2:end}; % not time
% restData = abs(restData {:,:}) ./ 128; % change units of EMG

% find the mean of the phase before starting to extend, the mean of bottom 90% of activity
% only keep the middle 50% of the data
ReadyMean = mean(restData);

%%
function [ReadyMean] = classifyCalibrations_findReadyMean (restData)

%%
restData = restData (:,2:end); % not time
restData = abs(restData {:,:}) ./ 128; % change units of EMG

% find the mean of the phase before starting to extend, the mean of bottom 90% of activity
% only keep the middle 50% of the data
Ready = restData;
ReadyMean = zeros(1,size(Ready,2));
p = prctile(restData, [5 95]);
for col = 1:size(Ready,2) % for each col.
    mid = Ready(Ready(:,col) >= p(1,col)) ;
    mid = mid (mid <= p(2,col)) ;
    ReadyMean(1,col) = mean(mid) ;
end

%%
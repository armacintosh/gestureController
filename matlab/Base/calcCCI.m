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





% %% OLD WAY
% 
% [~, C] = size(binned_signal_allCHs);
% [R, ~] = size(binned_signal_allCHs{1});
% 
% preCCI = zeros(R,C);
% % get MMAV for each bin
% for nCH = 1:size(binned_signal_allCHs,2)
%     preCCI(:,nCH) = sqrt(calcMAV(binned_signal_allCHs{nCH}));
% %     preMMAV(:,nCH) = calcMAV(binned_signal_allCHs(:,nCH));
% end
% 
% if size(preCCI,2) == 4
%     rmsEx = mean(preCCI(:,1:2),2);
%     rmsFx = mean(preCCI(:,3:4),2);
% else 
%     rmsEx = mean(preCCI(:,2:3),2);
%     rmsFx = mean(preCCI(:,6:7),2);
% end    
% 
% answ = rmsEx ./ rmsFx ; % Should be bin long by 1 val.
% % < 1 means that flexors are more active than extensors...
% % no limit to max.
% 
% 
% 
% 
% % % ratio of RMS of the antagonist muscle to the RMS of the agonist muscle (Fig. 2).
% % 
% % % Single bin
% % % rms = sqrt (mean (binned_signal_allCHs .^2) ); % should be 1 row 8 ch
% % % answ = mean(rms(2:3)) / mean(rms(6:7)) ;
% % 
% % % manu bins
% % rms = sqrt (mean (binned_signal_allCHs .^2) ); % should be 1 row 8 ch
% % answ = mean(rms(2:3)) / mean(rms(6:7)) ;
%   % 2:3 are extensors
%   % 6:7 are flexors
%   % could standardize this better for 4 ch problems..

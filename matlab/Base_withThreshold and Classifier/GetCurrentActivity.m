function [out] = GetCurrentActivity(const, out)

% baseline already subtracted from data
% the extensor / flexor sensors are: 
try
    
    % just use the first sensor or both.
    if const.nChActivity  == 1
        SenE = const.extensor_sensors(1); % +2 for time stamps 
        SenF = const.flexor_sensors(1);
    elseif const.nChActivity == 2
        SenE = const.extensor_sensors; % +2 for time stamps 
        SenF = const.flexor_sensors;
    end 
    
catch

    % default to how we instructed them to put it on
    SenE = [2, 3]; % +2 for time stamps 
    SenF = [6, 7];
end 
    
% get only required data into 2 aray (2*BinSize * N bins); 
% removes time col and picks the E and F channels data
E = out.dataEMG(:,SenE); 
E = E(:); % stack the 2 extensor channels in each frame

F = out.dataEMG(:,SenF); 
F = F(:); % stack the 2 extensor channels in each frame


% get MAV of each bin
out.mavE = mean(abs(E)); % one number for this bin
out.mavF = mean(abs(F)); % one number for this bin

function [ answ_OUT ] = calcZC(EMGb)
% Returns the number of times the signal amplitude in each bin crosses the
% Thresh, traditionally 0, but adjuested to thresh here
[R, C, F] = size(EMGb);

answ = zeros(1, C, F);
for f = 1:F % for each frame
    for i = 1:C % for each channel
        thresh = abs(mean(prctile(EMGb(:,i,:),50))); % 20th percentile of the EMG activity of the channel.
%         thresh = 0;
        count = 0;
        for j = 1 : R-2 % for each row 
            if((((EMGb(j,i,f) > 0) && (EMGb(j+1,i,f) < 0))... % if it crosses 0
                    || ((EMGb(j,i,f) < 0) && (EMGb(j+1,i,f) > 0)))... % or if it crosses 0 the other way
                    && ((abs(EMGb(j,i,f)) >= thresh)... % and the difference in activity is > a value thresh
                    || (abs(EMGb(j+1,i,f)) >= thresh))) % or the difference in activity is > a value thresh
            count = count + 1;
            end
        end
        answ(1,i,f) = count;
    end
end 

answ_OUT = reshape(answ,[C,F])';


end
function [ answ_OUT ] = calcWAMP(EMGb)
% Calculates the Willison amplitude (WAMP) of a bin
%
% WAMP equals the number of times the absolute difference between
% two consecutive EMG samples exceeds a predetermined threshold
[R, C, F] = size(EMGb);


absdiff = abs(diff(EMGb,[],1));

answ = zeros(1, C, F);
for f = 1:F % for each frame
    for i = 1:C % for each channel
        thresh = abs(mean(prctile(absdiff(:,i,:),20))); % 20th percentile of the EMG activity of the channel.
        count = 0;
        for j = 1 : R-1 % for each row 
            if absdiff(j,i,f) >= thresh
                count = count + 1;
            end
        end
        answ(1,i,f) = count;
    end
end 

answ_OUT = reshape(answ,[C,F])';

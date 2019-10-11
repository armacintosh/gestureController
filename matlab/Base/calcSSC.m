function [ answ_OUT ] = calcSSC(EMGb)
% Number of slope sign changes of a signal
%
% Returns the number of times the slope of the signal's
% sign changes and the absolute value of one of the slopes
% is greater than or equal to the threshold 'thresh'

% signal slope change, how many times it moves over 20th percentile of the
% activity 

[R, C, F] = size(EMGb);

slopes = diff(EMGb,[],1);

answ = zeros(1, C, F);
for f = 1:F % for each frame
    for i = 1:C % for each channel
        thresh = abs(mean(prctile(slopes(:,i,:),20))); % 20th percentile of the EMG activity of the channel.
        count = 0;
        for j = 1 : R-2 % for each row 
            if((((slopes(j,i,f) > 0) && (slopes(j+1,i,f) < 0))... % if it crosses 0
                    || ((slopes(j,i,f) < 0) && (slopes(j+1,i,f) > 0)))... % or if it crosses 0 the other way
                    && ((abs(slopes(j,i,f)) >= thresh)... % and the difference in activity is > a value thresh
                    || (abs(slopes(j+1,i,f)) >= thresh))) % or the difference in activity is > a value thresh

            count = count + 1;
            end
        end
        answ(1,i,f) = count;
    end
end 

answ_OUT = reshape(answ,[C,F])';



%%

%  OLD WAY
% [R, C] = size(binned_signal);
% slopes = diff(binned_signal,[],2);
% 
% 
% for i = 1:R % for each bin
%     count = 0;
%     for j = 1 : C-2
%         if((((slopes(i,j) > 0) && (slopes(i,j+1) < 0))...
%                 || ((slopes(i,j) < 0) && (slopes(i,j+1) > 0)))...
%                 && ((abs(slopes(i,j)) >= thresh)...
%                 || (abs(slopes(i,j+1)) >= thresh)))
%             
%         count = count + 1;
%         end
%     end
%     answ(i,:) = count;
% end
% 
% 
% end

function [ answ_OUT  ] = calcWL( EMGb )
% Returns the waveform length for the signal in each bin
%%
[R, C, F] = size(EMGb);
answ = zeros(1, C, F);
for f = 1:F
    for i =1:C % for each col.
        len = 0;
        for j = 1: R-1 % cols = number of elements in bin
            len  = len + abs(EMGb(j+1,i, f) - EMGb(j,i,f));
        end
        answ(1,i,f) = len;
    end

end

answ_OUT = reshape(answ,[C,F])';



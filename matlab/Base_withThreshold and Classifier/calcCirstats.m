function [ circTbl, ori ] = calcCirstats(EMGb)

%%

[~ , nCH, nFrames] = size(EMGb); % winLen is the unused dimension
preMMAV = mean(EMGb,1); % each CH mean in the frame (ABS already done).
mav = reshape(preMMAV,[nFrames, nCH]);

OriIncrement = pi/(size(mav,2)/2); % only using 4 sensors... ideally would be evenly spaced around the arm...
ori = 0 : OriIncrement : 2*pi - OriIncrement;
dori = diff(ori(1:2)); % spacing of bins
[R, C] = size(mav);

%%

% would like to make these into array functions.
[circMean, circVar, circStd, circSkw, circKrt, circR] = deal(zeros (R,1));
for bin = 1:R
    % store circ stat values for each bin
    circMean(bin,1)= circ_mean(    ori,mav(bin,:),2); % mean direction for the bin in rads, can be w 95% CI
    circVar(bin,1) = circ_var(     ori,mav(bin,:),dori,2); % 1-resultant vector mag. the bin [0 1]
    circStd(bin,1) = circ_std(     ori,mav(bin,:),dori,2); % angular deviation of the bin [0 Root2]
    circSkw(bin,1) = circ_skewness(ori,mav(bin,:),2); % circular skewness can be computed as (Pewsey 2004). 0 indicates a symmetric population around the mean direction.
    circKrt(bin,1) = circ_kurtosis(ori,mav(bin,:),2); % large positive sample value of k close to one indicates a strongly peaked distribution.
    circR(bin,1)   = circ_r(       ori,mav(bin,:),dori,2); % length of the mean resultant vector [0 1]

end

circTbl = table(circMean, circVar, circStd, circSkw, circKrt, circR);
circTbl.Properties.VariableNames = {'C_circMean' 'C_circVar' 'C_circStd' 'C_circSkw' 'C_circKrt' 'C_circR'};



function [ circStat ] = calcCirc(EMGb, const,calcOnFtName)

%%

[~ , nCH, nFrames] = size(EMGb); % winLen is the unused dimension
preMMAV = mean(EMGb,1); % each CH mean in the frame (ABS already done).
mav = reshape(preMMAV,[nFrames, nCH]);


%% Using Circstat2012a toolbox

switch calcOnFtName 
           
    % store circ stat values for each bin
    case 'circMean'
        circStat(nFrames,1)= circ_mean(const.ori,mav(nFrames,:),2); % mean direction for the bin in rads, can be w 95% CI
    case 'circVar'
        circStat(nFrames,1) = circ_var(const.ori,mav(nFrames,:),const.dori,2); % 1-resultant vector mag. the bin [0 1]
    case 'circStd'
        circStat(nFrames,1) = circ_std(const.ori,mav(nFrames,:),const.dori,2); % angular deviation of the bin [0 Root2]
    case 'circSkw'
        circStat(nFrames,1) = circ_skewness(const.ori,mav(nFrames,:),2); % circular skewness can be computed as (Pewsey 2004). 0 indicates a symmetric population around the mean direction.
    case 'circKrt'
        circStat(nFrames,1) = circ_kurtosis(const.ori,mav(nFrames,:),2); % large positive sample value of k close to one indicates a strongly peaked distribution.
    case 'circR'
        circStat(nFrames,1)   = circ_r(const.ori,mav(nFrames,:),const.dori,2); % length of the mean resultant vector [0 1]

end



function [ madn_OUT ] = calcMADN( EMGb )
% described from: https://bidal.sfsu.edu/~kazokada/research/okada_embc17_myoFeature.pdf v

if isa (EMGb, 'double') 
    %%
    % for when there is ia 3 dimensionial array, 3rd D is nFrames
    [winLen , nCH, nFrames] = size(EMGb); % winLen is the unused dimension
       
    % each window of data first has its mean value subtracted from each raw data point
    preMMAV = mean(EMGb,1); % each CH mean in the frame (ABS already done).
    frameMean = mean(preMMAV,2); % average of whole arm at that instant.
    C = EMGb - frameMean;
    
    % gets SD of each frame 
    frameVals = reshape(EMGb,[winLen*nCH , nFrames]);
    frameSTD = std(frameVals);
    frameSTD = reshape(frameSTD, [1,1,nFrames]);
    
    %  the resulting values (C) are divided by their standard deviation
    D = C ./ frameSTD;
    
    %% find abs difference between neighbours 
    
    % Numerator:
    
    % element wise abs diff between nCH and nCH+1
    Dif18 = abs( D(:,1,:) - D(:,nCH,:) );
    y = abs(diff(D,[],2)); % does 1-7
    y = [y Dif18];
    
    % sum of difference between all elements 
    ySum = sum(y);
    
    % denominator is window length (binsize)
    madn = ySum / winLen;
    
    % this is an array  N bin rows and nCH colomuns
    madn_OUT = reshape(madn,[nCH,nFrames])';

    
    
    
end



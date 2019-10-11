function [ Resultant ] = calcIMUMag_OL(Acc)
% input the binned Gyr/acceleration as a 1x3 cell
% each cell has binned rows 'window' columns long by n rows.

%%

% for when there is ia 3 dimensionial array, 3rd D is nFrames
[nRows , nCH, nFrames] = size(Acc); % winLen is the unused dimension

preRes = mean(Acc,1); % each CH mean in the frame (ABS already done).
Res = sqrt(     preRes(1,1,:).^2 + ...
                preRes(1,2,:).^2 + ...
                preRes(1,3,:).^2) ; 
Resultant = reshape(Res,[nFrames,1]);
                

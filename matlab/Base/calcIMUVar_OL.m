function [ Variance ] = calcIMUVar_OL(Acc)
% input the binned Gyr/acceleration as a 1x3 cell
% each cell has binned rows 'window' columns long by n rows.

% for when there is ia 3 dimensionial array, 3rd D is nFrames
[nRows , nCH, nFrames] = size(Acc); % winLen is the unused dimension

Var = sqrt( Acc(:,1,:).^2 + ...
            Acc(:,2,:).^2 + ...
            Acc(:,3,:).^2) ; 
preVar = var(Var,1); % each CH mean in the frame (ABS already done).        
Variance = reshape(preVar,[nFrames,1]);


end
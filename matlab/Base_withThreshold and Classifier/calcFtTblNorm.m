function [XNorm, mu, stddev] = calcFtTblNorm(X)
% This function provides feature normalization by taking in the input X and
% calculating the normalized inputs along with the mean and standard
% deviation or range for each feature.
% X = (m x d) dimensions
% mean = (1 x d)
% stddev = (1 x d)

% Declare variables
XNorm = zeros(size(X));

mu = real(mean(X{:,:}));
stddev = real(std(X{:,:})) ;
% rng = max(X{:,:}) - min(X{:,:}) ;

% subtracts the average from each row
Num = bsxfun(@minus, X{:,:}, mu);

% divides Num by the range for each row
XNorm = real(bsxfun(@rdivide, Num, stddev)); % could be rng too

XNorm = array2table(XNorm);

XVarNames = X.Properties.VariableNames;
XNorm.Properties.VariableNames = XVarNames;



end

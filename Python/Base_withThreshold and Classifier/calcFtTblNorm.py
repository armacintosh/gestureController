# Generated with SMOP  0.41
from libsmop import *
# calcFtTblNorm.m

    
@function
def calcFtTblNorm(X=None,*args,**kwargs):
    varargin = calcFtTblNorm.varargin
    nargin = calcFtTblNorm.nargin

    # This function provides feature normalization by taking in the input X and
# calculating the normalized inputs along with the mean and standard
# deviation or range for each feature.
# X = (m x d) dimensions
# mean = (1 x d)
# stddev = (1 x d)
    
    # Declare variables
    XNorm=zeros(size(X))
# calcFtTblNorm.m:10
    mu=real(mean(X[arange(),arange()]))
# calcFtTblNorm.m:12
    stddev=real(std(X[arange(),arange()]))
# calcFtTblNorm.m:13
    # rng = max(X{:,:}) - min(X{:,:}) ;
    
    # subtracts the average from each row
    Num=bsxfun(minus,X[arange(),arange()],mu)
# calcFtTblNorm.m:17
    # divides Num by the range for each row
    XNorm=real(bsxfun(rdivide,Num,stddev))
# calcFtTblNorm.m:20
    
    XNorm=array2table(XNorm)
# calcFtTblNorm.m:22
    XVarNames=X.Properties.VariableNames
# calcFtTblNorm.m:24
    XNorm.Properties.VariableNames = copy(XVarNames)
# calcFtTblNorm.m:25
    return XNorm,mu,stddev
    
if __name__ == '__main__':
    pass
    
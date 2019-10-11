# Generated with SMOP  0.41
from libsmop import *
# calcIMUVar_OL.m

    
@function
def calcIMUVar_OL(Acc=None,*args,**kwargs):
    varargin = calcIMUVar_OL.varargin
    nargin = calcIMUVar_OL.nargin

    # input the binned Gyr/acceleration as a 1x3 cell
# each cell has binned rows 'window' columns long by n rows.
    
    # for when there is ia 3 dimensionial array, 3rd D is nFrames
    nRows,nCH,nFrames=size(Acc,nargout=3)
# calcIMUVar_OL.m:6
    
    Var=sqrt(Acc(arange(),1,arange()) ** 2 + Acc(arange(),2,arange()) ** 2 + Acc(arange(),3,arange()) ** 2)
# calcIMUVar_OL.m:8
    preVar=var(Var,1)
# calcIMUVar_OL.m:11
    
    Variance=reshape(preVar,concat([nFrames,1]))
# calcIMUVar_OL.m:12
    return Variance
    
if __name__ == '__main__':
    pass
    
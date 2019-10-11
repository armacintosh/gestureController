# Generated with SMOP  0.41
from libsmop import *
# calcIMUMag_OL.m

    
@function
def calcIMUMag_OL(Acc=None,*args,**kwargs):
    varargin = calcIMUMag_OL.varargin
    nargin = calcIMUMag_OL.nargin

    # input the binned Gyr/acceleration as a 1x3 cell
# each cell has binned rows 'window' columns long by n rows.
    
    ##
    
    # for when there is ia 3 dimensionial array, 3rd D is nFrames
    nRows,nCH,nFrames=size(Acc,nargout=3)
# calcIMUMag_OL.m:8
    
    preRes=mean(Acc,1)
# calcIMUMag_OL.m:10
    
    Res=sqrt(preRes(1,1,arange()) ** 2 + preRes(1,2,arange()) ** 2 + preRes(1,3,arange()) ** 2)
# calcIMUMag_OL.m:11
    Resultant=reshape(Res,concat([nFrames,1]))
# calcIMUMag_OL.m:14
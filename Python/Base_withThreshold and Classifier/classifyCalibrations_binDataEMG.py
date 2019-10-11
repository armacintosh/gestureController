# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_binDataEMG.m

    
@function
def classifyCalibrations_binDataEMG(D=None,const=None,*args,**kwargs):
    varargin = classifyCalibrations_binDataEMG.varargin
    nargin = classifyCalibrations_binDataEMG.nargin

    Dd=D[arange(),arange(2,end())]
# classifyCalibrations_binDataEMG.m:3
    
    # WINBIN rows * NCH cols * N Frames of time
    remainder=rem(size(Dd,1),const.WINBIN)
# classifyCalibrations_binDataEMG.m:6
    
    x=Dd(arange(1,end() - remainder),arange())
# classifyCalibrations_binDataEMG.m:7
    x=x.T
# classifyCalibrations_binDataEMG.m:8
    x=ravel(x)
# classifyCalibrations_binDataEMG.m:9
    # check this
    Db=permute(reshape(x,size(Dd,2),const.WINBIN,[]),concat([2,1,3]))
# classifyCalibrations_binDataEMG.m:12
    
    EMGb=Db(arange(),arange(1,end() - 1),arange())
# classifyCalibrations_binDataEMG.m:14
    
    TLb=Db(arange(),end(),arange())
# classifyCalibrations_binDataEMG.m:15
    
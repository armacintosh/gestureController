# Generated with SMOP  0.41
from libsmop import *
# evalGyro.m

    
@function
def evalGyro(const=None,out=None,store=None,*args,**kwargs):
    varargin = evalGyro.varargin
    nargin = evalGyro.nargin

    ##
# get last few second of Gyroeration activity, # out.normGyro = store.GyroRes(end);
    out.normGyro = copy(max(store.GyroRes(arange(end() - (const.runningAvg),end()))))
# evalGyro.m:5
    out.maxGyro = copy(const.aboveBaseGyro)
# evalGyro.m:6
    # decide to give IMU feedback or not.
    if out.normGyro > out.maxGyro:
        out.PredGyro = copy(1)
# evalGyro.m:10
    else:
        out.PredGyro = copy(0)
# evalGyro.m:12
    
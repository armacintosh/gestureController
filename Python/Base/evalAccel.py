# Generated with SMOP  0.41
from libsmop import *
# evalAccel.m

    
@function
def evalAccel(const=None,out=None,store=None,*args,**kwargs):
    varargin = evalAccel.varargin
    nargin = evalAccel.nargin

    # get last few second of acceleration activity, # out.normAccel = store.AccelRes(end);
    out.normAccel = copy(max(store.AccelRes(arange(end() - (const.runningAvg),end()))))
# evalAccel.m:4
    
    if (out.currentMaxAccel - out.currentBaseAccel) < std(store.AccelRes):
        out.maxAccel = copy(out.currentMaxAccel + (dot((dot((out.currentMaxAccel - out.currentBaseAccel),2)),const.aboveBaseAccel)))
# evalAccel.m:7
    else:
        out.maxAccel = copy(out.currentMaxAccel + (dot(((out.currentMaxAccel - out.currentBaseAccel) / 2),const.aboveBaseAccel)))
# evalAccel.m:9
    
    # decide to give IMU feedback or not.
    if out.normAccel > out.maxAccel:
        out.PredAccel = copy(1)
# evalAccel.m:14
    else:
        out.PredAccel = copy(0)
# evalAccel.m:16
    
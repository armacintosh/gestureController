# Generated with SMOP  0.41
from libsmop import *
# GetCurrentActivity.m

    
@function
def GetCurrentActivity(const=None,out=None,*args,**kwargs):
    varargin = GetCurrentActivity.varargin
    nargin = GetCurrentActivity.nargin

    # baseline already subtracted from data
# the extensor / flexor sensors are:
    try:
        # just use the first sensor or both.
        if const.nChActivity == 1:
            SenE=const.extensor_sensors(1)
# GetCurrentActivity.m:9
            SenF=const.flexor_sensors(1)
# GetCurrentActivity.m:10
        else:
            if const.nChActivity == 2:
                SenE=const.extensor_sensors
# GetCurrentActivity.m:12
                SenF=const.flexor_sensors
# GetCurrentActivity.m:13
    finally:
        pass
    
    
    # get only required data into 2 aray (2*BinSize * N bins); 
# removes time col and picks the E and F channels data
    E=out.dataEMG(arange(),SenE)
# GetCurrentActivity.m:25
    E=ravel(E)
# GetCurrentActivity.m:26
    
    F=out.dataEMG(arange(),SenF)
# GetCurrentActivity.m:28
    F=ravel(F)
# GetCurrentActivity.m:29
    
    # get MAV of each bin
    out.mavE = copy(mean(abs(E)))
# GetCurrentActivity.m:33
    
    out.mavF = copy(mean(abs(F)))
# GetCurrentActivity.m:34
    
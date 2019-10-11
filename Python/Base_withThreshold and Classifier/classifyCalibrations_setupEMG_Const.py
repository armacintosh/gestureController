# Generated with SMOP  0.41
from libsmop import *
# classifyCalibrations_setupEMG_Const.m

    
@function
def classifyCalibrations_setupEMG_Const(const=None,*args,**kwargs):
    varargin = classifyCalibrations_setupEMG_Const.varargin
    nargin = classifyCalibrations_setupEMG_Const.nargin

    ## CONST
    
    const.WAMPthresh = copy(0.02)
# classifyCalibrations_setupEMG_Const.m:6
    const.ZCthresh = copy(0.02)
# classifyCalibrations_setupEMG_Const.m:7
    const.SSCthresh = copy(0.02)
# classifyCalibrations_setupEMG_Const.m:8
    # const.WINBIN = 20;
# const.EMGch = 2:9; # D has time in col. 1 and true label in col 10
# const.Cal_extensor_sensors = [1 2]; # since we have always moved it to the top.
# const.Cal_flexor_sensors = [5 6];
    
    # filter characteristics
# const.sfEMG = 200;
# const.low_freq = 2.5;
    const.sfIMU = copy(50)
# classifyCalibrations_setupEMG_Const.m:17
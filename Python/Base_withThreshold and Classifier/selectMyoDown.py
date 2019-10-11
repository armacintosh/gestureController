# Generated with SMOP  0.41
from libsmop import *
# selectMyoDown.m

    
@function
def selectMyoDown(const=None,*args,**kwargs):
    varargin = selectMyoDown.varargin
    nargin = selectMyoDown.nargin

    if length(const.EMGch) == 8:
        if const.useUserProfile == 1:
            const=selectMyoDownCalibrated(const)
# selectMyoDown.m:7
        else:
            ## The way below just gets the opposite side, 
            # If I just always use opposite side, then It would work regardless of the way you put it on…
            # AND I WOULD NOT NEED TO calibrateUserProfile…
            # BUT, it would not get cases when flexors are closer to extensors… and may allow side movement…
            # if overlap, assumme opposite side
            # distance to opposite sensor
            lookaway=round(length(const.EMGch) / 2)
# selectMyoDown.m:16
            dist1=abs(const.EMGch - const.extensor_sensors(1))
# selectMyoDown.m:19
            FI1=dist1 == 0 + lookaway
# selectMyoDown.m:20
            dist2=abs(const.EMGch - const.extensor_sensors(2))
# selectMyoDown.m:22
            FI2=dist2 == 0 + lookaway
# selectMyoDown.m:23
            const.flexor_sensors[1]=const.EMGch(FI1)
# selectMyoDown.m:25
            const.flexor_sensors[2]=const.EMGch(FI2)
# selectMyoDown.m:26
    else:
        lookaway=round(length(const.EMGch) / 2)
# selectMyoDown.m:32
        dist1=abs(const.EMGch - const.extensor_sensors(1))
# selectMyoDown.m:35
        FI1=dist1 == 0 + lookaway
# selectMyoDown.m:36
        dist2=abs(const.EMGch - const.extensor_sensors(2))
# selectMyoDown.m:38
        FI2=dist2 == 0 + lookaway
# selectMyoDown.m:39
        const.flexor_sensors[1]=const.EMGch(FI1)
# selectMyoDown.m:41
        const.flexor_sensors[2]=const.EMGch(FI2)
# selectMyoDown.m:42
    
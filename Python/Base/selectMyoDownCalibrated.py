# Generated with SMOP  0.41
from libsmop import *
# selectMyoDownCalibrated.m

    
@function
def selectMyoDownCalibrated(const=None,*args,**kwargs):
    varargin = selectMyoDownCalibrated.varargin
    nargin = selectMyoDownCalibrated.nargin

    try:
        # to define: from First Day Calibration, know how far flexors are
        # relative to extensors, then on new day, when you find the new
        # extensor location, put the flexors in the same relative position
        # const.flexorDistance-- only there if using a calib. profile
        # to recreate/ find the flexor sensor given the extensor sensor and the
        # flesorDistance, do: extensor_sensor - (flexorDistance);
        const.flexor_sensors = copy(const.extensor_sensors - const.flexorDistance)
# selectMyoDownCalibrated.m:10
        # overlapping?
        overlap=ismember(const.extensor_sensors,const.flexor_sensors)
# selectMyoDownCalibrated.m:15
        if overlap(1) or overlap(2):
            disp('overlapping e f channles')
            # if overlap, pick sensor next to the non-overlapping
                # flexor that is not an extensor sensor
                # this happens becuase I am not sorting them...
            # just use opposite sensors
            lookaway=(length(const.EMGch) / 2)
# selectMyoDownCalibrated.m:26
            if const.extensor_sensors(1) < lookaway + 1:
                opposite_sensors[1]=const.extensor_sensors(1) + lookaway
# selectMyoDownCalibrated.m:29
            else:
                opposite_sensors[1]=const.extensor_sensors(1) - lookaway
# selectMyoDownCalibrated.m:31
            if const.extensor_sensors(2) < lookaway + 1:
                opposite_sensors[2]=const.extensor_sensors(2) + lookaway
# selectMyoDownCalibrated.m:35
            else:
                opposite_sensors[2]=const.extensor_sensors(2) - lookaway
# selectMyoDownCalibrated.m:37
            #             opposite_sensors = sort(opposite_sensors);
            const.flexor_sensors = copy(const.EMGch(opposite_sensors))
# selectMyoDownCalibrated.m:41
        # out of range?
    # >8 case
        if const.flexor_sensors(1) > const.EMGch(end()):
            const.flexor_sensors[1]=const.flexor_sensors(1) - length(const.EMGch)
# selectMyoDownCalibrated.m:48
        # if only ch2 is > 8, then loop back to 1.
        if const.flexor_sensors(2) > const.EMGch(end()):
            const.flexor_sensors[2]=const.flexor_sensors(2) - length(const.EMGch)
# selectMyoDownCalibrated.m:53
        # - case
        if const.flexor_sensors(1) < const.EMGch(1):
            const.flexor_sensors[1]=const.flexor_sensors(1) + length(const.EMGch)
# selectMyoDownCalibrated.m:58
        if const.flexor_sensors(2) < const.EMGch(1):
            const.flexor_sensors[2]=const.flexor_sensors(2) + length(const.EMGch)
# selectMyoDownCalibrated.m:62
        #            # NEED TO CHANGE SO THAT CANNOT GET VAL > 8
#            if const.flexor_sensors(1) > const.EMGch # 8 
#                const.flexor_sensors(1) = const.flexor_sensors(1) - const.EMGch;
#            end
#            if const.flexor_sensors(2) > const.EMGch # if only ch2 is > 8, then loop back to 1.
#               const.flexor_sensors(2) = const.flexor_sensors(2) - const.EMGch;
#            end
        # double check for overlapping
        const=checkEFOverlap(const)
# selectMyoDownCalibrated.m:74
        # if there is no flexor distnace, assume the opposite side
    finally:
        pass
    
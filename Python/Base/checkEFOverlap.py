# Generated with SMOP  0.41
from libsmop import *
# checkEFOverlap.m

    
@function
def checkEFOverlap(const=None,*args,**kwargs):
    varargin = checkEFOverlap.varargin
    nargin = checkEFOverlap.nargin

    # overlapping?
    overlap=ismember(const.extensor_sensors,const.flexor_sensors)
# checkEFOverlap.m:5
    if overlap(1) or overlap(2):
        disp('overlapping e f channles')
        lookaway=(length(const.EMGch) / 2)
# checkEFOverlap.m:10
        if const.extensor_sensors(1) < lookaway + 1:
            opposite_sensors[1]=const.extensor_sensors(1) + lookaway
# checkEFOverlap.m:13
        else:
            opposite_sensors[1]=const.extensor_sensors(1) - lookaway
# checkEFOverlap.m:15
        if const.extensor_sensors(2) < lookaway + 1:
            opposite_sensors[2]=const.extensor_sensors(2) + lookaway
# checkEFOverlap.m:19
        else:
            opposite_sensors[2]=const.extensor_sensors(2) - lookaway
# checkEFOverlap.m:21
        #         opposite_sensors = sort(opposite_sensors);
        const.flexor_sensors = copy(const.EMGch(opposite_sensors))
# checkEFOverlap.m:25
    
    # # if overlap, assumme opposite side
# lookaway = round ( length(const.EMGch) / 2) ;
# 
# # get the index as far away as possible from the extensor index.
# dist1 = abs( const.EMGch - const.extensor_sensors(1));
# FI1 = dist1==0 + lookaway;
# 
# dist2 = abs( const.EMGch - const.extensor_sensors(2));
# FI2 = dist2==0 + lookaway;
# 
# const.flexor_sensors(1) = const.EMGch(FI1);
# const.flexor_sensors(2) = const.EMGch(FI2);
#
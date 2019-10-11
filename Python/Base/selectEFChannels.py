# Generated with SMOP  0.41
from libsmop import *
# selectEFChannels.m

    
@function
def selectEFChannels(const=None,out=None,calData=None,*args,**kwargs):
    varargin = selectEFChannels.varargin
    nargin = selectEFChannels.nargin

    ##
# index of when cal game went from ready to active
    strtind=const.CalGoTime
# selectEFChannels.m:5
    # remove rest phase mean ch activity while playing ASTRO
    EMG=calData.cal(arange(strtind,end()),arange(2,end())) - const.ReadyMean
# selectEFChannels.m:8
    ## select the top 50 percent of the trail data..
    
    cumEMG=sum(EMG,2)
# selectEFChannels.m:12
    
    B,index=sortrows(cumEMG,nargout=2)
# selectEFChannels.m:13
    
    indkp=index(B > median(B))
# selectEFChannels.m:14
    
    EMGuse=EMG(index(indkp),arange())
# selectEFChannels.m:15
    
    ## Select which ch are extensors.
    
    # create const.extensor_sensors
    # third argument to avoid filtering (used in C_calibrateUserProfile.m)
    # 2:end are the EMG CHANNELS (regardless of the number used)
    const=findMyoUp(EMGuse,const,1)
# selectEFChannels.m:22
    
    # select flexors based on either a) calib. flexor distnace, or b) assume the opposite side
    const=selectMyoDown(const)
# selectEFChannels.m:25
    
    fprintf('Extensors Sensor == Myo Sensors:  %i-%i \n\n',const.extensor_sensors(1),const.extensor_sensors(2))
    fprintf('Flexor Sensor == Myo Sensors:   %i-%i \n\n',const.flexor_sensors(1),const.flexor_sensors(2))
    # const.extensor_sensors outputs in terms of actual Myo channles [e.g. 3:6, 1:8, 2:7]
# convert to col. index of const.myoCHsUsed, which has col 1 == time
    ESI1=find(const.EMGch == const.extensor_sensors(1))
# selectEFChannels.m:31
    ESI2=find(const.EMGch == const.extensor_sensors(2))
# selectEFChannels.m:32
    const.extensor_sensors[1]=ESI1 + 1
# selectEFChannels.m:33
    
    const.extensor_sensors[2]=ESI2 + 1
# selectEFChannels.m:34
    
    # const.extensor_sensors are now the col. index of const.myoCHsUsed to use
    
    # convert to col. index of const.myoCHsUsed, which has col 1 == time
    FSI1=find(const.EMGch == const.flexor_sensors(1))
# selectEFChannels.m:38
    FSI2=find(const.EMGch == const.flexor_sensors(2))
# selectEFChannels.m:39
    const.flexor_sensors[1]=FSI1 + 1
# selectEFChannels.m:40
    
    const.flexor_sensors[2]=FSI2 + 1
# selectEFChannels.m:41
    
    # const.flexor_sensors are now the col. index of const.myoCHsUsed, not the channel number
    
    # maybe to remove if not using old calib.
    try:
        close_('calibrate')
    finally:
        pass
    
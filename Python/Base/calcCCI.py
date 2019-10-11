# Generated with SMOP  0.41
from libsmop import *
# calcCCI.m

    
@function
def calcCCI(EMGb=None,const=None,*args,**kwargs):
    varargin = calcCCI.varargin
    nargin = calcCCI.nargin

    try:
        senE=const.Cal_extensor_sensors
# calcCCI.m:4
        senF=const.Cal_flexor_sensors
# calcCCI.m:5
    finally:
        pass
    
    
    # for when there is ia 3 dimensionial array, 3rd D is nFrames
    winLen,nCH,nFrames=size(EMGb,nargout=3)
# calcCCI.m:12
    
    # RMS
    preCCI=rms(EMGb(arange(),concat([senE,senF]),arange()),1)
# calcCCI.m:15
    
    rmsEx=mean(preCCI(arange(),arange(1,2),arange()),2)
# calcCCI.m:17
    rmsFx=mean(preCCI(arange(),arange(3,4),arange()),2)
# calcCCI.m:18
    # Should be 1 col * nFrames rows
    answ=rmsEx / rmsFx
# calcCCI.m:21
    # this is an array  N bin rows and 1 colomuns
    CCI_OUT=reshape(answ,concat([1,nFrames])).T
# calcCCI.m:24
    # ## OLD WAY
# 
# [~, C] = size(binned_signal_allCHs);
# [R, ~] = size(binned_signal_allCHs{1});
# 
# preCCI = zeros(R,C);
# # get MMAV for each bin
# for nCH = 1:size(binned_signal_allCHs,2)
#     preCCI(:,nCH) = sqrt(calcMAV(binned_signal_allCHs{nCH}));
# #     preMMAV(:,nCH) = calcMAV(binned_signal_allCHs(:,nCH));
# end
# 
# if size(preCCI,2) == 4
#     rmsEx = mean(preCCI(:,1:2),2);
#     rmsFx = mean(preCCI(:,3:4),2);
# else 
#     rmsEx = mean(preCCI(:,2:3),2);
#     rmsFx = mean(preCCI(:,6:7),2);
# end    
# 
# answ = rmsEx ./ rmsFx ; # Should be bin long by 1 val.
# # < 1 means that flexors are more active than extensors...
# # no limit to max.
# 
# 
# 
# 
# # # ratio of RMS of the antagonist muscle to the RMS of the agonist muscle (Fig. 2).
# # 
# # # Single bin
# # # rms = sqrt (mean (binned_signal_allCHs .^2) ); # should be 1 row 8 ch
# # # answ = mean(rms(2:3)) / mean(rms(6:7)) ;
# # 
# # # manu bins
# # rms = sqrt (mean (binned_signal_allCHs .^2) ); # should be 1 row 8 ch
# # answ = mean(rms(2:3)) / mean(rms(6:7)) ;
#   # 2:3 are extensors
#   # 6:7 are flexors
#   # could standardize this better for 4 ch problems..
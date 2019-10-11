# Generated with SMOP  0.41
from libsmop import *
# calcSCCI.m

    
@function
def calcSCCI(smav=None,const=None,*args,**kwargs):
    varargin = calcSCCI.varargin
    nargin = calcSCCI.nargin

    # in theory this should be the rms imbalance using SMAV...
    
    try:
        senE=const.Cal_extensor_sensors
# calcSCCI.m:5
        senF=const.Cal_flexor_sensors
# calcSCCI.m:6
    finally:
        pass
    
    rmsEx=mean(smav(arange(),senE),2)
# calcSCCI.m:12
    rmsFx=mean(smav(arange(),senF),2)
# calcSCCI.m:13
    # Should be 1 col * nFrames rows
    SCCI_OUT=rmsEx / rmsFx
# calcSCCI.m:16
    # 
# if iscell(smav)
#     smav = cell2mat(smav);
# end 
# 
# if size(smav,2) == 4
#     rmsEx = mean(smav(:,1:2),2);
#     rmsFx = mean(smav(:,3:4),2);
# else 
#     rmsEx = mean(smav(:,2:3),2);
#     rmsFx = mean(smav(:,6:7),2);
# end    
# 
# 
# answ = rmsEx ./ rmsFx ; # Should be bin long by 1 val.
    
    # [~, C] = size(binned_signal_allCHs);
# [R, ~] = size(binned_signal_allCHs{1});
    
    # preCCI = zeros(R,C);
# # get MMAV for each bin
# for nCH = 1:size(binned_signal_allCHs,2)
#     preCCI(:,nCH) = sqrt(calcMAV(binned_signal_allCHs{nCH}));
# #     preMMAV(:,nCH) = calcMAV(binned_signal_allCHs(:,nCH));
# end
# 
# rmsEx = mean(preCCI(:,2:3),2);
# rmsFx = mean(preCCI(:,6:7),2);
# rmsMean = mean(preCCI(:,:),2);
# 
# # dividing extensor rms by mean rms, and then flexor rms by mean rms
# # or should this be norm to the current bin (xi-mu)/mu?
# SrmsEx = rmsEx ./ rmsMean;
# SrmsFx = rmsFx ./ rmsMean;
# 
# answ = SrmsEx ./ SrmsFx ; # Should be bin long by 1 val.
# # < 1 means that flexors are more active than extensors...
# # no limit to max.
#
    
    # rms = sqrt (mean (binned_signal_allCHs .^2) ); # should be 1 row 8 ch
# # mrms = mean(rms);
# maxrms = max(rms); # the current max activity
# # minrms = min(rms);
# 
# sext = mean(rms(2:3)) / maxrms;
# sflx = mean(rms(6:7)) / maxrms;
# 
# answ = sext / sflx;
# Generated with SMOP  0.41
from libsmop import *
# updateBase.m

    
@function
def updateBase(const=None,out=None,store=None,*args,**kwargs):
    varargin = updateBase.varargin
    nargin = updateBase.nargin

    # Update baseline
    
    ## Extensor
    
    # find this window's mean (SD) baseline activity (lowest seek peeks)
    out.currentBaseESD = copy(std(store.mavE))
# updateBase.m:7
    # base
    mavEinv=max(store.mavE) - store.mavE
# updateBase.m:10
    
    indEi,__=peakseek(mavEinv,const.minpeakdist,out.currentBaseESD,nargout=2)
# updateBase.m:11
    
    indE,__=peakseek(store.mavE,const.minpeakdist,out.currentBaseESD,nargout=2)
# updateBase.m:12
    
    # if no peaks  # ile.
    if length(indE) < 5 or length(indEi) < 5:
        out.currentBaseE = copy(prctile(store.mavE,20))
# updateBase.m:16
    else:
        out.currentBaseE = copy(prctile(store.mavE(indEi),50))
# updateBase.m:19
        if (prctile(store.mavE(indEi),50)) > const.AllTimeBaseE:
            const.AllTimeBaseE = copy(prctile(store.mavE(indEi),5))
# updateBase.m:23
        else:
            const.AllTimeBaseE = copy(const.AllTimeBaseE)
# updateBase.m:25
        # ensure that base is not high
        if out.currentBaseE >= const.AllTimeBaseE:
            out.currentBaseE = copy(const.AllTimeBaseE)
# updateBase.m:30
    
    ## FLEXOR
    
    # find this window's mean (SD) baseline activity (lowest seek peeks)
    out.currentBaseFSD = copy(std(store.mavF))
# updateBase.m:40
    # base
    mavFinv=max(store.mavF) - store.mavF
# updateBase.m:43
    
    indFi,__=peakseek(mavFinv,const.minpeakdist,out.currentBaseFSD,nargout=2)
# updateBase.m:44
    
    indF,__=peakseek(store.mavF,const.minpeakdist,out.currentBaseFSD,nargout=2)
# updateBase.m:45
    
    # if no peaks  # ile.
    if length(indF) < 5 or length(indFi) < 5:
        out.currentBaseF = copy(prctile(store.mavF,20))
# updateBase.m:50
    else:
        out.currentBaseF = copy(prctile(store.mavF(indFi),50))
# updateBase.m:52
        # update the forever base
        if (prctile(store.mavF(indFi),50)) > const.AllTimeBaseF:
            const.AllTimeBaseF = copy(prctile(store.mavF(indFi),5))
# updateBase.m:56
        else:
            const.AllTimeBaseF = copy(const.AllTimeBaseF)
# updateBase.m:58
        # check that it is not too high
        if out.currentBaseF >= const.AllTimeBaseF:
            out.currentBaseF = copy(const.AllTimeBaseF)
# updateBase.m:63
    
    # + fix the window change overlap...
    const.lastBaseUpdate = copy(store.time(end()) + (store.time(end()) - store.time(const.jump)))
# updateBase.m:69
    ## Accel
    
    # base
    AccelInv=max(store.AccelRes) - store.AccelRes
# updateBase.m:74
    
    AccelSD=std(store.AccelRes)
# updateBase.m:75
    indAi,__=peakseek(AccelInv,const.minpeakdist,AccelSD,nargout=2)
# updateBase.m:76
    
    indA,__=peakseek(store.AccelRes,const.minpeakdist,AccelSD,nargout=2)
# updateBase.m:77
    
    if length(indAi) < 5 or length(indA) < 5:
        out.currentBaseAccel = copy(prctile(store.AccelRes,10))
# updateBase.m:80
        out.currentMaxAccel = copy(prctile(store.AccelRes,90))
# updateBase.m:81
    else:
        out.currentBaseAccel = copy(prctile(store.AccelRes(indAi),10))
# updateBase.m:83
        out.currentMaxAccel = copy(prctile(store.AccelRes(indA),90))
# updateBase.m:84
    
    ## GYRO
    
    # base
    GyroInv=max(store.GyroRes) - store.GyroRes
# updateBase.m:90
    
    GyroSD=std(store.GyroRes)
# updateBase.m:91
    indAi,__=peakseek(GyroInv,const.minpeakdist,GyroSD,nargout=2)
# updateBase.m:92
    
    indA,__=peakseek(store.GyroRes,const.minpeakdist,GyroSD,nargout=2)
# updateBase.m:93
    
    if length(indAi) < 5 or length(indA) < 5:
        out.currentBaseGyro = copy(prctile(store.GyroRes,25))
# updateBase.m:96
        out.currentMaxGyro = copy(prctile(store.GyroRes,95))
# updateBase.m:97
    else:
        out.currentBaseGyro = copy(prctile(store.GyroRes(indAi),25))
# updateBase.m:99
        out.currentMaxGyro = copy(prctile(store.GyroRes(indA),95))
# updateBase.m:100
    
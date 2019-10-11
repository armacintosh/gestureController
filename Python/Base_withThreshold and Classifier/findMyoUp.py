# Generated with SMOP  0.41
from libsmop import *
# findMyoUp.m

    
@function
def findMyoUp(EMG=None,const=None,nargin=None,*args,**kwargs):
    varargin = findMyoUp.varargin
    nargin = findMyoUp.nargin

    # no time col. here
    
    # case for calibration
    if logical_not(exist('nargin','var')):
        # filter
        fn=(const.sf / 2) + 1
# findMyoUp.m:9
        b,a=butter(2,(const.low_freq / fn),nargout=2)
# findMyoUp.m:10
        pLen=round(dot(0.2,length(EMG)))
# findMyoUp.m:11
        EMGp=padarray(EMG,pLen,'symmetric','both')
# findMyoUp.m:12
        EMGfil=filtfilt(b,a,EMGp)
# findMyoUp.m:13
        EMGuse=EMGfil(arange(pLen + 1,end() - pLen),arange())
# findMyoUp.m:14
    else:
        EMGuse=copy(EMG)
# findMyoUp.m:18
    
    ## get the Up Direction
    
    if const.upFinder == 2:
        # circ data for finding extensor_sensors
        OriIncrement=pi / (size(EMGuse,2) / 2)
# findMyoUp.m:27
        ori=arange(0,dot(2,pi) - OriIncrement,OriIncrement)
# findMyoUp.m:28
        # REASON FOR CHANGE
        # at the 4/5 split. when circMean uses - values, averaging over a group
        # gives you a bad mean, because values close to pi are mirrored, so if you
        # have a mean of 2 values such as + / - 2.7 (which is between ch. 3/4 and
        # 4/5) your mean would actually be 0... this is wrong.. it should be pi.
        # FIX. circMean returns only + vals...
        # you get the same problem with a 1/8 split... either just above 0 or just
        # below 2pi, should average 0, but actually will average pi...
        # Fix... select channel for each instant and take the most commonly chosne channel...
        # test = [1 1 1 0 0 0 0 1 ];
        # test_circMean = circ_mean(ori,test,2)
        circMean=zeros(size(EMGuse,1),1)
# findMyoUp.m:42
        extensor_sensors=zeros(size(EMGuse,1),2)
# findMyoUp.m:43
        for R in arange(1,size(EMGuse,1)).reshape(-1):
            circMean[R,arange()]=circ_mean(ori,EMGuse(R,arange()),2)
# findMyoUp.m:46
            # select the 2 closest channels for this instant
        # deal with 1/8 split, where abs distance would not be correct
            if (circMean(R,arange()) > ori(end())):
                extensor_sensors[R,arange()]=const.EMGch(concat([end(),1]))
# findMyoUp.m:51
                # do not sort 1 8 combo...
            else:
                distance=abs((ori - circMean(R,arange())))
# findMyoUp.m:54
                __,DistInd=sort(distance,2,'ascend',nargout=2)
# findMyoUp.m:55
                extensor_sensors[R,arange()]=DistInd(arange(1,2))
# findMyoUp.m:56
        # choose the 2 most frequent channels
        x=ravel(extensor_sensors)
# findMyoUp.m:62
        a=unique(x)
# findMyoUp.m:63
        out=concat([a,histc(ravel(x),a)])
# findMyoUp.m:64
        __,I=sort(out(arange(),2),'descend',nargout=2)
# findMyoUp.m:65
        const.extensor_sensors = copy(out(I(arange(1,2)),1).T)
# findMyoUp.m:67
    else:
        if const.upFinder == 1:
            # just use the highest channels.
            x=mean(EMGuse)
# findMyoUp.m:72
            # I needs to say the ch. numbers
            __,I0=sort(x,'descend',nargout=2)
# findMyoUp.m:76
            I=const.EMGch(I0)
# findMyoUp.m:77
            # pick the higher of the 2 indicies next to the highest sensor...
            if I(1) == const.EMGch(1):
                Cval=max(x(arange(),concat([2,end()])))
# findMyoUp.m:81
                iC=x == Cval
# findMyoUp.m:82
            else:
                if I(1) == const.EMGch(end()):
                    Cval=max(x(arange(),concat([1,end() - 1])))
# findMyoUp.m:85
                    iC=x == Cval
# findMyoUp.m:86
                else:
                    Cval=max(x(arange(),concat([I0(1) + 1,I0(1) - 1])))
# findMyoUp.m:89
                    iC=x == Cval
# findMyoUp.m:90
            const.extensor_sensors[1]=I(1)
# findMyoUp.m:94
            const.extensor_sensors[2]=const.EMGch(iC)
# findMyoUp.m:95
    
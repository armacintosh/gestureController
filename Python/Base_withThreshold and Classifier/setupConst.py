# Generated with SMOP  0.41
from libsmop import *
# setupConst.m

    
@function
def setupConst(constfileLoc=None,*args,**kwargs):
    varargin = setupConst.varargin
    nargin = setupConst.nargin

    if nargin > 0:
        fid=copy(constfileLoc)
# setupConst.m:4
    else:
        # load text file
        fid='constFile.txt'
# setupConst.m:7
    
    constFile=importconstFile(fid)
# setupConst.m:11
    
    # up to where game loc is.
    constFileUse=constFile(arange(1,end() - 1),arange(1,2))
# setupConst.m:14
    fnames=cellstr(constFileUse(arange(),1))
# setupConst.m:15
    
    const=cell2struct(constFileUse(arange(),2),fnames,1).T
# setupConst.m:17
    
    const.gameLoc = copy(constFile[end(),3])
# setupConst.m:20
    # calc other vals.
# thresholds for PushtoGame2
    # check WINBIN/4 must be int to have whole bins for IMU data
    if mod(const.WINBIN / 4,1) == 0:
        # integer is good
        const.binsize = copy(const.WINBIN / const.sf)
# setupConst.m:28
    else:
        # change WINBIN so that WINBIN/4 is an integer
        const.WINBIN = copy(dot(4,round(const.WINBIN / 4)))
# setupConst.m:31
        const.binsize = copy(const.WINBIN / const.sf)
# setupConst.m:32
    
    
    
    const.binsize = copy(const.WINBIN / const.sf)
# setupConst.m:36
    
    const.nEMG = copy(dot(const.binsize,const.sf))
# setupConst.m:37
    const.pushbutton = copy(actxserver('WScript.Shell'))
# setupConst.m:38
    
    const.EMGch = copy(arange(const.EMGS1,const.EMGS2))
# setupConst.m:39
    
    #     const.calWinSetup= [const.calWinPosLR const.calWinPosUD const.calWinSizeW const.calWinSizeH];
    
    # to add to const file...
    # const.maxWindow = 300; # number of bins to look back on ~ 30 seconds...If they have not done a max in  this time...
    # const.useUserProfile = 1; # number of bins to look back on ~ 30 seconds...If they have not done a max in  this time...
    
    ## uers profile config
    
    if const.useUserProfile == 1:
        # get the file
        if isdeployed:
            status,result=system('path',nargout=2)
# setupConst.m:52
            playMyoDashyRoot=char(regexpi(result,'Path=(.*?);','tokens','once'))
# setupConst.m:53
            ProfileFile=strcat(playMyoDashyRoot,'\CurrentUserProfile.mat')
# setupConst.m:54
        else:
            ProfileFile='CurrentUserProfile.mat'
# setupConst.m:56
        Profile=load(ProfileFile)
# setupConst.m:59
        const.flexorDistance = copy(Profile.const.flexorDistance)
# setupConst.m:60
        const.DistIndBackup = copy(Profile.const.DistIndBackup)
# setupConst.m:61
        const.Profile_extensor_sensors = copy(Profile.const.Cal_extensor_sensors)
# setupConst.m:62
        const.Profile_flexor_sensors = copy(Profile.const.Cal_flexor_sensors)
# setupConst.m:63
    
    
    ## controller config
    
    const.minpeakdist = copy(const.sf / const.WINBIN / 2)
# setupConst.m:71
    
    ## Other config
    
    # initialize when to update base
    const.lastBaseUpdate = copy(datetime())
# setupConst.m:76
    
    const.jump = copy(const.maxWindow - const.maxWindowOverlap)
# setupConst.m:79
    
    const.AllTimeMaxE = copy(0)
# setupConst.m:82
    
    const.AllTimeMaxF = copy(0)
# setupConst.m:83
    
    const.AllTimeBaseE = copy(0)
# setupConst.m:84
    const.AllTimeBaseF = copy(0)
# setupConst.m:85
    const.AllTimeMaxAccel = copy(0)
# setupConst.m:86
    const.lastPressTime = copy(cputime)
# setupConst.m:87
    
    const.logFileMatlab = copy('logFileMatlab.txt')
# setupConst.m:88
    const.syncCam = copy(0)
# setupConst.m:89
    const.DashyOpened = copy(0)
# setupConst.m:90
    const.playAstro = copy(0)
# setupConst.m:91
    
    const.DashyActiveWindow = copy(0)
# setupConst.m:92
    const.JumperActiveWindow = copy(0)
# setupConst.m:93
    const.calibrating = copy(1)
# setupConst.m:94
    
    const.speedMax = copy(0)
# setupConst.m:95
    if logical_not(isfield(const,'useLoadFig')):
        const.useLoadFig = copy(0)
# setupConst.m:98
    
    if logical_not(isfield(const,'closeLauncher')):
        const.closeLauncher = copy(0)
# setupConst.m:101
    
    
    if logical_not(isfield(const,'secondsMissing')):
        const.closeLauncher = copy(3)
# setupConst.m:105
    
    # option to update E thresh based on visual inspection...
    if const.updateEThresh == 1 and const.updateEThreshVal > 0:
        const.Low = copy(const.updateEThreshVal)
# setupConst.m:109
        try:
            const.minE = copy(const.updateEThreshVal)
# setupConst.m:111
        finally:
            pass
    
    
    
    ## Bayes Filter Parameters EMG
    
    # -------------  Parameters for Bayesian filter  -------------
    const.param.sf = copy(const.sf)
# setupConst.m:120
    
    const.param.bins = copy(100)
# setupConst.m:121
    
    const.param.alpha = copy(10 ** - 10)
# setupConst.m:122
    
    const.param.beta = copy(10 ** - 2)
# setupConst.m:123
    
    const.param.model = copy('Laplace')
# setupConst.m:124
    
    const.param.pointmax = copy(false)
# setupConst.m:125
    
    # true: use maximum of posterior as point estimation
    const.param.sigmaMVC = copy(1)
# setupConst.m:127
    
    # -------------  Parameters for Bayesian filter END  -------------
    
    const.param.pri = copy(ones(const.param.bins,1) / const.param.bins)
# setupConst.m:131
    
    # x == WINBIN
# x = x/param.sigmaMVC;   # rescale data with respect to sigma MVC. 
#     # This helps avoiding numerical problems in case of the raw data being 
#     # especially if not single values are processed with the function 
#     # BayesFilter but instead multiple EMG measurements at a time. Refer also 
#     # to the comments in BayesFilter.m.
    
    const.param.sig = copy(linspace(const.param.bins ** - 1,1,const.param.bins).T)
# setupConst.m:141
    
    # sigma=0 will always have zero probability by definition (0 is an absorbing 
    # boundary) due to the divergence at 0 when computing the likelihood. Refer
    # also to the comments in BayesFilter.m.
    
    ## IMU Bayes Filt param
    
    # -------------  Parameters for Bayesian filter  -------------
    const.paramIMU.sf = copy(const.sf / 4)
# setupConst.m:150
    
    const.paramIMU.bins = copy(100)
# setupConst.m:151
    
    const.paramIMU.alpha = copy(10 ** - 10)
# setupConst.m:152
    
    const.paramIMU.beta = copy(10 ** - 2)
# setupConst.m:153
    
    const.paramIMU.model = copy('Laplace')
# setupConst.m:154
    
    const.paramIMU.pointmax = copy(false)
# setupConst.m:155
    
    # true: use maximum of posterior as point estimation
    const.paramIMU.sigmaMVC = copy(1)
# setupConst.m:157
    
    # -------------  Parameters for Bayesian filter END  -------------
    
    const.paramIMU.pri = copy(ones(const.param.bins,1) / const.param.bins)
# setupConst.m:161
    # x == WINBIN
# x = x/param.sigmaMVC;   # rescale data with respect to sigma MVC.
    const.paramIMU.sig = copy(linspace(const.param.bins ** - 1,1,const.param.bins).T)
# setupConst.m:164
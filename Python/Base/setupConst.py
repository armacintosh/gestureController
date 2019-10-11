# Generated with SMOP  0.41
from libsmop import *
# setupConst.m

    
@function
def setupConst(*args,**kwargs):
    varargin = setupConst.varargin
    nargin = setupConst.nargin

    # load text file
    fid='constFile.txt'
# setupConst.m:4
    constFile=importconstFile(fid)
# setupConst.m:5
    
    # up to where game loc is.
    constFileUse=constFile(arange(1,end() - 1),arange(1,2))
# setupConst.m:8
    fnames=cellstr(constFileUse(arange(),1))
# setupConst.m:9
    const=cell2struct(constFileUse(arange(),2),fnames,1).T
# setupConst.m:10
    const.gameLoc = copy(constFile[end(),3])
# setupConst.m:11
    # check WINBIN/4 must be int to have whole bins for IMU data
    if mod(const.WINBIN / 4,1) == 0:
        # integer is good
        const.binsize = copy(const.WINBIN / const.sf)
# setupConst.m:16
    else:
        # change WINBIN so that WINBIN/4 is an integer
        const.WINBIN = copy(dot(4,round(const.WINBIN / 4)))
# setupConst.m:19
        const.binsize = copy(const.WINBIN / const.sf)
# setupConst.m:20
    
    
    
    const.binsize = copy(const.WINBIN / const.sf)
# setupConst.m:24
    
    const.nEMG = copy(dot(const.binsize,const.sf))
# setupConst.m:25
    const.pushbutton = copy(actxserver('WScript.Shell'))
# setupConst.m:26
    
    const.EMGch = copy(arange(const.EMGS1,const.EMGS2))
# setupConst.m:27
    
    ## uers profile config
    
    if const.useUserProfile == 1:
        # get the file
        if isdeployed:
            status,result=system('path',nargout=2)
# setupConst.m:35
            playMyoDashyRoot=char(regexpi(result,'Path=(.*?);','tokens','once'))
# setupConst.m:36
            ProfileFile=strcat(playMyoDashyRoot,'\CurrentUserProfile.mat')
# setupConst.m:37
        else:
            ProfileFile='CurrentUserProfile.mat'
# setupConst.m:39
        Profile=load(ProfileFile)
# setupConst.m:42
        const.flexorDistance = copy(Profile.const.flexorDistance)
# setupConst.m:43
        const.DistIndBackup = copy(Profile.const.DistIndBackup)
# setupConst.m:44
        const.Profile_extensor_sensors = copy(Profile.const.Cal_extensor_sensors)
# setupConst.m:45
        const.Profile_flexor_sensors = copy(Profile.const.Cal_flexor_sensors)
# setupConst.m:46
    
    
    ## controller config
    
    const.minpeakdist = copy(const.sf / const.WINBIN / 2)
# setupConst.m:54
    
    ## Other config
    
    # initialize when to update base
    const.lastBaseUpdate = copy(datetime())
# setupConst.m:59
    
    const.jump = copy(const.maxWindow - const.maxWindowOverlap)
# setupConst.m:62
    
    const.AllTimeMaxE = copy(0)
# setupConst.m:65
    
    const.AllTimeMaxF = copy(0)
# setupConst.m:66
    
    const.AllTimeBaseE = copy(0)
# setupConst.m:67
    const.AllTimeBaseF = copy(0)
# setupConst.m:68
    const.AllTimeMaxAccel = copy(0)
# setupConst.m:69
    const.lastPressTime = copy(cputime)
# setupConst.m:70
    
    const.logFileMatlab = copy('logFileMatlab.txt')
# setupConst.m:71
    const.syncCam = copy(0)
# setupConst.m:72
    const.DashyOpened = copy(0)
# setupConst.m:73
    const.playAstro = copy(0)
# setupConst.m:74
    
    const.DashyActiveWindow = copy(0)
# setupConst.m:75
    const.JumperActiveWindow = copy(0)
# setupConst.m:76
    const.calibrating = copy(1)
# setupConst.m:77
    
    const.speedMax = copy(0)
# setupConst.m:78
    if logical_not(isfield(const,'useLoadFig')):
        const.useLoadFig = copy(0)
# setupConst.m:81
    
    if logical_not(isfield(const,'closeLauncher')):
        const.closeLauncher = copy(0)
# setupConst.m:84
    
    
    if logical_not(isfield(const,'secondsMissing')):
        const.closeLauncher = copy(3)
# setupConst.m:88
    
    # option to update E thresh based on visual inspection...
    if const.updateEThresh == 1 and const.updateEThreshVal > 0:
        const.Low = copy(const.updateEThreshVal)
# setupConst.m:92
        try:
            const.minE = copy(const.updateEThreshVal)
# setupConst.m:94
        finally:
            pass
    
    
    
    ## Bayes Filter Parameters EMG - see bayes reference in README
    
    # -------------  Parameters for Bayesian filter  -------------
    const.param.sf = copy(const.sf)
# setupConst.m:103
    
    const.param.bins = copy(100)
# setupConst.m:104
    
    const.param.alpha = copy(10 ** - 10)
# setupConst.m:105
    
    const.param.beta = copy(10 ** - 2)
# setupConst.m:106
    
    const.param.model = copy('Laplace')
# setupConst.m:107
    
    const.param.pointmax = copy(false)
# setupConst.m:108
    
    # true: use maximum of posterior as point estimation
    const.param.sigmaMVC = copy(1)
# setupConst.m:110
    
    # -------------  Parameters for Bayesian filter END  -------------
    
    const.param.pri = copy(ones(const.param.bins,1) / const.param.bins)
# setupConst.m:114
    
    # x == WINBIN
# x = x/param.sigmaMVC;   # rescale data with respect to sigma MVC. 
#     # This helps avoiding numerical problems in case of the raw data being 
#     # especially if not single values are processed with the function 
#     # BayesFilter but instead multiple EMG measurements at a time. Refer also 
#     # to the comments in BayesFilter.m.
    
    const.param.sig = copy(linspace(const.param.bins ** - 1,1,const.param.bins).T)
# setupConst.m:124
    
    # sigma=0 will always have zero probability by definition (0 is an absorbing 
    # boundary) due to the divergence at 0 when computing the likelihood. Refer
    # also to the comments in BayesFilter.m.
    
    ## IMU Bayes Filt param
    
    # -------------  Parameters for Bayesian filter  -------------
    const.paramIMU.sf = copy(const.sf / 4)
# setupConst.m:133
    
    const.paramIMU.bins = copy(100)
# setupConst.m:134
    
    const.paramIMU.alpha = copy(10 ** - 10)
# setupConst.m:135
    
    const.paramIMU.beta = copy(10 ** - 2)
# setupConst.m:136
    
    const.paramIMU.model = copy('Laplace')
# setupConst.m:137
    
    const.paramIMU.pointmax = copy(false)
# setupConst.m:138
    
    # true: use maximum of posterior as point estimation
    const.paramIMU.sigmaMVC = copy(1)
# setupConst.m:140
    
    # -------------  Parameters for Bayesian filter END  -------------
    
    const.paramIMU.pri = copy(ones(const.param.bins,1) / const.param.bins)
# setupConst.m:144
    # x == WINBIN
# x = x/param.sigmaMVC;   # rescale data with respect to sigma MVC.
    const.paramIMU.sig = copy(linspace(const.param.bins ** - 1,1,const.param.bins).T)
# setupConst.m:147
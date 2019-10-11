function [const] = setupConst (constfileLoc)

if nargin > 0 
    fid = constfileLoc;
else
    % load text file
    fid = 'constFile.txt';

end 

    constFile = importconstFile(fid);  % will change this if I edit .txt file

    % up to where game loc is.
    constFileUse = constFile(1:end-1,1:2);    
    fnames = cellstr(constFileUse(:,1));
    % make into struct
    const = cell2struct(constFileUse(:,2),fnames,1)';    

    % get name of game loc from imported cell
    const.gameLoc = constFile{end,3};


% calc other vals.
% thresholds for PushtoGame2
    % check WINBIN/4 must be int to have whole bins for IMU data
    if mod( const.WINBIN/4 ,1) == 0
      % integer is good
      const.binsize = const.WINBIN / const.sf; % number of seconds / bin - This must be even        
    else
      % change WINBIN so that WINBIN/4 is an integer
      const.WINBIN  = 4*round(const.WINBIN/4); 
      const.binsize = const.WINBIN / const.sf;
    end
    
        
    const.binsize = const.WINBIN / const.sf; % number of seconds / bin - This must be even        
    const.nEMG=const.binsize*const.sf;
    const.pushbutton=actxserver('WScript.Shell'); % start button movements
    const.EMGch= const.EMGS1:const.EMGS2; % channels to use..
%     const.calWinSetup= [const.calWinPosLR const.calWinPosUD const.calWinSizeW const.calWinSizeH];

    % to add to const file...
    % const.maxWindow = 300; % number of bins to look back on ~ 30 seconds...If they have not done a max in  this time...
    % const.useUserProfile = 1; % number of bins to look back on ~ 30 seconds...If they have not done a max in  this time...

%% uers profile config  
    
    if const.useUserProfile == 1
        
        % get the file
        if isdeployed % Stand-alone mode.
            [status, result] = system('path');
            playMyoDashyRoot = char(regexpi(result, 'Path=(.*?);', 'tokens', 'once'));
            ProfileFile = strcat(playMyoDashyRoot,'\CurrentUserProfile.mat');
        else % MATLAB mode.
            ProfileFile = 'CurrentUserProfile.mat';
        end    
        
        Profile = load (ProfileFile); % loads last one
        const.flexorDistance = Profile.const.flexorDistance;
        const.DistIndBackup = Profile.const.DistIndBackup;
        const.Profile_extensor_sensors = Profile.const.Cal_extensor_sensors;
        const.Profile_flexor_sensors = Profile.const.Cal_flexor_sensors;
        
  
    end 

    
    %% controller config

    const.minpeakdist = const.sf/const.WINBIN /2; % 1/2 a second. people dont jump faster than that usually    

%% Other config
    
    % initialize when to update base
    const.lastBaseUpdate = datetime();
    
    % jump should be the index of store % overlap = 100%, jump = 1
    const.jump = const.maxWindow - const.maxWindowOverlap;
    
    % used to limit reduction of currentMax
    const.AllTimeMaxE = 0;% prctile(trialdata.mavE, 95);
    const.AllTimeMaxF = 0;% prctile(trialdata.mavF, 95);
    const.AllTimeBaseE = 0;
    const.AllTimeBaseF = 0;
    const.AllTimeMaxAccel = 0;
    const.lastPressTime = cputime; % ajmal added this
    const.logFileMatlab = 'logFileMatlab.txt';
    const.syncCam = 0;
    const.DashyOpened = 0;
    const.playAstro = 0; % start by not playing astro, until pressed enter 
    const.DashyActiveWindow = 0;
    const.JumperActiveWindow = 0;
    const.calibrating = 1; % calibrating to start
    const.speedMax = 0; 
    
    if ~isfield(const,'useLoadFig')
        const.useLoadFig = 0;
    end
    if ~isfield(const,'closeLauncher')
        const.closeLauncher = 0;
    end
    
    if ~isfield(const,'secondsMissing')
        const.closeLauncher = 3;
    end
    % option to update E thresh based on visual inspection...
    if const.updateEThresh == 1 && const.updateEThreshVal > 0 
        const.Low = const.updateEThreshVal;
        try
            const.minE = const.updateEThreshVal; % incase using profile.
        catch
        end 
    end
    
    
%% Bayes Filter Parameters EMG

% -------------  Parameters for Bayesian filter  -------------
const.param.sf = const.sf;           % set sampling frequency (2500 in the demo) - Myo samples EMG at 200 Hz
const.param.bins = 100;         % output i.e. parameter quantization levels
const.param.alpha = 10^-10;     % sets diffusion rate (10^-10 in Example), talking with Jules and testing
const.param.beta = 10^-2;       % sets probability of sudden jumps (10^-40 in example) - makes more sensitive to jumps, can play with if you want
const.param.model = 'Laplace';  % choose between 'Laplace' and 'Gauss' ('Gauss' seems too sensitive)
const.param.pointmax = false;   % false: use expectation value as point estimation, 
                          % true: use maximum of posterior as point estimation
const.param.sigmaMVC = 1;       % maximum voluntary contraction amplitude value (0.5 in Example)

% -------------  Parameters for Bayesian filter END  -------------

const.param.pri = ones(const.param.bins,1)/const.param.bins; 
    % define uniform prior

% x == WINBIN
% x = x/param.sigmaMVC;   % rescale data with respect to sigma MVC. 
%     % This helps avoiding numerical problems in case of the raw data being 
%     % especially if not single values are processed with the function 
%     % BayesFilter but instead multiple EMG measurements at a time. Refer also 
%     % to the comments in BayesFilter.m.
    
const.param.sig = linspace(const.param.bins^-1,1,const.param.bins)';  
    % sigma (amplitude) axis can start at 0 or param.bins^-1. This is a matter of taste. Note howeverthat 
    % sigma=0 will always have zero probability by definition (0 is an absorbing 
    % boundary) due to the divergence at 0 when computing the likelihood. Refer
    % also to the comments in BayesFilter.m.

%% IMU Bayes Filt param

% -------------  Parameters for Bayesian filter  -------------
const.paramIMU.sf = const.sf/4;           % set sampling frequency (2500 in the demo)
const.paramIMU.bins = 100;         % output i.e. parameter quantization levels
const.paramIMU.alpha = 10^-10;     % sets diffusion rate (10^-10 in Example)
const.paramIMU.beta = 10^-2;       % sets probability of sudden jumps (10^-40 in example) - makes more sensitive to jumps
const.paramIMU.model = 'Laplace';  % choose between 'Laplace' and 'Gauss' ('Gauss' seems more sensitive)
const.paramIMU.pointmax = false;   % false: use expectation value as point estimation, 
                          % true: use maximum of posterior as point estimation
const.paramIMU.sigmaMVC = 1;       % maximum voluntary contraction amplitude value (0.5 in Example)

% -------------  Parameters for Bayesian filter END  -------------

const.paramIMU.pri = ones(const.param.bins,1)/const.param.bins; 
% x == WINBIN
% x = x/param.sigmaMVC;   % rescale data with respect to sigma MVC. 
const.paramIMU.sig = linspace(const.param.bins^-1,1,const.param.bins)';  



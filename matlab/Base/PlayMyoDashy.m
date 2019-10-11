% Running this script will initiate the calibration and main game.
% Runs checks for Myo and MyoMex readers/buffers

% Scripts are all in development and not expected to run bug free without
% adjustment. Please use at own risk.

%% Clear
clc;clear;close all;

%% make lock file to avoid multiple instances of program running

% check if there is an old lock file: 
try 
    FileInfo = dir('lockFile.txt');
    TimeStamp = FileInfo.date; % will throw error if no file exists
    locFileCreated = datetime(TimeStamp, 'InputFormat','dd-MMM-yyyy HH:mm:ss');
    currentTime = datetime();
    timeSinceMade = currentTime - locFileCreated;
catch 
    timeSinceMade = minutes (1);
end

% if there is a lock file and it has been there for < 5 minutes, then you
% are currently playing, and do no want to open another playMyoDashy.m
if exist ('lockFile.txt','file') && timeSinceMade < minutes(5)
    % Close this program
    fprintf('PlayMyoDashy.m already running, quitting program \n');

% if there is a lockFile, and it has been there for more than 5 minutes, 
% than you probably crashed and the old LockFile did not delete, so delete
% timeSinceMade > 30 mintues, delete the locfile
elseif exist ('lockFile.txt','file') && timeSinceMade > minutes(5) || ~exist ('lockFile.txt','file') 
    
    delete('lockFile.txt'); % delete file if it already existed
   
    % creat lock file
    fid = fopen( 'lockFile.txt', 'wt' );
    fclose(fid);
    fprintf('Created lock file, running this PlayMyoDashy.m \n');


%% Load .txt or user profile, this is where thresholds are set
const = setupConst();

%% Loading Screen

if const.useLoadFig == 1
    gif = 'Images\Loading.gif';
    LoadFigHandle = gifplayer(gif,0.05);
end

%% Load constants --> to be loaded from player profile, and update player profile

% if using classifier, get the classifier
if const.useClassifier == 1

% get the file
    if isdeployed % Stand-alone mode.
        
        fprintf('In old way test');
        [status, result] = system('path');
        playMyoDashyRoot = char(regexpi(result, 'Path=(.*?);', 'tokens', 'once'));
        ClassifierFile = strcat(playMyoDashyRoot,'\CurrentUserClassifier.mat');
        fprintf('OLD WAY : %s \n',ClassifierFile);
        
    else % MATLAB mode.
        ClassifierFile = 'CurrentUserClassifier.mat';
        ClassifierFile = strcat(pwd,'\',ClassifierFile);
        fprintf('%s \n',ClassifierFile);     
        
    end               

        
    load(ClassifierFile);
    classify.gameClass = gameClass;
    const.classify = gameClass;
    
    % mav should be nCH
    OriIncrement = pi/(size(const.EMGch,2)/2); % only using 4 sensors... ideally would be evenly spaced around the arm...
    const.ori = 0 : OriIncrement : 2*pi - OriIncrement;
    const.dori = diff(const.ori(1:2)); % spacing of bins
        
end    

%% open programs

% turn on MyoConnect if necessary
CheckMyoConnect(const);
datetime.setDefaultFormats('default','yyyy-MM-dd hh:mm:ss.SSS'); % sometime FFF
set(0,'DefaultFigureWindowStyle','normal');

% setup to check for keypress
NET.addAssembly('PresentationCore');
escKey = System.Windows.Input.Key.Escape;
state.keys = System.Enum.GetValues(escKey.GetType);  %get all members of enumeration

% for checking for program states and setup mouse clicks
import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;
NET.addAssembly('System'); 
import System.Diagnostics.Process.* 

% for checking active window
loadlibrary('C:\WINDOWS\system32\user32.dll', @user32Librarymfile);  
windowTitle = 'We need a really big string that is long enough to hold the window title. How long question mark I dont know';
const.windowTitlePtr = libpointer('voidPtr',[int8(windowTitle) 0]); % makes an empty pointer 
    
%% Setup close button and timers

% start timer, For external sync with video.
if const.useSyncTimer == 1
    [syncTimer] = showSyncTimer();
    set(syncTimer.h, 'visible','on'); %
end
launchedJumper = 0;

% close button
stopTrialFig (const);
state.stopTrial = 0;
stopTrial = 0; % used with Figure
inError = 0;
state.hadError = 0;
state.hadForceQuit = 0; % used if Bluetooth dies or battery and cannot reconnect
state.launchedJumper = 0; % saying to play the game or not

%% start myo server

myo = connectMyoServer(const);

% Select the ch. to process (only the data for ch. touching the arm)
const.myoCHsUsed = myo.emgCols(const.EMGch); % the col. index of raw data

%% prepare store structure for collection loop

out.lastRowUsed = 1;
out.lastRowUsedImu = 1;
    out.dataEMG = myo.emgData;
    out.dataEMG = myo.emgData(:,[1 const.myoCHsUsed]);
    out.dataEMGraw = myo.emgData(:,[1 const.myoCHsUsed]);
    out.dataAccel = myo.accelData;
    out.dataGyro = myo.gyroData;
    out.dataOrient = myo.orientData; 


% anything after time field will be appended to in store struct.
out.time = datetime;

    out.currentMaxE = 0.001;
    out.currentMaxF = 0.001;
    
    out.currentMaxAccel = 0; 
    out.currentBaseAccel = 0;
    out.maxAccel= 1;
    
    out.currentMaxGyro = 100;
    out.currentBaseGyro = 0;
    out.maxGyro = 100;
    
    out.mavE = 0;
    out.mavF = 0;
    out.AccelRes = 0;
    out.GyroRes = 0;

    out.ThreshLow = 0;
    out.ThreshHigh = 0;

    out.minE = const.minE;
    out.maxF = const.maxF;
    
    out.currentBaseE = 0; 
    out.currentBaseF = 0; 
    out.currentBaseESD = 0; 
    out.currentBaseFSD = 0; 
    
    out.stylePressed = 0;
    out.pressed = 0;
    out.wholeLoopTime = 0;
    out.processBinTime = 0;

    if const.useClassifier == 1
        out.PredLabel = 0;
        out.PredAccel = 0;
        out.PredGyro = 0;
        out.normGest = 1;
        out.normAccel = 1;
        out.normGyro = 1;
        out.gaveFeedback = 0; 
        out.speedGest = 0;
    end
 
% setup save 
[const, out] = setupSaveTrial(const, out);

% store should now only be used for updating max and should only be a few
% seconds long = const.maxWindow, which is the moving window of max
% out is the temp.struct of store. stor holds the out from each bin
storeStartInd = find(strcmp(const.outFieldNames,'time')); % index of time field 
store = out;
store = rmfield(store,const.outFieldNames(1:storeStartInd-1));

% make into table
store = struct2table(store);
for storesize = 1:const.maxWindow
    store(storesize,:) = store(1,:); 
end 
const.storeFieldNames = store.Properties.VariableNames; % get the var names to update
    
%% while myoServer is pushing data...

% keep cal data only
calData.cal = out.dataEMG;

% reset the escape key to 0
[const,state] = resetKeyToggle(const,state);

%%

while (true) &&  const.closeTrial == 0

   
%% Setup 

    % Start timer 
    wholeloop0 = datetime();

    % clear buffers before first run of while loop
    [myo] = clearBuffer (myo);       
        
%%  Process Myo data to game 

    [myo, const, state] = ReadMyoData_AddRow(myo, const,state);    
    
    % launch the calibration game 1x
    if state.launchedJumper  == 0
        MyoJumperOpen = GetProcessesByName('MyoJumper'); 
        if MyoJumperOpen.Length == 0
            [const] = showCalGame(const);           
        end 
        
        state.launchedJumper = 1; % have alrady tried it once.
        const.finishedJumper = 0; % have alrady tried it once.
        
        % to close loading figure
        if exist ('LoadFigHandle','var') && const.useLoadFig == 1
            close('Loading MyoDashy');
            clear('LoadFigHandle');
        end
        
    end
        
    
%% Pausing check for non-active window

    % check if dashy is open and the active window - for pausing.
     if const.DashyOpened == 1 % set to 1 after opening dashy
        % check if dashy is active window, and pause if not
        [const,state,myo] = getActiveWindow (const,state,myo);
    end
    
    % check if jumper is open and the active window - for pausing.
    if state.launchedJumper == 1 && const.finishedJumper == 0 && const.DashyOpened == 0
        MyoJumperOpen = GetProcessesByName('MyoJumper'); 
        if MyoJumperOpen.Length > 0
            % reopens Jumper until calibrated
            [const,state,myo] = getActiveWindowJumper (const,state,myo);
        elseif MyoJumperOpen.Length == 0
            % close trial
            stopTrial = 1; 
        end
    end

%%  process when there is a full window of data (e.g. ~20 rows)
   
    % check it is active before processing the bin    
    newestRow = myo.emgDataIndex-1; 
    if  newestRow >= const.WINBIN %&& const.inError == 0  ? full window of data?
        
        if const.DashyOpened == 1 
            if const.DashyActiveWindow == 1 % pauses it if dashy is running but not active window...
                [const, myo, out, store, calData, state] = ProcessBin (const, myo, out, store, newestRow, calData, state);
            end    
        elseif const.DashyOpened == 0
            if const.calibrating == 1 % pauses it if dashy is running but not active window...
                [const, myo, out, store, calData, state] = ProcessBin (const, myo, out, store, newestRow, calData, state);
            end
        end
           

        % do not store the data in myo struct.(not accumulating)
        out.lastRowUsed = 1;
            myo.emgDataIndex = 1;
            myo.accelDataIndex = 1;
            myo.gyroDataIndex = 1;
            myo.orientDataIndex = 1;  
            myo.eventDataIndex = 1; 

    end
    
%% for testing: check if pressed the stop button and close the trial.
    
    % close the trial, made from figure window 
    if stopTrial == 1     
        state.stopTrial = stopTrial;
    end
    
    if state.stopTrial == 0
        const.closeTrial = 0;
    else 
        const.closeTrial = 1;
        

        % Setup holding screen so they do not shut down unexpectedly
        if const.language == 1 % english 0 french
            holdText = {'Saving data','Please wait'};
        else 
            holdText = {'Sauvegarder des données','Veuillez attendre'};
        end
        showHoldScreen(holdText);

        % close open apps
        dos('taskkill /F /IM "MyoServer.exe"');
        dos('taskkill /F /IM "Myo Connect.exe"');
        dos('taskkill /F /IM "Dashy.exe"');
        dos('taskkill /F /IM "cmd.exe"');

    end
               

%%

    % counts the seconds of this loop.  
    out.wholeLoopTime = seconds(datetime()-wholeloop0);
    
    % hold loop
    if const.holdloop == 1
        pause(0.0005);    
    end
    
       
end

%% Save and close

% the file writing the processed data 
fclose(const.fileID_STORE); 
if exist('calData','var')
    const.calData = calData;
end 

% always saves whatever exists...
saveTrial (const);
    
    % closes myoLauncher if desired
    if const.closeLauncher == 1
        try
           dos('taskkill /F /IM "MyoLauncher.exe"');
           fprintf('Closed MyoLauncher \n');
        catch
            fprintf('MyoLauncher not open \n');
        end
    end
   
end

% reminder to stretch and hold for save
if const.remindStretch == 1 &&  state.hadForceQuit == 0
   if const.language == 1
        stretchText = {'Remember to stretch your hand after playing'};
        qtst='Quit';
   else
        stretchText = {'N’OUBLIE PAS D’ETIRER TA MAIN APRES AVOIR JOUE'};
        qtst='Quitter';
   end
   showStretchScreen(stretchText,qtst);
   
   while ~isempty(findobj('type','figure','name','Stretch'))
       pause(.5);
       disp('..waiting to close fig');
   end
   disp('done');
   
               
end

%% clear everything

forceQuit(const);

%% Clear
clc;clear;close all;
   
%% Load constants --> to be loaded from player profile, and update player profile
 
% Load .txt or user profile, this is where thresholds are set
const = setupConst();
const.calGest = 1;  % starts at 1 and incrtements 3x

% if using classifier, get the classifier
if const.useClassifier == 1

    % get the 
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
    
    % add classifier to const
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

%% Setup initial states

launchedJumper = 0;
stopTrial = 0; % used with Figure
inError = 0;

state.hadError = 0;
state.hadForceQuit = 0; % used if Bluetooth dies or battery and cannot reconnect
state.launchedJumper = 0; % saying to play the game or not
state.stopTrial = 0;
state.pressedX = 0;
state.pressingEnter = 0; 
state.storeTime = 0;


%% start myo server

myo = connectMyoServer(const);
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


% anything after time field will also be in store struct.
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
    
    out.currentBaseE = 0; % to be updated
    out.currentBaseF = 0; % to be updated 
    out.currentBaseESD = 0; % to be updated
    out.currentBaseFSD = 0; % to be updated 
    
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
calData.time = out.time;

% reset the escape key to 0
[const,state] = resetKeyToggle(const,state);

%%

while (true) &&  const.closeTrial == 0
    

%% Setup 
       
    % Start timer 
    wholeloop0 = datetime();

    % clear buffers before first run of while loop
    myo = clearBuffer (myo);       

%%  Process Myo data to game 
    
    % fill the myo data array, and error check while waiting for emg data
    [myo, const,state] = ReadMyoData_AddRow(myo, const,state);
        
    % launch the calibration game
    if state.launchedJumper  == 0

        MyoJumperOpen = GetProcessesByName('MyoJumper'); 
        if MyoJumperOpen.Length == 0
            [const] = showCalGame(const);
        end 
    end
        
%% Pausing check for non-active window

    % check if dashy is open and the active window - for pausing.
    if const.DashyOpened == 1 % set to ,uku, 1 after opening dashy
        % check if dashy is active window, and pause if not
        [const,state,myo] = getActiveWindow (const,state,myo);
    end
    
    % check if jumper is open and the active window - for pausing.
    if launchedJumper == 1 && const.finishedJumper == 0 && const.DashyOpened == 0
        MyoJumperOpen = GetProcessesByName('MyoJumper'); 
        if MyoJumperOpen.Length > 0
            % reopens Jumper until calibrated
            [const,state,myo] = getActiveWindowJumper (const,state,myo);
        elseif MyoJumperOpen.Length == 0
            % close trial
            stopTrial = 1; 
        end
    end

%%  process when there is a full window of data (20 rows)
   
    % check it is active before processing the bin    
    newestRow = myo.emgDataIndex-1;
    if  newestRow > (const.WINBIN) %&& const.inError == 0  
        
        if const.DashyOpened == 1 
            if const.DashyActiveWindow == 1 % pauses it if dashy is running but not active window...
                [const, myo, out, store, calData, state] = ProcessBin (const, myo, out, store, newestRow, calData, state);
            end
            
        elseif const.DashyOpened == 0
            if const.calibrating == 1 % pauses it if dashy is running but not active window...
                % if Jumper is open
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
            holdText = {'Saving date','Please wait'};
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
    % update timer
    if const.showPlayTimer == 1
        if toc > 60
            timeplayed = round(minutes(datetime() - handles.startTime ));
            set(handles.h2, 'String', strcat(num2str(timeplayed),' min')); %
            tic
        end
    end

%%

    % counts the seconds of this loop.
    out.wholeLoopTime = seconds(datetime()-wholeloop0);

    % hold loop
    if const.holdloop == 1
        pause(0.005);    
    end
    
       
end

%% Save and close

% the file writing the processed data 
fclose(const.fileID_STORE); 
if exist('calData','var')
    const.calData = calData;
end 

if const.savedata == 1 %% && const.calibrating == 0 %% && isfield(const,'extensor_sensors')
    % close other windows if still open by accident
    if ~isempty(findall(0,'type','figure','name','Error Notice'))
        close(findall(0,'type','figure','name','Error Notice'));
    end
    if ~isempty(findall(0,'type','figure','name','Connected again!'))
        close(findall(0,'type','figure','name','Connected again!'));
    end
    if ~isempty(findall(0,'type','figure','name','Restart Notice'))
        close(findall(0,'type','figure','name','Restart Notice'));
    end
    
    saveTrial (const);
end

% reminder to stretch
% Setup holding screen so they do not shut down unexpectedly
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

%% POST PROCESSING THRESHOLD and CLASSIFY
% Ask to classify: 
option = [	{'Finish Trial Now'}...
            {'Run Post-Processing'}...
            ];
        
% get user to select gesture code 1 or 2
[v0,~] = listdlg('PromptString','Do you want to finish here or run post?',...
                'SelectionMode','single',...
                'ListSize',[200 100],...
                'ListString',option);

if option{v0} == "Run Post-Processing"            
            
          
    %% select top %
    option = [	{'Adjust Thresholds'}...
                {'Close'}...
                ];

    % get user to select gesture code 1 or 2
    [v1,~] = listdlg('PromptString','Do you want to adjust thresholds based on this trial?',...
                    'SelectionMode','single',...
                    'ListSize',[200 100],...
                    'ListString',option);

        if option{v1} == "Adjust Thresholds"
            % run thresholder 
            % addpath(genpath('..\1_thresholdAdjustor')); 
            Review_GamePlayThresholds_Now();
        end


        %% Classify based on this trial

    % select top %
    option = [	{'Classify'}...
                {'Close'}...
                ];

    % get user to select gesture code 1 or 2
    [v,~] = listdlg('PromptString','Do you want to classify based on this trial?',...
                    'SelectionMode','single',...
                    'ListSize',[200 100],...
                    'ListString',option);

    if option{v} == "Classify"
        % run classifier 
        % addpath(genpath('..\1_classifyCombined'));
        classifyCalibrations_RndFrstSVMgrd_Now();
    end
    
%%
    
end

function [const, myo, out, store, calData, state] = ProcessBin (const, myo, out, store, newestRow, calData, state)

% start the timer for how long the loop takes to execute
loop0 = datetime();

%% setup 

import java.awt.Robot;
import java.awt.event.*;
import System.Diagnostics.Process.* 

%% Get raw data

% get the window of data
iWindow = (newestRow-const.WINBIN+1) : 1 : newestRow ; % the most recent 20 samples
    out.dataEMG = myo.emgData(iWindow,[1 const.myoCHsUsed]); % cut to used sensor only, everything else is 2:end
    out.dataEMGraw = myo.emgData(iWindow,[1 const.myoCHsUsed]); % cut to used sensor only, everything else is 2:end
    out.dataAccel = myo.accelData(:,:);
    out.dataGyro = myo.gyroData(:,:);
    out.dataOrient = myo.orientData(:,:);
    out.time = datetime();
    

%% pre process raw data

% repeated in selectEFChannels and updateMaxInit becuse uses more than 1 bin of data
% convert from bits -127-128 to -+1 (EMG comes in 256 bit intravel from Myo)
    % then take abs. (Reaz 2006, Techniques of EMG Signal Analysis)
    % out.dataEMG has time col 1, and only used EMG ch after that.
    % subtract resting mean after calibration.
out.dataEMG(:,2:end)  = abs( (out.dataEMG (:,2:end ) ./128) ); 

% IMU Data preprocessing  just using resultant the abs sum of all axis for the whole window of times
out.AccelRes = sum( sqrt(sum( out.dataAccel(:,myo.emgCols(1):end) .^2 )));
out.GyroRes  = sum( sqrt(sum( out.dataGyro (:,myo.emgCols(1):end) .^2 )));

%% calibration for the trial, find up direction and inital max

% before finding the extensor sensors
if const.calibrating == 1 && ~isfield(const,'extensor_sensors') % starts at 1, changes to 0 at the end of this sequence
    
    
    % if an error occured during calibration, recalibrate if so
    if state.hadError == 1
        [const, state] = resetCalGame(const,state);
    end
    
    % check if pressed enter while in Jumper
    state = EnterInJumper(const, state); % state.rtnStatus == 1 if true
    
    % store cal data before finding extensor_sensors, once pressed enter while in astro...
    if state.rtnStatus == 1 && const.playAstro == 0 %
        % sync:
        % get the time they pressed enter 
        % cut video when you see hand show up in astro, that time == this time
            % this + seconds(const.calReady) == startTime#_active
            % this + seconds(const.calReady) + seconds(const.calTimer) == startTime#_end
        if const.calGest == 1
            const.startTime1_rest = out.time;
        elseif const.calGest == 2
            const.startTime2_rest = out.time;
        elseif const.calGest == 3
            const.startTime3_rest = out.time;
        end
        
        const.playAstro = 1;
        state.hadError = 0; % reset error status (to only check if got error during cal.)
        out.pressed = const.calGest*10; % *10 so it does not overlap with other codes. thus 10 = fingers up, 20= hand up... 
        [const,state] = resetKeyToggle(const,state); % reset rtnStatus - this presses enter returns it 
    end
    
    state.readytocalibrate = 0;
    fprintf('const.playAstro = %i \n', const.playAstro);
    if const.playAstro == 1  
        % collect rest and gesture data for calibrating
        [const, out, state, calData] = playAstroBootle (const, out, state, calData);
        
    end
        
%% Reset for the next cal loop...
    
    if state.pressedX == 1
        

        if const.calGest < 4
            % reset for next cal gesture:
            [const,state] = resetKeyToggle(const,state);    % reset rtnStatus - this presses enter
            state.pressedX = 0;                             % reset pressedX
            const.playAstro = 0;                            % waiting for enter again
            const.calibrating = 1;                          % continue  calibrating
            state.hadError = 0;       
            state.storeTime = 0;                            % to store the time elements of each change

        end
    end

    % Jumper should close by itself.
    if state.readytocalibrate == 1  % calGest == 4
        
            % set const/state to switch modes
            const.calibrating = 0;                          % not calibrating anymore, move to Dashy
            const.CalGest_v = 1;                            % for Dashy setup
            const.CalGest_s = 2;                            % for Dashy setup
            state.launchedJumper = 1;                       % to not open Jumper any more.
            save(const.trialConst,'const');                 % save the const data, before validation, incase crash
            
            % calculate userdata needed for gameplay: 
            [const,out,store,state,calData, myo] = validatecalData (const,out,store,state,calData, myo);
            save(const.trialConst,'const');                 % save the const data, before validation, incase crash
            
    end    
  
    
end % end of if Calibrating



%% Gameplay Actions

% bring the game to front...if it is setup
if const.calibrating == 0 && isfield(const,'extensor_sensors')
   
    % Initialize Dashy, should only happen 1 time   
    if const.goDashy == 1         
        [const,calData] = setupDashy (const, calData);  
        out.pressed = 0; % signal start of dashy
    end
        
%% Procecss Bin Main

    % Every Loop - Only after Extensor Sensor is selected
    % subtract resting mean from each channel
    out.dataEMG(:,2:end) = out.dataEMG(:,2:end) - const.ReadyMean; 
    
    % process: get %E %F
    out = GetCurrentActivity(const, out);
    
    % update running max and base
    [const, out, store] = updateMax(const,out,store);
    
    % 50% overlap / e.g. every 5 seconds update the last 10 seconds...
    if store.time(end) >= const.lastBaseUpdate % nextBaseUpdate
        [const, out, store] = updateBase(const,out,store); % For PB3
    end

%%  Game Decisions

    % push to game decisions 
    if const.countFromStart <= const.maxWindow
        const.countFromStart = const.countFromStart+1; 
    end
    out = PushtoGame3(const, out, store);
       
   % Classification (if used) / IMU
   % calculate feature values if using classifier
   if const.useClassifier == 1

       % check if aceptable IMU
       % returns out.PredAccel = 1 if arm moving too much in the last few seconds
       if const.useIMU == 1
           out = evalAccel(const, out, store);
           out.predGyro = 0;
       elseif const.useIMU == 2
           out = evalGyro (const, out, store);
           out.predAccel = 0;
       elseif const.useIMU == 3
           out = evalAccel(const, out, store);
           out = evalGyro (const, out, store);
       end
      
       % set default Predicted Label, only change to 1 or 2 if jumping
       out.PredLabel = 0;
       
       if out.pressed == 1 % jumping
           
           % pick if it is with open or closed fingers
            % returns out.PredLabel and out.normGest as 1 or 2
           [const, out] = calculateFeatures(const,out, store);
                 
            %% Speed feedback
            if const.speedFeedback == 1
              [const,out] = speedFeedback(const, out, store);
            end
            
            % Push class and IMU decisions to game
            % presses or not based on: out.normGest  and out.normAccel 
           [const,out] = pushFeedback (const,out);        
           
       end
           
   end 
          
end

%% Store and Track, both with/w0 Extensor_sensor

% counts the seconds of this loop.
out.processBinTime = seconds(datetime()-loop0);
    
% store keeps the window of data that updates max.
store = storeWindowOutput(const,out,store);

% write append row to .txt in results
writeWindowOutput(const,out);

% probably dont need anymore, update lastRowUsed, 
out.lastRowUsed = newestRow;

% corresponding window for IMU data
out.lastRowUsedImu = myo.accelDataIndex-1; % just for corresponding data
 
    

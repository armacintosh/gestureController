function [const, myo, out, store, calData, state] = ProcessBin (const, myo, out, store, newestRow, calData, state)

% start the timer for how long the loop takes to execute
loop0 = datetime();

%% setup 

% setup mouse click functions
import java.awt.Robot;
import java.awt.event.*;

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

% convert from bits -127-128 to -+1 (EMG comes in 256 bit intravel from Myo)
    % then take abs. (Reaz 2006, Techniques of EMG Signal Analysis)
    % out.dataEMG has time col 1, and only used EMG ch after that.
    % subtract resting mean after calibration.
out.dataEMG(:,2:end)  = abs( (out.dataEMG (:,2:end ) ./128) ); 

% IMU Data preprocessing  just using resultant, the abs sum of all axis for the whole window of times
out.AccelRes = sum( sqrt(sum( out.dataAccel(:,myo.emgCols(1):end) .^2 )));
out.GyroRes  = sum( sqrt(sum( out.dataGyro (:,myo.emgCols(1):end) .^2 )));

%% calibration for the trial, find up direction and inital max

% before finding the extensor sensors
if const.calibrating == 1 && ~isfield(const,'extensor_sensors') % starts at 1, changes to 0 at the end of this sequence
    
    % go to the window/File 
    const.pushbutton.AppActivate('Myo Jumper'); % make sure it is the same game

    % check if pressed enter while in Jumper
    hWnd = calllib('user32','GetForegroundWindow');
    [retVal, ~] = calllib('user32','GetWindowTextA', int32(hWnd), const.windowTitlePtr, int32(100));
    activeWindowTitle = char(const.windowTitlePtr.Value(1:retVal));
    
    if contains(activeWindowTitle,'jumper','IgnoreCase',true)
         state.rtnStatus = System.Windows.Input.Keyboard.IsKeyToggled(state.keys(8));  
    end   
         
    % if an error occured during calibration, recalibrate
    if state.hadError == 1
        [const, state] = resetCalGame(const,state);
    end
    
    % store cal data before finding extensor_sensors, once pressed enter
    if state.rtnStatus == 1 && const.playAstro == 0 %

        % get the time they pressed enter and cut video when you see hand show up in astro, that time == this time
        const.startTime = out.time;
        fprintf('pressed  enter at:  %s \n', char(const.startTime)  );
        const.syncCam = 1;  
        const.playAstro = 1;
        state.hadError = 0; % reset error status (to only check if got error during cal.)
    end
    
    readytocalibrate = 0;
    if const.playAstro == 1  
        % collect rest and gesture data for calibrating
        fprintf('ProcessBin - entering playAstroBootle:  %s \n', char(datetime())  );  
        [const, out, calData, readytocalibrate] = playAstroBootle(const, out, calData);        
    end
      
    if readytocalibrate == 1          

            % save the first instance of the const file
            save(const.trialConst,'const'); % before in case there is an error in the validation stage

            % indicate to skip this section next time and process calibrated data for playing.
            [const,out,store,state,calData] = validatecalData (const,out,store,state,calData);
                        
            % save the first instance of the const file
            save(const.trialConst,'const');
            
            const.calibrating = 0; % done calibrating
            
    end    
        
end





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
        % this is where min is updated...
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

% store processed ouput to out struct
if const.syncCam == 1 % only 1 when goes into calib.
    out.pressed = 2;
    const.syncCam = 0;
end

% counts the seconds of this loop.
out.processBinTime = seconds(datetime()-loop0);

% store keeps the window of data that updates max.
store = storeWindowOutput(const,out,store);

% write append row to .txt in results
writeWindowOutput(const,out);

% update lastRowUsed 
out.lastRowUsed = newestRow;

% corresponding window for IMU data
out.lastRowUsedImu = myo.accelDataIndex-1; % just for corresponding data

    

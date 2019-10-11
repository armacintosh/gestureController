function [const, out, state, calData] = playAstroBootle (const, out, state, calData)
        
% setup mouse click functions
import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;

%%

% if doing the first Hand up with fingers active
if const.calGest == 1
    % add  row of calibration data
     calData.cal =  [calData.cal; out.dataEMG]; % only relevant columns...(no time)
end

%%

% Press space if active to Launch bootle
% activity of the instant, element wise subtraction, should be nCH indipendent
presVal = sum(calData.cal(end, 2:end)); % the raw activity of all used channels
fprintf('presVal = %s \n', presVal);

%%

% store the time it transitioned from rest to active
if state.storeTime == 0

    % get the time 
    switch const.calGest 
        case 1
            state.freshStart = const.startTime1_rest;
        case 2
            state.freshStart = const.startTime2_rest;
        case 3
            state.freshStart = const.startTime3_rest;
    end
          
    if out.time >= (state.freshStart + seconds(const.calReady) )
        
        % press space 
        mouse.keyPress(KeyEvent.VK_SPACE); %  
        disp('pressing space');
        state.pressingEnter = 1; 
        
        if const.calGest == 1
            const.startTime1_active = out.time;
            % index of calData.cal where they switch from rest to active
            calData.switch1 = size(calData.cal,1);
        elseif const.calGest == 2
            const.startTime2_active = out.time;
            calData.switch2 = size(calData.cal,1);
        elseif const.calGest == 3
            const.startTime3_active = out.time;
            calData.switch3 = size(calData.cal,1);
        end
    
        [const,state] = resetKeyToggle(const,state); % reset rtnStatus - this presses enter returns it 
        state.storeTime = 1; % to not go into this loop again
        
    end
    
end 
    

% after designated calibration playing time: 'calTimer', press x to go to next calGest.
if out.time >= (state.freshStart + seconds(const.calReady+const.calTimer))

    % Press X to close astro bootle
    mouse.keyPress(KeyEvent.VK_X);
    pause(1/30); % slow it for an instant
    disp('pressed X');
    mouse.keyRelease(KeyEvent.VK_X);
    state.pressedX = 1;
    
    mouse.keyRelease(KeyEvent.VK_SPACE);
    disp('no space');
    state.pressingEnter = 0;

    % update calGest
    const.calGest = const.calGest + 1;
end 

% update readyto CalStatus     readytocalibrate = 1;
    if const.calGest == 4
        state.readytocalibrate = 1; % move to next phase
    else
        state.readytocalibrate = 0;
    end
        
    
end



function [const, out] = speedFeedback(const, out, store)

%% setup mouse click functions and thresholds
import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;
%%

if const.speedFeedbackType == 1
    try % try if not enough bins to start
        pressPositive = store.PredLabel(store.pressed>0); % get the gesture label every time they pressed from store.
        pressPositive = [pressPositive; out.PredLabel]; % adds the latest gest
        pressPositive = pressPositive(pressPositive>0); % Removes that latest predLabel if it is 0
        speedGest = pressPositive(end-const.runningAvg:end); % 10 bins at 100 ms = 1 second
        out.speedGest = median(speedGest); % % will always be 1 or 2
    catch
        out.speedGest = store.PredLabel(end); % can be 0
    end 

    % push feedback to game
    if out.speedGest == 1 && const.keepHandClosed == 0 % undesired gesture
        % Feedback - change game speed based on gesture produced.
        % slow down game if jumping in undesired gesture (normally closed hand)
        const.pushbutton.AppActivate(char(const.gameLoc)); 
        mouse.keyPress(KeyEvent.VK_DOWN); % slows the game down
        mouse.keyRelease(KeyEvent.VK_DOWN); % slows the game down
        
        const.speedMax = const.speedMax -1; % tracks how much the speed is going down, and prevents it from going above game preset
        fprintf('SLOWER, count == %i \n\n' ,const.speedMax);
        
        
    elseif out.speedGest == 2 && const.keepHandClosed == 1 % undesired gesture
        % slow down game if jumping in undesired gesture (normally closed hand)
        const.pushbutton.AppActivate(char(const.gameLoc)); 
        mouse.keyPress(KeyEvent.VK_DOWN); % slows the game down
        mouse.keyRelease(KeyEvent.VK_DOWN); % slows the game down
        
        const.speedMax = const.speedMax -1; % tracks how much the speed is going down, and prevents it from going above game preset
        fprintf('SLOWER, count == %i \n\n' ,const.speedMax);
        
    else
        
        if const.speedMax < 0
            % else they performed the desired gesture and the speed can increase
            const.pushbutton.AppActivate(char(const.gameLoc)); 
            mouse.keyPress(KeyEvent.VK_UP); % slows the game down
            mouse.keyRelease(KeyEvent.VK_UP); % slows the game down
            const.speedMax = const.speedMax +1; % tracks how much the speed is going down, and prevents it from going above game preset
            fprintf('SLOWER, count == %i \n\n' ,const.speedMax);
        end
        
    end      

elseif const.speedFeedbackType == 2
    % change speed of game based on recent IMU history
    % get recent history of IMU
    try % try if not enough bins to start
        pressPositiveA = store.PredAccel(store.pressed>0); % get the gesture label every time they pressed from store.
        pressPositiveA = [pressPositiveA; out.PredAccel]; % adds the latest gest
        speedGestA = pressPositiveA(end-const.runningAvg:end); % 10 bins at 100 ms = 1 second
        speedGestA = median(speedGestA); % % will always be 1 or 0
        
        pressPositiveG = store.PredGyro(store.pressed>0); % get the gesture label every time they pressed from store.
        pressPositiveG = [pressPositiveG; out.PredGyro]; % adds the latest gest
        speedGestG = pressPositiveG(end-const.runningAvg:end); % 10 bins at 100 ms = 1 second
        speedGestG = median(speedGestG); % % will always be 1 or 0
    catch
        speedGestA = store.PredAccel(end); % can be 0
        speedGestG = store.PredGyro(end); % can be 0
    end 
    
    % push feedback to game
    if speedGestA || speedGestG == 1 % undesired arm movement
        % Feedback - change game speed based on gesture produced.
        % slow down game if jumping in undesired gesture (normally closed hand)
        if const.speedMax > const.speedChangeMax
            const.pushbutton.AppActivate(char(const.gameLoc)); 
            mouse.keyPress(KeyEvent.VK_DOWN); % slows the game down
            mouse.keyRelease(KeyEvent.VK_DOWN); % slows the game down
            out.speedGest = 5; % 5 is code for IMU speed gest passed
            const.speedMax = const.speedMax -1; % tracks how much the speed is going down, and prevents it from going above game preset
        end
        
    else 
        if const.speedMax < 0 % if not already at max speed
            % else they performed the desired gesture and the speed can increase
            const.pushbutton.AppActivate(char(const.gameLoc)); 
            mouse.keyPress(KeyEvent.VK_UP); % slows the game down
            mouse.keyRelease(KeyEvent.VK_UP); % slows the game down
            out.speedGest = 0; % 5 is code for IMU speed gest passed
            const.speedMax = const.speedMax +1; % tracks how much the speed is going down, and prevents it from going above game preset
        end
    end      
    
end
 
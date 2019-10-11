function [const,out] = pushFeedback (const,out)

% sends keypress based on: Gesture Classification and IMU movement 
% If gesture class  == hand closed (code == 1) --> send Key Y
% If IMU  == >> Baseline --> send Key Z
%
% Key X --> signals 'Reminder' message in Practice Panel
% Key Y --> signals 'Fingers Open' message in Practice Panel
% Key U --> signals 'Fingers Closed' message in Practice Panel
% Key Z --> signals 'Arm Still' message in Practice Panel

% class = out.PredLabel 
% excessIMU = out.IMU >> IMU lim

% only going to show one at a time, do not want info. overload
% if IMU is too great, show first. If IMU ok, but hand closed, send class

%% setup mouse click functions and thresholds
import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;

%%
% Add IMU decision Here then if no IMU decision do class decision
if out.PredAccel == 1 || out.PredGyro == 1
    const.pushbutton.AppActivate(char(const.gameLoc)); 
    mouse.keyPress(KeyEvent.VK_Z);
    mouse.keyRelease(KeyEvent.VK_Z);
    out.gaveFeedback = 1; % imu  feedback


%  normGest==1 means classifier predicted hand closed. keepHandClosed ==0
%  Means desired gesture is Fingers up, thus predicted undesired gesture...
% feedback: if practice panel comes, show the hand active reminder.
elseif out.normGest == 1 && const.keepHandClosed == 0

    const.pushbutton.AppActivate(char(const.gameLoc)); 
    mouse.keyPress(KeyEvent.VK_Y);
    mouse.keyRelease(KeyEvent.VK_Y);
    out.gaveFeedback = 2; % gesture feedback , 1 is IMU feedback
    
    
%  normGest==2 means classifier predicted fingers Up. keepHandClosed ==1
%  means desired gesture is rested fingers, thus predicted undesired gesture...
% feedback: if practic panel comes, show the wrist up reminder.
elseif out.normGest == 2 && const.keepHandClosed == 1
    
    const.pushbutton.AppActivate(char(const.gameLoc)); 
    mouse.keyPress(KeyEvent.VK_U);
    mouse.keyRelease(KeyEvent.VK_U);    
    out.gaveFeedback = 2; % classification based feedback 
    

else % and out.normAccel == 0 and out.normGest == 2 (i.e. still arm and fingers up)
    const.pushbutton.AppActivate(char(const.gameLoc)); 
    mouse.keyPress(KeyEvent.VK_X);
    mouse.keyRelease(KeyEvent.VK_X);
    out.gaveFeedback = 0;
    
end 
    

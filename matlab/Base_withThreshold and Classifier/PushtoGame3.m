function [out] = PushtoGame3  (const, out, store)
% for PB3
    % get first ratio from Caltimer, use inverse of ratio to get inital baseline (updateMaxInit.m)
    % in game, update baseline from store using peakseek
    % then use const.ratio* updated baseine  .... 
    % + leeway to get the threshold min E and max F for the window to use in PB3
    % could also use peakseek to update ratio or expected or leeway could be SD of baseline
    % could just make PB3 be based on the ratio...i.e. if the current mavE
    % has a Up:Rest ratio similar to expectd, need windows baseline 
    % if you dont want to use leeway and just use the ratio the set const.ThreshScale == 0

%% setup mouse click functions and thresholds
import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;

%%

if const.countFromStart <= const.maxWindow
    out.minE = (out.currentMaxE * const.aboveBaseE); % will be ~Max * 0.25
    out.maxF = out.currentMaxF;
else 
    out.minE = out.currentBaseE + ((out.currentMaxE - out.currentBaseE) * const.aboveBaseE);
    out.maxF = out.currentBaseF + ((out.currentMaxF - out.currentBaseF) * const.aboveBaseF);
end 

% set boundaries for expected minE/maxF
if (out.minE > out.currentMaxE*0.75) || (out.minE < out.currentBaseE)
    % go back to expected from calib.
    if isfield(const,'Cal')
        out.minE = out.currentMaxE * (const.Cal.const.thresh.percentEinExt/100);
    else
        out.minE = out.currentBaseE * (1 + const.aboveBaseE) ; % or...
    end
end 


if (out.maxF >= out.currentMaxF) || (out.maxF <= out.currentBaseF * (1+out.currentBaseF) ) 
    % go back to expected from calib.
    if isfield (const,'Cal')
        out.maxF = out.currentMaxF * (const.Cal.const.thresh.percentFinExt/100)*const.ThreshScale;
    else 
        out.maxF = out.currentMaxF / const.ThreshScale ; % or
    end 

end     

%  if something messes up.
if isnan(out.minE)
    out.minE = out.currentBaseE * const.ThreshScale ;
end 

if isnan(out.maxF)
    out.maxF = out.currentMaxF / const.ThreshScale ;
end 


%% get the %of thresh for passing to game

extensors = max(store.mavE(end-(const.runningAvg):end,:)); % 5 rows == how much time? , 2 second back...?
act = round(((extensors / out.currentMaxE)*10),0); % interger from 0 to inf. probably less than 10
out = pressStyle(const,out,act); % get newest extension quality score

%%
% release condition, dont press if too little E or too much F
if (out.mavE < out.minE) || (out.mavF > out.maxF)

    if (out.pressed == 1) % if last button was down, and this new button will be rest
        timePressed = cputime - const.lastPressTime;

        % 1/30 is 1 frame assuming 30 frames per second. 
        % Adjust this parameter as you see fit activate game
        if (timePressed > 1/30) 
%             pushbutton.AppActivate('minigames'); % make sure it is the same game

            if const.press == 1
                const.pushbutton.AppActivate(char(const.gameLoc)); % make sure it is the same game

                % release all other keys
                mouse.keyRelease(KeyEvent.VK_E);
                mouse.keyRelease(KeyEvent.VK_F);
                mouse.keyRelease(KeyEvent.VK_P);
        %         mouse.keyRelease(KeyEvent.VK_SPACE);
                fprintf ('all keys released \n');

            end
        %     [out] = releaseStyle (const,out,act); % % recordes/passes style points - needs to be 0 or 1 pretty much / below threshold...
        end
        
    end

%     fprintf ('all keys released \n');
    out.pressed = 0;
    
% press condition, press if enough E and low enough F
elseif (out.mavE > out.minE) && (out.mavF < out.maxF)

    % only re-press if a new press
    if (out.pressed == 0) % if last button was up, and this new button will be down
        
        if const.press == 1
            % activate game
            const.pushbutton.AppActivate(char(const.gameLoc)); % make sure it is the same game
            % pushbutton.AppActivate('minigames'); % make sure it is the same game

            % pressed all 3 keys
            mouse.keyPress(KeyEvent.VK_E);
            mouse.keyPress(KeyEvent.VK_P);
            mouse.keyPress(KeyEvent.VK_F); % press
    %         mouse.keyPress(KeyEvent.VK_SPACE); % press
            fprintf ('Pressing E-P-F \n');
        end
    end 
    
%     fprintf ('Pressing E-P-F \n');
    out.pressed = 1;
    const.lastPressTime = cputime; % ajmal added this
    
else
    fprintf ('not any option \n');
    out.pressed = 0;
    
end
  

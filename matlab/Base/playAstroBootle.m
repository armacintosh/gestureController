function [const, out, calData, readytocalibrate] = playAstroBootle (const, out, calData)
        
% for checking for program states and setup mouse clicks
NET.addAssembly('PresentationCore');
import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;
NET.addAssembly('System'); 
import System.Diagnostics.Process.* 

%%
% add  row of calibration data
calData.cal = [calData.cal; out.dataEMG]; % only relevant columns...(no time)

% if 'Ready set go' is done...col. 1 is cputime
if out.time >= (const.startTime + seconds(const.calReady-0.5))

    % get rest data
    if ~isfield (const,'ReadyMean')
    
        % end Ready phase of calibration after ~3 seconds (end of ready set go), index of row 
        const.CalGoTime = length(calData.cal(:,1)); % the index where they start to extend

        % get the ready mean once
        const = findReadyMean (const,calData); % returns const.ReadyMean  
            
            
    elseif sum(isnan(const.ReadyMean(:)))>0
        % if there is an NAN in the mean vals... reclaculate it
        % end Ready phase of calibration after ~3 seconds (end of ready set go), index of row 
        const.CalGoTime = length(calData.cal(:,1)); % the index where they start to extend

        % get the ready mean once
        const = findReadyMean (const,calData); % returns const.ReadyMean              
    end

%     after you have const.ReadyMean, press space if active to Launch bootle
%     activity of the instant, element wise subtraction 
%     should be nCH indipendent
    presVal = calData.cal(end, 2:end) - const.ReadyMean; 
    if sum(presVal) > sum(const.ReadyMean)*const.ReadyMeanMultiplier
        
        % go to the window/File 
        mouse.keyPress(KeyEvent.VK_SPACE); %  
        disp('playAstro - pressing space');
        
    elseif sum(presVal) < sum(const.ReadyMean)*const.ReadyMeanMultiplier
        
        % release space 
        mouse.keyRelease(KeyEvent.VK_SPACE);
        disp('playAstro - released space');
        
    else 
        mouse.keyRelease(KeyEvent.VK_SPACE);
        disp('no space');
    end 

end

% after designated calibration playing time: 'calTimer', press x to quit.
if out.time >= (const.startTime + seconds(const.calReady+const.calTimer))

    % Press X to close astro bootle
        mouse.keyPress(KeyEvent.VK_X);
        pause(1/30); % slow it for an instant
        mouse.keyRelease(KeyEvent.VK_X);
        disp('playAstro - pressed X');
        
    readytocalibrate = 1;
    
else
    
    readytocalibrate = 0;
end




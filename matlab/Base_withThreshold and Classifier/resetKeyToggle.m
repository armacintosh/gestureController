function [const,state] = resetKeyToggle(const,state)

% for checking for program states and setup mouse clicks
import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;
NET.addAssembly('System'); 
import System.Diagnostics.Process.* 

%%
% make sure escape toggled is set to false to start
if const.errorChecking == 1
    state.activlyPlaying = 0;
    state.qStatePrevious = 0;
    state.sinceLastCheck = seconds(0);
end

% toggle return to set status at 0
state.rtnStatus = System.Windows.Input.Keyboard.IsKeyToggled(state.keys(8));
fprintf('rtnStatus before setting: %i \n', state.rtnStatus); % should always be 0 here
    if state.rtnStatus == 1
        % press to untoggle
        fprintf('state.RtnStatus == 1, toggled at %s, resetting toggle state \n', char(datetime));
%         switch qState back to 0
            mouse.keyPress(KeyEvent.VK_ENTER);
            pause(1/10); 
            mouse.keyRelease(KeyEvent.VK_ENTER); 
        state.rtnStatus = System.Windows.Input.Keyboard.IsKeyToggled(state.keys(8));
        fprintf('rtnStatus before loop - Toggled to: %i \n', state.rtnStatus); % should always be 0 here
    else 
        fprintf('rtnStatus before loop: %i \n', state.rtnStatus); % should always be 0 here
    end 

function [const,state] = resetCalGame(const,state)

import java.awt.Robot;
import java.awt.event.*;
mouse = Robot;
import System.Diagnostics.Process.* 

% close game . wait until it is closes
dos('taskkill /F /IM "MyoJumper.exe"');
MyoJumperClosed = GetProcessesByName('MyoJumper'); 
while MyoJumperClosed.Length ~= 0
    pause(0.1);
    disp('...closing MyoJumper')
    MyoJumperClosed = GetProcessesByName('MyoJumper'); 
end 

% reset the calibratio8zn values
const.calData = [];
calData = [];
const.playAstro = 0;
const.calibrating = 1;
state.hadError = 0;

% note user saying did not get good calibration
% tell participant with figure window
if const.language == 1
    errorText = {'Lets try that one more time!'};
else
    errorText = {'Essayer une fois de plus!'};
end
[Err] = showErrorScreen(const,errorText);


% relaunch calibration game
[const] = showCalGame(const);

% % close error window
if ~isempty(findall(0,'type','figure','name','Error Notice'))
    close(findall(0,'type','figure','name','Error Notice'));
end


% toggle return key
[const,state] = resetKeyToggle(const,state);

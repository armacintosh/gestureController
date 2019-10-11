function [const] = showCalGame(const)
% calibration game

% lets me check if the program extist in .NET framework
import System.Diagnostics.Process.* 


%% open game

str = 'start "" /AboveNormal "Programs\MyoJumper\MyoJumper.exe"';
dos(str); 

MyoJumperOpen = GetProcessesByName('MyoJumper'); 
% wait until it is open
while MyoJumperOpen.Length == 0
    pause(0.1);
    disp('...opening MyoJumper')
    MyoJumperOpen = GetProcessesByName('MyoJumper'); 
end 

% show and log it opened
fprintf('Myo Jumper opened at: %s \n', datetime());
fileID = fopen(const.logFileMatlab,'a+');
fprintf(fileID,'Myo Jumper opened at: %s \n\n', datetime());
fclose(fileID);

dos('taskkill /F /IM "cmd.exe"'); % they may mess other stuff up?


pause(2);
const.pushbutton.AppActivate('Myo Jumper'); 

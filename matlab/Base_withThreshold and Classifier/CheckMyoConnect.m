function [] = CheckMyoConnect(const) 

% lets me check if the program extist in .NET framework
import System.Diagnostics.Process.* 

% open the game
MyoConnectOpen = GetProcessesByName('Myo Connect'); 
if MyoConnectOpen.Length == 0

    ! Programs\Myo Connect\Myo Connect.exe &
    fprintf('Wait 2 seconds...opening Myo Connect \n');
    
    % wait until it is open
    while MyoConnectOpen.Length == 0
        pause(0.1);
        disp('...opening Myo Connect')
        MyoConnectOpen = GetProcessesByName('Myo Connect'); 
    end 
    
else 
    fprintf('Myo Connect already running \n');
end 

% write output
% show and log
fprintf('Myo Connect started at: %s \n', datetime());
fileID = fopen(const.logFileMatlab,'a+');
fprintf(fileID,'Myo Connect started  at: %s \n\n', datetime());
fclose(fileID);

dos('taskkill /F /IM "cmd.exe"'); 




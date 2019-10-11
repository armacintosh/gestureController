function [] = openDashyMyo(const)

% lets me check if the program extist in .NET framework
import System.Diagnostics.Process.* 

%%

MyoDashyOpen = GetProcessesByName('Dashy'); 
if MyoDashyOpen.Length == 0

    % open it
    str = 'Programs\Games\Dashy.exe &'; 
    dos(str); 

    % wait until it is open
    while MyoDashyOpen.Length == 0
        pause(0.1);
        disp('...opening Dashy')
        MyoDashyOpen = GetProcessesByName('Dashy'); 
    end 
    
else
    disp('MyoDashy already open');
end


% show and log
fprintf('Dashy opened at: %s \n', datetime());
fileID = fopen(const.logFileMatlab,'a+');
fprintf(fileID,'Dashy opened at: %s \n\n', datetime());
fclose(fileID);

dos('taskkill /F /IM "cmd.exe"'); % 
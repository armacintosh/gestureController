function[const,state, myo] = getActiveWindow (const,state, myo)

% addpath('C:\WINDOWS\system32\'); savepath;
% loadlibrary('C:\WINDOWS\system32\user32.dll','win32.h');

% lets me check if the program extist in .NET framework
import System.Diagnostics.Process.* 

%% Check if Dashy is active or not

hWnd = calllib('user32','GetForegroundWindow');
[retVal, ~] = calllib('user32','GetWindowTextA', int32(hWnd), const.windowTitlePtr, int32(100));
activeWindowTitle = char(const.windowTitlePtr.Value(1:retVal));
if contains(activeWindowTitle,'dashy','IgnoreCase',true)
    const.DashyActiveWindow = 1;
else 
    fprintf('Dashy Paused at %s, waiting to resume \n', char(datetime));
    const.DashyActiveWindow = 0;   
end

%% Pause if Dashy not active window

while const.DashyActiveWindow == 0 

    % need to wait until Dashy is active window again.
    hWnd = calllib('user32','GetForegroundWindow');
    [retVal, ~] = calllib('user32','GetWindowTextA', int32(hWnd), const.windowTitlePtr, int32(100));
    activeWindowTitle = char(const.windowTitlePtr.Value(1:retVal));
    if contains(activeWindowTitle,'dashy','IgnoreCase',true)
        disp('Dashy is active window');
        const.DashyActiveWindow = 1;      
    else
        const.DashyActiveWindow = 0;
        fprintf('Dashy still paused at %s, continuing to collect Myo \n', char(datetime));
        
        % check that Dashy is still open
        DashyOpen = GetProcessesByName('Dashy'); 
        if DashyOpen.Length == 0  % it's 0, then there isn't running
            % get out of the loop
           const.DashyActiveWindow = 1;
           % signal to close the trial
           state.stopTrial = 1;
           fprintf('Dashy Not Running at %s, ending trial \n', char(datetime));
        end
    end
   
    pause(1);
        
end


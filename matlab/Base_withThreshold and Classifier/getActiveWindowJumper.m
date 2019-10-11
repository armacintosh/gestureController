function[const,state, myo] = getActiveWindowJumper (const,state, myo)
% change to check 
% addpath('C:\WINDOWS\system32\'); savepath;
% loadlibrary('C:\WINDOWS\system32\user32.dll','win32.h');

% lets me check if the program extist in .NET framework
import System.Diagnostics.Process.* 

%% Check if Dashy is active or not

hWnd = calllib('user32','GetForegroundWindow');
[retVal, ~] = calllib('user32','GetWindowTextA', int32(hWnd), const.windowTitlePtr, int32(100));
activeWindowTitle = char(const.windowTitlePtr.Value(1:retVal));
if contains(activeWindowTitle,'jumper','IgnoreCase',true)
    const.JumperActiveWindow = 1;
else 
    fprintf('Jumper Paused at %s, waiting to resume \n', char(datetime));
    const.JumperActiveWindow = 0;   
end

%% Pause if Dashy not active window

while const.JumperActiveWindow == 0 

    % need to wait until Dashy is active window again.
    hWnd = calllib('user32','GetForegroundWindow');
    [retVal, ~] = calllib('user32','GetWindowTextA', int32(hWnd), const.windowTitlePtr, int32(100));
    activeWindowTitle = char(const.windowTitlePtr.Value(1:retVal));
    if contains(activeWindowTitle,'jumper','IgnoreCase',true)
        disp('jumper is active window');
        const.JumperActiveWindow = 1;     
        
    else
        const.JumperActiveWindow = 0;
        fprintf('Jumper still paused at %s, continuing to collect Myo \n', char(datetime));
        
        % clear buffer
        myo = clearBuffer (myo);              
        
        % check that Dashy is still open
        DashyOpen = GetProcessesByName('myoJumper'); 
        if DashyOpen.Length == 0  % it's 0, then there isn't running
            % get out of the loop
           const.JumperActiveWindow = 1;
           % signal to close the trial
           state.stopTrial = 1;
           fprintf('Jumper Not Running at %s, ending trial \n', char(datetime));
        end
    end
   
    pause(1);
        
end

function [const,calData] = setupDashy (const, calData)


import System.Diagnostics.Process.* 

%%
% wait for jumper to close
MyoJumperOpen = GetProcessesByName('MyoJumper'); 
while MyoJumperOpen.Length ~= 0
    pause(0.01);
    disp('...waiting for Jumper to Close')
    MyoJumperOpen = GetProcessesByName('MyoJumper'); 
end 

    % show and log jumper closed
    fprintf('Myo Jumper closed at: %s \n', datetime());
    fileID = fopen(const.logFileMatlab,'a+');
    fprintf(fileID,'Myo Jumper closed at: %s \n\n', datetime());
    fclose(fileID);

% if calibrating gestures indicate which gesture it was
if const.calibratingGestures == 1
    % add TrueLabel col. to cal data.
    if const.CalGest_v == 1
        TrueLabel = ones(length(calData.cal),1)*const.CalGest_s;
        calData.cal = [calData.cal TrueLabel];
    elseif const.CalGest_v == 0
        TrueLabel = ones(length(calData.cal),1)*0;
        calData.cal = [calData.cal TrueLabel];
    end
    
end

% if jumper is closed,  the length of the string for when myo is running
if  MyoJumperOpen.Length == 0
    
    % open DASHY
    openDashyMyo(const); 
    const.pushbutton.AppActivate(char(const.gameLoc)); 
    const.goDashy = 0;
    const.DashyOpened = 1;
end


% wait until dashy is open
MyoDashyOpen = GetProcessesByName('Dashy'); 
fprintf('\n\n MyoDashyOpen.Length == %i \n\n',MyoDashyOpen.Length);
while MyoDashyOpen.Length == 0
    pause(0.01);
    disp('...waiting for Dashy to open')
    MyoDashyOpen = GetProcessesByName('Dashy'); 
end 


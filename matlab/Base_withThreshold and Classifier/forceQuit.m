function [] = forceQuit(const)
% forceQUIT

% these are the TCP/IP buffer objs
clear tEMG;
clear tAccel;
clear tGyro;
clear tOrient;
clear tEvent;

% clear MyoServer\Logs folder or move to other spot...
dos('taskkill /F /IM "Myo Connect.exe"');
dos('taskkill /F /IM "MyoServer.exe"');
dos('taskkill /F /IM "Dashy.exe"');
dos('taskkill /F /IM "MyoJumper.exe"');
dos('taskkill /F /IM "cmd.exe"');
close all;

% return to Launcher
if nargin > 0
    const.pushbutton.AppActivate('MyoLauncher'); 
end

delete('lockFile.txt'); % delete file if it already existed

clc;clear;

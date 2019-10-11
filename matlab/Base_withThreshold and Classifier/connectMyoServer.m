function [myo]= connectMyoServer (const)

% lets me check if the program extist in .NET framework
import System.Diagnostics.Process.* 

%%
% make sure Myo Connect is already Open
MyoConnectOpen = GetProcessesByName('Myo Connect'); 
% wait until it is open
while MyoConnectOpen.Length == 0
    pause(0.1);
    disp('...opening Myo Connect')
    CheckMyoConnect(const); 
    MyoConnectOpen = GetProcessesByName('Myo Connect'); 
end 

%% open MyoServer - already open before running 

MyoServerOpen = GetProcessesByName('MyoServer'); 
if MyoServerOpen.Length == 0
    
    % open myoServer    
    ! Programs\MyoServer\MyoServer.exe &
    fprintf('...opening MyoServer \n')
    
    % wait until it is open
    while MyoServerOpen.Length == 0
        pause(0.1);
        disp('...opening MyoServer')
        MyoServerOpen = GetProcessesByName('MyoServer'); 
    end 

else 
    fprintf('...MyoServer already running \n')
end 

% log opened
fprintf('MyoServer started at: %s \n', datetime());
fileID = fopen(const.logFileMatlab,'a+');
fprintf(fileID,'MyoServer started  at: %s \n\n', datetime());
fclose(fileID);

% close cmd window
dos('taskkill /F /IM "cmd.exe"'); 


%%
% connect to EMG data source
myoServerConnected = 0;

% connects to TCPIP port on myo server
% timestart = datetime();
while (myoServerConnected ~= 1)
    
    % connect to Myo Server
    try
        myo.tEMG = tcpclient('127.0.0.1', 30100, 'Timeout', 0); % timeout is , change to 0 or 1/200
        myoServerConnected = 1;
        disp('MyoServer Connected');
    catch
        disp('Waiting for connection to MyoServer...');
        pause (2);   
       
    end    
end

% then accelerometer data source
myoServerConnected = 0;

while (myoServerConnected ~= 1)
    try
        myo.tAccel = tcpclient('127.0.0.1', 30101, 'Timeout', 0);
        myoServerConnected = 1;
    catch
        disp('Waiting for connection to accelerometer data...');
        pause(2);
    end
end

% then gyro data source
myoServerConnected = 0;

while (myoServerConnected ~= 1)
    try
        myo.tGyro = tcpclient('127.0.0.1', 30102, 'Timeout', 0);
        myoServerConnected = 1;
    catch
        disp('Waiting for connection to gyro data...');
        pause(2);
    end
end

% then orientation data source
myoServerConnected = 0;

while (myoServerConnected ~= 1)
    try
        myo.tOrient = tcpclient('127.0.0.1', 30103, 'Timeout', 0);
        myoServerConnected = 1;
    catch
        disp('Waiting for connection to orientation data...');
        pause(2);
    end
end


%%
% then event data source
myoServerConnected = 0;

while (myoServerConnected ~= 1)
    try
        myo.tEvent = tcpclient('127.0.0.1', 30104, 'Timeout', 0);
        myoServerConnected = 1;
    catch
        disp('Waiting for connection to event data...');
        pause(2);
    end
end

%%

% now connected to MyoServer
fprintf('Connected to MyoServer! \n\n');

% initializing matrix to hold data
% added column here to add in CPU time.
myo.emgData = zeros(1,10);
myo.emgDataIndex = 1;

myo.accelData = zeros(1,5);
myo.accelDataIndex = 1;

myo.gyroData = zeros(1,5);
myo.gyroDataIndex = 1;

myo.orientData = zeros(1,6);
myo.orientDataIndex = 1;

myo.eventData = zeros(1,2);
myo.eventDataIndex = 1;

myo.lastTime = cputime();
myo.emgCols = 3:10;

end
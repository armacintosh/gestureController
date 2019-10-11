function [Data,timeString] = classifyCalibrations_createDataStruct(resultsPath,trialDataFiles,tr)

% get the file name
% trFileName = ParticipantVid.trialDataFileName{tr}; % for videoDate
trFileName = trialDataFiles{tr}; % for videoDate

% get the names of all corresponding files based on time string
% get file names --> to change to automatically by time.
fileTrial = strcat(resultsPath,'trialData\',trFileName);
timeString = fileTrial(end-16:end-4);

% get associated file names
fileConst = strcat(resultsPath,'trialData\','trialConst_',timeString,'.mat');
fileEMG = strcat(resultsPath,'myoServer\EMG_',timeString,'.csv');
fileAccel = strcat(resultsPath,'myoServer\Accelerometer_',timeString,'.csv');
fileGyro = strcat(resultsPath,'myoServer\Gyroscope_',timeString,'.csv');
fileOrient = strcat(resultsPath,'myoServer\Orientation_',timeString,'.csv');
fileServer = strcat(resultsPath,'myoServer\Server_',timeString,'.csv');

d=dir(strcat(resultsPath,'gameData\Events_*_',timeString,'.csv'));
disp('Loading data, may take a minute...');

%% Load data

% make all import stuff into a function

% import trialData
fileID = fopen(fileTrial);
formatSpec = '%s';

% get header
tDHeader = textscan(fileID, '%[^\n]', 1);
tDHeader = split(tDHeader{1,1},',')'; % splits 1 col into all cols.

% get data
tD = textscan(fileID,formatSpec,'HeaderLines',1); 
tD = split(tD{1,1},','); % splits 1 col into all cols.

% format Time from str to datetime
tDTime = datetime(tD(:,1),'InputFormat','HH:mm:ss.SSS'); 
tDTime.Format = 'HH:mm:ss.SSS';

% format Other cols. from str. to num
tDData = str2double(tD(:,2:end));

% put back together into table (or other usefule format)
t1 = array2table(tDTime);
t2 = array2table(tDData);
trialData = [t1 t2];
trialData.Properties.VariableNames = tDHeader;

% close file, and stuff I do not eed
fclose(fileID);
% clear_all_but ('resultsPath','trialData');

% load const data
load(fileConst);

%% Load game data...

gameData = [];
% put all events together: 
for lv = 1:length(d)

    fileEvenet = strcat(resultsPath,'gameData\',d(lv).name); % this on has a wierd piece

    % need to just find the matching date/time end string
    fileID = fopen(fileEvenet);
    formatSpec = '%s';

    % get header
    tDHeader = textscan(fileID, '%[^\n]', 1);
    tDHeader = split(tDHeader{1,1},',')'; % splits 1 col into all cols.

    % get data
    tD = textscan(fileID,formatSpec,'HeaderLines',1,'Delimiter',','); 
    tDTime = tD{1,1}(1:2:end-1,:);
    tDTime = datetime(tDTime(:,1),'InputFormat','HH:mm:ss.SSS'); 
    tDTime.Format = 'HH:mm:ss.SSS';

    % game event 
    tDEvent = tD{1,1}(2:2:end,:);

    % put back together into table (or other usefule format)
    t1 = array2table(tDTime);
    t2 = array2table(tDEvent);
    gameDataf = [t1 t2];
    
    % close file, and stuff I do not eed
    fclose(fileID);
    % clear_all_but ('resultsPath','gameData','trialData'); 
    
    gameData = [gameData; gameDataf];
    
end
gameData.Properties.VariableNames = tDHeader;

%% Load MyoServer Raw data

%% EMG

fileID = fopen(fileEMG);
formatSpec = '%s';

% get header
tDHeader = textscan(fileID, '%[^\n]', 1);
tDHeader = split(tDHeader{1,1},',')'; % splits 1 col into all cols.

% get data
tD = textscan(fileID,formatSpec,'HeaderLines',1); 
tD = split(tD{1,1},','); % splits 1 col into all cols.

% format Time from str to datetime
tDTime = datetime(tD(:,1),'InputFormat','HH:mm:ss.SSS'); 
tDTime.Format = 'HH:mm:ss.SSS';

% format Other cols. from str. to num
tDData = str2double(tD(:,3:end)); % skip col. 2 because it is MyoTime % this can take a very long time...:S

% put back together into table (or other usefule format)
t1 = array2table(tDTime);
t2 = array2table(tDData);
EMG = [t1 t2];
EMG.Properties.VariableNames = [tDHeader(1) tDHeader(3:end)];

% close file, and stuff I do not eed
fclose(fileID);

%% IMU

fileID = fopen(fileAccel);
formatSpec = '%s';

% get header
tDHeader = textscan(fileID, '%[^\n]', 1);
tDHeader = split(tDHeader{1,1},',')'; % splits 1 col into all cols.

% get data
tD = textscan(fileID,formatSpec,'HeaderLines',1); 
tD = split(tD{1,1},','); % splits 1 col into all cols.

% format Time from str to datetime
tDTime = datetime(tD(:,1),'InputFormat','HH:mm:ss.SSS'); 
tDTime.Format = 'HH:mm:ss.SSS';

% format Other cols. from str. to num
tDData = str2double(tD(:,3:end)); % skip col. 2 because it is MyoTime. this can take a very long time...:S

% put together into table (or other usefule format)
t1 = array2table(tDTime);
t2 = array2table(tDData);
Accel = [t1 t2];

% add Accel to header of xyz
AccelHeader = strcat('Accel_', tDHeader(3:end));
Accel.Properties.VariableNames = [tDHeader(1) AccelHeader];

% close file, and stuff I do not eed
fclose(fileID);

%%

% GYRO
fileID = fopen(fileGyro);
formatSpec = '%s';

% get header
tDHeader = textscan(fileID, '%[^\n]', 1);
tDHeader = split(tDHeader{1,1},',')'; % splits 1 col into all cols.

% get data
tD = textscan(fileID,formatSpec,'HeaderLines',1); 
tD = split(tD{1,1},','); % splits 1 col into all cols.

% format Time from str to datetime
tDTime = datetime(tD(:,1),'InputFormat','HH:mm:ss.SSS'); 
tDTime.Format = 'HH:mm:ss.SSS';

% format Other cols. from str. to num
tDData = str2double(tD(:,3:end)); % skip col. 2 because it is MyoTime

% put together into table (or other usefule format)
t1 = array2table(tDTime);
t2 = array2table(tDData);
Gyro = [t1 t2];

% add Accel to header of xyz
GyroHeader = strcat('Gyro_', tDHeader(3:end));
Gyro.Properties.VariableNames = [tDHeader(1) GyroHeader];

% close file, and stuff I do not eed
fclose(fileID);


%% Orientation

fileID = fopen(fileOrient);
formatSpec = '%s';

% get header
tDHeader = textscan(fileID, '%[^\n]', 1);
tDHeader = split(tDHeader{1,1},',')'; % splits 1 col into all cols.

% get data
tD = textscan(fileID,formatSpec,'HeaderLines',1); 
tD = split(tD{1,1},','); % splits 1 col into all cols.

% format Time from str to datetime
tDTime = datetime(tD(:,1),'InputFormat','HH:mm:ss.SSS'); 
tDTime.Format = 'HH:mm:ss.SSS';

% format Other cols. from str. to num
tDData = str2double(tD(:,3:end)); % skip col. 2 because it is MyoTime

% put together into table (or other usefule format)
t1 = array2table(tDTime);
t2 = array2table(tDData);
Orient = [t1 t2];
        
% add Accel to header of xyz
OrientHeader = strcat('Orient_', tDHeader(3:end));
Orient.Properties.VariableNames = [tDHeader(1) OrientHeader];

% close file, and stuff I do not eed
fclose(fileID);

%% Server Events data

fileID = fopen(fileServer);
formatSpec = '%s';

% get header
tDHeader = textscan(fileID, '%[^\n]', 1);
tDHeader = split(tDHeader{1,1},',')'; % splits 1 col into all cols.

% get data
tD = textscan(fileID,formatSpec,'Delimiter', ',', 'HeaderLines',1); 

% time
tDTime = tD{1,1}(1:2:end-1,:);
tDTime = datetime(tDTime(:,1),'InputFormat','HH:mm:ss.SSS'); 
tDTime.Format = 'HH:mm:ss.SSS';

% event 
tDData = tD{1,1}(2:2:end,:);

% put together into table (or other usefule format)
t1 = array2table(tDTime);
t2 = array2table(tDData);
Server = [t1 t2];
        
% add Accel to header of xyz
ServerHeader = strcat('Server_', tDHeader(2:end));
Server.Properties.VariableNames = [tDHeader(1) ServerHeader];

% close file, and stuff I do not end
fclose(fileID);

%% Put all data together

% put IMU into same table
IMU = [Accel Gyro(:,2:end) Orient(:,2:end)];

% put myoServer data together
myoServer = struct();
myoServer.EMG = EMG;
myoServer.IMU = IMU;
myoServer.Events = Server;

% add Dashy events to trialData at the correct time
trialData.dashyEvent  = cell(size(trialData,1),1);
trialData.dashyEvent(:) = {''};
for evt = 1:size(gameData.Time)
    [~,EventInd(evt)]= min(abs(trialData.time - gameData.Time(evt)));
    trialData.dashyEvent(EventInd(evt))= gameData.Event(evt);
end


%% Put Data together and Save

Data.EMG = myoServer.EMG;
Data.IMU = myoServer.IMU;
% Data.VID = ParticipantVid.VideoData{tr};
Data.const = const;
Data.Trial = trialData;
Data.gameData = gameData;
Data.myoServerEvents = myoServer.Events;


function trialData = loadTrialData(fileTrial)

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
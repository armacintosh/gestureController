function [const, out] = setupSaveTrial(const, out)

% setup file directory
formatOutFolder = 'yyyy mm dd';
dateFolder = datestr(now,formatOutFolder);
outputfolderTD = strcat('Results\',dateFolder,'\trialData\');
mkdir(outputfolderTD);

% output file names
formatOut = 'yyyymmdd_HHMM';
date = datestr(now,formatOut);
const.trialDatafile = strcat(outputfolderTD,'trialData_',date,'.txt');

const.outFieldNames = fieldnames(out);
const.dateFormat = 'HH:MM:SS.FFF';

% save the const file used in this run
const.trialConst = strcat(outputfolderTD,'trialConst_',date,'.mat');


%% save the first row headers of trial data

const.fileID_STORE = fopen(const.trialDatafile, 'a');

storeStartInd = find(strcmp(const.outFieldNames,'time')); % index of time field 
for fieldIndex = storeStartInd:length(const.outFieldNames)
    
    field = char(const.outFieldNames(fieldIndex));
    
    if fieldIndex == length(const.outFieldNames)
        fprintf(const.fileID_STORE, '%s', field) ;
    else 
        fprintf(const.fileID_STORE, '%s,', field) ;
    end
end 

fprintf(const.fileID_STORE, ' \n') ;  

% save first instance
save(const.trialConst,'const');



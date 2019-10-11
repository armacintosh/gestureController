function [] = logTrialNotes(const,dateFolder,trialTime)
% Open trial log and input new trial information save excel log

formatOutFolder = 'yyyymmdd';
Today = datestr(now,formatOutFolder);

logfile = strcat('Results\',dateFolder,'\TrialLog_',Today,'.txt');
header = {'time', 'trial', 'note'};

    % checks if log file exists
    if exist(logfile,'file') == 0 % if it does not exist
        % make the file
        disp('Creating Log File');
        
        % write csv
        fid = fopen(logfile,'wt');
            [rows,~]=size(header);
            for i=1:rows
                  fprintf(fid,'%s,',header{i,1:end-1});
                  fprintf(fid,'%s\n',header{i,end});
            end
            fclose(fid);
    end  
        
    % build the row to add 
    postcollectiontime = datetime('now','Format','yyyy mm dd hh:mm:ss:ms');
    
    if const.makeTrialNotes == 1
        Note = inputdlg({
                    'Enter Stage number (Calibration = 1, Think aloud = 2, Alg/Explore = 3 )',...
                    'Write any notes for this trial - dont use commas'},...
                    'Config Trial', [1 100; 1 100]);
    else
        Note = {'' ;''};
    end
                        
    appendLog = {char(trialTime), char(Note(1)), char(Note(2))};
        
    % append new line to logfile
    fid = fopen(logfile,'at');
    [rows2,~]=size(appendLog);
    for i=1:rows2
          fprintf(fid,'%s,',appendLog{i,1:end-1});
          fprintf(fid,'%s\n',appendLog{i,end});  
    end
    fclose(fid); 

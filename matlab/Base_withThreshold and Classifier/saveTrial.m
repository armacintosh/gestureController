function [] = saveTrial (const)

%%
% move to beginning and put outfolder into const.
% setup file directory
formatOutFolder = 'yyyy mm dd';
dateFolder = datestr(now,formatOutFolder);
outputfolderLM = strcat('Results\',dateFolder,'\logMatlab\');
outputfolderMS = strcat('Results\',dateFolder,'\myoServer\');
outputfolderGD = strcat('Results\',dateFolder,'\gameData\');
mkdir(outputfolderLM);
mkdir(outputfolderMS);
mkdir(outputfolderGD);

save(const.trialConst,'const');
trialTime = const.trialDatafile(end-16:end-4);

%% Myo Server

% save raw from MyoServer
ServerLogFolder = 'Programs\MyoServer\Logs\'; % all files in folder
% copyfile(ServerLogFolder,outputfolderMS);

% rename to match trial
    serverFiles = dir(fullfile(ServerLogFolder, '*-*'));
    serverFiles  = struct2table(serverFiles );
    serverFiles  = sortrows(serverFiles ,'date','descend'); 
    
    % if there are files to store
    if numel(serverFiles)>0
        
        % only keep the most recent 
        serverFiles  = serverFiles(1:5,:);
        ServerNameOld = strcat( ServerLogFolder,char(serverFiles.name(:,:)) );

        % rename
        serverTime = serverFiles.name{1,1}(1:15);
        serverFiles.name = strrep(serverFiles.name,serverTime,''); 
        suffix = strcat('_',trialTime,'.csv');
        serverFiles.name = strrep(serverFiles.name,'.csv',suffix); 
        ServerNameNew = strcat( outputfolderMS,char(serverFiles.name(:,:)) );

        % rename 
        % will not work if half saved files...
        for filenum = 1:size(ServerNameNew,1)
            movefile(ServerNameOld(filenum,:),ServerNameNew(filenum,:));
        end

        % delete old data, should already be gone.
        delete (strcat(ServerLogFolder,'*.csv'));
    else
        % note in a text file that there were no files to store
        noteText = strcat(outputfolderMS,'No MyoServer data to write','_',trialTime,'.txt');
        fid = fopen(noteText,'w+');
        fprintf(fid, '%s\n', 'No MyoServer data to write');
        fclose(fid);

    end

%%

%%
%% Myo Jumper

% save raw from MyoServer
JumperLogFolder = 'Programs\MyoJumper\MyoJumper_Data\Logs\'; % all files in folder
% copyfile(JumperLogFolder,outputfolderMS);

% rename to match trial
    JumperFiles = dir(fullfile(JumperLogFolder, '*-*'));
    JumperFiles  = struct2table(JumperFiles );
    JumperFiles  = sortrows(JumperFiles ,'date','descend'); 
    
    % if there are files to store
    if numel(JumperFiles)>0
        
        % only keep the most recent 
        JumperFiles  = JumperFiles(:,:);
        ServerNameOld = strcat(JumperLogFolder,char(JumperFiles.name(:,:)) );

%         % rename
%         serverTime = JumperFiles.name{1,1}(1:16);
%         JumperFiles.name = strrep(JumperFiles.name,serverTime,''); 
%         suffix = strcat('_',trialTime,'.csv');
%         JumperFiles.name = strrep(JumperFiles.name,'.csv',suffix); 
        ServerNameNew = strcat( outputfolderGD,'JumperEvents_',trialTime,'.csv');

        % rename 
        for filenum = 1:size(ServerNameNew,1)
            movefile(ServerNameOld(filenum,:),ServerNameNew(filenum,:));
        end

        % delete old data, should already be gone.
        delete (strcat(JumperLogFolder,'*.csv'));
    else
        % note in a text file that there were no files to store
        noteText = strcat(outputfolderMS,'No MyoJumper data to write','_',trialTime,'.txt');
        fid = fopen(noteText,'w+');
        fprintf(fid, '%s\n', 'No MyoJumper data to write');
        fclose(fid);

    end
    
%%
%% save raw Dashy
DashyFolder = 'Programs\Games\Results\';

% rename results to match time stamps...
    gameFiles = dir(fullfile(DashyFolder, '*-*'));
    gameFiles = struct2table(gameFiles);
    gameFiles = sortrows(gameFiles,'date','descend'); 
    
    % if there are files to store
    if numel(gameFiles)>0
        
        % this will get all the game files, even if dashy was opened without matlab saving it..
        gameFileNameOld = strcat( DashyFolder,char(gameFiles.name(:,:)) ); 
       
         % setup new name
            % remove the first item, Data, 
            % move second item (time) to after the words, 
            % place trailTime at end, add extension
            % cut based on '-'
            
        % remove extension
        gameFiles.name = strrep(gameFiles.name,'.csv',''); 
        
        % remove gameDate
        if iscell(gameFiles.name)
            gameDate = gameFiles.name{1}(1:9); % if cell
                gameFiles.name = strrep(gameFiles.name,gameDate,'');   
                gameFiles.name = strrep(gameFiles.name,'-','_');
                % get the time characters
                B = cellfun(@(x) x(1:6), gameFiles.name, 'un', 0);
                           % remove them from the front
                gameFiles.name = cellfun(@(x) strrep(x,x(1:7),''), gameFiles.name, 'un', 0);   
                %  add the time to the end add suffix 
                suffix = strcat('_',trialTime,'.csv');      
                gameFiles.name = strcat(gameFiles.name,'_',B,suffix);
        else 
            gameDate = gameFiles.name(1:9); % if cell
                gameFiles.name = strrep(gameFiles.name,gameDate,'');   
                gameFiles.name = strrep(gameFiles.name,'-','_');
                % get the time characters
                B = gameFiles.name(1:6);
                % remove them from the front
                gameFiles.name = strrep(gameFiles.name,gameFiles.name(1:7),'');   
                %  add the time to the end add suffix 
                suffix = strcat('_',trialTime,'.csv');      
                gameFiles.name = strcat(gameFiles.name,'_',B,suffix);
        end

        gameFileNameNew = strcat( outputfolderGD,char(gameFiles.name(:,:)) );
        
        % rename 
        for filenum = 1:size(gameFileNameNew,1)
            movefile(gameFileNameOld(filenum,:),gameFileNameNew (filenum,:));
        end
        
    else
            % note in a text file that there were no files to store
            noteText = strcat(outputfolderGD,'No Dashy data to write','_',trialTime,'.txt');
            fid = fopen(noteText,'w+');
            fprintf(fid, '%s\n', 'No Dashy data to write');
            fclose(fid);

    end

%%
    
% add time to logFileMatlab
logFileMatlabNew = strcat(outputfolderLM,const.logFileMatlab(1:end-4),'_',trialTime,'.txt');
movefile(const.logFileMatlab,logFileMatlabNew);
    
% Log file notes if required.
logTrialNotes(const,dateFolder, trialTime);



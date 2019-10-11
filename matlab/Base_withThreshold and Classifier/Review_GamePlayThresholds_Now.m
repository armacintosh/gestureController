function [] = Review_GamePlayThresholds_Now()
% Review_GamePlayThresholds

%     goal is to:
%         find the best RatioE and RatioF 
%         find the aboveBaseE and aboveBaseF


%% input for participant ID and E and F cutoff

%% Select participant

%Options
option = [	
{'F01'}...
{'F02'}...
{'F03'}...
{'F04'}...
{'F05'}...
{'F06'}...
{'F07'}...
{'F08'}...
{'F09'}...
{'F10'}...
    {'AM'}...
{'P12'}...
{'P43'}...
{'P52'}...
{'P63'}...
{'P81'}...
{'P84'}...
{'P96'}...
{'P97'}...
{'P98'}...
    {'A'}...
    {'B'}...
    {'C'}...              
    {'D'}...
    {'E'}...
    {'F'}...
    {'G'}...
                    ];
        
% get user to select gesture code 1 or 2
[s,~] = listdlg('PromptString','Select Participant',...
                'SelectionMode','single',...
                'ListSize',[200 100],...
                'ListString',option);

participant = option{s};

%%

% choosing 10 means: 
%     anything above 10%ile peak extension is accepted as extending
%     anything below 90%ile peak flexor activity during extension is accepted as extending
%     increasing from 10 to 20 means it requires more extensor and less flexor activity to be considered extending
%     generally start at 10 and 10

cutoffE = 10; % str2num(Note{1});
cutoffF = 10; % str2num(Note{2}); 
cutoffGyroRes = 10; % str2num(Note{3});
getweekGroupPlayStats = 'n'; % Note{4};
drawPlot = 'y'; %Note{5};

% Note = inputdlg({
%                 'Enter %ile of mavE peaks to be ACCEPTED (0-100), usually 10-30',...
%                 'Enter %ile of mavF peaks to be REJECTED (0-100), usually 10-30',...
%                 'Enter %ile of MaxGyro peaks to be REJECTED (0-100), usually 10-30',...
%                 'get weekGroupPlayStats? y or n',...
%                 'Draw a Plot for each trial? y or n'},...
%                 'Inputs for Threshold check', [1 100; 1 100; 1 100; 1 100; 1 100]);
% 
% % participant = Note{1};
% cutoffE = str2num(Note{1});
% cutoffF = str2num(Note{2}); 
% cutoffGyroRes = str2num(Note{3});
% getweekGroupPlayStats = Note{4};
% drawPlot = Note{5};
% 
% if isempty(cutoffE)
%     cutoffE = 10; % you want everything > the cutoffE %ile of mavE peaks to be accepted (0-100) 0 easier / maybe too easy
% end
% if isempty(cutoffF)
%     cutoffF = 10; % you want everything > the cutoffE %ile of mavE peaks to be accepted (0-100) 0 easier / maybe too easy
% end
% if isempty(cutoffGyroRes)
%     cutoffGyroRes = 10;
% end
% if isempty(getweekGroupPlayStats)   
%     getweekGroupPlayStats = 'n';
% end
% if isempty(drawPlot)   
%     drawPlot = 'y';
% end

%% move all files to same folder

if getweekGroupPlayStats == 'y'
%%
    
    % get the root results folder
    rootResultsFolder = uigetdir('RESULTS FOLDER LOCATION');

    % get the files
    filesConst = dir(strcat(rootResultsFolder,'\**\trialConst_*.mat'));
    filesTrialData = dir(strcat(rootResultsFolder,'\**\trialData_*.txt'));

    % move these files to the same folder
    mkdir(strcat(rootResultsFolder,'\weekGroupPlayStats'));
    saveFolder = strcat(rootResultsFolder,'\weekGroupPlayStats');
    
    % remove any trialData.txt that does not have a constFile.
    ConstNames = {filesConst.name}.'; % makes double from bytes
    C = erase(ConstNames, 'trialConst_');
    C = erase(C, '.mat'); % has the times.
    
    % remove the same in the trialData
    TrialNames = {filesTrialData.name}.'; % makes double from bytes
    T = erase(TrialNames, 'trialData_');
    T = erase(T, '.txt'); % has the times.
    
    % find the index of filesTrialData that match each C
    [~,matchInd] = ismember(C(:),T(:));
    
    filesTrialDataUse = filesTrialData(matchInd); % all of these trials have a const file
    

%% copyfiles filesTrialDataUse and corresponding constData to saveFolder

    for f = 1:numel(filesTrialDataUse)

        % move trialData files
        s = strcat(filesTrialDataUse(f).folder,'\',filesTrialDataUse(f).name);
        d = strcat(saveFolder,'\',filesTrialDataUse(f).name);
        copyfile(s,d);
        
        % move trialData files
        sc = strcat(filesConst(f).folder,'\',filesConst(f).name);
        dc = strcat(saveFolder,'\',filesConst(f).name);
        copyfile(sc,dc);
        
    end
    
%%
end
    
%% Select files

% % go to a participant and pick all trialData
formatOutFolder = 'yyyymmdd'; % for save
date = datestr(now,formatOutFolder);

formatOutFolder1 = 'yyyy mm dd'; %for folder directory
date1 = datestr(now,formatOutFolder1);

if getweekGroupPlayStats == 'y'
    resultsfolder = saveFolder;
else
    resultsfolder = strcat('Results\',date1,'\trialData\');
end

[trialoutput_file, trialoutput_path, ext] = uigetfile(strcat(resultsfolder,'\*.txt'),'Select 1 or more "trialData_" files, > 50 KB ','multiselect','on');

% remove files that dont have a const... or make analysis work without const file...
if class(trialoutput_file) == 'cell'
    trialoutput_file = sort(trialoutput_file);
else
    % turn single string into cell 1x1
    trialoutput_file = {trialoutput_file};
end 

%%
%% for each trial
for t = 1:length(trialoutput_file)
  
%% Load data    

    % load trial data
    loadthis = strcat(trialoutput_path,trialoutput_file(t));
    % NOTE: NEED TO UPDATE THIS IF CHANGEING the trialData cols.
    trialData = loadTrialData(char(loadthis));
    
    % load autogenerated user profile for review
    % there should always be a const file associated with a trial file
    constfile = strrep(trialoutput_file(t),'trialData','trialConst');
    constfile = strrep(constfile,'txt','mat');
    loadconst = strcat(trialoutput_path,constfile);
    const = load(char(loadconst)); 
    const = const.const;
    
    % make the time recorded a string for the name
    t_id = char(trialoutput_file(t));
    t_id = t_id(end-7:end-4);
    
    
%% calculate ratioE and aboveBaseE
%   raitioE would be activity of a median extenion / base
%   aboveBase would be value that lets 90% of extensions pass, above base

    % first, turn into percent currentMax
    trialData.perE = trialData.mavE ./ trialData.currentMaxE;
    trialData.perF = trialData.mavF ./ trialData.currentMaxF;

    % percent base of current max
    trialData.perBaseE = trialData.currentBaseE ./ trialData.currentMaxE;
    trialData.perBaseF = trialData.currentBaseF ./ trialData.currentMaxF;

%%

    % get activity range and peaks above baseline E
    % every mavE should first be a % between base and max...
    perCurrentRng = trialData.currentMaxE - trialData.currentBaseE; % 1 is always current max.
    z = trialData.mavE - trialData.currentBaseE; % amount above baseline
    perAboveBaseE = z ./ perCurrentRng ; % mav expressed as percent above baseline
    
    % pick peak indicies of max from z
    [peaks.indE, peaks.valPkE] = peakseek(perAboveBaseE,const.minpeakdist,std(perAboveBaseE) ); % maxima
    
    % get the above base that would let most extensions things pass
    % tryig to tell me: const.aboveBaseE for pb3
    minAboveBaseE = prctile(perAboveBaseE(peaks.indE), cutoffE ); % an acceptable activity for E when extending   
        
    % predicted min E
    out.minE = trialData.currentBaseE + ((trialData.currentMaxE - trialData.currentBaseE) * minAboveBaseE);
    
    % get activity range and peaks above baseline E
    % every mavE should first be a % between base and max...
    perCurrentRngF = trialData.currentMaxF - trialData.currentBaseF; % 1 is always current max.
    zF = trialData.mavF - trialData.currentBaseF; % amount above baseline
    perAboveBaseF = zF ./ perCurrentRngF ; % mav expressed as percent above baseline
    
    % want activity of flexors duing extension, thus use previous index    
        % get the above base that would let most extensions things pass
        % tryig to tell me: const.aboveBaseF for pb3
    maxAboveBaseF = prctile(perAboveBaseF(peaks.indE), 100-cutoffF ); % a regular activity for E when extending   
        
    % predicted max F
    out.maxF = trialData.currentBaseF + ((trialData.currentMaxF - trialData.currentBaseF) * maxAboveBaseF);


    %% get MaxGryo

    %get Gyro Data
    GyroResPeak = trialData.GyroRes(trialData.pressed==1);
    out.maxGyroRes = prctile(GyroResPeak, 100-cutoffGyroRes ); % Nth %ile is the limit of acceptable GyroRes   


   %% plot

if drawPlot == 'y'   
    Review_GamePlayThresholds_Plot (const, t_id, trialData, peaks, out);
end

    
%% store relevant infromation
    
    % store the abs. vals of the thresh
    result(t).trial = trialoutput_file{t};
    result(t).ID = t_id;
    result(t).const = const;
    result(t).trialData = trialData;
    
    % cutoff of peaks percent
    result(t).cutoffE = cutoffE;  
    result(t).cutoffF = cutoffF;  
    result(t).cutoffGyroRes = cutoffGyroRes;  
    
    % place holder
    result(1).aboveBaseE_x = [];
    result(1).aboveBaseF_x = [];
    
    % expected perent aboveBase values to use in the future
    result(t).aboveBaseE = minAboveBaseE; 
    result(t).aboveBaseF = maxAboveBaseF;
    result(t).nPeaks = length(peaks.indE);
       
    % range/ data for above base vals (peaks.indE) is during extension peaks only
    result(t).perAboveBaseE = perAboveBaseE((peaks.indE));
    result(t).perAboveBaseF = perAboveBaseF((peaks.indE));
    result(t).perAboveBaseE_x = mean(perAboveBaseE(peaks.indE));
    result(t).perAboveBaseE_sd = std(perAboveBaseE(peaks.indE));
    result(t).perAboveBaseF_x = mean(perAboveBaseF(peaks.indE));
    result(t).perAboveBaseF_sd = std(perAboveBaseF(peaks.indE));
    
    % Base estimates
    result(t).perBaseE_x = mean(trialData.perBaseE);
    result(t).perBaseE_sd = std(trialData.perBaseE);
    result(t).perBaseF_x = mean(trialData.perBaseF);
    result(t).perBaseF_sd = std(trialData.perBaseF);
    result(t).perBaseE = trialData.perBaseE;
    result(t).perBaseF = trialData.perBaseF;
    
    % predicted output using new % aboveBase values
    result(t).minE_pred = out.minE;
    result(t).maxF_pred = out.maxF;
    
    % Gyro
    result(t).maxGyroRes = out.maxGyroRes;
    result(t).nPeaksGyro = length(GyroResPeak);

    
          
end    
  

%% Clean result to not include rows with NAN

% None of these can have NAN:  aboveBaseE, aboveBaseF, maxGyroRes
index = structfind(result,'aboveBaseE',NaN);
result(index) = [];

index = structfind(result,'aboveBaseF',NaN);
result(index) = [];

index = structfind(result,'maxGyroRes',NaN);
result(index) = [];

%%
%  weigthed average of aboveBase E /F for use in constFile.txt
% get % totals of weight (n rows used), based on number of peaks used to set %ile
all = [result(:).nPeaks];
S(:,1) = all(:) ./ sum(all);
E = [result(:).aboveBaseE]';
F = [result(:).aboveBaseF]';
G = [result(:).maxGyroRes]';

% the main extensor sensor overall
yE = wmean(E,S,1);
yF = wmean(F,S,1);
yG = wmean(G,S,1);

% to suggest and put into constFile.
result(1).aboveBaseE_x = yE;
result(1).aboveBaseF_x = yF;
result(1).maxGyroRes_x = yG;

    %% 

% Say weather making it easier or harder
if yE < const.aboveBaseE
    changedirE = ' --> easier';
else 
    changedirE = ' --> harder';
end 

if yF > const.aboveBaseF
    changedirF = ' --> easier';
else 
    changedirF = ' --> harder';
end 

if yG > const.aboveBaseGyro
    changedirG = ' --> easier';
else 
    changedirG = ' --> harder';
end 

strE = 'aboveBaseE will be changed from:  %.2f,  to:  %.2f , making it %s  \n\n';
strF = 'aboveBaseF will be changed from:  %.2f,  to:  %.2f , making it %s  \n\n';
strG = 'aboveBaseGyro will be changed from:  %.2f,  to:  %.2f , making it %s  \n\n';
strAskE = 'Change aboveBaseE? \n\n';
strAskF = 'Change aboveBaseF? \n\n';
strAskG = 'Change aboveBaseGyro? \n\n';

strAll_Final = strcat(strE, strF, strG);
strE_Final = strcat(strE, strAskE);
strF_Final = strcat(strF, strAskF);
strG_Final = strcat(strG, strAskG);

promptAll = sprintf(strAll_Final,...
                     const.aboveBaseE, yE, changedirE,...
                     const.aboveBaseF, yF, changedirF,...
                     const.aboveBaseGyro, yG, changedirG);

promptE = sprintf(strE_Final,...
                     const.aboveBaseE, yE, changedirE);
                 
promptF = sprintf(strF_Final,...
                     const.aboveBaseF, yF, changedirF);

promptG = sprintf(strG_Final,...
                     const.aboveBaseGyro, yG, changedirG);
                 
f = msgbox({promptAll,'Paused script to view graph(s)'});
while ishandle(f)
    pause(0.5);
end
    
                 
%% Questions

updateE = 0;
updateF = 0;
updateG = 0;


options.Interpreter = 'tex';
% Include the desired Default answer
options.Default = 'Don''t know';
% Construct a questdlg with three options for E
choice = questdlg(promptE,...
	'Update Extensor thresh?', ...
	'Yes','No',options);
% Handle response
switch choice
    case 'Yes'
        disp([choice ', Updating constFile.txt'])
        updateE = 1;        
    case 'No'
        disp([choice ', Keeping constFile.txt'])
        updateE = 0;
    case 'Don''t know'
        updateE = 0;
end


% Construct a questdlg with three options for F
choiceF = questdlg(promptF,...
	'Update Flexor thresh?', ...
	'Yes','No',options);
% Handle response
switch choiceF
    case 'Yes'
        disp([choiceF ', Updating constFile.txt'])
        updateF = 1;        
    case 'No'
       
        disp([choiceF ', Keeping constFile.txt'])
        updateF = 0;
    case 'Don''t know'
        updateF = 0;
end


% GYRO Dialgue
% Construct a questdlg with three options for G
choiceG = questdlg(promptG,...
	'Update Gyro Thresh?', ...
	'Yes','No',options);
% Handle response
switch choiceG
    case 'Yes'
        disp([choiceG ', Updating constFile.txt'])
        updateG = 1;        
    case 'No'
        disp([choiceG ', Keeping constFile.txt'])
        updateG = 0;
    case 'Don''t know'
        updateG = 0;
end


%% this should update const.Low or const.minE

% replace in constFile.txt, w strfind.
if updateE == 1 || updateF == 1 || updateG == 1

    % select constfile to open:
    [constFileName,constFilePath] = uigetfile(strcat('..\..\..',resultsfolder,'*.txt'),'Select constFile.txt to update');
    constfileLoc = strcat(constFilePath,constFileName);

    % open the const file
    fid  = fopen(constfileLoc,'r');
    f=fread(fid,'*char')';
    fclose(fid);

    if updateE == 1
        % update the value aboveBaseE
        newStr = strcat('aboveBaseE=',num2str(yE),'; %');
        oldStr = strcat('aboveBaseE=');
        f = strrep(f,oldStr ,newStr);
    end
    
    if updateF == 1
        % update the value aboveBaseF
        newStr = strcat('aboveBaseF=',num2str(yF),'; %');
        oldStr = strcat('aboveBaseF=');
        f = strrep(f,oldStr ,newStr);
    end

    if updateG == 1
        % update the value aboveBaseF
        newStr = strcat('aboveBaseGyro=',num2str(yG),'; %');
        oldStr = strcat('aboveBaseGyro=');
        f = strrep(f,oldStr ,newStr);
    end
    
%%    % save 
    fid  = fopen(constfileLoc,'w');
    fprintf(fid,'%s',f);
    fclose(fid);
        
    % copy constFile
    constFileSave1 = strcat(trialoutput_path,'constFile.txt');
    copyfile(constfileLoc,constFileSave1);
    
    constFileStore = strcat(trialoutput_path,'constFile_',participant,'_',date,'.txt');
    copyfile(constfileLoc,constFileStore);
%%

end 

% keep result used or unused
result(1).usedUpdate = [updateE updateF updateG];

%% Save

% Store info that may be needed
% save summary info. if required...
try
    filename = strcat(trialoutput_path,participant,'_Review_AboveBase_',date,'.mat');
catch
    filename = strcat(trialoutput_path,'XX_Review_AboveBase_',date,'.mat');
end
save(filename,'result');


%% simple printout of stats for therapist

% only want rows with peaks
result = result([result(:).nPeaks]> 1); 

% get total number of times played 
nPlaySessions = size(result(:),1);

% get total number  of extensions
nExtensions = sum([result(:).nPeaks]);
nxExtensions = mean([result(:).nPeaks]);
nSDExtensions = std([result(:).nPeaks]);

% get total time playing
sPlayed = seconds(0);
for s = 1:nPlaySessions
    sPlayed = sPlayed  + (result(s).trialData.time(end) - result(s).trialData.time(2) );
end
sPlayed = minutes(sPlayed);


%% 

% setup output string for therapists.
% str0 = strcat('Number of seessions        -->', num2str(nPlaySessions));
% str1 = strcat('Total minutes playing      -->', num2str(round(sPlayed,2)));
% str2 = strcat('Total number of extensions -->', num2str(nExtensions));
% 
% f = msgbox({str0;str1;str2},'\fontsize{15} text');


% %%
% % setup output string for therapists.
% str0 = 'During the session they: \n';
% str1 = '- were activly playing for a total of: %s,  \n';
% str2 = '- extended their wrist a total of: %i times, and \n';
% str3 = '- had an average extension muscle activity of %.2f when extending. \n\n';
% str = strcat(str0, str1, str2, str3);
% 
% % if isstruct(result)
% %     % mean extensor activity while extending - baseline activity (all relative to current max)
% %     % should do this a better way probably reshape with (:)
% %     xExtActivity_1 = result.perAboveBaseE_x;
% %     xExtBase_1 = result.perBaseE_x;
% %     timePlaying = result.trialData.time(end) - result.trialData.time(1);
% %     for trl = 2:length(result)
% %         xExtActivity_1 = vertcat(xExtActivity_1,result(trl).perAboveBaseE);
% %         xExtBase_1 = vertcat(xExtBase_1,result(trl).perBaseE);
% %         timePlaying = timePlaying  + (result(trl).trialData.time(end) - result(trl).trialData.time(1));
% %     end
% %     xExtActivity = mean(xExtActivity_1) - mean(xExtBase_1);    
% %     
% % else
% 
%     % mean extensor activity while extending - baseline activity (all relative to current max)
%     % should do this a better way probably reshape with (:)
%     xExtActivity_1 = result(1).perAboveBaseE;
%     xExtBase_1 = result(1).perBaseE;
%     timePlaying = result(1).trialData.time(end) - result(1).trialData.time(1);
%     
%     for trl = 2:length(result)
%         xExtActivity_1 = vertcat(xExtActivity_1,result(trl).perAboveBaseE);
%         xExtBase_1 = vertcat(xExtBase_1,result(trl).perBaseE);
%         timePlaying = timePlaying  + (result(trl).trialData.time(end) - result(trl).trialData.time(1));
%     end
%     xExtActivity = mean(xExtActivity_1) - mean(xExtBase_1);
% 
% % end
% 
% 
% 
% fprintf(str, char(timePlaying),nExtensions,xExtActivity);

% next would add data from the game / performance
close all

% winopen(trialoutput_path);



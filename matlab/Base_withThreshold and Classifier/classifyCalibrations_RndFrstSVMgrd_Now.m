function [] = classifyCalibrations_RndFrstSVMgrd_Now()

% to adjust as desired
topPercent = 80;

%% import ParticipantVid table
[trialoutput_file, trialoutput_path, ~] = uigetfile('Results\*.txt','multiselect','on','select the trialData_DATE file you want to use to classify');
resultsfolder = strrep(trialoutput_path,'trialData\','');

%% CHAR for single trial
if class(trialoutput_file) == 'cell'
    trialoutput_file = sort(trialoutput_file);
else
    % turn single string into cell 1x1
    trialoutput_file = {trialoutput_file};
end 

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


%% for each trial

for t = 1:length(trialoutput_file) % these files have to be from MyoDashy3 - with automated 3 gesture calibration

    % put File components together
    [Data,~] = classifyCalibrations_createDataStruct(resultsfolder,trialoutput_file,t);
    
    % return FtTbl of 
    [CalFtTbl, const, ~, y] = classifyCalibrations_calcFtTbl (Data);
    
end


%% do one Random Forest and SVM grid for all calData trials put together

% remove selected gestures
FtTbl = CalFtTbl (CalFtTbl.TrueLabel < 3,:); % THIS IS FOR 2 CLASS CALIBRATION- STILL TO CHANGE

% normalize FtTbl to mu and SD, after i have all true labels
[FtTblN, const.mu, const.stddev] = calcFtTblNorm(FtTbl(:,2:end));

   
% truelabel first in FtTbleNorm
TrueLabel = array2table(FtTbl.TrueLabel);
TrueLabel.Properties.VariableNames = {'TrueLabel'};
FtTblNorm = [TrueLabel FtTblN];


%%  Random Forest 

% returns the FtTble with only most important features
fprintf('learning gestures \n');
outPut = StaticAnalysis_RandomForest_setup (FtTblNorm, topPercent); 
FtTblTop = outPut.FtTblTop; % for use in svm grid

% get the top mu and sd to use in 
const.muTop = const.mu(1,outPut.indkpTop-1); 
const.sdTop = const.stddev(1,outPut.indkpTop-1);

%% SVM Grid using top features.

% SVM using only the top features, found during random forest
ClassOutputTop = StatisticalAnalysis_SVMGrid_setup(FtTblTop);
fprintf('done learning gestures \n');

%% setup save struct

% get the model to use in the game.
gameClass.Mdl = ClassOutputTop{1,1}.TestingModel;

% need mu and SD to normalize in game
gameClass.mu = const.muTop;
gameClass.std = const.sdTop;


%% get distance from extensor sensor of channels used in classification
    % ID channels used in classificaiton
    
    % gets last char from each feature name
    FtTopNames = gameClass.Mdl.ExpandedPredictorNames; 
    ch = cellfun(@(S) S(1,end), FtTopNames, 'Uniform', 0); 
    
    % last char is a # return for each ch.
    for Ft = 1:length(ch)
        
        % dont actually need this anymore
        if length(const.EMGch) == 4
            isCH = strfind('3456',ch{Ft});
        elseif length(const.EMGch) == 6
            isCH = strfind('234567',ch{Ft});
        else
            isCH = strfind('12345678',ch{Ft});
        end
        
        % incase circ is the feature
        if isCH
            % set distance from extensor sensor for that Feature
            chABS = str2double(ch{Ft});
            chdist(1,Ft) = chABS - y ; 
            
        else
            chdist(1,Ft) = nan;
        end
        
    end
        
gameClass.FtChDist = chdist;
gameClass.allFts = FtTblNorm.Properties.VariableNames;
        

%% Save the workspace for review/ safe keeping

% update name and date saving 
formatOutFolder = 'yyyymmdd';
dateFolder = datestr(now,formatOutFolder);
gameClassfile = strcat(trialoutput_path,participant,'_1v2_gameClass_',dateFolder);
Classfile = strcat(trialoutput_path,participant,'_1v2_RndFrstSVMgrd_',dateFolder);

save(strcat(trialoutput_path,'CurrentUserClassifier.mat'),'gameClass');
save(strcat(trialoutput_path,'CurrentUserClassifier_',participant,'_',dateFolder,'.mat'),'gameClass');
save(gameClassfile,'gameClass'); % for use in game
save(Classfile,'ClassOutputTop'); % for backup

%%

start = gameClass.Mdl.PredictorNames;
start = cellfun(@(c)[c ', '],start,'uni',false);
finish = arrayfun(@(i)[start{i,:}], 1:size(start,1), 'UniformOutput',false)';
Output1 = strcat('Top Features are:', finish);

confmat = num2str(ClassOutputTop{1,1}.ConfusionMat{:,:});
Output2a = strcat('Confusion Matrix (code 1): ',num2str(confmat(1,:))); 
Output2b = strcat('Confusion Matrix (code 2): ',confmat(2,:)); 

Output = msgbox({Output1{1};Output2a;Output2b});

%%
% Open the folder where data is saved
winopen(trialoutput_path);
msgbox('Copy constFile.txt and CurrentUserClassifier.mat to users MyoDashy folder');


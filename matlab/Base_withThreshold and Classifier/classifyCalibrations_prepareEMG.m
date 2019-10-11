function [const,EMG, D_EMGF] = classifyCalibrations_prepareEMG(Data, const, ind)

%% Renew const file

const = classifyCalibrations_setupEMG_Const(const); % get constants and change units of EMG

%% Get resting data (ReadyMean)

ChUsed = [1,const.EMGch+1];
RestUse = [ind.EMG.startTime1_rest:ind.EMG.startTime1_active,...
           ind.EMG.startTime2_rest:ind.EMG.startTime2_active,...
           ind.EMG.startTime3_rest:ind.EMG.startTime3_active...
           ];
EMGReady = Data.EMG(RestUse,ChUsed); % Get the raw resting data
ReadyMeanEMG = classifyCalibrations_findReadyMean (EMGReady); % changes const.ReadyMean;


%% FIND CORRECT EMG DATA

% Fingers Open
E2 = Data.EMG(ind.EMG.startTime1_active:ind.EMG.startTime1_end, ChUsed );
TL = ones(size(E2,1),1)*2;
E2 = [E2, array2table(TL)];

% Fingers closed
E1 = Data.EMG(ind.EMG.startTime2_active:ind.EMG.startTime2_end,ChUsed ); % E1 and startTime2 do not match on purposes (Gesture 2 is dones first in cal game)
TL = ones(size(E1,1),1);
E1 = [E1, array2table(TL)];

% Pinch
E3 = Data.EMG(ind.EMG.startTime3_active:ind.EMG.startTime3_end,ChUsed ); % E1 and startTime2 do not match on purposes (Gesture 2 is dones first in cal game)
TL = ones(size(E3,1),1)*3;
E3 = [E3, array2table(TL)];

EMG = [E2;E1;E3]; % put all gestures with TLs into single table

switch const.EMGS1
    case 1
        EMG.Properties.VariableNames = {'time' 'S1' 'S2' 'S3' 'S4' 'S5' 'S6' 'S7' 'S8' 'TL'};
    case 2
        EMG.Properties.VariableNames = {'time' 'S2' 'S3' 'S4' 'S5' 'S6' 'S7' 'TL'};
    case 3
        EMG.Properties.VariableNames = {'time' 'S3' 'S4' 'S5' 'S6' 'TL'};
end

EMG{:,2:end-1} = abs (EMG{:,2:end-1}) ./ 128; % change to normalized units
EMG{:,2:end-1} = EMG{:,2:end-1} - ReadyMeanEMG; % subtract resting values from all channels 


%% Bayes Filter

% create Bayes filtered version of D_EMG
% most features use filtered data (these do not filter: SSC, ZC, WAMP)
if const.BayesFilter == 1
    D_EMGF = EMG;
    [param,D_EMGF{:,2:end-1}] = bayesOnlineFilter(const.param,D_EMGF{:,2:end-1}); % returns out.dataEMG filtered
    const.param = param;
    
    % check if error
    if sum(ismissing( D_EMGF{:,2:end-1} )) > 0
        fprintf('NAN in filtered data \n\n');
    else
        fprintf('all EMG filtered \n\n');
    end 
end

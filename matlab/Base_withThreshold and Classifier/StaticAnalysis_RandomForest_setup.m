function  [Output] = StaticAnalysis_RandomForest_setup (FtTbl,topPercent)

%% Scale the features
FtTblNorm = FtTbl;

% edit TrueLabel so it is not normalized
FtTblNorm.TrueLabel  = FtTbl.TrueLabel ;

% remove NAN cols.
FtTblNorm = FtTblNorm(:,~any(ismissing(FtTblNorm))); % but for a table

%% separates predictor and response data

inputTable = FtTblNorm;
predictorNames = inputTable.Properties.VariableNames(:,2:end); % {'MAV_2', 'WL_2', 'ZC_2', 'MC_2', 'SMAV_2', 'MADN_2', 'MAV_3', 'WL_3', 'ZC_3', 'MC_3', 'SMAV_3', 'MADN_3', 'MAV_6', 'WL_6', 'ZC_6', 'MC_6', 'SMAV_6', 'MADN_6', 'MAV_7', 'WL_7', 'ZC_7', 'MC_7', 'SMAV_7', 'MADN_7', 'circMean', 'circVar', 'circStd', 'circSkw', 'circKrt', 'circR', 'circKpa', 'GyrMag', 'AccMag'};
predictors = inputTable(:, predictorNames);
response = inputTable.TrueLabel;

%% PCA - goes here if desired 

PCADetails = [];

%% separate data into training (60), validation (20) and test sets (20)

% DOES NOT DO CV thus use all data and OBB is the generalization
TrainingPredictors = table2array(predictors);
TrainingResponse = response;

%% Random Forest classification

% Bootstrap-aggregated (bagged) decision trees
% TreeBagger selects a random subset of predictors to use at each decision split as in the random forest algorithm [1].
% [1] Breiman, L. Random Forests. Machine Learning 45, pp. 5–32, 2001.

NumTrees = 200; % can adjust as desired
Mdl = TreeBagger(...
                NumTrees,...
                TrainingPredictors,...
                TrainingResponse,...
                'Method','classification',...
                'Prior','Empirical',... % default, determines class probabilities from class frequencies in Y
                'OOBPredictorImportance','on',...
                'Surrogate','on',...
                'PredictorSelection','interaction-curvature'...
                );

%%  evaluate best model on TestSet with the Use the best hyperparameters

pred = oobPredict(Mdl);  % this is a different thing than other pred.. not using the 30% holdout data...
err = oobError(Mdl);

%% store output
Output = struct(...
            'InputFile',FtTbl, ...
            'PCA',PCADetails,...
            'TestingModel', Mdl, ...
            'oobError',err);

%%  Importance table

% importance 
FeatureName = FtTblNorm.Properties.VariableNames(2:end);
importance = Output.TestingModel.OOBPermutedPredictorDeltaError;

ImpTable = array2table(importance');
ImpTable.Properties.VariableNames = {'Importance'};
ImpTable.FeatureName = FeatureName';
[ImpTable,Ind] = sortrows(ImpTable,{'Importance'},{'descend'});

% number of ft. to include (90/95% of error);
B = ImpTable.Importance;
indkp = find(B < prctile(B,topPercent),1); % keep the first indkp values. outPut

N = ImpTable.FeatureName;
FtTblTop = FtTbl(:,N(1:indkp));     % index of most important features to use in SVMGRID of original FtTbl
indTop = Ind(1:indkp)+1; % + 1 because TrueLabel removed
FtTblTop.TrueLabel = FtTbl.TrueLabel; % add codes back in.

% add to function ouput
Output.ImpTable = ImpTable;
Output.FtTblTop = FtTblTop;
Output.indkpTop = indTop;


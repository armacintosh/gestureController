function  [ClassOutput] = StatisticalAnalysis_SVMGrid_setup (FtTbl)


FtTblNorm = FtTbl;
FtTblNorm = sortrows(FtTblNorm,'TrueLabel'); 

inputTableO{1} = FtTblNorm;

%% Classify using SVM Grid search   

ClassOutput = cell(size(inputTableO));
for iTbl = 1:length (inputTableO)

    %% separates predictor and response data
    
    inputTable = inputTableO{iTbl};
    predictorNames = inputTable.Properties.VariableNames(:,1:end-1); % true label is last col.
    predictors = inputTable(:, predictorNames);
    response = inputTable.TrueLabel;

%% PCA - goes here if desired

PCADetails = [];

%% separate data into training (60), validation (20) and test sets (20)

    % Set up holdout validation
    cvp = cvpartition(response, 'Holdout', 0.2); % 30% hold out for testing set.
    trainingPredictors = predictors(cvp.training, :);
    trainingResponse = response(cvp.training, :);
    TestingPredictors = predictors(cvp.test, :);
    TestingResponse = response(cvp.test, :);
    

    %% make classification algo. with trainingData = Train a classifier
    % Optimize hyperperameters within k-fold classification
    % do grid search for hyperparameters on each fold.

    targets = trainingResponse;
    kFolds = 10; % this is where you specify your number of folds
    kIdx = crossvalind('Kfold', length(targets), kFolds); % contain the cross validation indices based on the data and the number of folds

    %%

    % setup the output structure
    bestFeatScore = inf;
    % bestFeatCombo = struct('SVM', NaN, 'feat', NaN, 'C', NaN);
    SVMBest = struct('BestSVMModel', NaN, ...     % this is to store the best SVM
                     'BestBoxConstraint', NaN, ...
                     'BestScore', Inf, ... 
                     'FeaturesIdx', NaN);     

    SVMHistory = struct('Fold',NaN, ...
                        'SVMModel', NaN, ...     % this is to store the best SVM
                        'LossScores', NaN, ...  % loss.       
                        'BestBoxConstraint', NaN, ...
                        'BestScore', Inf); % loss.        


    for k = 1:kFolds
        % prepare a training set and a validation set for this fold.
        trainData = trainingPredictors(kIdx~=k, :);
        trainTarg = targets(kIdx~=k);
        testData = trainingPredictors(kIdx==k, :);
        testTarg = targets(kIdx==k);
        bestCScore = inf;
        bestC = NaN;
        bestCSVM = NaN;
        gridC = 2.^(-5:2:15); % search for best BoxConstraint
        L = ones ( 1, length ( gridC ) );

        % grid on C
        for C = gridC
            Cind = find(gridC==C);
            % This code specifies all the classifier options and trains the classifier.
            template = templateSVM(...
                'KernelFunction', 'rbf', ... % how to select?
                'PolynomialOrder', [], ... % maybe to optimize?
                'KernelScale', 'auto', ... % maybe to optimize?
                'BoxConstraint', C, ... % to optimize
                'Standardize', false); % already normalized to [0 1]
            anSVMModel = fitcecoc(...
                trainData, ...
                trainTarg, ...
                'Learners', template, ...
                'Coding', 'onevsall', ... % onevsall or onevsone?
                'ClassNames', unique(targets)); %

            % determine how well the SVM performed:
            L(Cind) = loss(anSVMModel,testData, testTarg); % returns classification error? is this what i want?
            

            if L(Cind) < bestCScore        % saving best SVM on parameter
                bestCSVM = anSVMModel;
                bestC = C;
                bestCScore = L(Cind);
            end 

        end

        % for this fold, save the best SVM and its parameters, with all
        % classification errors from gridsearch
        SVMHistory(k).Fold = k;
        SVMHistory(k).SVMModel = bestCSVM;
        SVMHistory(k).LossScores = L;
        SVMHistory(k).BestBoxConstraint = bestC;
        SVMHistory(k).BestScore = bestCScore;


        % saving the best SVM over all folds
        if bestCScore < bestFeatScore
            SVMBest.BestSVMModel = SVMHistory(k).SVMModel;
            SVMBest.BestBoxConstraint = SVMHistory(k).BestBoxConstraint;
            SVMBest.BestScore = SVMHistory(k).BestScore;
        end 

    end 


    %% Retrain

    % we need to retrain here and save the SVM for the best C
    templateOptim = templateSVM(...
                                'KernelFunction', 'rbf', ... % how to select?
                                'PolynomialOrder', [], ... % maybe to optimize?
                                'KernelScale', 'auto', ... % maybe to optimize?
                                'BoxConstraint', SVMBest.BestBoxConstraint, ... % to optimize
                                'Standardize', false); % already normalized to [0 1]

    % maybe I can just use the model output from before instead of re-training...?
    [Mdl,~] = fitcecoc(...
                        trainingPredictors, ...
                        trainingResponse, ...
                        'Learners', templateOptim, ...
                        'Coding', 'onevsall', ... % onevsall or onevsone?
                        'ClassNames', unique(targets)); %


    %%  evaluate best model on TestSet with the Use the best hyperparameters 

    % get predicted labels for final testing set, 
    pred = predict(Mdl,TestingPredictors);

    % evaluate accuracy of predicted labels 
    [confus,accuracy,numcorrect,precision,recall,F,PatN,MAP,NDCGatN] = compute_accuracy_F (TestingResponse,pred,unique(TestingResponse));

    Labels = num2str(unique(TestingResponse));
    Labels = cellstr(Labels);
    Labels = strcat('g_',Labels);
    confus = array2table(confus);
    confus.Properties.VariableNames = Labels ;
    
    %% store output
    ClassOutput{iTbl} = struct(...
                'InputFile',FtTbl, ...
                'PCA',PCADetails,...
                'SVMBest',SVMBest,...                    
                'SVMHistory',SVMHistory, ...
                'TestingModel', Mdl, ...
                'ConfusionMat',confus, ...
                'Accuracy',accuracy,...
                'Precision',precision,...
                'Recall',recall,...
                'Fscore',F...
               );

end